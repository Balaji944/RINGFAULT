"""
Store credentials directly in Python to avoid JSON formatting errors
"""

# 1. Copy the LONG private key string from your JSON file.
# 2. Paste it inside the triple quotes """ below.
# 3. Make sure it includes -----BEGIN PRIVATE KEY----- and -----END PRIVATE KEY-----

PRIVATE_KEY_STRING = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCzi6CkSHaLZ3h2
t6LBdsdMKTZbXdklMLqD00zVZcDq4fGV2DDp97yRhiSdQjNNMsrciJRWwqLkIOvb
lhO8PK1DmTBKvL8IZyIAiKp4oS/nGvEYppCQ71v2Wovqg0STxb40izUE5x27mVMS
qFhyLmxAZTIC0MgA0leYFOhhTAhbSKcE4FNswfWaQmcHGKifUTN2ZaLY+90kJ0Zs
oU0GUTUtX1eGO0o7CnXhukYiAH83/AAI3nqWEmRwhp3K60a0tbeLguudKYccV62y
gVRfOvJToYxrnbeKlfmOWYFdukCTLY1DWpfy+uUb5CVdBc8g9cG42QUY/tXkPuNP
CYpgb1VvAgMBAAECggEAKEfIB3NWXRoelYvHUN4EAlswnbjlUYmoHpEWKL4GVOvR
1ktFVghFXuSYbEuA1O3zQxzFIt3Ry5pzL7Vwwgde286PXgUQWqNAppwCmsOWyqNp
uZ0My+dXW2KfB0Lh7MEtVf5xK6NqMT9JuuLXzO4LTTsmyCjs5fpKuozeQY3cRhYa
Wx0ub9DusKViRFhqU9PfK2hdV2HHoKdUv5qplnztEJcrsi+6emUibk8MWW10IMkl
2AtvpYUzZ0GQEcyGvMHpNcvM7YU/lo8Dyx89wiT8KuqFanmVRgQGU4gsbQ2f641P
htw05ASUMn0aM0KrqAXRhWX+roE63yqQEG2iGoI2SQKBgQD4fdHJF/o6zFLnD4IZ
dZ6YErtcItv5Pxsnt4j3z9ja3rWDBCT5F6PASDFiaivKIVFdd1pK44pnLavk8br2
MUAAD2qLkbaeWRlQh42tSB2PFz6DpTLeVjxmiOUL60igc0aURep9hjpV2hvsP2+s
VX5yg6JU/FpapQU036lMseXx7QKBgQC4+HuYifczqhWLmkkwSKtLU6ed3CYkB+Nn
snnnL/vwR7rENHE6T01YDtO6z3Yr0BNsYXkwC98v3kB3/A2sgq60cV6eHF6j9MTB
qgCS9LtSNZEmvXw/MKvADhCa5SHG92Y2vsvZKbXHN1AJnGViqkn+1UAWtWlqVWZf
WkLbz0ypSwKBgDEWGaTRubp3tkCyjY6d73A28w/mSvHXh3O3C7V4N2w05kI1RWB3
TP+kwyyfsHrDTiFafFmizSpImVYmcjpDzFK2uONNK3foPdnsjQ4X2s7zVoQG1B+b
hV7z19sc5UHcw6pyjTmylD91UGLAvTybvti8LAsBto+FXZvuOrFNyxCZAoGAD2KD
njTV0fTSZZCoqCj0RGkvT9jpYZcjOLlLW9taz4tFkhGtEO7Ba44cgLzqQPqao5uvY
k5l5L9cRj6lETeP0ugdv8kCz0nlKYD1OnOqEJhtUfl9mVS8sKeZBlVCXlaAAPW9z
LxXcC7zbCGGcwS8exnZgRUNDiFegEzBDvVqpqq8CgYA4X09Hsn+7olWWUITfjCYs
lHDPt+tCPkjhKsRc0dorokKU2t84MqE1iW0RvEweWvFW0YHSEcj/EaIlYdtAhvbG
pmpWcW10A44bRdNsVTs/SR4cnC0YhbJt+Okp5W3sBc9MlPGp5vSm8boJNtLB/Gqy
JF0oW3xCbqN4LRYNPCmoww==
-----END PRIVATE KEY-----"""

# This dictionary is what we will send to Firebase
FIREBASE_CREDENTIALS = {
  "type": "service_account",
  "project_id": "ring-detection-c6326",
  "private_key_id": "06a50683f37feed590939c37da178d7cc82a7bf2",
  "private_key": PRIVATE_KEY_STRING,
  "client_email": "firebase-adminsdk-fbsvc@ring-detection-c6326.iam.gserviceaccount.com",
  "client_id": "117116960268735901645",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40ring-detection-c6326.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Your Database URL
DATABASE_URL = "https://ring-detection-c6326-default-rtdb.firebaseio.com/"