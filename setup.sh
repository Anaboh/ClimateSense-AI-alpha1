#!/bin/bash
# Lightweight install for mobile
pip install --upgrade pip
pip install --no-cache-dir -r requirements.txt

# Create directories
mkdir -p data/reports
mkdir -p data/chroma_db
mkdir -p data/feedback

# Download only essential reports
python download_reports.py --essential#!/bin/bash
# Upgrade pip and setuptools first
pip install --upgrade pip setuptools wheel

# Install dependencies
pip install --no-cache-dir -r requirements.txt

# Create data directories
mkdir -p data/reports
mkdir -p data/chroma_db

# Download IPCC reports
python download_reports.py

# Precompute vector stores asynchronously
python precompute_vectors.py
