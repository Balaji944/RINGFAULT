"""
Cloud Client for Firebase Realtime Database
Replaces MQTT client - sends detection results to cloud
"""

import firebase_admin
from firebase_admin import credentials, db
import json
from datetime import datetime
from pathlib import Path
import time
from typing import Optional, Dict, Any


class CloudClient:
    """Firebase Realtime Database client for detection results"""
    
    def __init__(self, service_account_key_path: str = None, database_url: str = None):
        """
        Initialize Firebase connection
        
        Args:
            service_account_key_path: Path to service account JSON key
            database_url: Firebase Realtime Database URL
        """
        self.connected = False
        self.app = None
        self.db = None
        self.session_id = self._generate_session_id()
        self.detection_count = 0
        
        try:
            # Use provided credentials or fall back to config file
            if service_account_key_path and database_url:
                self.key_path = service_account_key_path
                self.db_url = database_url
            else:
                # Load from firebase_config.py
                import firebase_config
                self.key_path = firebase_config.SERVICE_ACCOUNT_KEY_PATH
                self.db_url = firebase_config.FIREBASE_DATABASE_URL
            
            # Validate
            if not Path(self.key_path).exists():
                raise FileNotFoundError(f"Service account key not found: {self.key_path}")
            
            print("✓ Firebase config loaded")
            
            # AUTO-CONNECT on init
            self.connect()
            
        except Exception as e:
            print(f"✗ Error loading config: {e}")
            raise
    
    def connect(self) -> bool:
        """
        Connect to Firebase Realtime Database
        
        Returns:
            bool: True if connected successfully
        """
        try:
            # Initialize Firebase only once
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.key_path)
                self.app = firebase_admin.initialize_app(cred, {
                    'databaseURL': self.db_url
                })
            else:
                self.app = firebase_admin.get_app()
            
            self.db = db
            
            # Test connection by writing a test message
            test_data = {
                'timestamp': datetime.now().isoformat(),
                'status': 'connected',
                'session_id': self.session_id
            }
            self.db.reference('system/last_connection').set(test_data)
            
            self.connected = True
            print(f"✓ Cloud client connected (Session ID: {self.session_id})")
            
            return True
            
        except Exception as e:
            print(f"✗ Cloud connection failed: {e}")
            self.connected = False
            return False
    
    def disconnect(self):
        """Disconnect from Firebase"""
        try:
            if self.app:
                firebase_admin.delete_app(self.app)
            self.connected = False
            print("✓ Cloud client disconnected")
        except Exception as e:
            print(f"⚠ Error disconnecting: {e}")
    
    def publish_detection(self, 
                         defect_type: str, 
                         confidence: float, 
                         image_filename: str = None,
                         timestamp: float = None,
                         additional_data: Dict = None) -> bool:
        """
        Publish detection result to cloud
        
        Args:
            defect_type: Type of defect (breakage, crack, scratch)
            confidence: Confidence score (0-1)
            image_filename: Name of the detected image
            timestamp: Unix timestamp
            additional_data: Any additional data to store
        
        Returns:
            bool: True if published successfully
        """
        if not self.connected:
            return False
        
        try:
            timestamp = timestamp or time.time()
            detection_data = {
                'timestamp': datetime.fromtimestamp(timestamp).isoformat(),
                'unix_timestamp': timestamp,
                'defect_type': defect_type.lower(),
                'confidence': round(confidence, 4),
                'image_filename': image_filename,
                'session_id': self.session_id,
            }
            
            # Add additional data if provided
            if additional_data:
                detection_data.update(additional_data)
            
            # Write to cloud - creates unique entry with timestamp
            ref = self.db.reference(f"detections/{int(timestamp * 1000)}")
            ref.set(detection_data)
            
            self.detection_count += 1
            return True
            
        except Exception as e:
            print(f"⚠ Failed to upload detection: {e}")
            return False
    
    def send_detection(self, confidence: float, ring_count: int = 1, 
                      defect_type: str = "defect", image_filename: str = None) -> bool:
        """
        Simple method to send detection (for backward compatibility)
        
        Args:
            confidence: Confidence score (0-1)
            ring_count: Number of defects found
            defect_type: Type of defect (default: "defect")
            image_filename: Name of the saved image file (optional)
        
        Returns:
            bool: True if sent successfully
        """
        if not self.connected:
            return False
        
        try:
            timestamp = time.time()
            detection_data = {
                'timestamp': datetime.fromtimestamp(timestamp).isoformat(),
                'unix_timestamp': timestamp,
                'defect_type': defect_type.lower(),
                'confidence': round(confidence, 4),
                'ring_count': ring_count,
                'session_id': self.session_id,
            }
            
            # Add image filename if provided
            if image_filename:
                detection_data['image_filename'] = image_filename
            
            # Write to cloud
            ref = self.db.reference(f"detections/{int(timestamp * 1000)}")
            ref.set(detection_data)
            
            self.detection_count += 1
            return True
            
        except Exception as e:
            print(f"⚠ Failed to send detection: {e}")
            return False
    
    def publish_batch_detections(self, detections_list: list) -> int:
        """
        Publish multiple detections at once
        
        Args:
            detections_list: List of detection dicts with keys:
                           defect_type, confidence, image_filename, etc.
        
        Returns:
            int: Number of successfully published detections
        """
        if not self.connected:
            print("⚠ Not connected to cloud")
            return 0
        
        success_count = 0
        for detection in detections_list:
            if self.publish_detection(**detection):
                success_count += 1
        
        print(f"☁️  Batch upload: {success_count}/{len(detections_list)} detections saved")
        return success_count
    def update_camera_status(self, status: str, capture_count: int = 0, 
                           last_capture: str = None, defects_found: int = 0) -> bool:
        """
        Update camera status in cloud
        
        Args:
            status: Status message (running, stopped, error, etc.)
            capture_count: Number of captures so far
            last_capture: Timestamp of last capture
            defects_found: Number of defects found so far
        
        Returns:
            bool: True if updated successfully
        """
        if not self.connected:
            return False
        
        try:
            status_data = {
                'timestamp': datetime.now().isoformat(),
                'status': status,
                'session_id': self.session_id,
                'capture_count': capture_count,
                'last_capture': last_capture,
                'defects_found': defects_found,
            }
            
            ref = self.db.reference(f"camera_status/current")
            ref.set(status_data)
            
            return True
            
        except Exception as e:
            print(f"⚠ Failed to update status: {e}")
            return False
    
    def update_system_status(self, is_active: bool) -> bool:
        """
        Update system status (active/inactive)
        
        Args:
            is_active: True if system is active, False if stopped
        
        Returns:
            bool: True if updated successfully
        """
        if not self.connected:
            return False
        
        try:
            status_data = {
                'timestamp': datetime.now().isoformat(),
                'is_active': is_active,
                'status': 'running' if is_active else 'stopped',
                'session_id': self.session_id,
                'detection_count': self.detection_count,
            }
            
            ref = self.db.reference(f"system/status")
            ref.set(status_data)
            
            return True
            
        except Exception as e:
            print(f"⚠ Failed to update system status: {e}")
            return False
    
    def publish_session_stats(self, stats: Dict[str, Any]) -> bool:
        """
        Publish session statistics to cloud
        
        Args:
            stats: Dictionary with statistics (total_captures, total_defects, 
                   defects_by_type, avg_confidence, etc.)
        
        Returns:
            bool: True if published successfully
        """
        if not self.connected:
            return False
        
        try:
            stats_data = {
                'timestamp': datetime.now().isoformat(),
                'session_id': self.session_id,
                **stats
            }
            
            ref = self.db.reference(f"statistics/{self.session_id}")
            ref.set(stats_data)
            
            return True
            
        except Exception as e:
            print(f"⚠ Failed to upload stats: {e}")
            return False
    
    def get_recent_detections(self, limit: int = 10) -> list:
        """
        Fetch recent detections from cloud
        
        Args:
            limit: Number of recent detections to fetch
        
        Returns:
            list: List of recent detection dicts
        """
        if not self.connected:
            return []
        
        try:
            ref = self.db.reference("detections")
            detections = ref.order_by_child('unix_timestamp').limit_to_last(limit).get()
            
            if detections.val():
                return list(detections.val().values())
            return []
            
        except Exception as e:
            print(f"⚠ Failed to fetch detections: {e}")
            return []
    
    def get_session_stats(self, session_id: str = None) -> Dict:
        """
        Fetch statistics for a session
        
        Args:
            session_id: Session ID to fetch stats for (default: current session)
        
        Returns:
            dict: Session statistics
        """
        if not self.connected:
            return {}
        
        try:
            session = session_id or self.session_id
            ref = self.db.reference(f"statistics/{session}")
            stats = ref.get()
            
            return stats.val() or {}
            
        except Exception as e:
            print(f"⚠ Failed to fetch stats: {e}")
            return {}
    
    def _generate_session_id(self) -> str:
        """Generate unique session ID"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def is_connected(self) -> bool:
        """Check if connected to cloud"""
        return self.connected


# For backward compatibility with old MQTT code
class MQTTClient(CloudClient):
    """Compatibility wrapper - CloudClient acts like MQTTClient"""
    pass
