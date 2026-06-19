markdown
# ADB APK Installer

A simple GUI tool to install APK files on Android devices using ADB (Android Debug Bridge).

## Features

- 🖥️ Simple graphical interface
- 📱 Install APK files with one click
- 🔄 Support for downgrade installation (-d flag)
- 🚀 Bypass low target SDK block for old apps
- 📊 Real-time installation logs
- 🔌 Device connection testing

## Requirements

- Linux (Ubuntu/Debian recommended)
- ADB installed on your system
- Android phone with USB Debugging enabled

## Installation

### Install ADB

```bash
sudo apt update
sudo apt install adb
Download the App
Download the latest executable from Releases.

Or run directly with Python:

bash
python3 main.py

How to Use

Connect your phone via USB with USB Debugging enabled

Launch the app by running ./main or python3 main.py

Click "Test Connection" to verify your device is connected

Click "Browse" to select your APK file

Choose options (Bypass SDK block is enabled by default)

Click "Install APK" to start installation

Check the log for installation progress

Phone Setup (First Time)
Go to Settings → About Phone

Tap Build Number 7 times to enable Developer Options

Go to Settings → Developer Options

Enable USB Debugging

Connect phone via USB and tap "Allow" when prompted

Troubleshooting

Issue			Solution
No device found	Enable		USB Debugging and reconnect cable
INSTALL_FAILED_DEPRECATED_SDK_VERSION		Keep "Bypass Low Target SDK Block" checked
INSTALL_FAILED_ALREADY_EXISTS		Uninstall app first or use "Install (Downgrade)"
Permission denied		Make sure phone is unlocked and permission is allowed

Build from Source
bash
# Clone the repository
git clone https://github.com/mobinrezaina/adb-apk-installer.git
cd adb-apk-installer

# Install PyInstaller (if needed)
pip install pyinstaller

# Build the executable
pyinstaller --onefile --windowed main.py

# The executable will be in dist/
./dist/main
License
MIT License - see LICENSE file for details.

Author
Mubk2005

⭐ If you find this tool useful, please give it a star on GitHub!
# adb-apk-installer
# adb-apk-installer
# adb-apk-installer
