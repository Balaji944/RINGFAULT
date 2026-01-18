"""
Faulty Rings Detection - Real-time Dashboard
Streamlit app to visualize detection results from Firebase
FIXED VERSION - Handles Firebase response correctly
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import credentials, db
from pathlib import Path
import time
from datetime import datetime, timedelta
import os

# ============================================================================
# PAGE CONFIG
# ============================================================================
st.set_page_config(
    page_title="Ring Detection Dashboard",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# STYLING
# ============================================================================
st.markdown("""
<style>
    .metric-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .defect-badge {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        margin: 2px;
    }
    .breakage { background-color: #FF6B6B; color: white; }
    .crack { background-color: #FFA500; color: white; }
    .scratch { background-color: #4ECDC4; color: white; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FIREBASE INITIALIZATION
# ============================================================================
@st.cache_resource
def init_firebase():
    """Initialize Firebase connection (cached)"""
    try:
        try:
            from firebase_config import FIREBASE_DATABASE_URL, SERVICE_ACCOUNT_KEY_PATH
        except:
            st.error("❌ firebase_config.py not found. Please create it with your Firebase credentials.")
            return None
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
            firebase_admin.initialize_app(cred, {
                'databaseURL': FIREBASE_DATABASE_URL
            })
        
        return db
    except Exception as e:
        st.error(f"❌ Firebase Connection Failed: {str(e)}")
        return None


# ============================================================================
# DATA FETCHING FUNCTIONS - ROBUST VERSION
# ============================================================================
def safe_get_data(path):
    """Safely get data from Firebase"""
    try:
        database = init_firebase()
        if not database:
            return None
        
        ref = database.reference(path)
        snapshot = ref.get()
        
        # Handle both DataSnapshot and direct dict returns
        if snapshot is None:
            return {}
        
        if hasattr(snapshot, 'val'):
            data = snapshot.val()
        else:
            data = snapshot
        
        return data if data else {}
    except Exception as e:
        return None


def get_all_detections():
    """Fetch all detections from Firebase"""
    try:
        data = safe_get_data("detections")
        
        if not data or not isinstance(data, dict):
            return pd.DataFrame()
        
        detections = []
        for key, detection in data.items():
            if isinstance(detection, dict):
                detection['id'] = key
                detections.append(detection)
        
        if detections:
            df = pd.DataFrame(detections)
            # Parse timestamp safely
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
            return df
        
        return pd.DataFrame()
    except Exception as e:
        st.warning(f"⚠️ Error fetching detections: {str(e)}")
        return pd.DataFrame()


def get_recent_detections(hours=24):
    """Fetch recent detections from last N hours"""
    try:
        df = get_all_detections()
        
        if df.empty:
            return pd.DataFrame()
        
        # Filter by time
        cutoff_time = datetime.now() - timedelta(hours=hours)
        if 'timestamp' in df.columns:
            df = df[df['timestamp'] >= cutoff_time]
        
        return df.sort_values('timestamp', ascending=False) if not df.empty else pd.DataFrame()
    except Exception as e:
        st.warning(f"⚠️ Error filtering detections: {str(e)}")
        return pd.DataFrame()


def get_system_status():
    """Fetch current system status"""
    try:
        data = safe_get_data("system/status")
        return data if data and isinstance(data, dict) else None
    except:
        return None


def get_camera_status():
    """Fetch current camera status"""
    try:
        data = safe_get_data("camera_status/current")
        return data if data and isinstance(data, dict) else None
    except:
        return None


def get_all_statistics():
    """Fetch all session statistics"""
    try:
        data = safe_get_data("statistics")
        
        if not data or not isinstance(data, dict):
            return pd.DataFrame()
        
        stats = []
        for key, stat in data.items():
            if isinstance(stat, dict):
                stat['session_id'] = key
                stats.append(stat)
        
        if stats:
            return pd.DataFrame(stats)
        
        return pd.DataFrame()
    except Exception as e:
        st.warning(f"⚠️ Error fetching statistics: {str(e)}")
        return pd.DataFrame()


def get_database_stats():
    """Get total counts from database"""
    try:
        all_detections = get_all_detections()
        all_stats = get_all_statistics()
        
        return {
            'total_detections': len(all_detections),
            'total_sessions': len(all_stats)
        }
    except:
        return {'total_detections': 0, 'total_sessions': 0}

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Initialize Firebase
    database = init_firebase()
    
    if not database:
        st.error("Cannot connect to Firebase. Please check your configuration in firebase_config.py")
        return
    
    # ========================================================================
    # HEADER
    # ========================================================================
    st.title("🔍 Faulty Rings Detection Dashboard")
    st.markdown("Real-time monitoring of ring defect detection system")
    
    # Auto-refresh controls
    col1, col2, col3 = st.columns([2, 1, 1])
    with col2:
        auto_refresh = st.checkbox("🔄 Auto-refresh", value=True)
    with col3:
        if auto_refresh:
            refresh_interval = st.select_slider(
                "Refresh every (seconds)", 
                options=[5, 10, 15, 30, 60], 
                value=10
            )
    
    st.markdown("---")
    
    # ========================================================================
    # STATUS CARDS
    # ========================================================================
    st.markdown("### System Status")
    
    # Get current data
    system_status = get_system_status()
    camera_status = get_camera_status()
    detections_df = get_recent_detections(hours=24)
    db_stats = get_database_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        is_active = system_status.get('is_active', False) if system_status else False
        status_text = "🟢 RUNNING" if is_active else "🔴 STOPPED"
        st.metric("System Status", status_text)
    
    with col2:
        detection_count = len(detections_df) if not detections_df.empty else 0
        st.metric("Detections (24h)", detection_count)
    
    with col3:
        if not detections_df.empty and 'defect_type' in detections_df.columns:
            defect_count = detections_df[detections_df['defect_type'].notna()].shape[0]
        else:
            defect_count = 0
        st.metric("Defects Found", defect_count)
    
    with col4:
        if not detections_df.empty and 'confidence' in detections_df.columns:
            try:
                avg_confidence = float(detections_df['confidence'].mean())
                st.metric("Avg Confidence", f"{avg_confidence:.1%}")
            except:
                st.metric("Avg Confidence", "N/A")
        else:
            st.metric("Avg Confidence", "N/A")
    
    st.markdown("---")
    
    # ========================================================================
    # TABS
    # ========================================================================
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "📋 Detection History", "📈 Statistics", "⚙️ Live Status"])
    
    # ========================================================================
    # TAB 1: ANALYTICS
    # ========================================================================
    with tab1:
        st.markdown("### Detection Analytics")
        
        if not detections_df.empty:
            # Ensure timestamp is datetime
            if 'timestamp' in detections_df.columns:
                detections_df['timestamp'] = pd.to_datetime(detections_df['timestamp'], errors='coerce')
            
            col1, col2 = st.columns(2)
            
            # Defect Type Distribution
            with col1:
                if 'defect_type' in detections_df.columns:
                    defect_counts = detections_df['defect_type'].value_counts()
                    if not defect_counts.empty:
                        fig = px.pie(
                            values=defect_counts.values,
                            names=defect_counts.index,
                            title="Defects by Type",
                            color_discrete_map={
                                'breakage': '#FF6B6B',
                                'crack': '#FFA500',
                                'scratch': '#4ECDC4'
                            }
                        )
                        st.plotly_chart(fig, width='stretch')
                    else:
                        st.info("No defect type data available")
                else:
                    st.info("No defect type column found")
            
            # Confidence Distribution
            with col2:
                if 'confidence' in detections_df.columns:
                    try:
                        confidence_data = pd.to_numeric(detections_df['confidence'], errors='coerce').dropna()
                        if not confidence_data.empty:
                            fig = px.histogram(
                                confidence_data,
                                nbins=20,
                                title="Confidence Distribution",
                                labels={'value': 'Confidence', 'count': 'Count'}
                            )
                            fig.update_layout(showlegend=False)
                            st.plotly_chart(fig, width='stretch')
                        else:
                            st.info("No valid confidence data")
                    except:
                        st.info("Could not process confidence data")
                else:
                    st.info("No confidence column found")
            
            # Timeline
            st.markdown("#### Detection Timeline (24h)")
            
            try:
                hourly_counts = detections_df.set_index('timestamp').resample('h').size()
                if not hourly_counts.empty:
                    fig = px.bar(
                        hourly_counts,
                        title="Hourly Detection Count",
                        labels={'value': 'Count', 'timestamp': 'Time'}
                    )
                    st.plotly_chart(fig, width='stretch')
                else:
                    st.info("No timeline data available")
            except:
                st.info("Could not generate timeline")
        
        else:
            st.info("💡 No detection data available yet. Start the detection system to see analytics.")
    
    # ========================================================================
    # TAB 2: DETECTION HISTORY
    # ========================================================================
    with tab2:
        st.markdown("### Recent Detections")
        
        if not detections_df.empty:
            # Filters
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if 'defect_type' in detections_df.columns:
                    defect_filter = st.multiselect(
                        "Filter by Defect Type",
                        options=detections_df['defect_type'].unique(),
                        default=detections_df['defect_type'].unique()
                    )
                else:
                    defect_filter = None
            
            with col2:
                if 'confidence' in detections_df.columns:
                    try:
                        min_conf = float(st.slider("Min Confidence", 0.0, 1.0, 0.0, 0.05))
                    except:
                        min_conf = 0.0
                else:
                    min_conf = 0.0
            
            with col3:
                st.write("")  # Spacing
            
            # Apply filters
            filtered_df = detections_df.copy()
            
            if defect_filter and 'defect_type' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['defect_type'].isin(defect_filter)]
            
            if 'confidence' in filtered_df.columns:
                try:
                    filtered_df['confidence_numeric'] = pd.to_numeric(filtered_df['confidence'], errors='coerce')
                    filtered_df = filtered_df[filtered_df['confidence_numeric'] >= min_conf]
                except:
                    pass
            
            # Display table
            if not filtered_df.empty:
                # Select columns to display
                display_cols = [col for col in ['timestamp', 'defect_type', 'confidence', 'image_filename', 'ring_count'] 
                               if col in filtered_df.columns]
                
                st.dataframe(
                    filtered_df[display_cols].sort_values('timestamp', ascending=False),
                    width='stretch',
                    hide_index=True
                )
                
                # Display detected fault images
                st.markdown("#### Detected Fault Images")
                
                detections_with_images = filtered_df[filtered_df['image_filename'].notna()].sort_values('timestamp', ascending=False)
                
                if not detections_with_images.empty:
                    # Create a grid of images
                    cols_per_row = 3
                    num_images = len(detections_with_images)
                    
                    for row_idx in range(0, num_images, cols_per_row):
                        cols = st.columns(cols_per_row)
                        
                        for col_idx, col in enumerate(cols):
                            img_idx = row_idx + col_idx
                            if img_idx < num_images:
                                detection = detections_with_images.iloc[img_idx]
                                image_filename = detection['image_filename']
                                image_path = Path("detected_faults") / image_filename
                                
                                with col:
                                    if image_path.exists():
                                        try:
                                            from PIL import Image
                                            img = Image.open(str(image_path))
                                            st.image(
                                                img, 
                                                caption=f"{detection['defect_type'].upper()}\n{detection['confidence']:.1%}"
                                            )
                                        except Exception as e:
                                            st.error(f"Error: {str(e)[:40]}")
                                    else:
                                        st.error(f"Not found: {image_filename}")
                else:
                    st.info("💡 No detected fault images available yet")
            else:
                st.info("No detections match the selected filters")
        
        else:
            st.info("💡 No detection history available yet.")
    
    # ========================================================================
    # TAB 3: STATISTICS
    # ========================================================================
    with tab3:
        st.markdown("### Session Statistics")
        
        stats_df = get_all_statistics()
        
        if not stats_df.empty:
            # Summary metrics
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Sessions", len(stats_df))
            
            with col2:
                if 'total_detections' in stats_df.columns:
                    try:
                        total = pd.to_numeric(stats_df['total_detections'], errors='coerce').sum()
                        st.metric("Total Detections", int(total))
                    except:
                        st.metric("Total Detections", "N/A")
                else:
                    st.metric("Total Detections", "N/A")
            
            with col3:
                if 'avg_confidence' in stats_df.columns:
                    try:
                        avg = pd.to_numeric(stats_df['avg_confidence'], errors='coerce').mean()
                        st.metric("Avg Session Confidence", f"{avg:.2%}")
                    except:
                        st.metric("Avg Session Confidence", "N/A")
                else:
                    st.metric("Avg Session Confidence", "N/A")
            
            st.markdown("#### Session Details")
            
            # Display sessions table
            display_cols = [col for col in stats_df.columns if col != 'session_id']
            st.dataframe(stats_df, width='stretch', hide_index=True)
        
        else:
            st.info("💡 No session statistics available yet.")
    
    # ========================================================================
    # TAB 4: LIVE STATUS
    # ========================================================================
    with tab4:
        st.markdown("### Live System Status")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### System Status")
            if system_status:
                st.json(system_status)
            else:
                st.info("No system status data available")
        
        with col2:
            st.markdown("#### Camera Status")
            if camera_status:
                st.json(camera_status)
            else:
                st.info("No camera status data available")
        
        # Database stats
        st.markdown("#### Database Statistics")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            total_det = db_stats['total_detections']
            st.metric("Total Detections in DB", total_det)
        
        with col2:
            total_sess = db_stats['total_sessions']
            st.metric("Total Sessions in DB", total_sess)
        
        with col3:
            st.metric("Last Updated", datetime.now().strftime("%H:%M:%S"))
    
    # ========================================================================
    # AUTO-REFRESH
    # ========================================================================
    if auto_refresh:
        time.sleep(refresh_interval)
        st.rerun()

if __name__ == "__main__":
    main()
