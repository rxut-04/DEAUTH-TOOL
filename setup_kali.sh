#!/bin/bash

echo "========================================"
echo "WiFi Deauth Tool - Kali Linux Setup"
echo "========================================"
echo

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "[!] Please run as root or with sudo"
    echo "    sudo ./setup_kali.sh"
    exit 1
fi

# Check if Kali Linux
if ! grep -q "Kali" /etc/os-release 2>/dev/null; then
    echo "[!] This script is optimized for Kali Linux"
    echo "[*] Continuing anyway..."
fi

echo "[*] Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "[-] Python3 not found! Installing..."
    apt-get update
    apt-get install -y python3 python3-pip
else
    PYTHON_VERSION=$(python3 --version)
    echo "[+] $PYTHON_VERSION found"
fi

echo
echo "[*] Checking and installing Python dependencies..."
pip3 install --upgrade pip
pip3 install scapy

echo
echo "[*] Checking system tools..."

# Check aircrack-ng
if command -v airmon-ng &> /dev/null; then
    echo "[+] aircrack-ng is installed"
    airmon-ng --version | head -1
else
    echo "[-] aircrack-ng not found. Installing..."
    apt-get update
    apt-get install -y aircrack-ng
fi

# Check wireless-tools
if command -v iwconfig &> /dev/null; then
    echo "[+] wireless-tools installed"
else
    echo "[-] wireless-tools not found. Installing..."
    apt-get install -y wireless-tools
fi

# Check iw
if command -v iw &> /dev/null; then
    echo "[+] iw tool installed"
else
    echo "[-] iw not found. Installing..."
    apt-get install -y iw
fi

echo
echo "[*] Checking WiFi interfaces..."
INTERFACES=$(iwconfig 2>/dev/null | grep -o "^[^ ]*" | grep -v "^$")
if [ -z "$INTERFACES" ]; then
    echo "[!] No WiFi interfaces found"
    echo "[!] Make sure your WiFi adapter is plugged in"
else
    echo "[+] Found WiFi interfaces:"
    for iface in $INTERFACES; do
        echo "    - $iface"
    done
fi

echo
echo "[*] Making scripts executable..."
chmod +x deauth_attack.py find_led_panel.py 2>/dev/null

echo
echo "========================================"
echo "[+] Setup complete!"
echo "========================================"
echo
echo "[*] Next steps:"
echo "    1. Find your interface: iwconfig"
echo "    2. Enable monitor mode: sudo airmon-ng start wlan0"
echo "    3. Scan for networks: sudo python3 find_led_panel.py wlan0mon 30"
echo "    4. Launch attack: sudo python3 deauth_attack.py -i wlan0mon -t <BSSID>"
echo
echo "[*] For detailed instructions, see QUICK_START.md"
echo

