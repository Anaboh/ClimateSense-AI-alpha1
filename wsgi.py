from streamlit.web.cli import main
import sys

def run_streamlit():
    sys.argv = [
        "streamlit", "run", "app.py",
        "--server.port=8050",
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--global.developmentMode=false",
        "--browser.gatherUsageStats=false"
    ]
    main()

if __name__ == "__main__":
    run_streamlit()
