#!/bin/bash
# Install dependencies
pip install -r requirements.txt

# Create data directories
mkdir -p data/reports
mkdir -p data/chroma_db

# Download IPCC reports
python download_reports.py
