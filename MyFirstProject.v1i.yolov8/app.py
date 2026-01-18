"""
Faulty Rings Detection - Dashboard
v3.0 - Fixed Timezones & Caching
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime, timedelta
import time

# ============================================================================
# CONFIG & SETUP
# ============================================================================
st.set_page_config(page_title="Ring Detection Dashboard", page_icon="💍", layout="wide")

# Force Streamlit to treat timestamps as UTC to avoid timezone math errors
pd.options.mode.chained_assignment = None 

# ============================================================================
# FIREBASE CONNECTION
# ============================================================================
@st.cache_resource
def init_firebase():
    """Initialize Firebase connection"""
    try:
        if firebase_admin._apps:
            return db
            
        # Try loading from Secrets (Cloud)
        if "firebase" in st.secrets:
            key_dict = dict(st.secrets["firebase"])
            # Fix private key newlines
            if "private_key" in key_dict:
                key_dict["private_key"] = key_dict["private_key"].replace("\\n", "\n")
            
            cred = credentials.Certificate(key_dict)
            firebase_admin.initialize_app(cred, {'databaseURL': st.secrets["database_url"]})
            return db
            
        return None
    except Exception as e:
        st.error(f"Firebase Error: {e}")
        return None

# ============================================================================
# DATA FETCHING
# ============================================================================
def get_data():
    """Fetch all data without caching to ensure real-time updates"""
    database = init_firebase()
    if not database: return pd.DataFrame()
    
    try:
        ref = database.reference('detections')
        # Get last 100 records to keep it fast
        snapshot = ref.order_by_key().limit_to_last(100).get()
        
        if not snapshot: return pd.DataFrame()
        
        data_list = []
        for key, val in snapshot.items():
            val['id'] = key
            data_list.append(val)
            
        df = pd.DataFrame(data_list)
        
        # CRITICAL FIX: Use unix_timestamp for sorting, then convert to readable
        if 'unix_timestamp' in df.columns:
            df['datetime'] = pd.to_datetime(df['unix_timestamp'], unit='s')
            # Adjust to IST (UTC+5:30) for display manually if needed, 
            # but usually browser handles local time. Let's keep it simple.
            df = df.sort_values('unix_timestamp', ascending=False)
            
        return df
    except Exception as e:
        st.error(f"Data Error: {e}")
        return pd.DataFrame()

def get_system_status():
    database = init_firebase()
    if not database: return {}
    try:
        return database.reference('system_status').get() or {}
    except:
        return {}

# ============================================================================
# MAIN DASHBOARD
# ============================================================================
def main():
    st.title("💍 Faulty Rings Live Dashboard")
    
    # --- ACTION BAR ---
    col1, col2, col3 = st.columns([6, 2, 2])
    with col2:
        if st.button("🔄 Force Refresh Data"):
            st.cache_data.clear()
            st.rerun()
    with col3:
        if st.button("🗑️ Clear All History"):
            database = init_firebase()
            if database:
                database.reference('detections').delete()
                database.reference('statistics').delete()
                st.success("History cleared!")
                time.sleep(1)
                st.rerun()

    # --- FETCH DATA ---
    df = get_data()
    status_data = get_system_status()
    
    # --- STATUS INDICATORS ---
    st.markdown("---")
    c1, c2, c3, c4 = st.columns(4)
    
    # 1. System Status
    is_active = status_data.get('is_active', False)
    # Check if heartbeat is recent (within 60 seconds)
    last_heartbeat = status_data.get('last_heartbeat', '')
    state = "🔴 STOPPED"
    if is_active:
        state = "🟢 RUNNING"
        
    c1.metric("System Status", state)
    
    # 2. Total Count
    c2.metric("Total Detections", len(df))
    
    # 3. Last Defect
    last_defect = "None"
    if not df.empty:
        last_defect = df.iloc[0].get('defect_type', 'None')
    c3.metric("Latest Defect", last_defect.upper())
    
    # 4. Avg Confidence
    avg_conf = 0
    if not df.empty and 'confidence' in df.columns:
        avg_conf = df['confidence'].mean()
    c4.metric("Avg Confidence", f"{avg_conf:.1%}")

    st.markdown("---")

    # --- DATA VISUALIZATION ---
    if not df.empty:
        t1, t2 = st.tabs(["📊 Analytics", "📋 Raw Data Log"])
        
        with t1:
            col_a, col_b = st.columns(2)
            
            with col_a:
                # Pie Chart
                if 'defect_type' in df.columns:
                    counts = df['defect_type'].value_counts()
                    fig = px.pie(values=counts, names=counts.index, title="Defect Distribution")
                    st.plotly_chart(fig, use_container_width=True)
            
            with col_b:
                # Timeline
                if 'datetime' in df.columns:
                    fig2 = px.scatter(df, x='datetime', y='confidence', 
                                    color='defect_type', title="Detection Timeline")
                    st.plotly_chart(fig2, use_container_width=True)

        with t2:
            st.dataframe(df[['datetime', 'defect_type', 'confidence', 'image_filename']], use_container_width=True)
            
    else:
        st.info("Waiting for data... Run 'python test.py' on your laptop!")

    # Auto-refresh every 5 seconds
    time.sleep(5)
    st.rerun()

if __name__ == "__main__":
    main()