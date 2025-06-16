#!/bin/bash
# Upgrade pip and setuptools first
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Create data directories
mkdir -p data/reports
mkdir -p data/chroma_db

# Download IPCC reports
python download_reports.py
