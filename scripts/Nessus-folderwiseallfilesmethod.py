import requests
import time
import os
import urllib3
 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
# REPLACE KEYS
access_key = "Generate from Nessus API Key"
secret_key = "Generate from Nessus API Key"
 
# CORRECT BASE URL (IMPORTANT)
base_url = "https://localhost:8834"
 
# USE FOLDER IDs ONLY (NOT URLs)
TARGET_FOLDER_IDS = [38, 162, 39, 186, 187, 59, 120]
 
headers = {
    "X-ApiKeys": "accessKey=" + access_key + "; secretKey=" + secret_key
}
 
# Get folders
folders_response = requests.get(base_url + "/folders", headers=headers, verify=False)
folders = folders_response.json()["folders"]
 
# Create folder dictionary
folder_dict = {folder["id"]: folder["name"] for folder in folders}
 
# Get scans
scans_response = requests.get(base_url + "/scans", headers=headers, verify=False)
scans = scans_response.json()["scans"]
 
for scan in scans:
 
    if scan["folder_id"] not in TARGET_FOLDER_IDS:
        continue
 
    if scan["status"] != "completed":
        continue
 
    scan_id = scan["id"]
    scan_name = scan["name"]
    folder_name = folder_dict.get(scan["folder_id"], "Unknown")
 
    print("Exporting:", scan_name, "| Folder:", folder_name)
 
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
 
    export = requests.post(
        base_url + "/scans/" + str(scan_id) + "/export",
        headers=headers,
        json={"format": "csv"},
        verify=False
    )
 
    export_data = export.json()
 
    if "file" not in export_data:
        print("❌ Export failed:", export_data)
        continue
 
    file_id = export_data["file"]
 
    while True:
        status = requests.get(
            base_url + "/scans/" + str(scan_id) + "/export/" + str(file_id) + "/status",
            headers=headers,
            verify=False
        ).json()
 
        if status["status"] == "ready":
            break
 
        time.sleep(2)
 
    download = requests.get(
        base_url + "/scans/" + str(scan_id) + "/export/" + str(file_id) + "/download",
        headers=headers,
        verify=False
    )
 
    with open(os.path.join(folder_name, scan_name + ".csv"), "wb") as f:
        f.write(download.content)
 
print("All selected folders exported successfully!")
