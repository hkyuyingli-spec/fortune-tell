import json
import glob
import os

downloads = os.path.join(os.path.expanduser("~"), "Downloads")
candidates = glob.glob(os.path.join(downloads, "*firebase-adminsdk*.json"))
if not candidates:
    print("Could not find a firebase-adminsdk json file in Downloads.")
    print("Please tell me the exact filename and I'll adjust the script.")
    exit(1)

json_path = max(candidates, key=os.path.getmtime)
print(f"Found service account file: {os.path.basename(json_path)}")

with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

def toml_line(key, value):
    if "\n" in value:
        return f'{key} = """{value}"""'
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'{key} = "{escaped}"'

keys = ["type", "project_id", "private_key_id", "private_key", "client_email",
        "client_id", "auth_uri", "token_uri", "auth_provider_x509_cert_url",
        "client_x509_cert_url"]

lines = ["", "[firebase]"] + [toml_line(k, data[k]) for k in keys if k in data]

with open(".streamlit/secrets.toml", "a", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print("Done. Firebase credentials added to .streamlit/secrets.toml")
print("The original downloaded JSON file was not changed or moved.")
