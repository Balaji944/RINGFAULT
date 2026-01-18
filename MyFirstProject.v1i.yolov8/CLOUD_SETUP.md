# Firebase Cloud Integration Setup Guide

## Phase 2: Cloud Backend Configuration

This guide walks you through setting up Firebase Realtime Database for the Faulty Rings Detection system.

---

## Step 1: Create Firebase Project (if not done)

1. Go to [firebase.google.com](https://firebase.google.com)
2. Click **"Go to console"**
3. Click **"+ Create a project"**
   - Project name: `Ring Detection` (or your choice)
   - Accept terms and create

---

## Step 2: Set Up Realtime Database

1. In Firebase Console, click **"Realtime Database"** (in left sidebar)
2. Click **"Create Database"**
   - Location: Choose closest to your location
   - Security Rules: Start in **"Test Mode"** (for development)
   - Click **"Enable"**

3. Once created, you'll see your database URL in the format:
   ```
   https://YOUR-PROJECT-ID.firebaseio.com
   ```

4. Copy this URL - you'll need it in Step 5

---

## Step 3: Create Service Account Key

1. In Firebase Console, go to **Project Settings** (⚙️ icon, top right)
2. Click **"Service Accounts"** tab
3. Click **"Generate New Private Key"**
4. A JSON file will download - this is your `serviceAccountKey.json`
5. **Move this file** to your project folder:
   ```
   d:\Codes\DCS PBl\My First Project.v1i.yolov8\serviceAccountKey.json
   ```

⚠️ **IMPORTANT**: Keep this file SECRET! Do NOT share or commit to Git.

---

## Step 4: Update firebase_config.py

Open `firebase_config.py` and replace the URL:

```python
FIREBASE_DATABASE_URL = "https://YOUR-PROJECT-ID.firebaseio.com"
```

Example:
```python
FIREBASE_DATABASE_URL = "https://ring-detection-abc123.firebaseio.com"
```

---

## Step 5: Install Firebase Admin

Firebase Admin should already be installed, but if not:

```bash
pip install firebase-admin
```

---

## Step 6: Update Security Rules (Optional - for Production)

⚠️ **Important**: Test Mode is NOT secure. For production, set proper rules:

1. In Firebase Console, go to **Realtime Database**
2. Click **"Rules"** tab
3. Replace with:

```json
{
  "rules": {
    ".read": "auth != null",
    ".write": "auth != null",
    "detections": {
      ".read": true,
      ".write": true
    },
    "statistics": {
      ".read": true,
      ".write": true
    },
    "camera_status": {
      ".read": true,
      ".write": true
    }
  }
}
```

4. Click **"Publish"**

---

## Step 7: Test Connection

Run this to verify everything works:

```bash
python -c "from cloud_client import CloudClient; c = CloudClient(); c.connect() and print('✓ Connected!') or print('✗ Failed')"
```

You should see:
```
✓ Firebase config loaded
✓ Cloud client connected (Session ID: 20240118_153000)
✓ Connected!
```

---

## Directory Structure

After setup, your project should have:

```
My First Project.v1i.yolov8/
├── cloud_client.py              ← Cloud integration
├── firebase_config.py           ← Your database URL
├── serviceAccountKey.json       ← Service account (KEEP SECRET!)
├── test.py                      ← Updated to use cloud
├── requirements_ip_camera.txt   ← Now includes firebase-admin
└── ... other files
```

---

## Cloud Data Structure

Your Firebase database will be organized like this:

```
detections/
├── 1705598123456
│   ├── timestamp: "2024-01-18T15:35:23.456"
│   ├── defect_type: "crack"
│   ├── confidence: 0.87
│   └── image_filename: "IMG_001.jpg"
└── 1705598456789
    ├── timestamp: "2024-01-18T15:37:36.789"
    ├── defect_type: "breakage"
    └── confidence: 0.92

statistics/
└── 20240118_153000
    ├── total_captures: 150
    ├── total_defects: 12
    └── clean_images: 138

camera_status/
└── current
    ├── status: "running"
    ├── capture_count: 150
    └── defects_found: 12
```

---

## Troubleshooting

### ❌ "Service account key not found"
- Make sure `serviceAccountKey.json` is in the same folder as `test.py`

### ❌ "FIREBASE_DATABASE_URL not set"
- Edit `firebase_config.py` and add your database URL

### ❌ Connection fails
- Check that Firebase Console shows your database is online
- Verify internet connection
- Check the URL format (should start with `https://`)

### ❌ Permission denied errors
- Make sure you're in Test Mode or rules are set correctly
- Service account key is valid and not corrupted

---

## Next Steps

Once Phase 2 is complete:

1. **Phase 3**: Create Streamlit Dashboard to view data in real-time
2. **Phase 4**: Deploy dashboard for team access

---

## Getting Help

If stuck, check:
- Firebase Console > Realtime Database > Data (see if your data appears)
- Check rules tab if writes are failing
- Verify `serviceAccountKey.json` is valid JSON

