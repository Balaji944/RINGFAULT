# 🚀 How to Run the Faulty Rings Detection Project

Complete guide on running this YOLOv8-based ring defect detection system.

---

## 📋 **What This Project Does**

This project is a **Faulty Rings Detection System** that uses YOLOv8 deep learning to automatically detect defects in O-rings (circular seals). It can identify three types of defects:

- **🔴 breakage** - Complete breaks or fractures in the ring
- **⚡ crack** - Cracks or fissures in the ring material  
- **➖ scratch** - Surface scratches or abrasions

### **Key Features:**
- ✅ Train a custom YOLOv8 model on your ring dataset
- ✅ Test on static images (single or batch)
- ✅ Live detection using IP camera from your mobile phone
- ✅ Continuous monitoring with periodic captures
- ✅ Detailed detection reports with confidence scores

---

## 🛠️ **Prerequisites**

Before running, ensure you have:

1. **Python 3.8+** installed
2. **Dependencies installed:**
   ```bash
   cd "My First Project.v1i.yolov8"
   pip install -r requirements_ip_camera.txt
   ```

3. **For IP Camera (optional):**
   - IP Webcam app installed on Android phone
   - Phone and computer on same Wi-Fi network
   - IP address configured in `ip_camera_config.yaml`

---

## 📝 **Step-by-Step Guide**

### **Step 1: Train the Model (First Time Only)**

If you haven't trained the model yet, or want to retrain:

```bash
cd "My First Project.v1i.yolov8"
python train.py
```

**What it does:**
- Loads YOLOv8 nano model (`yolov8n.pt`)
- Trains on your dataset (369 training images)
- Saves trained model to `runs/detect/train/weights/best.pt`
- Takes ~30-60 minutes depending on your CPU/GPU

**Expected Output:**
- Training progress with loss metrics
- Validation results
- Saved model at `runs/detect/train/weights/best.pt`
- Training plots and graphs in `runs/detect/train/`

---

### **Step 2: Test the Model**

You can test the model in several ways:

#### **Option A: Interactive Mode (Easiest)**

```bash
python test.py
```

This will ask you to choose:
- **1. Realtime (IP Camera)** - Live detection from mobile phone
- **2. Upload (Test Folder)** - Test images from `test/images` folder
- **3. Exit**

#### **Option B: Test with Static Images**

```bash
# Test single image
python test.py --source test.jpg

# Test all images in test folder
python test.py --source test/images

# Test full dataset
python test.py --source dataset
```

**What it does:**
- Loads your trained model (or default if not trained)
- Processes image(s) through YOLOv8
- Detects ring defects (breakage, crack, scratch)
- Saves annotated images to `runs/detect/predict/`
- Prints detailed detection summary

**Expected Output:**
```
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
✓ Ring Defects Detected: 2 (breakage/crack ≥ 60%, scratch ≥ 50%)

Defect Breakdown:
────────────────────────────────────────────────────────────
  • BREAKAGE    :  1 detected | Avg Confidence: 85.2% | Max: 87.5%
  • CRACK       :  0 detected
  • SCRATCH     :  1 detected | Avg Confidence: 62.3% | Max: 65.0%
────────────────────────────────────────────────────────────
```

#### **Option C: Test with IP Camera (Live Detection)**

**First, setup IP Camera:**
1. Install "IP Webcam" app on Android phone
2. Start the server in the app
3. Note the IP address (e.g., `http://192.168.1.105:8080`)
4. Update `ip_camera_config.yaml` with your IP:
   ```yaml
   ip_camera_url: "http://YOUR_PHONE_IP:8080/video"
   ```

**Then run:**
```bash
# Continuous detection (every 5 seconds)
python test.py --source ip_camera

# Single capture
python test.py --source ip_camera --single

# Custom interval (every 10 seconds)
python test.py --source ip_camera --interval 10

# Custom confidence threshold
python test.py --source ip_camera --conf 0.7
```

**What it does:**
- Connects to your phone's camera via Wi-Fi
- Captures frames at specified intervals
- Runs YOLOv8 detection on each frame
- Saves original images to `captured_images/`
- Saves annotated images to `runs/detect/predict/`
- Prints detection results in real-time
- Continues until you press `Ctrl+C`

**Expected Output:**
```
📷 LIVE FAULTY RINGS DETECTION - IP Camera Mode
============================================================
Detecting: breakage, crack, scratch
Capture Interval: 5 seconds
============================================================

Connecting to IP camera...
✓ Successfully connected to IP camera!

🔄 Starting continuous detection (every 5s)
Press Ctrl+C to stop

────────────────────────────────────────────────────────────
[20251225_143022] Capture #1
────────────────────────────────────────────────────────────
📸 Capturing frame from IP camera...
🔍 Running YOLOv8 detection for faulty rings...
✓ Images saved: ip_camera_20251225_143022.jpg (annotated) + ip_camera_20251225_143022.jpg (original in captured_images)

✓ Ring Defects Detected: 1
  • CRACK: 1 detected | Avg Confidence: 78.5% | Max: 78.5%

⏳ Waiting 5 seconds until next capture...
```

---

### **Step 3: IP Camera Periodic Capture (Alternative)**

For continuous image capture without detection:

```bash
# Test connection (single capture)
python ip_camera_capture.py --test

# Continuous capture (every 30 seconds by default)
python ip_camera_capture.py

# Capture for 10 minutes
python ip_camera_capture.py --duration 10

# Capture 20 images
python ip_camera_capture.py --max-captures 20

# Interactive mode
python start_ip_capture.py
```

**What it does:**
- Captures images from IP camera at intervals
- Saves to `captured_images/` folder
- Optionally runs detection if enabled in config
- Saves detection results to `detections/` folder

---

## 📂 **Output Directories**

After running, you'll find results in:

- **`runs/detect/predict/`** - Annotated images with detection boxes
- **`captured_images/`** - Original images from IP camera
- **`detections/`** - Detection results (if using `ip_camera_capture.py`)
- **`runs/detect/train/`** - Training results and model weights

---

## ⚙️ **Command Line Options**

### **test.py Options:**

```bash
python test.py [OPTIONS]

Options:
  --model PATH          Path to trained model (default: runs/detect/train/weights/best.pt)
  --source SOURCE       Image file, directory, "dataset", or "ip_camera"
  --conf FLOAT          Confidence threshold (default: 0.6)
  --output DIR          Output directory (default: runs/detect/predict)
  --ip-config FILE       IP camera config file (default: ip_camera_config.yaml)
  --interval SECONDS    Capture interval for IP camera (default: 5)
  --single              Capture only one frame (default: continuous)
  --interactive, -i     Interactive mode
```

### **Examples:**

```bash
# Test with custom model
python test.py --model path/to/model.pt --source test.jpg

# Test with lower confidence (more detections, more false positives)
python test.py --source test.jpg --conf 0.4

# Test on specific directory
python test.py --source path/to/images --conf 0.7

# IP camera with custom settings
python test.py --source ip_camera --interval 10 --conf 0.8
```

---

## 🎯 **Quick Start Examples**

### **1. First Time Setup:**
```bash
# 1. Install dependencies
pip install -r requirements_ip_camera.txt

# 2. Train model (optional, can use default)
python train.py

# 3. Test with sample image
python test.py --source test.jpg
```

### **2. Daily Testing:**
```bash
# Interactive mode - easiest
python test.py

# Or test specific image
python test.py --source path/to/ring_image.jpg
```

### **3. Production Monitoring:**
```bash
# Continuous IP camera monitoring
python test.py --source ip_camera --interval 5

# Or use periodic capture
python ip_camera_capture.py --duration 60  # 60 minutes
```

---

## 🔍 **Understanding the Output**

### **Detection Summary:**
- **Confidence Threshold**: Only detections above threshold are shown (default 60%)
- **Breakage/Crack**: Require ≥60% confidence
- **Scratch**: Requires ≥50% confidence (more subtle defect)
- **False Positives**: Low confidence detections are filtered out

### **File Naming:**
- Original images: `ip_camera_YYYYMMDD_HHMMSS.jpg`
- Annotated images: Same name in `runs/detect/predict/`
- Detection labels: `image_name.txt` (YOLO format)

---

## ⚠️ **Common Issues & Solutions**

### **"Model not found"**
- Train first: `python train.py`
- Or use default: The script will use `yolov8n.pt` automatically

### **"Failed to connect to IP camera"**
- Check IP address in `ip_camera_config.yaml`
- Ensure phone and computer on same Wi-Fi
- Verify IP Webcam app is running
- Test in browser: `http://YOUR_IP:8080`

### **"No detections found"**
- Lower confidence: `--conf 0.3`
- Check if ring is visible in image
- Verify model was trained on similar data

### **"High CPU usage"**
- Increase capture interval: `--interval 10`
- Disable detection in `ip_camera_config.yaml`
- Use smaller model (yolov8n)

---

## 📊 **Project Workflow**

```
1. Prepare Dataset
   ├── train/images/ (369 images)
   ├── valid/images/ (13 images)
   └── test/images/ (8 images)

2. Train Model
   └── python train.py
       └── Output: runs/detect/train/weights/best.pt

3. Test Model
   ├── Static: python test.py --source test.jpg
   ├── Batch: python test.py --source test/images
   └── Live: python test.py --source ip_camera

4. Monitor Results
   ├── View: runs/detect/predict/
   └── Analyze detection confidence scores
```

---

## ✅ **Success Checklist**

Your project is working correctly if:

- [ ] Model trains without errors
- [ ] Test images show detection boxes
- [ ] Detection classes match (breakage, crack, scratch)
- [ ] IP camera connects successfully
- [ ] Images are saved to correct directories
- [ ] Detection confidence scores are reasonable (>50%)

---

## 🎓 **Next Steps**

1. **Fine-tune Model**: Adjust training parameters in `train.py`
2. **Collect More Data**: Add more images to improve accuracy
3. **Optimize Settings**: Adjust confidence thresholds and intervals
4. **Deploy**: Set up for production monitoring
5. **Analyze Results**: Review detection patterns over time

---

## 📞 **Need Help?**

- Check `TESTING_GUIDE.md` for detailed testing procedures
- Check `IP_CAMERA_SETUP.md` for IP camera setup
- Check `PROJECT_STRUCTURE.md` for file explanations

---

**Happy Detecting! 🔍✨**

