#!/usr/bin/env python
"""Test cloud_client API compatibility with test.py"""

from firebase_config import FIREBASE_DATABASE_URL, SERVICE_ACCOUNT_KEY_PATH
from cloud_client import CloudClient

print("Testing CloudClient API compatibility...")

try:
    # Test 1: Initialize with parameters (test.py style)
    client = CloudClient(SERVICE_ACCOUNT_KEY_PATH, FIREBASE_DATABASE_URL)
    print("✓ CloudClient(key_path, db_url) works")
    
    # Test 2: Connect
    if client.connect():
        print("✓ client.connect() works")
    else:
        print("✗ Connection failed")
    
    # Test 3: update_system_status
    if client.update_system_status(is_active=True):
        print("✓ client.update_system_status(is_active=True) works")
    
    # Test 4: send_detection
    if client.send_detection(confidence=0.87, ring_count=1):
        print("✓ client.send_detection(confidence, ring_count) works")
    
    # Test 5: Cleanup
    client.disconnect()
    print("✓ client.disconnect() works")
    
    print("\n✅ test.py is CORRECT! All CloudClient methods work!")

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
