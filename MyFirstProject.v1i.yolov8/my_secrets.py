import json

# Your Database URL
DATABASE_URL = "https://ring-detection-c6326-default-rtdb.firebaseio.com/"

# Load the fresh JSON file
try:
    with open("serviceAccountKey.json", "r") as f:
        FIREBASE_CREDENTIALS = json.load(f)
    print("✅ Credentials loaded from serviceAccountKey.json")
except Exception as e:
    print(f"❌ Error loading JSON: {e}")
    FIREBASE_CREDENTIALS = None