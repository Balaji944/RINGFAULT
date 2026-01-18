# 🔍 Faulty Rings Detection System - Complete Setup Guide

## Overview

A **cloud-based real-time detection system** for identifying defects in rings using YOLOv8 and Firebase, with a live web dashboard.

### Features
✅ Real-time detection (breakage, crack, scratch)  
✅ Cloud-based data storage (Firebase)  
✅ Live web dashboard (Streamlit)  
✅ Multi-user access (team collaboration)  
✅ IP camera support  
✅ Detection history & analytics  
✅ One-click deployment to cloud

---

## Quick Start (5 Minutes)

### 1. Prerequisites
- Python 3.8+
- Firebase account (free tier available)
- IP Webcam app (on mobile phone) - optional

### 2. Installation

```bash
# Install dependencies
pip install -r requirements.txt

# OR install specific components
pip install firebase-admin streamlit plotly pandas
```

### 3. Configure Firebase

Edit `firebase_config.py`:
```python
FIREBASE_DATABASE_URL = "https://YOUR-PROJECT-ID.firebaseio.com"
SERVICE_ACCOUNT_KEY_PATH = "serviceAccountKey.json"
```

Get your database URL from: Firebase Console → Realtime Database → Your Database URL

### 4. Run Detection System

```bash
# Terminal 1: Start detection
python test.py --source ip_camera --interval 5
```

### 5. View Dashboard

```bash
# Terminal 2: Start dashboard
streamlit run app.py
```

Open browser to `http://localhost:8501`

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Ring Detection System                    │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴──────────┐
                    │                    │
            ┌───────▼────────┐    ┌──────▼──────────┐
            │  IP Webcam     │    │  Test Images   │
            │  (live stream) │    │  (batch test)  │
            └────────┬────────┘    └────────┬──────┘
                     │                      │
                     └──────────────┬───────┘
                                   │
                         ┌─────────▼────────┐
                         │  YOLOv8 Model    │
                         │  (test.py)       │
                         └────────┬─────────┘
                                  │
                     ┌────────────▼────────────┐
                     │   CloudClient          │
                     │   (Firebase Uploader)  │
                     └────────────┬────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │  Firebase Realtime DB      │
                    │  (Cloud Storage)           │
                    └─────────────┬──────────────┘
                                  │
                    ┌─────────────▼──────────────┐
                    │  Streamlit Dashboard       │
                    │  (app.py)                 │
                    │  Live Analytics & Charts  │
                    └────────────────────────────┘
```

---

## File Structure

```
My First Project.v1i.yolov8/
├── test.py                      # Main detection script
├── app.py                       # Streamlit dashboard
├── cloud_client.py              # Firebase integration
├── firebase_config.py           # Configuration
├── serviceAccountKey.json       # Firebase credentials (KEEP SECRET!)
├── generate_test_data.py        # Demo data generator
├── requirements.txt             # Python dependencies
├── CLOUD_SETUP.md              # Cloud setup guide
├── DASHBOARD_SETUP.md          # Dashboard guide
├── .streamlit/config.toml      # Streamlit configuration
│
├── test/images/                 # Test dataset images
├── train/images/                # Training dataset
├── captured_images/             # Live camera captures
├── runs/detect/predict/         # Detection outputs
└── ...other files
```

---

## Component Descriptions

### 1. test.py - Detection System
**Purpose**: Run YOLOv8 detection on images or live IP camera feed

**Usage**:
```bash
# Live IP camera detection
python test.py --source ip_camera --interval 5

# Single image
python test.py --source image.jpg

# Directory of images
python test.py --source test/images

# Full dataset test
python test.py --source dataset
```

**What it does**:
- Connects to IP camera or loads images
- Runs YOLO detection every N seconds
- Uploads results to Firebase automatically
- Shows real-time console output

### 2. app.py - Dashboard
**Purpose**: Interactive web interface to view detection results

**Tabs**:
- **Analytics**: Charts, graphs, defect distribution
- **Detection History**: Filterable list of all detections
- **Statistics**: Session stats, defect rates
- **Live Status**: Real-time system status

**Features**:
- Auto-refresh (configurable)
- Responsive design
- Works on mobile phones
- No local installation needed (when deployed)

### 3. cloud_client.py - Firebase Integration
**Purpose**: Handle all Firebase database operations

**Methods**:
```python
client = CloudClient(key_path, db_url)
client.connect()
client.send_detection(confidence=0.87, ring_count=1)
client.update_system_status(is_active=True)
client.disconnect()
```

### 4. firebase_config.py - Configuration
**Purpose**: Store Firebase credentials and settings

**Must contain**:
```python
FIREBASE_DATABASE_URL = "https://your-database.firebaseio.com"
SERVICE_ACCOUNT_KEY_PATH = "serviceAccountKey.json"
```

---

## Usage Examples

### Example 1: Live Detection with Dashboard

**Terminal 1** (Detection):
```bash
python test.py --source ip_camera --interval 5
```

**Terminal 2** (Dashboard):
```bash
streamlit run app.py
```

Result: Camera runs detection every 5 seconds, data appears on dashboard in real-time!

### Example 2: Batch Testing

```bash
python test.py --source test/images --conf 0.6
```

This tests all images in `test/images/` folder and uploads results to cloud.

### Example 3: Demo Dashboard Without Detection

Want to see the dashboard working?

```bash
python generate_test_data.py
streamlit run app.py
```

This generates sample data and shows dashboard with demo analytics!

---

## Cloud Deployment (Phase 4)

### Deploy Dashboard to Everyone (Free!)

1. **Push to GitHub**:
```bash
git init
git add .
git commit -m "Ring detection system"
git push -u origin main
```

2. **Deploy on Streamlit Cloud** (share.streamlit.io):
   - Select your GitHub repo
   - Click Deploy
   - Get a shareable URL!

Your team can now access the dashboard from anywhere:
```
https://YOUR_USERNAME-ring-detection.streamlit.app
```

---

## Troubleshooting

### ❌ "Firebase connection failed"
- Check `firebase_config.py` has correct URL
- Verify `serviceAccountKey.json` exists
- Ensure internet connection is stable

### ❌ "No data showing on dashboard"
- Run `python test.py` or `python generate_test_data.py`
- Wait 10 seconds for auto-refresh
- Check browser console for errors (F12)

### ❌ "IP camera not connecting"
- Verify IP Webcam app is running on phone
- Check `ip_camera_config.yaml` has correct IP
- Phone and computer must be on same WiFi

### ❌ "Dashboard won't load"
```bash
pip install --upgrade streamlit
streamlit run app.py --logger.level=debug
```

### ❌ "Import errors"
```bash
pip install -r requirements.txt --upgrade
```

---

## Configuration Files

### firebase_config.py
```python
FIREBASE_DATABASE_URL = "https://ring-detection-abc123.firebaseio.com"
SERVICE_ACCOUNT_KEY_PATH = "serviceAccountKey.json"
DEBUG = True
```

### ip_camera_config.yaml
```yaml
ip: "192.168.1.100:8080"  # Your phone's IP
username: "admin"
password: "admin"
quality: 0.8
```

### .streamlit/config.toml
Theme, colors, and UI settings for dashboard

---

## Data Storage

Your Firebase database stores:

```
detections/
├── 1705598123456  # timestamp
│   ├── defect_type: "crack"
│   ├── confidence: 0.87
│   └── timestamp: "2024-01-18T15:35:23"
└── ...

statistics/
├── 20240118_153000  # session ID
│   ├── total_captures: 150
│   ├── total_defects: 12
│   └── timestamp: "2024-01-18T15:30:00"
└── ...

system/
└── status
    ├── is_active: true
    └── detection_count: 250
```

---

## Performance Tips

1. **Faster Dashboard**: Increase refresh interval
   ```python
   refresh_interval = 30  # seconds
   ```

2. **Lower CPU Usage**: Reduce detection frequency
   ```bash
   python test.py --interval 10  # Check every 10 seconds
   ```

3. **Better Accuracy**: Increase confidence threshold
   ```bash
   python test.py --conf 0.7  # Only show 70%+ confidence
   ```

4. **Store Less Data**: Archive old detections
   ```python
   # In cloud_client.py, delete records older than 30 days
   ```

---

## Security Checklist

- ✅ `serviceAccountKey.json` is in `.gitignore`
- ✅ Never commit credentials to GitHub
- ✅ Use Firebase security rules in production
- ✅ Enable authentication for dashboard
- ✅ Regularly rotate service account keys

---

## Next Steps

1. ✅ **Phase 1**: Firebase Setup - DONE
2. ✅ **Phase 2**: Cloud Client - DONE
3. ✅ **Phase 3**: Streamlit Dashboard - DONE
4. ⏭️ **Phase 4**: Cloud Deployment (Optional)
   - Deploy dashboard (Streamlit Cloud)
   - Add user authentication
   - Set up monitoring alerts
   - Archive old data

---

## Support & Resources

- **Streamlit Docs**: https://docs.streamlit.io
- **Firebase Docs**: https://firebase.google.com/docs
- **YOLOv8 Guide**: https://docs.ultralytics.com
- **GitHub Issues**: Report bugs on this repo

---

## License

This project is open source. Modify freely for your needs!

---

## Team Access

To share with your team:

1. **Deploy dashboard** to Streamlit Cloud
2. **Share link**: `https://username-ring-detection.streamlit.app`
3. **Everyone can view** - no installation needed!
4. **Only you can** - run detection (requires Firebase credentials)

---

## Quick Commands Reference

```bash
# Installation
pip install -r requirements.txt

# Generate demo data
python generate_test_data.py

# Run detection system
python test.py --source ip_camera --interval 5

# Launch dashboard
streamlit run app.py

# Test cloud connection
python -c "from cloud_client import CloudClient; c = CloudClient(); c.connect()"

# Clear Streamlit cache
rm -rf ~/.streamlit/cache
```

---

**Made with ❤️ for Ring Defect Detection**
