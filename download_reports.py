import os
import requests
from tqdm import tqdm

REPORTS = {
    "AR6 Synthesis Report (SPM)": "https://www.ipcc.ch/report/ar6/syr/downloads/report/IPCC_AR6_SYR_SPM.pdf",
    "AR6 Climate Science (WGI SPM)": "https://www.ipcc.ch/report/ar6/wg1/downloads/report/IPCC_AR6_WGI_SPM.pdf",
    "AR6 Impacts & Adaptation (WGII SPM)": "https://www.ipcc.ch/report/ar6/wg2/downloads/report/IPCC_AR6_WGII_SPM.pdf",
    "AR6 Mitigation (WGIII SPM)": "https://www.ipcc.ch/report/ar6/wg3/downloads/report/IPCC_AR6_WGIII_SPM.pdf"
}

def download_reports():
    os.makedirs("data/reports", exist_ok=True)
    
    print("Downloading IPCC reports...")
    for name, url in tqdm(REPORTS.items()):
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
        else:
            print(f"{filename} already exists")

if __name__ == "__main__":
    download_reports()
