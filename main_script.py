# run_all.py
import subprocess
import threading
import sys
import os

def run_streamlit():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "main.py"])

def run_telegram():
    subprocess.run([sys.executable, "main_telegram.py"])

def main():
    print("Starting applications...")
    
    # Start both applications in separate threads
    streamlit_thread = threading.Thread(target=run_streamlit)
    telegram_thread = threading.Thread(target=run_telegram)
    
    streamlit_thread.daemon = True
    telegram_thread.daemon = True
    
    streamlit_thread.start()
    telegram_thread.start()
    
    # Keep the main process running
    try:
        # This keeps the main thread alive until Ctrl+C
        streamlit_thread.join()
        telegram_thread.join()
    except KeyboardInterrupt:
        print("\nShutting down applications...")
        sys.exit(0)

if __name__ == "__main__":
    main()