from agents.ingestion_agent import monitor_ipcc_reports
from agents.processing_agent import process_report
import os

def daily_processing():
    monitor_ipcc_reports()
    
    for file in os.listdir("data/reports"):
        if file.endswith(".txt"):
            process_report(f"data/reports/{file}")
