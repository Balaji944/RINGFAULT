# IP Camera Integration Guide

This guide explains how to use your mobile phone as an IP webcam with this YOLOv8 project.

## 📱 Setup IP Webcam on Android Phone

### Step 1: Install IP Webcam App
1. Open Google Play Store on your Android phone
2. Search for "IP Webcam" by Pavel Khlebovich
3. Install the app

### Step 2: Configure IP Webcam
1. Open the IP Webcam app
2. Scroll down and tap **"Start server"**
3. You'll see a URL displayed, something like:
   ```
   http://192.168.1.105:8080
   ```
4. **Note down this IP address and port** - you'll need it for configuration

### Step 3: Connect Phone and Computer to Same Wi-Fi
- Make sure both your phone and Raspberry Pi/computer are connected to the same Wi-Fi network

## 🖥️ Setup on Raspberry Pi/Computer

### Step 1: Install Dependencies
```bash
# Activate your virtual environment (if using one)
source venv/bin/activate  # On Linux/Mac
# or
venv\Scripts\activate  # On Windows

# Install required packages
pip install -r requirements_ip_camera.txt
```

### Step 2: Configure IP Camera URL
1. Open `ip_camera_config.yaml`
2. Update the `ip_camera_url` with your phone's IP address:
   ```yaml
   ip_camera_url: "http://192.168.1.105:8080/video"
   ```
   Replace `192.168.1.105:8080` with your actual IP and port from the app.

### Step 3: Configure Capture Settings
Edit `ip_camera_config.yaml` to customize:
- `capture_interval_seconds`: Time between captures (default: 30 seconds)
- `output_directory`: Where to save captured images
- `enable_detection`: Enable/disable YOLOv8 detection on captured images
- `model_path`: Path to your trained YOLOv8 model

## 🚀 Usage

### Test Camera Connection
First, test if the camera connection works:
```bash
python ip_camera_capture.py --test
```
This will capture a single image to verify everything is working.

### Start Periodic Capture
```bash
# Capture images every 30 seconds (default interval)
python ip_camera_capture.py

# Capture for 60 minutes
python ip_camera_capture.py --duration 60

# Capture maximum 100 images
python ip_camera_capture.py --max-captures 100

# Use custom config file
python ip_camera_capture.py --config my_config.yaml
```

## 📁 Output Structure

```
My First Project.v1i.yolov8/
├── captured_images/          # Original captured images
│   ├── capture_20250101_120000.jpg
│   ├── capture_20250101_120030.jpg
│   └── ...
├── detections/               # Images with detection boxes (if enabled)
│   ├── detection_20250101_120000.jpg
│   └── ...
```

## ⚙️ Configuration Options

### `ip_camera_config.yaml` Parameters:

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ip_camera_url` | Full URL to IP webcam video stream | `http://192.168.1.105:8080/video` |
| `capture_interval_seconds` | Seconds between captures | `30` |
| `output_directory` | Directory for saved images | `captured_images` |
| `image_prefix` | Prefix for image filenames | `capture` |
| `enable_detection` | Run YOLOv8 detection | `true` |
| `model_path` | Path to trained model | `runs/detect/train/weights/best.pt` |
| `save_detections` | Save annotated detection images | `true` |
| `detection_output_dir` | Directory for detection results | `detections` |
| `image_quality` | JPEG quality (1-100) | `95` |
| `save_format` | Image format (jpg/png) | `jpg` |

## 🔧 Troubleshooting

### Camera Connection Failed
1. **Check IP address**: Make sure the IP address in config matches the one shown in IP Webcam app
2. **Check Wi-Fi**: Ensure phone and computer are on the same network
3. **Check firewall**: Temporarily disable firewall to test
4. **Test in browser**: Try opening `http://YOUR_IP:8080` in a web browser

### Images Not Saving
1. Check write permissions for the output directory
2. Ensure sufficient disk space
3. Check the path in `output_directory` is correct

### Detection Not Working
1. Verify model path exists: `runs/detect/train/weights/best.pt`
2. If model not found, it will use default `yolov8n.pt`
3. Check that `enable_detection: true` in config

### High CPU Usage
- Increase `capture_interval_seconds` to reduce capture frequency
- Disable detection if you only need images: `enable_detection: false`

## 📝 Example Workflow

1. **Setup**: Install IP Webcam app, note IP address
2. **Configure**: Update `ip_camera_config.yaml` with your IP
3. **Test**: Run `python ip_camera_capture.py --test`
4. **Start**: Run `python ip_camera_capture.py` for continuous capture
5. **Monitor**: Check `captured_images/` and `detections/` folders

## 🎯 Integration with Your Project

The captured images can be:
- **Used for dataset collection**: Copy images from `captured_images/` to `train/images/` or `valid/images/`
- **Analyzed in real-time**: Detection results are saved automatically if enabled
- **Processed later**: Use YOLOv8 predict on the captured images

## 💡 Tips

- **Battery**: Keep phone plugged in during long capture sessions
- **Storage**: Monitor disk space if capturing many high-resolution images
- **Network**: Use 5GHz Wi-Fi for better performance if available
- **Positioning**: Use a phone mount for consistent camera angle


