import requests
from bs4 import BeautifulSoup
import os
from utils.helpers import download_pdf, extract_text

def monitor_ipcc_reports():
    response = requests.get(os.getenv("IPCC_MONITOR_URLS"))
    soup = BeautifulSoup(response.content, 'html.parser')
    
    for link in soup.find_all('a', href=True):
        if 'report' in link['href'] and link['href'].endswith('.pdf'):
            pdf_url = link['href']
            filename = pdf_url.split('/')[-1]
            
            if not os.path.exists(f"data/reports/{filename}"):
                download_pdf(pdf_url)
                extract_text(f"data/reports/{filename}")
                print(f"New report ingested: {filename}")
