"""
IP Camera Capture Script for YOLOv8 Project
Captures images from mobile IP webcam at periodic intervals
"""

import cv2
import time
import os
import yaml
from datetime import datetime
from pathlib import Path
from ultralytics import YOLO
import argparse

# Get the project directory (where this script is located)
PROJECT_DIR = Path(__file__).parent.absolute()


class IPCameraCapture:
    def __init__(self, config_path="ip_camera_config.yaml"):
        """Initialize IP Camera Capture with configuration"""
        # Resolve config path relative to project directory
        if not Path(config_path).is_absolute():
            config_path = PROJECT_DIR / config_path
        
        self.config = self.load_config(str(config_path))
        self.cap = None
        self.model = None
        
        # Create output directories (project-relative)
        self.output_dir = PROJECT_DIR / self.config['output_directory']
        self.output_dir.mkdir(exist_ok=True)
        
        # Initialize YOLOv8 model if detection is enabled
        if self.config['enable_detection']:
            model_path = self.config['model_path']
            # Resolve model path relative to project directory if not absolute
            if not Path(model_path).is_absolute():
                model_path = PROJECT_DIR / model_path
            
            if os.path.exists(model_path):
                print(f"Loading YOLOv8 model from {model_path}")
                self.model = YOLO(str(model_path))
            else:
                print(f"Warning: Model not found at {model_path}. Using default yolov8n.pt")
                # Try project directory first, then current directory
                default_model = PROJECT_DIR / "yolov8n.pt"
                if default_model.exists():
                    self.model = YOLO(str(default_model))
                else:
                    self.model = YOLO("yolov8n.pt")
            
            if self.config['save_detections']:
                self.detection_dir = PROJECT_DIR / self.config['detection_output_dir']
                self.detection_dir.mkdir(exist_ok=True)
    
    def load_config(self, config_path):
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
            return config
        except FileNotFoundError:
            print(f"Config file {config_path} not found. Using default settings.")
            return self.get_default_config()
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}. Using default settings.")
            return self.get_default_config()
    
    def get_default_config(self):
        """Return default configuration"""
        return {
            'ip_camera_url': 'http://192.168.0.192:8080/video',
            'capture_interval_seconds': 30,
            'output_directory': 'captured_images',
            'image_prefix': 'capture',
            'enable_detection': False,
            'model_path': 'runs/detect/train/weights/best.pt',
            'save_detections': True,
            'detection_output_dir': 'detections',
            'image_quality': 95,
            'save_format': 'jpg'
        }
    
    def connect_camera(self):
        """Connect to IP camera"""
        url = self.config['ip_camera_url']
        print(f"Connecting to IP camera at {url}...")
        
        self.cap = cv2.VideoCapture(url)
        
        if not self.cap.isOpened():
            raise ConnectionError(f"Failed to connect to IP camera at {url}. "
                                f"Please check:\n"
                                f"1. IP Webcam app is running on your phone\n"
                                f"2. Phone and computer are on the same Wi-Fi network\n"
                                f"3. URL is correct: {url}")
        
        # Set buffer size to get latest frame
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        print("✓ Successfully connected to IP camera!")
        return True
    
    def capture_frame(self):
        """Capture a single frame from the camera"""
        if self.cap is None:
            raise RuntimeError("Camera not connected. Call connect_camera() first.")
        
        ret, frame = self.cap.read()
        
        if not ret:
            raise RuntimeError("Failed to capture frame from camera")
        
        return frame
    
    def save_image(self, frame, filename=None):
        """Save captured frame to disk"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{self.config['image_prefix']}_{timestamp}.{self.config['save_format']}"
        
        filepath = self.output_dir / filename
        
        # Save image with specified quality
        if self.config['save_format'].lower() == 'jpg':
            cv2.imwrite(str(filepath), frame, 
                       [cv2.IMWRITE_JPEG_QUALITY, self.config['image_quality']])
        else:
            cv2.imwrite(str(filepath), frame)
        
        print(f"✓ Image saved: {filepath}")
        return filepath
    
    def run_detection(self, frame):
        """Run YOLOv8 detection on frame"""
        if self.model is None:
            return None
        
        results = self.model(frame)
        return results
    
    def save_detection(self, frame, results, filename=None):
        """Save frame with detection boxes"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"detection_{timestamp}.{self.config['save_format']}"
        
        # Annotate frame with detection results
        annotated_frame = results[0].plot()
        
        filepath = self.detection_dir / filename
        cv2.imwrite(str(filepath), annotated_frame,
                   [cv2.IMWRITE_JPEG_QUALITY, self.config['image_quality']])
        
        print(f"✓ Detection saved: {filepath}")
        
        # Print detection summary
        if len(results[0].boxes) > 0:
            print(f"  Detected {len(results[0].boxes)} object(s):")
            for box in results[0].boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = self.model.names[cls] if hasattr(self.model, 'names') else f"class_{cls}"
                print(f"    - {class_name}: {conf:.2f}")
        else:
            print("  No objects detected")
        
        return filepath
    
    def capture_loop(self, duration_minutes=None, max_captures=None):
        """Main capture loop with periodic intervals"""
        interval = self.config['capture_interval_seconds']
        capture_count = 0
        start_time = time.time()
        
        print(f"\n{'='*60}")
        print(f"Starting IP Camera Capture")
        print(f"  Interval: {interval} seconds")
        print(f"  Output directory: {self.output_dir}")
        if self.config['enable_detection']:
            print(f"  Detection: Enabled")
            print(f"  Detection output: {self.detection_dir}")
        print(f"{'='*60}\n")
        
        try:
            while True:
                # Check duration limit
                if duration_minutes:
                    elapsed = (time.time() - start_time) / 60
                    if elapsed >= duration_minutes:
                        print(f"\nDuration limit ({duration_minutes} minutes) reached.")
                        break
                
                # Check capture limit
                if max_captures and capture_count >= max_captures:
                    print(f"\nCapture limit ({max_captures}) reached.")
                    break
                
                print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Capture #{capture_count + 1}")
                
                # Capture frame
                try:
                    frame = self.capture_frame()
                    
                    # Save original image
                    image_path = self.save_image(frame)
                    
                    # Run detection if enabled
                    if self.config['enable_detection']:
                        results = self.run_detection(frame)
                        if results and self.config['save_detections']:
                            self.save_detection(frame, results)
                    
                    capture_count += 1
                    
                except Exception as e:
                    print(f"✗ Error during capture: {e}")
                    print("  Retrying connection...")
                    time.sleep(5)
                    try:
                        self.connect_camera()
                    except Exception as reconnect_error:
                        print(f"✗ Reconnection failed: {reconnect_error}")
                        break
                
                # Wait for next capture
                if duration_minutes or (max_captures and capture_count < max_captures):
                    print(f"Waiting {interval} seconds until next capture...")
                    time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n\nCapture interrupted by user.")
        
        finally:
            self.cleanup()
            print(f"\n{'='*60}")
            print(f"Capture session completed!")
            print(f"  Total captures: {capture_count}")
            print(f"  Images saved to: {self.output_dir}")
            if self.config['enable_detection'] and self.config['save_detections']:
                print(f"  Detections saved to: {self.detection_dir}")
            print(f"{'='*60}\n")
    
    def cleanup(self):
        """Release camera resources"""
        if self.cap is not None:
            self.cap.release()
            print("Camera connection closed.")


def main():
    parser = argparse.ArgumentParser(description='IP Camera Capture for YOLOv8')
    parser.add_argument('--config', type=str, default='ip_camera_config.yaml',
                       help='Path to configuration file')
    parser.add_argument('--duration', type=int, default=None,
                       help='Capture duration in minutes (None for infinite)')
    parser.add_argument('--max-captures', type=int, default=None,
                       help='Maximum number of captures (None for infinite)')
    parser.add_argument('--test', action='store_true',
                       help='Test camera connection and capture one image')
    
    args = parser.parse_args()
    
    # Initialize capture system
    capture = IPCameraCapture(args.config)
    
    try:
        # Connect to camera
        capture.connect_camera()
        
        if args.test:
            # Test mode: capture one image
            print("\n[TEST MODE] Capturing single image...")
            frame = capture.capture_frame()
            capture.save_image(frame)
            if capture.config['enable_detection']:
                results = capture.run_detection(frame)
                if results and capture.config['save_detections']:
                    capture.save_detection(frame, results)
            print("\nTest completed successfully!")
        else:
            # Normal mode: periodic capture
            capture.capture_loop(
                duration_minutes=args.duration,
                max_captures=args.max_captures
            )
    
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())


