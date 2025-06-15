#!/bin/bash
pip install -r requirements.txt
mkdir -p data/reports
mkdir -p data/chroma_db
python download_reports.py
