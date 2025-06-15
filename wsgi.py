from streamlit.web.cli import main

def run_streamlit():
    import sys
    sys.argv = [
        "streamlit", "run", "app.py",
        "--server.port=8050",  # Use fixed internal port
        "--server.address=0.0.0.0",
        "--server.headless=true",
        "--global.developmentMode=false"
    ]
    main()
