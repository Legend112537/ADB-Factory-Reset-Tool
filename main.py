```python
import subprocess
import sys
import json
import os

def connect_device(ip: str, port: int = 5555) -> bool:
    """Connect to an Android device via ADB."""
    try:
        result = subprocess.run(
            ["adb", "connect", f"{ip}:{port}"],
            capture_output=True,
            text=True,
            check=True
        )
        print(f"[+] Connected to {ip}:{port}")
        return True
    except subprocess.CalledWithProcessError as e:
        print(f"[-] Failed to connect: {e.stderr}")
        return False

def get_device_serial(ip: str) -> str:
    """Get the device serial number."""
    try:
        result = subprocess.run(
            ["adb", "devices"],
            capture_output=True,
            text=True,
            check=True
        )
        lines = result.stdout.strip().split("\n")[1:]  # Skip header
        for line in lines:
            if ip in line:
                return line.split()[0]
    except subprocess.CalledWithProcessError:
        pass
    return ""

def factory_reset(device_serial: str) -> bool:
    """Trigger a factory reset via ADB."""
    commands = [
        f"adb -s {device_serial} shell wm reset-user 0",
        f"adb -s {device_serial} shell pm clear com.android.providers.settings",
        f"adb -s {device_serial} shell am broadcast -a android.intent.action.FACTORY_RESET"
    ]

    for cmd in commands:
        try:
            print(f"[+] Executing: {cmd}")
            result = subprocess.run(
                cmd.split(),
                capture_output=True,
                text=True,
                check=False  # Some commands may not return 0
            )
            if "success" in result.stdout.lower() or result.returncode == 0:
                print(f"[+] Command executed successfully.")
                return True
            else:
                print(f"[-] Output: {result.stderr}")
        except Exception as e:
            print(f"[-] Error: {e}")

    return False

def main():
    if len(sys.argv) < 3 or sys.argv[1] != "--device":
        print("Usage: python main.py --device <ip_address>")
        sys.exit(1)

    ip = sys.argv[2]
    
    if not connect_device(ip):
        sys.exit(1)

    device_serial = get_device_serial(ip)
    if not device_serial:
        print("[-] Device not found.")
        sys.exit(1)

    print(f"[+] Found device: {device_serial}")
    factory_reset(device_serial)

if __name__ == "__main__":
    main()
