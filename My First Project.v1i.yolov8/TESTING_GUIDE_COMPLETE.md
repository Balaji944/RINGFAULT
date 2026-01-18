# 🧪 Complete Testing Guide for Faulty Rings Detection with MQTT

Step-by-step guide to test your detection system with and without MQTT integration.

---

## 📋 **Quick Test Checklist**

- [ ] Install dependencies
- [ ] Test without MQTT (basic functionality)
- [ ] Set up MQTT broker (optional)
- [ ] Configure MQTT settings
- [ ] Test with MQTT enabled
- [ ] Verify MQTT messages

---

## 🚀 **Step 1: Install Dependencies**

First, ensure all required packages are installed:

```bash
cd "My First Project.v1i.yolov8"
pip install -r requirements_ip_camera.txt
```

This installs:
- `opencv-python` - Image processing
- `pyyaml` - Configuration files
- `ultralytics` - YOLOv8 model
- `paho-mqtt` - MQTT client (optional)

---

## ✅ **Step 2: Test Without MQTT (Basic Functionality)**

Test the core detection functionality first to ensure everything works.

### **Option A: Interactive Mode (Easiest)**

```bash
python test.py
```

This will ask you to choose:
1. **Realtime (IP Camera)** - Live detection from phone
2. **Upload (Test Folder)** - Test images from test/images folder
3. **Exit**

### **Option B: Test Single Image**

```bash
# Test with default test image
python test.py --source test.jpg

# Or test with specific image
python test.py --source path/to/your/image.jpg

# With custom confidence threshold
python test.py --source test.jpg --conf 0.5
```

**Expected Output:**
```
============================================================
🔍 FAULTY RINGS DETECTION SYSTEM
============================================================
Detecting: breakage | crack | scratch
============================================================

📦 Loading model from: runs/detect/train/weights/best.pt
✓ Model loaded successfully
  Model classes: ['breakage', 'crack', 'scratch']

🔍 Testing Faulty Rings Detection on Image: test.jpg
✓ Prediction completed. Results saved to runs/detect/predict/test/

============================================================
Detection Results for: test.jpg
============================================================
✓ Ring Defects Detected: 2

Defect Breakdown:
────────────────────────────────────────────────────────────
  • BREAKAGE    :  0 detected
  • CRACK       :  1 detected | Avg Confidence: 85.2% | Max: 87.5%
  • SCRATCH     :  1 detected | Avg Confidence: 62.3% | Max: 65.0%
────────────────────────────────────────────────────────────
```

### **Option C: Test Multiple Images (Batch)**

```bash
# Test all images in test/images folder
python test.py --source test/images

# Test full dataset
python test.py --source dataset
```

### **Option D: Test with IP Camera**

```bash
# Continuous detection (every 5 seconds)
python test.py --source ip_camera

# Single capture
python test.py --source ip_camera --single

# Custom interval (every 10 seconds)
python test.py --source ip_camera --interval 10
```

### **Verify Results**

After testing, check:
- ✅ Annotated images in `runs/detect/predict/`
- ✅ Detection labels in `runs/detect/predict/test/labels/`
- ✅ Console output shows detection results
- ✅ No errors in console

---

## 📡 **Step 3: Set Up MQTT Broker (Optional)**

To test MQTT integration, you need an MQTT broker. Choose one option:

### **Option 1: Local Mosquitto (Recommended for Testing)**

#### **Windows:**
1. Download from: https://mosquitto.org/download/
2. Install Mosquitto
3. Start broker:
   ```bash
   mosquitto -v
   ```

#### **Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install mosquitto mosquitto-clients
sudo systemctl start mosquitto
sudo systemctl status mosquitto
```

#### **macOS:**
```bash
brew install mosquitto
brew services start mosquitto
```

#### **Docker (All Platforms):**
```bash
docker run -it -p 1883:1883 -p 9001:9001 eclipse-mosquitto
```

### **Option 2: Cloud MQTT (No Installation)**

1. Sign up for free at: https://www.hivemq.com/mqtt-cloud-broker/
2. Create a free cluster
3. Get connection details (host, port, username, password)
4. Update `mqtt_config.yaml` with your credentials

### **Verify Broker is Running**

```bash
# Test broker connection
mosquitto_pub -h localhost -t test -m "Hello MQTT"

# Subscribe to test topic
mosquitto_sub -h localhost -t test -v
```

If you see "Hello MQTT" in the subscriber, broker is working! ✅

---

## ⚙️ **Step 4: Configure MQTT**

Edit `mqtt_config.yaml`:

```yaml
# MQTT Broker Settings
broker: "localhost"  # Change to your broker IP/hostname
port: 1883  # 1883 for standard, 8883 for SSL
username: ""  # Leave empty if not required
password: ""  # Leave empty if not required

# Client Settings
client_id: "rings_detector_001"  # Unique identifier

# Topic Configuration
base_topic: "rings/detection"  # Base topic prefix

# Publishing Settings
enable_mqtt: true  # Enable/disable MQTT
publish_on_detection: true  # Publish when defects found
publish_on_no_detection: false  # Publish even when no defects
publish_image_path: true  # Include image paths
```

**For Cloud Brokers:**
```yaml
broker: "your-broker.hivemq.cloud"
port: 8883
username: "your-username"
password: "your-password"
use_ssl: true
```

---

## 🧪 **Step 5: Test with MQTT Enabled**

### **Test 1: Subscribe to MQTT Messages (Terminal 1)**

Open a terminal and subscribe to see all messages:

```bash
mosquitto_sub -h localhost -t "rings/detection/#" -v
```

This will show:
- Detection results
- Status updates
- All messages under `rings/detection/` topic

### **Test 2: Run Detection (Terminal 2)**

In another terminal:

```bash
# Test with single image
python test.py --source test.jpg

# Test with multiple images
python test.py --source test/images

# Test with IP camera
python test.py --source ip_camera --interval 5
```

### **What to Look For:**

**In Detection Terminal:**
```
✓ MQTT client initialized and connected
📡 MQTT: ENABLED
📤 Published detection to: rings/detection/results
```

**In MQTT Subscriber Terminal:**
```
rings/detection/status {"timestamp":"2024-12-25T14:30:22","status":"online","device_id":"rings_detector_001"}
rings/detection/results {"timestamp":"2024-12-25T14:30:22","device_id":"rings_detector_001","detections":[...],"summary":{...}}
```

### **Test 3: Verify JSON Messages**

The MQTT messages should be valid JSON. Example detection message:

```json
{
  "timestamp": "2024-12-25T14:30:22.123456",
  "device_id": "rings_detector_001",
  "source": "test.jpg",
  "detections": [
    {
      "class": "crack",
      "confidence": 0.8542,
      "bbox": {
        "x1": 150.5,
        "y1": 200.3,
        "x2": 300.7,
        "y2": 350.9
      }
    }
  ],
  "summary": {
    "breakage": {"count": 0, "avg_confidence": 0.0, "max_confidence": 0.0},
    "crack": {"count": 1, "avg_confidence": 0.8542, "max_confidence": 0.8542},
    "scratch": {"count": 0, "avg_confidence": 0.0, "max_confidence": 0.0}
  },
  "total_defects": 1,
  "image_path": "runs/detect/predict/test/test.jpg"
}
```

---

## 🛠️ **Step 6: Advanced Testing Scenarios**

### **Scenario 1: Test with MQTT Disabled**

```bash
python test.py --source test.jpg --no-mqtt
```

Should work normally without MQTT messages.

### **Scenario 2: Test with Custom MQTT Config**

```bash
python test.py --source test.jpg --mqtt-config custom_mqtt.yaml
```

### **Scenario 3: Monitor Status Only**

Subscribe to status topic:
```bash
mosquitto_sub -h localhost -t "rings/detection/status" -v
```

Run detection:
```bash
python test.py --source test.jpg
```

You should see:
- `online` status when detection starts
- `offline` status when detection ends

### **Scenario 4: Test IP Camera with MQTT**

1. Set up IP camera (see `IP_CAMERA_SETUP.md`)
2. Subscribe to MQTT:
   ```bash
   mosquitto_sub -h localhost -t "rings/detection/#" -v
   ```
3. Run continuous detection:
   ```bash
   python test.py --source ip_camera --interval 5
   ```
4. Watch messages appear every 5 seconds (or when defects are detected)

---

## 🔍 **Step 7: Troubleshooting**

### **Problem: "MQTT module not available"**

**Solution:**
```bash
pip install paho-mqtt
```

### **Problem: "MQTT connection failed"**

**Check:**
1. Broker is running:
   ```bash
   # Test broker
   mosquitto_pub -h localhost -t test -m "test"
   ```
2. Correct IP/port in `mqtt_config.yaml`
3. Firewall allows connection
4. Credentials are correct (if required)

### **Problem: "No messages published"**

**Check:**
1. `enable_mqtt: true` in `mqtt_config.yaml`
2. `publish_on_detection: true` (or `publish_on_no_detection: true`)
3. MQTT client connected (check console output)
4. Subscribed to correct topic: `rings/detection/#`

### **Problem: "Model not found"**

**Solution:**
```bash
# Train model first
python train.py
```

Or use default model (will show warning but works):
```bash
python test.py --source test.jpg
```

### **Problem: "No detections found"**

**Solutions:**
1. Lower confidence threshold:
   ```bash
   python test.py --source test.jpg --conf 0.2
   ```
2. Check if image contains rings
3. Verify model was trained on similar data

---

## 📊 **Step 8: Verify Complete Workflow**

### **Complete Test Sequence:**

1. **Start MQTT Broker:**
   ```bash
   mosquitto -v
   ```

2. **Subscribe to Messages (Terminal 1):**
   ```bash
   mosquitto_sub -h localhost -t "rings/detection/#" -v
   ```

3. **Run Detection (Terminal 2):**
   ```bash
   python test.py --source test.jpg
   ```

4. **Check Results:**
   - ✅ Console shows detection results
   - ✅ MQTT subscriber receives messages
   - ✅ Annotated images saved in `runs/detect/predict/`
   - ✅ JSON messages are valid

5. **Verify Files:**
   ```bash
   # Check annotated images
   ls runs/detect/predict/test/

   # Check detection labels
   ls runs/detect/predict/test/labels/
   ```

---

## 🎯 **Quick Test Commands Reference**

```bash
# Basic test (no MQTT)
python test.py --source test.jpg --no-mqtt

# Test with MQTT
python test.py --source test.jpg

# Interactive mode
python test.py

# Test directory
python test.py --source test/images

# Test full dataset
python test.py --source dataset

# IP camera test
python test.py --source ip_camera --interval 5

# Custom confidence
python test.py --source test.jpg --conf 0.5

# Custom MQTT config
python test.py --source test.jpg --mqtt-config custom.yaml
```

---

## ✅ **Success Criteria**

Your project is working correctly if:

- [ ] Detection runs without errors
- [ ] Detection results appear in console
- [ ] Annotated images are saved
- [ ] MQTT connects successfully (if enabled)
- [ ] MQTT messages are published (if enabled)
- [ ] JSON messages are valid
- [ ] Status updates are published

---

## 🎉 **Next Steps**

Once testing is successful:

1. **Customize MQTT Topics**: Update `base_topic` in config
2. **Integrate with IoT Platform**: Connect to Home Assistant, Node-RED, etc.
3. **Set Up Alerts**: Configure notifications for defects
4. **Monitor Production**: Deploy for continuous monitoring
5. **Analyze Data**: Log detections for analytics

---

**Happy Testing! 🧪✨**

For more details, see:
- `MQTT_INTEGRATION.md` - Complete MQTT setup guide
- `HOW_TO_RUN.md` - General usage guide
- `TESTING_GUIDE.md` - Original testing guide

