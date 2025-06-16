import os
import requests
import argparse

# Essential reports only
ESSENTIAL_REPORTS = {
    "AR6 Synthesis Report (SPM)": "https://www.ipcc.ch/report/ar6/syr/downloads/report/IPCC_AR6_SYR_SPM.pdf",
    "AR6 Climate Science (WGI SPM)": "https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf"
}

def download_reports(essential_only=False):
    os.makedirs("data/reports", exist_ok=True)
    reports = ESSENTIAL_REPORTS if essential_only else REPORTS
    
    print("🌱 Downloading essential IPCC reports...")
    for name, url in reports.items():
        filename = url.split('/')[-1]
        path = f"data/reports/{filename}"
        
        if not os.path.exists(path):
            try:
                response = requests.get(url, stream=True)
                with open(path, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
                print(f"Downloaded {filename}")
            except Exception as e:
                print(f"Error downloading {filename}: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--essential", action="store_true", help="Download only essential reports")
    args = parser.parse_args()
    download_reports(essential_only=args.essential)
