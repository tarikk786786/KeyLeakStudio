#!/usr/bin/env python3
"""
KeyLeak Studio Launcher
Unified runner for KeyLeak Detector Web Interface and Security Scans.
Repository: https://github.com/Amal-David/keyleak-detector
"""

import os
import sys
import subprocess
import webbrowser
import time
from pathlib import Path

# Set UTF-8 encoding environment for Windows terminal unicode support
os.environ["PYTHONIOENCODING"] = "utf-8"
os.environ["PYTHONUTF8"] = "1"

# Paths
BASE_DIR = Path(__file__).resolve().parent
REPO_DIR = BASE_DIR if (BASE_DIR / "app.py").exists() else (BASE_DIR.parent.parent / "external_repos" / "keyleak-detector")

# Add keyleak repository and current folder to python path
sys.path.insert(0, str(REPO_DIR))
sys.path.insert(0, str(BASE_DIR))
os.environ["PYTHONPATH"] = f"{REPO_DIR};{os.environ.get('PYTHONPATH', '')}"

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
]

def get_chrome_executable():
    for p in CHROME_PATHS:
        if os.path.exists(p):
            return p
    return None

def open_in_chrome(url: str, profile: str = "Profile 3"):
    chrome = get_chrome_executable()
    if chrome:
        try:
            subprocess.Popen([chrome, f"--profile-directory={profile}", url])
            return
        except Exception:
            pass
    webbrowser.open(url)

def run_web_dashboard(port: int = 5002, host: str = "127.0.0.1"):
    print("=" * 70)
    print("  KEYLEAK DETECTOR - WEB DASHBOARD")
    print(f"  Target: http://{host}:{port}")
    print("=" * 70)
    
    os.environ["KEYLEAK_HOST"] = host
    os.environ["KEYLEAK_PORT"] = str(port)
    
    # Delayed browser opener in thread
    import threading
    def _open():
        time.sleep(1.8)
        open_in_chrome(f"http://{host}:{port}")
        
    threading.Thread(target=_open, daemon=True).start()
    
    # Change working directory to repo directory so templates and static assets resolve correctly
    os.chdir(str(REPO_DIR))
    
    import app
    app.app.run(host=host, port=port, debug=False)

def run_cli(args):
    os.chdir(str(ROOT_DIR))
    cmd = [sys.executable, "-m", "keyleak.cli"] + args
    subprocess.run(cmd)

def main():
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        if mode == "web":
            port = int(sys.argv[2]) if len(sys.argv) > 2 else 5002
            run_web_dashboard(port=port)
            return
        elif mode == "scan":
            run_cli(sys.argv[2:])
            return
        elif mode == "demo":
            run_cli(["demo"])
            return
        elif mode == "doctor":
            run_cli(["doctor"])
            return

    # Interactive menu
    while True:
        print("\n" + "=" * 65)
        print("        KEYLEAK DETECTOR STUDIO - SECURITY COMMAND CENTER")
        print("        Engine: Amal-David/keyleak-detector (v0.7.0)")
        print("=" * 65)
        print("  [1] Start Web Dashboard & Scanner (GUI on port 5002)")
        print("  [2] Scan Current Workspace for Secret Leaks")
        print("  [3] Scan Specific Directory or File")
        print("  [4] Scan Remote Website or Single-Page Application (SPA)")
        print("  [5] Run Incident & Dependency Supply Chain Check")
        print("  [6] Run KeyLeak Vulnerability Fixture Demo")
        print("  [7] Run Environment Diagnostic Doctor")
        print("  [8] Open Chrome Extension Installation Folder")
        print("  [9] Exit")
        print("=" * 65)
        
        choice = input("Select an option (1-9): ").strip()
        
        if choice == "1":
            run_web_dashboard()
            break
        elif choice == "2":
            print("\nScanning workspace for secret leaks (config, env, code, mcp, sourcemaps)...")
            run_cli(["local", str(ROOT_DIR), "--include", "config,env,mcp,docker,sourcemaps"])
        elif choice == "3":
            target = input("Enter directory or file path to scan: ").strip()
            if target:
                run_cli(["local", target, "--include", "config,env,code,docker,mcp,sourcemaps"])
        elif choice == "4":
            url = input("Enter website URL to scan (e.g. https://example.com): ").strip()
            if url:
                run_cli(["browser-scan", url])
        elif choice == "5":
            print("\nRunning incident check...")
            run_cli(["incident-check", str(ROOT_DIR)])
        elif choice == "6":
            print("\nRunning vulnerability demo...")
            run_cli(["demo"])
        elif choice == "7":
            print("\nRunning environment doctor...")
            run_cli(["doctor"])
        elif choice == "8":
            ext_dir = REPO_DIR / "extension"
            print(f"\nOpening extension folder: {ext_dir}")
            os.startfile(str(ext_dir))
            print("\nHow to install in Chrome:")
            print("1. Open Chrome and navigate to chrome://extensions/")
            print("2. Toggle 'Developer mode' in the top-right corner.")
            print("3. Click 'Load unpacked' and select the extension folder above.")
        elif choice == "9":
            print("Exiting KeyLeak Studio. Stay secure!")
            break
        else:
            print("Invalid choice, please select 1-9.")

if __name__ == "__main__":
    main()
