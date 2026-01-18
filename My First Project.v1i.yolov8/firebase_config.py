"""
Firebase Configuration
Stores Firebase database URL and credentials
"""
import os
import json

# Check if running on Streamlit Cloud
try:
    import streamlit as st
    IS_STREAMLIT_CLOUD = hasattr(st, 'secrets')
except:
    IS_STREAMLIT_CLOUD = False

# Your Firebase Realtime Database URL
if IS_STREAMLIT_CLOUD:
    # Read from Streamlit secrets when deployed
    FIREBASE_DATABASE_URL = st.secrets.get("firebase", {}).get("database_url", "https://ring-detection-c6326-default-rtdb.firebaseio.com/")
    SERVICE_ACCOUNT_KEY_PATH = st.secrets.get("firebase", {})  # Entire dict from secrets
else:
    # Read from local file when running locally
    FIREBASE_DATABASE_URL = "https://ring-detection-c6326-default-rtdb.firebaseio.com/"
    SERVICE_ACCOUNT_KEY_PATH = "serviceAccountKey.json"

# Database paths (collections where data will be stored)
DETECTION_RESULTS_PATH = "detections"  # Where detection results are stored
CAMERA_STATUS_PATH = "camera_status"   # Where camera status is stored
STATS_PATH = "statistics"              # Where statistics are stored

# Settings
DEBUG = True  # Set to False in production
MAX_RETRIES = 3  # Max retries for failed uploads
TIMEOUT_SECONDS = 10  # Timeout for Firebase operations
