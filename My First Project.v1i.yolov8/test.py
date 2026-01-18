"""
Faulty Rings Detection - Main Test Script
Integrates YOLOv8 with Firebase for Real-time Dashboard
"""

import cv2
import time
import argparse
import sys
import os
import base64
from pathlib import Path
from ultralytics import YOLO
from glob import glob
from datetime import datetime

# --- IMPORT CUSTOM MODULES ---
from ip_camera_capture import IPCameraCapture
from cloud_client import CloudClient

# --- IMPORT CONFIGURATION ---
try:
    from firebase_config import FIREBASE_DATABASE_URL, SERVICE_ACCOUNT_KEY_PATH
except ImportError:
    print("❌ Error: firebase_config.py not found.")
    print("Please ensure you have created the configuration file.")
    sys.exit(1)

def print_summary(results, capture_count):
    """Prints a clean summary of what was detected locally."""
    print(f"\n--- Capture #{capture_count} Summary ---")
    if not results:
        print("No objects detected.")
        return

    for result in results:
        if result.boxes:
            for box in result.boxes:
                cls_name = result.names[int(box.cls[0])]
                conf = float(box.conf[0])
                print(f" • {cls_name}: {conf:.1%} confidence")
    print("--------------------------------")

def run_detection_system(model, source, conf_threshold, interval):
    print("\n" + "="*60)
    print("🚀 STARTING RING DETECTION SYSTEM")
    print(f"📡 Database: {FIREBASE_DATABASE_URL}")
    print("="*60)

    # 1. Initialize Cloud Connection
    client = None
    try:
        client = CloudClient(SERVICE_ACCOUNT_KEY_PATH, FIREBASE_DATABASE_URL)
        client.update_system_status(is_active=True)
        print("✅ Firebase Connected Successfully!")
    except Exception as e:
        print(f"⚠ Firebase connection failed: {e}")
        print("⚠ System will run in OFFLINE mode.")

    # 2. Initialize Camera
    capture = IPCameraCapture(config_path="ip_camera_config.yaml")
    
    # 3. Prepare image list if source is a directory
    image_files = []
    if source != 'ip_camera':
        source_path = Path(source)
        if source_path.is_dir():
            # Get all image files from directory
            image_extensions = ('*.jpg', '*.jpeg', '*.png', '*.bmp', '*.tiff')
            for ext in image_extensions:
                image_files.extend(sorted(source_path.glob(ext)))
                image_files.extend(sorted(source_path.glob(ext.upper())))
            
            if not image_files:
                print(f"❌ No images found in directory: {source}")
                return
            
            print(f"📁 Found {len(image_files)} images to process")
            print(f"   Processing: {[f.name for f in image_files[:3]]}{'...' if len(image_files) > 3 else ''}")
        else:
            # Single image file
            image_files = [source_path]
    
    if source == 'ip_camera':
        print("📷 Connecting to IP Camera...")
        capture.connect_camera()
    
    capture_count = 0
    valid_classes = ['breakage', 'crack', 'scratch']
    
    # Create directory for saving detected images
    detections_dir = Path("detected_faults")
    detections_dir.mkdir(exist_ok=True)
    print(f"💾 Saving detected faults to: {detections_dir.absolute()}")

    try:
        while True:
            capture_count += 1
            
            # --- CAPTURE FRAME ---
            frame = None
            if source == 'ip_camera':
                if not capture.cap or not capture.cap.isOpened():
                    print("⚠ Camera disconnected. Reconnecting...")
                    capture.connect_camera()
                    time.sleep(2)
                    continue
                ret, frame = capture.cap.read()
                if not ret:
                    print("⚠ Empty frame received.")
                    time.sleep(1)
                    continue
            else:
                # Process from image files
                if capture_count > len(image_files):
                    print(f"\n✅ Finished processing all {len(image_files)} images")
                    break
                
                image_path = image_files[capture_count - 1]
                frame = cv2.imread(str(image_path))
                if frame is None:
                    print(f"❌ Could not load image: {image_path}")
                    continue

            # --- RUN INFERENCE ---
            # verbose=False keeps the terminal clean
            results = model.predict(source=frame, conf=conf_threshold, save=False, verbose=False)

            # --- PROCESS RESULTS ---
            max_conf = 0.0
            defects_found = 0
            detected_types = []

            for result in results:
                for box in result.boxes:
                    cls_name = model.names[int(box.cls[0])]
                    conf = float(box.conf[0])
                    
                    if cls_name.lower() in valid_classes:
                        # We use a slightly higher threshold (0.6) for cloud alerts 
                        # to prevent false alarms on the dashboard
                        if conf >= 0.6:
                            defects_found += 1
                            detected_types.append(cls_name)
                            if conf > max_conf:
                                max_conf = conf

            # --- SEND TO CLOUD ---
            if defects_found > 0:
                # Get the most confident defect type
                primary_defect = detected_types[0] if detected_types else "defect"
                print(f"🚨 DEFECT DETECTED: {', '.join(set(detected_types))} ({max_conf:.1%})")
                
                # Draw bounding boxes on frame and save annotated image
                annotated_frame = results[0].plot() if results else frame.copy()
                
                timestamp_str = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
                image_filename = f"detected_{primary_defect}_{timestamp_str}.jpg"
                image_path = detections_dir / image_filename
                
                try:
                    # Save annotated frame with bounding boxes
                    cv2.imwrite(str(image_path), annotated_frame)
                    print(f"   💾 Saved: {image_path.name} (with annotations)")
                except Exception as e:
                    print(f"   ⚠ Could not save image: {e}")
                    image_filename = None
                
                if client and client.connected:
                    # Send with the actual defect type detected
                    client.send_detection(
                        confidence=round(max_conf, 2), 
                        ring_count=defects_found,
                        defect_type=primary_defect,
                        image_filename=image_filename
                    )
            else:
                print(f"✅ Capture #{capture_count}: Ring OK (or no ring)")

            # --- LOCAL DISPLAY (Optional) ---
            # cv2.imshow("Monitor", results[0].plot())
            # if cv2.waitKey(1) == ord('q'): break

            # --- WAIT INTERVAL ---
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n👋 Stopping system...")
    finally:
        if client:
            client.update_system_status(is_active=False)
        capture.cleanup()
        try:
            cv2.destroyAllWindows()
        except:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', default='runs/detect/train/weights/best.pt', help='Path to model weights')
    parser.add_argument('--source', default='ip_camera', help='ip_camera or path/to/image.jpg')
    parser.add_argument('--conf', type=float, default=0.5, help='Confidence threshold')
    parser.add_argument('--interval', type=int, default=5, help='Seconds between checks')
    
    args = parser.parse_args()

    # Load Model
    try:
        print(f"📦 Loading Model: {args.model}")
        model = YOLO(args.model)
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        sys.exit(1)

    run_detection_system(model, args.source, args.conf, args.interval)