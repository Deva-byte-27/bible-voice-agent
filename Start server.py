"""
run this instead of main.py
It auto-finds your IP and prints the URLs for TV/phone/laptop
"""
import socket
import subprocess
import sys
import os

def get_local_ip():
    """Get the WiFi IP of this machine."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

ip = get_local_ip()

print("")
print("=" * 60)
print("   ✝  BIBLE SPEECH RECOGNITION SERVER  ✝")
print("=" * 60)
print("")
print(f"  📱 Preacher Control (this device):")
print(f"     http://localhost:5000")
print("")
print(f"  📺 TV / Phone / Other Laptop Display:")
print(f"     http://{ip}:5000/display")
print("")
print(f"  ⚠  All devices MUST be on the same WiFi!")
print(f"  ⚠  Share the display URL with congregation screens")
print("")
print("=" * 60)
print("")

# Now start the actual server
os.chdir(os.path.dirname(os.path.abspath(__file__)))
exec(open("main.py", encoding="utf-8").read())