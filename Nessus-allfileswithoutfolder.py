import requests
import time
import urllib3
 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
 
# 🔴 REPLACE THESE 3 VALUES ONLY
access_key = "57b72af4ce6affb42782bf6682e41978b8650cbb57a8097ebf2d3e2631236482"
secret_key = "3220bec1912561264ae1ef6cc6bbb52d7906de2e51e32ed8962f498bd91a6b42"
base_url = "https://localhost:8834"   # Change if Nessus is on another server
 
headers = {
    "X-ApiKeys": "accessKey=" + access_key + "; secretKey=" + secret_key
}
 
# Get all scans
response = requests.get(base_url + "/scans", headers=headers, verify=False)
scans = response.json()["scans"]
 
for scan in scans:
    scan_id = scan["id"]
    scan_name = scan["name"]
 
    print("Exporting:", scan_name)
 
    # Request CSV export
    export = requests.post(
        base_url + "/scans/" + str(scan_id) + "/export",
        headers=headers,
        json={"format": "csv"},
        verify=False
    )

    print(export.json())
  
    export_data = export.json()
    
    if "file" not in export_data:
        print("X Export failed for;-:", scan_name)
        print("Reason",export_data)
        continue
 
    file_id=export_data["file"]    
 
    # Wait until export ready
    while True:
        status = requests.get(
            base_url + "/scans/" + str(scan_id) + "/export/" + str(file_id) + "/status",
            headers=headers,
            verify=False
        ).json()
 
        if status["status"] == "ready":
            break
 
        time.sleep(2)
 
    # Download CSV
    download = requests.get(
        base_url + "/scans/" + str(scan_id) + "/export/" + str(file_id) + "/download",
        headers=headers,
        verify=False
    )
 
    with open(scan_name + ".csv", "wb") as f:
        f.write(download.content)
 
print("✅ All CSV reports downloaded successfully!")