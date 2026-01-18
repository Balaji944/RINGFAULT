"""
Test Data Generator for Dashboard Demo
Generates sample detection data in Firebase for testing the dashboard
"""

import time
import random
from datetime import datetime, timedelta
from cloud_client import CloudClient
from firebase_config import FIREBASE_DATABASE_URL, SERVICE_ACCOUNT_KEY_PATH

def generate_test_data():
    """Generate sample detection data"""
    print("🔧 Generating test data for dashboard demo...")
    
    # Initialize client
    client = CloudClient(SERVICE_ACCOUNT_KEY_PATH, FIREBASE_DATABASE_URL)
    if not client.connect():
        print("❌ Failed to connect to Firebase")
        return
    
    # Generate detections from last 24 hours
    defect_types = ['breakage', 'crack', 'scratch']
    
    print("\n📊 Generating 50 sample detections...")
    
    for i in range(50):
        # Random timestamp in last 24 hours
        hours_ago = random.randint(0, 24)
        minutes_ago = random.randint(0, 59)
        timestamp = datetime.now() - timedelta(hours=hours_ago, minutes=minutes_ago)
        
        # Random defect data
        defect = random.choice(defect_types)
        confidence = round(random.uniform(0.5, 0.99), 3)
        
        # Send detection
        client.send_detection(
            confidence=confidence,
            ring_count=random.randint(1, 3),
            defect_type=defect
        )
        
        if (i + 1) % 10 == 0:
            print(f"  ✓ Generated {i + 1} detections...")
    
    print("\n📈 Generating session statistics...")
    
    # Generate stats for multiple sessions
    for i in range(5):
        timestamp = datetime.now() - timedelta(hours=i*6)
        stats = {
            'timestamp': timestamp.isoformat(),
            'total_captures': random.randint(100, 500),
            'total_defects': random.randint(5, 50),
            'clean_images': random.randint(50, 450),
        }
        
        # Write to database
        import firebase_admin
        from firebase_admin import db
        
        session_id = timestamp.strftime("%Y%m%d_%H%M%S")
        ref = db.reference(f"statistics/{session_id}")
        ref.set(stats)
        
        print(f"  ✓ Session {i+1}/5 created")
    
    # Update system status
    client.update_system_status(is_active=True)
    
    # Update camera status
    client.update_camera_status(
        status="running",
        capture_count=sum([stats.get('total_captures', 0) for stats in [
            {
                'timestamp': (datetime.now() - timedelta(hours=i*6)).isoformat(),
                'total_captures': random.randint(100, 500),
            }
            for i in range(5)
        ]]),
        defects_found=50
    )
    
    print("\n✅ Test data generated successfully!")
    print("\nNow run the dashboard:")
    print("  streamlit run app.py")
    
    client.disconnect()

if __name__ == "__main__":
    generate_test_data()
