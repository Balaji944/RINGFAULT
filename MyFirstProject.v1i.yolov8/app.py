"""
Ring Fault Detection System - Operations Dashboard
v5.0 - Industrial UI & Image Gallery Integration
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import time

# ============================================================================
# 1. PAGE CONFIGURATION & STYLING
# ============================================================================
st.set_page_config(
    page_title="Quality Control Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Industrial/Professional Look
st.markdown("""
    <style>
        .block-container { padding-top: 1.5rem; }
        h1 { font-family: 'Helvetica', sans-serif; font-size: 2.2rem; }
        div[data-testid="stMetricValue"] { font-size: 24px; font-weight: 600; }
        .stAlert { padding: 0.5rem; border-radius: 4px; }
        img { border-radius: 4px; border: 1px solid #444; }
        .stButton>button { width: 100%; border-radius: 4px; }
    </style>
""", unsafe_allow_html=True)

# Avoid Pandas Chained Assignment warnings
pd.options.mode.chained_assignment = None 

# ============================================================================
# 2. FIREBASE CONNECTION
# ============================================================================
@st.cache_resource
def init_firebase():
    """Initialize Firebase connection safely"""
    try:
        if firebase_admin._apps:
            return db
            
        if "firebase" in st.secrets:
            key_dict = dict(st.secrets["firebase"])
            # Fix private key newlines formatting
            if "private_key" in key_dict:
                key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(key_dict)
            firebase_admin.initialize_app(cred, {'databaseURL': st.secrets["database_url"]})
            return db
        return None
    except Exception as e:
        st.error(f"Connection Error: {e}")
        return None

# ============================================================================
# 3. DATA FETCHING
# ============================================================================
def get_data():
    """Fetch recent detection data"""
    database = init_firebase()
    if not database: return pd.DataFrame()
    
    try:
        ref = database.reference('detections')
        # Fetch last 50 records for performance
        snapshot = ref.order_by_key().limit_to_last(50).get()
        
        if not snapshot: return pd.DataFrame()
        
        data_list = []
        for key, val in snapshot.items():
            val['id'] = key
            data_list.append(val)
            
        df = pd.DataFrame(data_list)
        
        # Process timestamps
        if 'unix_timestamp' in df.columns:
            df['datetime'] = pd.to_datetime(df['unix_timestamp'], unit='s')
            df = df.sort_values('unix_timestamp', ascending=False)
            
        return df
    except Exception as e:
        return pd.DataFrame()

def get_system_status():
    """Fetch live system status"""
    database = init_firebase()
    if not database: return {}
    try:
        return database.reference('system_status').get() or {}
    except:
        return {}

# ============================================================================
# 4. DASHBOARD LAYOUT
# ============================================================================
def main():
    # --- HEADER SECTION ---
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("Ring Fault Detection System")
        st.caption("Real-time Quality Control & Automated Inspection Log")
    with col2:
        st.write("") # Spacer
        if st.button("Refresh Data"):
            st.cache_data.clear()
            st.rerun()

    st.divider()

    # --- FETCH DATA ---
    df = get_data()
    status_data = get_system_status()
    
    # --- STATUS METRICS ---
    m1, m2, m3, m4 = st.columns(4)
    
    # 1. System Status Logic
    is_active = status_data.get('is_active', False)
    status_text = "OFFLINE"
    if is_active:
        status_text = "ONLINE"
        m1.success(f"System: {status_text}")
    else:
        m1.error(f"System: {status_text}")
    
    # 2. Total Defects
    total_count = len(df)
    m2.metric("Total Detections", total_count)
    
    # 3. Latest Defect
    latest_defect = "N/A"
    if not df.empty:
        latest_defect = df.iloc[0].get('defect_type', 'N/A').upper()
    m3.metric("Last Defect Type", latest_defect)
    
    # 4. Average Confidence
    avg_conf = 0
    if not df.empty and 'confidence' in df.columns:
        avg_conf = df['confidence'].mean()
    m4.metric("Avg. Confidence", f"{avg_conf:.1%}")

    # --- MAIN CONTENT AREA ---
    if not df.empty:
        st.markdown("### Operations Analytics")
        c1, c2 = st.columns([1, 2])
        
        with c1:
            # Donut Chart for Defect Distribution
            if 'defect_type' in df.columns:
                counts = df['defect_type'].value_counts().reset_index()
                counts.columns = ['Type', 'Count']
                fig = px.pie(counts, values='Count', names='Type', hole=0.5, 
                             color_discrete_sequence=px.colors.qualitative.Bold)
                fig.update_layout(showlegend=True, margin=dict(t=20, b=20, l=20, r=20), height=280)
                st.plotly_chart(fig, use_container_width=True)
        
        with c2:
            # Scatter Plot Timeline
            if 'datetime' in df.columns:
                fig2 = px.scatter(df, x='datetime', y='confidence', color='defect_type',
                                size='confidence', hover_data=['defect_type'],
                                color_discrete_sequence=px.colors.qualitative.Bold)
                fig2.update_layout(
                    xaxis_title="Timestamp", 
                    yaxis_title="Confidence Score",
                    margin=dict(t=20, b=20, l=0, r=0),
                    height=280,
                    showlegend=True
                )
                st.plotly_chart(fig2, use_container_width=True)

        # --- IMAGE GALLERY SECTION ---
        st.divider()
        st.markdown("### Defect Inspection Gallery")
        
        # Filter rows that have an image URL
        if 'image_url' in df.columns:
            gallery_df = df[df['image_url'].notna()].head(4) # Show 4 most recent
            
            if not gallery_df.empty:
                cols = st.columns(4)
                for idx, (_, row) in enumerate(gallery_df.iterrows()):
                    with cols[idx]:
                        st.image(row['image_url'], use_container_width=True)
                        st.markdown(f"**{row['defect_type'].upper()}**")
                        st.caption(f"{row['confidence']:.1%} | {row['datetime'].strftime('%H:%M:%S')}")
            else:
                st.info("No images uploaded. Run the detection client to capture data.")
        else:
            st.warning("Waiting for image data stream...")

        # --- RAW DATA TABLE ---
        with st.expander("View System Logs"):
            # Select specific columns for a cleaner view
            display_cols = ['datetime', 'defect_type', 'confidence', 'image_url']
            # Only keep columns that actually exist in the dataframe
            valid_cols = [c for c in display_cols if c in df.columns]
            
            st.dataframe(
                df[valid_cols].style.format({'confidence': '{:.2%}'}),
                use_container_width=True
            )
            
            if st.button("Clear System History"):
                database = init_firebase()
                if database:
                    database.reference('detections').delete()
                    database.reference('statistics').delete()
                    st.success("History cleared successfully.")
                    time.sleep(1)
                    st.rerun()

    else:
        st.info("System Ready. Waiting for incoming data stream...")

    # Auto-refresh every 3 seconds to keep dashboard live
    time.sleep(3)
    st.rerun()

if __name__ == "__main__":
    main()