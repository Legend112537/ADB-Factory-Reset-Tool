
# ADB Factory Reset Tool

A simple Python tool to trigger a factory reset on an Android device via ADB.

## How It Works
1. Connects to the target Android device via ADB.
2. Executes `adb shell wm reset-user 0` or `adb shell pm clear com.android.providers.settings depending on the version.
3. Optionally, triggers a reboot into recovery mode for a full wipe.

## Prerequisites
- Python 3.8+
- ADB installed and in PATH
- Android device with USB Debugging enabled
- Device must be paired via `adb connect <IP>` or `adb devices.`

## Usage
```bash
python main.py --device <device_ip> --reset
