"""
Cloud Client - Clean Version
"""
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import time

class CloudClient:
    def __init__(self, key_input=None, db_url=None):
        self.connected = False
        self.app = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"🔌 Initializing Cloud Connection...")

        try:
            # Import credentials from my_secrets
            from my_secrets import FIREBASE_CREDENTIALS, DATABASE_URL
            
            if not FIREBASE_CREDENTIALS:
                print("❌ Credentials are missing/empty.")
                return

            cred = credentials.Certificate(FIREBASE_CREDENTIALS)

            # Connect
            if not firebase_admin._apps:
                self.app = firebase_admin.initialize_app(cred, {
                    'databaseURL': DATABASE_URL
                })
            else:
                self.app = firebase_admin.get_app()
            
            self.db = db
            self.connected = True
            print("✅ Firebase Connected Successfully!")
            
            # Send heartbeat
            self.update_system_status(True)
            
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            self.connected = False

    def send_detection(self, confidence, ring_count=1, defect_type="unknown", image_filename=None):
        if not self.connected: return

        try:
            timestamp = time.time()
            data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "unix_timestamp": timestamp,
                "confidence": float(confidence),
                "ring_count": int(ring_count),
                "defect_type": str(defect_type).lower(),
                "image_filename": str(image_filename) if image_filename else None,
                "session_id": self.session_id
            }
            
            self.db.reference(f'detections/{int(timestamp * 1000)}').set(data)
            self.db.reference('statistics/current_session').update({
                "last_active": time.time(),
                "last_defect": defect_type
            })
            print(f"   ☁️ Uploaded to Cloud: {defect_type} ({confidence:.1%})")
            
        except Exception as e:
            print(f"   ⚠ Upload Failed: {e}")

    def update_system_status(self, is_active):
        if not self.connected: return
        try:
            self.db.reference('system_status').set({
                "is_active": is_active,
                "online": is_active,
                "last_heartbeat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "session_id": self.session_id
            })
        except Exception as e:
            print(f"   ⚠ Status Update Failed: {e}")