"""
Cloud Client - Robust Version for Local Script (test.py)
"""
import firebase_admin
from firebase_admin import credentials, db
from datetime import datetime
import time
from pathlib import Path

class CloudClient:
    def __init__(self, key_path, db_url):
        self.connected = False
        self.app = None
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        print(f"🔌 Initializing Cloud Connection...")

        try:
            # FORCE string conversion to fix 'AttrDict' and path errors
            key_path = str(key_path)
            db_url = str(db_url)
            
            # Check if file exists
            if not Path(key_path).exists():
                print(f"❌ Error: Key file not found at: {key_path}")
                return

            # Connect (Single Instance Check)
            if not firebase_admin._apps:
                cred = credentials.Certificate(key_path)
                self.app = firebase_admin.initialize_app(cred, {
                    'databaseURL': db_url
                })
            else:
                self.app = firebase_admin.get_app()
            
            self.db = db
            self.connected = True
            print("✅ Firebase Connected Successfully!")
            
            # Send initial heartbeat to prove write access
            self.update_system_status(True)
            
        except Exception as e:
            print(f"❌ Connection Critical Error: {e}")
            self.connected = False

    def send_detection(self, confidence, ring_count=1, defect_type="unknown", image_filename=None):
        """Sends detection data to cloud"""
        if not self.connected:
            return

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
            
            # Upload to 'detections' list
            self.db.reference(f'detections/{int(timestamp * 1000)}').set(data)
            
            # Update 'current_session' stats
            self.db.reference('statistics/current_session').update({
                "last_active": time.time(),
                "last_defect": defect_type
            })
            
            print(f"   ☁️ Uploaded to Cloud: {defect_type} ({confidence:.1%})")
            
        except Exception as e:
            print(f"   ⚠ Upload Failed: {e}")

    def update_system_status(self, is_active):
        """Updates ON/OFF status"""
        if not self.connected:
            return

        try:
            self.db.reference('system_status').set({
                "is_active": is_active,
                "online": is_active,
                "last_heartbeat": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "session_id": self.session_id
            })
        except Exception as e:
            print(f"   ⚠ Status Update Failed: {e}")