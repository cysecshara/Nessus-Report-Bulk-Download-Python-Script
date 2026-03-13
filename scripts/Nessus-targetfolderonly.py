import requests
import time
import os
import urllib3
 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
access_key = "Generate from Nessus API Key"
secret_key = "Generate from Nessus API Key"
base_url = "https://localhost:8834"   # Change if Nessus is on another server
 
TARGET_FOLDER = "DESKTOP"   # CHANGE HERE
 
headers = {
    "X-ApiKeys": "accessKey=" + access_key + "; secretKey=" + secret_key
}
 
# Get folders
folders_response = requests.get(base_url + "/folders", headers=headers, verify=False)
folders = folders_response.json()["folders"]
 
target_folder_id = None
 
for folder in folders:
    if folder["name"] == TARGET_FOLDER:
        target_folder_id = folder["id"]
        break
 
if not target_folder_id:
    print("❌ Folder not found!")
    exit()
 
# Get scans
scans_response = requests.get(base_url + "/scans", headers=headers, verify=False)
scans = scans_response.json()["scans"]
 
for scan in scans:
 
    if scan["folder_id"] != target_folder_id:
        continue
 
    if scan["status"] != "completed":
        continue
 
    scan_id = scan["id"]
    scan_name = scan["name"]
 
    print("Exporting:", scan_name)
 
    if not os.path.exists(TARGET_FOLDER):
        os.makedirs(TARGET_FOLDER)
 
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
 
    with open(os.path.join(TARGET_FOLDER, scan_name + ".csv"), "wb") as f:
        f.write(download.content)
 
print("Selected folder export completed!")
