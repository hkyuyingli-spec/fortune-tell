import firebase_db
import time

print("Checking if Firebase is configured...")
configured = firebase_db.is_configured()
print(f"is_configured(): {configured}")

if not configured:
    print("STOP: Firebase secrets not detected. Check that [firebase] section")
    print("exists in .streamlit/secrets.toml with all required fields.")
    exit(1)

test_marker = f"connection_test_{int(time.time())}"
print(f"Writing a test document with marker: {test_marker}")

firebase_db.log_chart_request({
    "test_marker": test_marker,
    "lang": "en",
    "mode": "connection_test",
    "gender": "male",
    "birth_year": 1990,
    "birth_month": 1,
    "day_master": "test",
    "bureau_name": "test",
    "life_palace_stars": ["test"],
})

print("Write call completed without raising an exception.")
print("Now reading back from Firestore to confirm it actually landed...")

db = firebase_db._client_or_none()
if db is None:
    print("FAILED: could not get a Firestore client even though is_configured() was True.")
    print("This means credentials exist but firebase_db is not initializing the client correctly.")
    exit(1)

collection = db.collection("chart_requests")
result = collection.where("test_marker", "==", test_marker).limit(1).get()
if not result:
    print("FAILED: no document with this test marker was found after the write.")
    print("This means the data was not persisted to Firestore.")
    exit(1)

print("SUCCESS: Firebase write and read-back both worked.")
print(f"Verified document count: {len(result)}")
