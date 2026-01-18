"""
Delete all test data from Firebase
Run this to clear out the generated test data so you can use your real detections
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

print("🗑️  Deleting test data from Firebase...")

# Delete all detections
try:
    db.reference("detections").delete()
    print("✓ Deleted all detections")
except Exception as e:
    print(f"⚠ Error deleting detections: {e}")

# Delete all statistics
try:
    db.reference("statistics").delete()
    print("✓ Deleted all statistics")
except Exception as e:
    print(f"⚠ Error deleting statistics: {e}")

# Delete system status
try:
    db.reference("system/status").delete()
    print("✓ Deleted system status")
except Exception as e:
    print(f"⚠ Error deleting system status: {e}")

# Delete camera status
try:
    db.reference("camera_status").delete()
    print("✓ Deleted camera status")
except Exception as e:
    print(f"⚠ Error deleting camera status: {e}")

firebase_admin.delete_app(firebase_admin.get_app())

print("\n✅ All test data cleared! Firebase is ready for your real detections.")
print("\nNow run your detection system:")
print("  python test.py --source ip_camera --interval 5")
print("\nThen open the dashboard:")
print("  streamlit run app.py")
