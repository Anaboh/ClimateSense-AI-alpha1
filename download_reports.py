import os
import requests
from utils.reports import IPCC_REPORTS

def download_reports():
    os.makedirs("data/reports", exist_ok=True)
    
    base_url = "https://www.ipcc.ch/report/ar6/"
    report_files = list(IPCC_REPORTS.values())
    
    for filename in report_files:
        path = f"data/reports/{filename}"
        
        if not os.path.exists(path):
            print(f"Downloading {filename}...")
            try:
                # Construct URL based on report type
                if "SYR" in filename:
                    url = f"{base_url}syr/downloads/report/{filename}"
                elif "WGI" in filename:
                    url = f"{base_url}wg1/downloads/report/{filename}"
                elif "WGII" in filename:
                    url = f"{base_url}wg2/downloads/report/{filename}"
                elif "WGIII" in filename:
                    url = f"{base_url}wg3/downloads/report/{filename}"
                
                response = requests.get(url)
                with open(path, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {filename}")
            except Exception as e:
                print(f"Error downloading {filename}: {str(e)}")
        else:
            print(f"{filename} already exists")

if __name__ == "__main__":
    download_reports()
