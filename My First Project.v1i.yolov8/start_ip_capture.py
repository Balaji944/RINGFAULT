"""
Quick Start Script for IP Camera Capture
Simplified version for easy usage
"""

import sys
from ip_camera_capture import IPCameraCapture

def main():
    print("=" * 60)
    print("IP Camera Capture - Quick Start")
    print("=" * 60)
    print("\nMake sure:")
    print("1. IP Webcam app is running on your phone")
    print("2. Phone and computer are on the same Wi-Fi")
    print("3. You've updated ip_camera_config.yaml with your phone's IP")
    print("\n" + "=" * 60 + "\n")
    
    # Ask user for confirmation
    response = input("Ready to start? (y/n): ").strip().lower()
    if response != 'y':
        print("Cancelled.")
        return 0
    
    # Initialize and start
    capture = IPCameraCapture()
    
    try:
        capture.connect_camera()
        
        # Ask for capture mode
        print("\nCapture Mode:")
        print("1. Continuous (until Ctrl+C)")
        print("2. Limited duration (minutes)")
        print("3. Limited captures (count)")
        print("4. Test mode (single capture)")
        
        choice = input("\nSelect mode (1-4): ").strip()
        
        if choice == '1':
            capture.capture_loop()
        elif choice == '2':
            minutes = int(input("Enter duration in minutes: "))
            capture.capture_loop(duration_minutes=minutes)
        elif choice == '3':
            count = int(input("Enter number of captures: "))
            capture.capture_loop(max_captures=count)
        elif choice == '4':
            frame = capture.capture_frame()
            capture.save_image(frame)
            if capture.config['enable_detection']:
                results = capture.run_detection(frame)
                if results and capture.config['save_detections']:
                    capture.save_detection(frame, results)
            print("\nTest completed!")
        else:
            print("Invalid choice. Using continuous mode.")
            capture.capture_loop()
    
    except KeyboardInterrupt:
        print("\n\nStopped by user.")
        capture.cleanup()
    except Exception as e:
        print(f"\nError: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())


