"""
Debug: Check what paths Streamlit can access
"""
import os
from pathlib import Path

print("=" * 60)
print("🔍 STREAMLIT PATH DEBUG")
print("=" * 60)

print(f"\n1. Current Working Directory:")
print(f"   os.getcwd() = {os.getcwd()}")

print(f"\n2. Detected Faults Directory Locations:")
paths_to_check = [
    Path("detected_faults"),
    Path(os.getcwd()) / "detected_faults",
]

for path in paths_to_check:
    exists = path.exists()
    print(f"   {path}")
    print(f"      → Exists: {exists}")
    if exists:
        files = list(path.glob("*.jpg"))
        print(f"      → Found {len(files)} images")

print(f"\n3. Script location:")
print(f"   __file__ = {__file__ if '__file__' in dir() else 'N/A (might be different in Streamlit)'}")

print("\n" + "=" * 60)
