# Phase 3: Streamlit Dashboard Setup & Deployment

## What You Just Got

A **real-time web dashboard** for monitoring your ring detection system with:
- 📊 Live analytics and charts
- 📋 Detection history with filters
- 📈 Session statistics
- ⚙️ System & camera status
- 🔄 Auto-refresh capability

---

## Step 1: Run Dashboard Locally

### Option A: Simple Run
```bash
streamlit run app.py
```

This will:
- Open dashboard at `http://localhost:8501`
- Show all Firebase data in real-time
- Auto-refresh every 10 seconds (configurable)

### Option B: Custom Configuration
```bash
streamlit run app.py --logger.level=info
```

---

## Step 2: Test Dashboard

1. **Start your detection system** (in another terminal):
   ```bash
   python test.py --source ip_camera --interval 5
   ```

2. **Open dashboard** in first terminal:
   ```bash
   streamlit run app.py
   ```

3. **Watch live detections** appear on the dashboard in real-time!

---

## Dashboard Tabs Explained

### 📊 Analytics Tab
- **Pie chart**: Defect type distribution (breakage, crack, scratch)
- **Histogram**: Confidence score distribution
- **Timeline**: Hourly detection count over last 24 hours

### 📋 Detection History Tab
- **Filters**: By time range and defect type
- **Table**: All detections with timestamp, type, confidence
- **Metrics**: Total count, average confidence, high-confidence detections

### 📈 Statistics Tab
- **Session overview**: Total sessions, captures, defects
- **Defect rate**: Percentage of defective rings detected
- **Session history**: List of all past sessions with stats

### ⚙️ Live Status Tab
- **System status**: Current system state
- **Camera status**: Camera connection info
- **Database metrics**: Total records in Firebase

---

## Phase 4: Deploy to Streamlit Cloud (Optional)

### Make Your Dashboard Public in 5 Minutes!

#### Step 1: Push to GitHub

1. Create a GitHub account (free): [github.com](https://github.com)

2. Create a new public repository:
   - Name: `ring-detection-dashboard`
   - Don't add .gitignore yet

3. Upload your files (do this in your project folder):
   ```bash
   git init
   git add app.py firebase_config.py cloud_client.py serviceAccountKey.json requirements_ip_camera.txt
   git commit -m "Initial dashboard commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/ring-detection-dashboard.git
   git push -u origin main
   ```

#### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)

2. Click "New app"

3. Fill in:
   - **Repository**: `YOUR_USERNAME/ring-detection-dashboard`
   - **Branch**: `main`
   - **Main file path**: `app.py`

4. Click "Deploy" - that's it!

Your dashboard will be live at:
```
https://YOUR_USERNAME-ring-detection-dashboard.streamlit.app
```

Share this link with your team - **everyone can access it!**

---

## Troubleshooting

### ❌ "Module not found" errors
```bash
pip install streamlit plotly pandas firebase-admin
```

### ❌ "Firebase connection failed"
- Verify `firebase_config.py` has correct database URL
- Confirm `serviceAccountKey.json` is present
- Check Firebase Console shows your data

### ❌ Dashboard loads but shows no data
- Start `python test.py` to send data to Firebase
- Wait 10 seconds for auto-refresh
- Check "Live Status" tab for database metrics

### ❌ Data not appearing after detection
- Check terminal where `test.py` is running
- Verify Firebase connection shows "✓ Cloud client connected"
- Click refresh button in Streamlit (top right)

---

## Customization Tips

### Change Auto-Refresh Speed
Edit `app.py` line in Tab 1:
```python
refresh_interval = st.select_slider("Refresh every (seconds)", 
                                   options=[5, 10, 15, 30, 60],  # Edit these
                                   value=10)  # Default
```

### Add More Analytics
Add to `app.py` in Tab 1 (Analytics):
```python
# Defect type over time
fig = px.line(detections_df, x='timestamp', y='confidence', color='defect_type')
st.plotly_chart(fig, use_container_width=True)
```

### Change Colors
Modify in STYLING section:
```python
marker=dict(colors=['#FF6B6B', '#FFA500', '#4ECDC4'])  # RGB hex codes
```

---

## What's Next?

✅ **Phase 1**: Firebase Setup  
✅ **Phase 2**: Cloud Client Integration  
✅ **Phase 3**: Streamlit Dashboard  
⏭️ **Phase 4**: Optional - Deploy to Cloud (Streamlit Cloud, Heroku, AWS, etc.)

---

## Quick Reference

| Action | Command |
|--------|---------|
| Run locally | `streamlit run app.py` |
| Stop dashboard | `Ctrl+C` in terminal |
| View logs | Check terminal output |
| Clear cache | Delete `.streamlit/` folder |
| Deploy | Push to GitHub → Connect on share.streamlit.io |

---

## Getting Help

**Common Issues:**
1. No data showing? → Run `test.py` first
2. Slow dashboard? → Increase refresh interval
3. Firebase errors? → Check credentials in `firebase_config.py`

**Resources:**
- Streamlit docs: https://docs.streamlit.io
- Firebase docs: https://firebase.google.com/docs
- Plotly docs: https://plotly.com/python/

