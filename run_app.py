#!/usr/bin/env python3
"""
Launch the Deaf-Mute Communication application
Starts all components: Server, Web Bridge, and Main GUI
"""
import subprocess
import sys
import time
import os
import io

# Force stdout/stderr to use UTF-8 if they are not already, preventing encoding errors on Windows
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    try:
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

def run_app():
    """Start all application components"""
    print("=" * 60)
    print("🚀 Deaf-Mute Communication System - Starting...")
    print("=" * 60)
    
    # Start Relay Server
    print("\n[1/3] Starting Relay Server...")
    server_process = subprocess.Popen(
        [sys.executable, "src/server.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    # Start Web Bridge
    print("[2/3] Starting Web Bridge...")
    web_process = subprocess.Popen(
        [sys.executable, "src/web_bridge.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    time.sleep(2)
    
    # Start Main GUI
    print("[3/3] Starting Main Application GUI...")
    gui_process = subprocess.Popen(
        [sys.executable, "src/welcome_gui.py"],
        cwd=os.path.dirname(os.path.abspath(__file__))
    )
    
    print("\n" + "=" * 60)
    print("✅ All components started successfully!")
    print("=" * 60)
    print("\n📱 Desktop App: Main GUI window is launching...")
    print("🌐 Web Interface: http://localhost:5000")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Keep processes running
        gui_process.wait()
    except KeyboardInterrupt:
        print("\n\n⏹️  Shutting down all services...")
        gui_process.terminate()
        web_process.terminate()
        server_process.terminate()
        time.sleep(1)
        gui_process.kill()
        web_process.kill()
        server_process.kill()
        print("✅ All services stopped.")
        sys.exit(0)

if __name__ == "__main__":
    run_app()
