#!/usr/bin/env python3
import uvicorn
import webbrowser
import threading
import time
import sys
from pathlib import Path

def open_browser():
    time.sleep(1.5)
    webbrowser.open('http://localhost:8000')

def main():
    print("=" * 50)
    print("AI女友 - Web版本")
    print("=" * 50)
    print("\n正在启动服务...")
    print("服务启动后将自动打开浏览器")
    print("按 Ctrl+C 停止服务\n")
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        uvicorn.run(
            "backend.main:app",
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n服务已停止")
        sys.exit(0)

if __name__ == "__main__":
    main()
