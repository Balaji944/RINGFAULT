# 📁 Project Structure & File Explanation

Complete guide to understanding your YOLOv8 Faulty Rings Detection Project with IP Camera Integration.

---

## 🎯 **Project Overview**

This project detects defects in rings (O-rings) using YOLOv8 deep learning model. It can detect:
- **breakage** (class 0)
- **crack** (class 1)  
- **scratch** (class 2)

The project now includes IP camera integration to capture images from your mobile phone for real-time or periodic detection.

---

## 📂 **Directory Structure**

```
My First Project.v1i.yolov8/
│
├── 📄 Core Python Scripts
│   ├── train.py                    # Model training script
│   ├── test.py                     # Model testing/prediction script (with IP camera support)
│   ├── ip_camera_capture.py        # IP camera capture class and functions
│   └── start_ip_capture.py         # Quick start script for IP camera
│
├── ⚙️ Configuration Files
│   ├── data.yaml                   # Dataset configuration (paths & class names)
│   ├── data.yaml.save              # Backup of data.yaml
│   └── ip_camera_config.yaml       # IP camera settings
│
├── 📚 Documentation Files
│   ├── IP_CAMERA_SETUP.md          # IP camera setup guide
│   ├── TESTING_GUIDE.md            # Testing instructions
│   ├── PROJECT_STRUCTURE.md        # This file
│   ├── README.roboflow.txt         # Dataset info from Roboflow
│   └── README.dataset.txt          # Dataset description
│
├── 📦 Dependencies
│   ├── requirements_ip_camera.txt # Python packages needed
│   └── yolov8n.pt                 # Pre-trained YOLOv8 nano model
│
├── 📁 Dataset Directories
│   ├── train/                      # Training data
│   │   ├── images/                 # 369 training images
│   │   └── labels/                 # 369 YOLO format labels
│   ├── valid/                      # Validation data
│   │   ├── images/                 # 13 validation images
│   │   └── labels/                 # 13 validation labels
│   └── test/                       # Test data
│       ├── images/                 # 7 test images
│       └── labels/                 # 7 test labels
│
├── 📁 Output Directories (Generated)
│   ├── runs/detect/                # All detection results
│   │   ├── train/                  # Training results
│   │   │   ├── weights/
│   │   │   │   ├── best.pt        # Best trained model ⭐
│   │   │   │   └── last.pt        # Last epoch model
│   │   │   ├── results.png         # Training metrics graph
│   │   │   ├── confusion_matrix.png # Confusion matrix
│   │   │   └── ...
│   │   └── predict*/               # Previous prediction results
│   ├── captured_images/            # Images from IP camera (created when used)
│   └── detections/                 # Detection results from IP camera (created when used)
│
└── 🐍 Virtual Environment
    └── venv/                       # Python virtual environment
```

---

## 📄 **File Descriptions**

### 🎓 **Core Training & Testing Scripts**

#### **1. `train.py`** ⭐ Main Training Script
**Purpose:** Trains the YOLOv8 model on your faulty rings dataset

**What it does:**
- Loads YOLOv8 nano model (`yolov8n.pt`)
- Trains on images in `train/images` with labels in `train/labels`
- Validates on `valid/images`
- Saves best model to `runs/detect/train/weights/best.pt`
- Runs for 50 epochs with batch size 16

**Usage:**
```bash
python train.py
```

**Output:**
- Trained model: `runs/detect/train/weights/best.pt`
- Training graphs and metrics in `runs/detect/train/`

---

#### **2. `test.py`** ⭐ Main Testing Script (UPDATED with IP Camera)
**Purpose:** Tests the trained model on images or IP camera feed

**What it does:**
- Loads trained model (`best.pt` or default `yolov8n.pt`)
- Can test on:
  - Single image file
  - Directory of images
  - **IP camera feed** (NEW!)
- Saves detection results with bounding boxes
- Prints detection summary (class names, confidence scores)

**Usage:**
```bash
# Test with single image
python test.py --source test.jpg

# Test with test directory
python test.py --source test/images

# Test with IP camera (NEW!)
python test.py --source ip_camera

# Test with custom confidence threshold
python test.py --source test.jpg --conf 0.5
```

**Output:**
- Annotated images saved to `runs/detect/predict/`
- Detection results printed to console

---

### 📷 **IP Camera Integration Scripts**

#### **3. `ip_camera_capture.py`** ⭐ IP Camera Core Module
**Purpose:** Main class and functions for IP camera capture and detection

**What it does:**
- `IPCameraCapture` class handles:
  - Connecting to mobile IP webcam
  - Capturing frames at periodic intervals
  - Running YOLOv8 detection on captured images
  - Saving images and detection results
- Configurable via `ip_camera_config.yaml`
- Supports continuous capture, limited duration, or limited count

**Key Functions:**
- `connect_camera()` - Connects to IP webcam
- `capture_frame()` - Captures single frame
- `save_image()` - Saves captured image
- `run_detection()` - Runs YOLOv8 detection
- `capture_loop()` - Main periodic capture loop

**Usage:**
```bash
# Test connection (single capture)
python ip_camera_capture.py --test

# Continuous capture
python ip_camera_capture.py

# Capture for 60 minutes
python ip_camera_capture.py --duration 60

# Capture 10 images
python ip_camera_capture.py --max-captures 10
```

---

#### **4. `start_ip_capture.py`** 🚀 Quick Start Script
**Purpose:** Interactive script for easy IP camera usage

**What it does:**
- Provides user-friendly menu
- Guides through setup
- Offers different capture modes:
  1. Continuous (until Ctrl+C)
  2. Limited duration (minutes)
  3. Limited captures (count)
  4. Test mode (single capture)

**Usage:**
```bash
python start_ip_capture.py
```

---

### ⚙️ **Configuration Files**

#### **5. `data.yaml`** 📋 Dataset Configuration
**Purpose:** Defines dataset structure and class names

**Contents:**
```yaml
path: .                    # Base path
train: train/images        # Training images path
val: valid/images          # Validation images path
test: test/images         # Test images path

names:                     # Class names
  0: breakage            # Class 0
  1: crack                # Class 1
  2: scratch              # Class 2
```

**Used by:** `train.py` to know where data is and what classes to detect

---

#### **6. `ip_camera_config.yaml`** 📷 IP Camera Settings
**Purpose:** Configures IP camera capture behavior

**Key Settings:**
- `ip_camera_url` - Your phone's IP address (UPDATE THIS!)
- `capture_interval_seconds` - Time between captures (default: 30)
- `output_directory` - Where to save captured images
- `enable_detection` - Run YOLOv8 detection (true/false)
- `model_path` - Path to trained model
- `save_detections` - Save annotated images (true/false)

**⚠️ IMPORTANT:** Update `ip_camera_url` with your phone's IP from IP Webcam app!

---

### 📚 **Documentation Files**

#### **7. `IP_CAMERA_SETUP.md`** 📖 Setup Guide
**Purpose:** Step-by-step guide to set up IP camera

**Contains:**
- How to install IP Webcam app
- How to configure IP camera URL
- Usage examples
- Troubleshooting tips

---

#### **8. `TESTING_GUIDE.md`** 🧪 Testing Instructions
**Purpose:** Complete testing workflow

**Contains:**
- Prerequisites checklist
- Step-by-step testing procedures
- Verification checklist
- Troubleshooting common issues

---

#### **9. `README.roboflow.txt`** 📊 Dataset Info
**Purpose:** Information about dataset from Roboflow

**Contains:**
- Dataset export date
- Number of images (389 total)
- Pre-processing information
- Roboflow project details

---

### 📦 **Dependencies**

#### **10. `requirements_ip_camera.txt`** 📦 Python Packages
**Purpose:** Lists required Python packages

**Packages:**
- `opencv-python>=4.8.0` - Computer vision library
- `pyyaml>=6.0` - YAML file parsing
- `ultralytics>=8.0.0` - YOLOv8 framework

**Install:**
```bash
pip install -r requirements_ip_camera.txt
```

---

#### **11. `yolov8n.pt`** 🤖 Pre-trained Model
**Purpose:** Pre-trained YOLOv8 nano model (starting point)

**Used by:**
- `train.py` - As base model for training
- `test.py` - As fallback if trained model not found

---

### 📁 **Dataset Directories**

#### **12. `train/`** 📚 Training Data
- **`train/images/`** - 369 training images
- **`train/labels/`** - 369 YOLO format annotation files
- **`train/labels.cache`** - Cached label data (auto-generated)

**Format:** YOLO format (normalized coordinates)

---

#### **13. `valid/`** ✅ Validation Data
- **`valid/images/`** - 13 validation images
- **`valid/labels/`** - 13 validation labels
- **`valid/labels.cache`** - Cached label data

**Used during training** to validate model performance

---

#### **14. `test/`** 🧪 Test Data
- **`test/images/`** - 7 test images
- **`test/labels/`** - 7 test labels

**Used for final testing** after training

---

### 📁 **Output Directories**

#### **15. `runs/detect/train/`** 📊 Training Results
**Generated by:** `train.py`

**Contents:**
- **`weights/best.pt`** ⭐ - Your trained model (use this!)
- **`weights/last.pt`** - Model from last epoch
- **`results.png`** - Training metrics graph
- **`confusion_matrix.png`** - Confusion matrix
- **`BoxP_curve.png`** - Precision curve
- **`BoxR_curve.png`** - Recall curve
- **`args.yaml`** - Training configuration used

---

#### **16. `runs/detect/predict*/`** 🎯 Prediction Results
**Generated by:** `test.py`

**Contains:** Annotated images with detection boxes

---

#### **17. `captured_images/`** 📷 IP Camera Captures
**Generated by:** `ip_camera_capture.py`

**Contains:** Raw images captured from IP camera

**Format:** `capture_YYYYMMDD_HHMMSS.jpg`

---

#### **18. `detections/`** 🔍 Detection Results
**Generated by:** `ip_camera_capture.py` (when detection enabled)

**Contains:** Annotated images with detection boxes from IP camera

---

## 🔄 **Workflow Overview**

### **Training Workflow:**
```
1. Prepare dataset (train/valid/test folders)
2. Configure data.yaml
3. Run: python train.py
4. Get trained model: runs/detect/train/weights/best.pt
```

### **Testing Workflow (Static Images):**
```
1. Run: python test.py --source test.jpg
2. View results in: runs/detect/predict/
```

### **Testing Workflow (IP Camera):**
```
1. Setup IP Webcam app on phone
2. Update ip_camera_config.yaml with phone IP
3. Run: python test.py --source ip_camera
   OR
   Run: python ip_camera_capture.py --test
4. View results in: runs/detect/predict/ or detections/
```

### **Periodic Capture Workflow:**
```
1. Setup IP Webcam app on phone
2. Update ip_camera_config.yaml
3. Run: python ip_camera_capture.py
4. Images saved to: captured_images/
5. Detections saved to: detections/
```

---

## 🎯 **Quick Reference**

### **Most Important Files:**
1. ⭐ `train.py` - Train your model
2. ⭐ `test.py` - Test your model
3. ⭐ `ip_camera_capture.py` - IP camera functionality
4. ⭐ `data.yaml` - Dataset config
5. ⭐ `ip_camera_config.yaml` - IP camera config
6. ⭐ `runs/detect/train/weights/best.pt` - Your trained model

### **Key Directories:**
- `train/` - Training data
- `valid/` - Validation data  
- `test/` - Test data
- `runs/detect/train/weights/` - Trained models
- `captured_images/` - IP camera captures
- `detections/` - IP camera detection results

---

## 💡 **Tips**

1. **Always use `best.pt`** for testing (not `last.pt`)
2. **Update `ip_camera_url`** in `ip_camera_config.yaml` before using IP camera
3. **Check `runs/detect/train/results.png`** to see training progress
4. **Use `--conf` flag** in test.py to adjust detection sensitivity
5. **Keep phone plugged in** during long IP camera sessions

---

## 🆘 **Need Help?**

- **IP Camera Setup:** See `IP_CAMERA_SETUP.md`
- **Testing:** See `TESTING_GUIDE.md`
- **Training Issues:** Check `runs/detect/train/` for error logs

---

**Last Updated:** Project structure with IP camera integration
**Project Type:** YOLOv8 Object Detection for Faulty Rings
**Classes:** breakage, crack, scratch

