"""
Check what data is actually in Firebase
"""

import firebase_admin
from firebase_admin import credentials, db
from firebase_config import FIREBASE_DATABASE_URL, SERVICE_ACCOUNT_KEY_PATH

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate(SERVICE_ACCOUNT_KEY_PATH)
    firebase_admin.initialize_app(cred, {
        'databaseURL': FIREBASE_DATABASE_URL
    })

print("🔍 Checking Firebase data structure...\n")

# Check detections
try:
    ref = db.reference("detections")
    snapshot = ref.get()
    
    # Handle both response types
    if snapshot is None:
        data = {}
    elif hasattr(snapshot, 'val'):
        data = snapshot.val()
    else:
        data = snapshot
    
    if data and isinstance(data, dict):
        count = len(data)
        print(f"✓ Found {count} detections in 'detections' path")
        if count > 0:
            first_key = list(data.keys())[0]
            first_detection = data[first_key]
            print(f"  First detection: {first_detection}")
    else:
        print("✗ No data in 'detections' path")
except Exception as e:
    print(f"✗ Error reading detections: {e}")

# Check statistics
try:
    ref = db.reference("statistics")
    snapshot = ref.get()
    
    if snapshot is None:
        data = {}
    elif hasattr(snapshot, 'val'):
        data = snapshot.val()
    else:
        data = snapshot
    
    if data and isinstance(data, dict):
        count = len(data)
        print(f"\n✓ Found {count} statistics in 'statistics' path")
    else:
        print("\n✗ No data in 'statistics' path")
except Exception as e:
    print(f"\n✗ Error reading statistics: {e}")

# Check system status
try:
    ref = db.reference("system/status")
    snapshot = ref.get()
    
    if snapshot is None:
        data = {}
    elif hasattr(snapshot, 'val'):
        data = snapshot.val()
    else:
        data = snapshot
    
    if data and isinstance(data, dict):
        print(f"\n✓ System status: {data}")
    else:
        print("\n✗ No system status")
except Exception as e:
    print(f"\n✗ Error reading system status: {e}")

firebase_admin.delete_app(firebase_admin.get_app())
