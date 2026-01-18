"""
Faulty Rings Detection - Real-time Dashboard
Streamlit app to visualize detection results from Firebase
FIXED VERSION - Full Features + Cloud Compatibility
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
from PIL import Image

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
</style>
""", unsafe_allow_html=True)

# ============================================================================
# FIREBASE INITIALIZATION (CRITICAL FIX FOR CLOUD)
# ============================================================================
@st.cache_resource
def init_firebase():
    """Initialize Firebase connection (Works with Secrets & Local file)"""
    try:
        # Check if already initialized to prevent errors
        if firebase_admin._apps:
            return db

        # ---------------------------------------------------------
        # OPTION 1: Streamlit Cloud (Secrets)
        # ---------------------------------------------------------
        if "firebase" in st.secrets:
            # Convert TOML secret back to dict
            service_key = dict(st.secrets["firebase"])
            
            # FIX: Handle newlines in private key (The \n issue)
            if "private_key" in service_key:
                service_key["private_key"] = service_key["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(service_key)
            
            # Get Database URL safely
            db_url = st.secrets.get("database_url")
            if not db_url and "database_url" in service_key:
                 db_url = service_key["database_url"]
            
            if not db_url:
                st.error("❌ Database URL is missing from Secrets!")
                return None

            firebase_admin.initialize_app(cred, {
                'databaseURL': db_url
            })
            return db

        # ---------------------------------------------------------
        # OPTION 2: Localhost (serviceAccountKey.json)
        # ---------------------------------------------------------
        elif os.path.exists("serviceAccountKey.json"):
            try:
                # Try to import URL from config, but handle failure
                try:
                    from firebase_config import FIREBASE_DATABASE_URL
                except ImportError:
                    st.error("❌ found serviceAccountKey.json but missing firebase_config.py for URL")
                    return None

                cred = credentials.Certificate("serviceAccountKey.json")
                firebase_admin.initialize_app(cred, {
                    'databaseURL': FIREBASE_DATABASE_URL
                })
                return db
            except Exception as local_err:
                 st.error(f"❌ Local init failed: {local_err}")
                 return None
        
        else:
            st.error("❌ Credentials not found! Please set up Streamlit Secrets or local key file.")
            return None

    except Exception as e:
        st.error(f"❌ Firebase Connection Failed: {str(e)}")
        return None


# ============================================================================
# DATA FETCHING FUNCTIONS (YOUR ORIGINAL LOGIC)
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
    try:
        data = safe_get_data("system_status") # Changed to match your test.py (system_status vs system/status)
        if not data:
             data = safe_get_data("system/status") # Fallback
        return data if data and isinstance(data, dict) else None
    except:
        return None

def get_all_statistics():
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
        return pd.DataFrame()

# ============================================================================
# MAIN APP
# ============================================================================
def main():
    # Initialize Firebase
    database = init_firebase()
    
    if not database:
        st.stop() # Stop execution if no DB
    
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
        if st.button("Force Refresh"):
            st.rerun()
    
    st.markdown("---")
    
    # ========================================================================
    # STATUS CARDS
    # ========================================================================
    st.markdown("### System Status")
    
    # Get current data
    system_status = get_system_status()
    detections_df = get_recent_detections(hours=24)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        # Check 'is_active' (from test.py) or 'online' (from cloud_client.py)
        is_active = False
        if system_status:
            is_active = system_status.get('is_active', system_status.get('online', False))
            
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
    tab1, tab2, tab3 = st.tabs(["📊 Analytics", "📋 Detection History", "📈 Live Feed"])
    
    # ========================================================================
    # TAB 1: ANALYTICS
    # ========================================================================
    with tab1:
        st.markdown("### Detection Analytics")
        
        if not detections_df.empty:
            col1, col2 = st.columns(2)
            
            # Defect Type Distribution
            with col1:
                if 'defect_type' in detections_df.columns:
                    defect_counts = detections_df['defect_type'].value_counts()
                    fig = px.pie(
                        values=defect_counts.values,
                        names=defect_counts.index,
                        title="Defects by Type",
                        color_discrete_sequence=px.colors.qualitative.Pastel
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No defect type data available")
            
            # Confidence Distribution
            with col2:
                if 'confidence' in detections_df.columns:
                    fig = px.histogram(
                        detections_df, x="confidence",
                        nbins=20,
                        title="Confidence Distribution",
                        labels={'confidence': 'Confidence Score'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info("No confidence data available")
            
            # Timeline
            st.markdown("#### Detection Timeline (24h)")
            try:
                # Group by hour
                timeline_df = detections_df.set_index('timestamp').resample('H').size().reset_index(name='count')
                fig = px.bar(
                    timeline_df, x='timestamp', y='count',
                    title="Hourly Detection Count",
                    labels={'timestamp': 'Time', 'count': 'Detections'}
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.info(f"Could not generate timeline: {e}")
        
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
                    types = list(detections_df['defect_type'].unique())
                    defect_filter = st.multiselect("Filter by Type", options=types, default=types)
                else:
                    defect_filter = []

            # Apply filters
            filtered_df = detections_df.copy()
            if defect_filter and 'defect_type' in filtered_df.columns:
                filtered_df = filtered_df[filtered_df['defect_type'].isin(defect_filter)]
            
            # Display Table
            if not filtered_df.empty:
                display_cols = ['timestamp', 'defect_type', 'confidence', 'ring_count']
                available_cols = [c for c in display_cols if c in filtered_df.columns]
                
                st.dataframe(
                    filtered_df[available_cols].sort_values('timestamp', ascending=False),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Image Gallery (Local only warning)
                st.markdown("#### Detected Fault Images (Local Only)")
                
                # Check if we are on cloud
                is_cloud = "firebase" in st.secrets
                
                if is_cloud:
                    st.warning("⚠️ Note: Images stored on your laptop cannot be viewed here on the Cloud. This gallery only works when running `streamlit run app.py` on your machine.")
                else:
                    # Logic for displaying local images
                    detections_with_images = filtered_df[filtered_df.get('image_filename', pd.Series()).notna()]
                    
                    if not detections_with_images.empty:
                        cols = st.columns(3)
                        for idx, row in detections_with_images.head(6).iterrows():
                            # Logic to find image
                            img_path = Path("detected_faults") / row['image_filename']
                            col_idx = idx % 3
                            
                            with cols[col_idx]:
                                if img_path.exists():
                                    try:
                                        img = Image.open(img_path)
                                        st.image(img, caption=f"{row.get('defect_type','Unknown')} ({row.get('confidence',0):.0%})")
                                    except:
                                        st.error(f"Error loading {row['image_filename']}")
            else:
                st.info("No detections match filters.")
        else:
            st.info("Log is empty.")

    # ========================================================================
    # TAB 3: LIVE FEED ALERT
    # ========================================================================
    with tab3:
        st.subheader("Latest System Event")
        if not detections_df.empty:
            latest = detections_df.iloc[0]
            
            st.markdown(f"""
            <div style='padding: 20px; background-color: #ffe6e6; border-radius: 10px; border: 2px solid #ff4b4b; text-align: center;'>
                <h1 style='color: #ff4b4b; margin:0;'>🚨 {latest.get('defect_type', 'UNKNOWN').upper()}</h1>
                <h3 style='margin:0;'>Confidence: {latest.get('confidence', 0):.1%}</h3>
                <p style='color: gray;'>{latest.get('timestamp', 'Just now')}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.success("System is running. No defects detected recently.")

    # ========================================================================
    # AUTO-REFRESH LOGIC
    # ========================================================================
    if auto_refresh:
        time.sleep(10)  # Refresh every 10 seconds
        st.rerun()

if __name__ == "__main__":
    main()