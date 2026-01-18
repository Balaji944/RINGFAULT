"""
Firebase Configuration
Stores Firebase database URL and credentials
"""

# Your Firebase Realtime Database URL
# Get this from Firebase Console > Realtime Database > Data tab
FIREBASE_DATABASE_URL = "https://ring-detection-c6326-default-rtdb.firebaseio.com/"

# Path to your Firebase service account key
# Download from: Firebase Console > Project Settings > Service Accounts > Generate New Private Key
SERVICE_ACCOUNT_KEY_PATH = "serviceAccountKey.json"

# Database paths (collections where data will be stored)
DETECTION_RESULTS_PATH = "detections"  # Where detection results are stored
CAMERA_STATUS_PATH = "camera_status"   # Where camera status is stored
STATS_PATH = "statistics"              # Where statistics are stored

# Settings
DEBUG = True  # Set to False in production
MAX_RETRIES = 3  # Max retries for failed uploads
TIMEOUT_SECONDS = 10  # Timeout for Firebase operations
