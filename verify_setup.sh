#!/bin/bash

echo "========================================"
echo "Kali Linux Setup Verification"
echo "========================================"
echo

ERRORS=0

# Check Python
echo "[*] Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VER=$(python3 --version)
    echo "[+] $PYTHON_VER"
else
    echo "[-] Python3 not found!"
    ERRORS=$((ERRORS+1))
fi

# Check Scapy
echo "[*] Checking Scapy..."
if python3 -c "import scapy" 2>/dev/null; then
    SCAPY_VER=$(python3 -c "import scapy; print(scapy.__version__)" 2>/dev/null)
    echo "[+] Scapy installed (version: $SCAPY_VER)"
else
    echo "[-] Scapy not installed! Run: pip3 install scapy"
    ERRORS=$((ERRORS+1))
fi

# Check aircrack-ng
echo "[*] Checking aircrack-ng..."
if command -v airmon-ng &> /dev/null; then
    AC_VERSION=$(airmon-ng --version 2>/dev/null | head -1)
    echo "[+] aircrack-ng installed: $AC_VERSION"
else
    echo "[-] aircrack-ng not found! Run: sudo apt-get install aircrack-ng"
    ERRORS=$((ERRORS+1))
fi

# Check wireless tools
echo "[*] Checking wireless tools..."
if command -v iwconfig &> /dev/null; then
    echo "[+] iwconfig available"
else
    echo "[-] iwconfig not found! Run: sudo apt-get install wireless-tools"
    ERRORS=$((ERRORS+1))
fi

# Check WiFi interfaces
echo "[*] Checking WiFi interfaces..."
INTERFACES=$(iwconfig 2>/dev/null | grep -o "^[^ ]*" | grep -v "^$")
if [ -n "$INTERFACES" ]; then
    echo "[+] Found interfaces:"
    for iface in $INTERFACES; do
        echo "    - $iface"
    done
else
    echo "[!] No WiFi interfaces found (adapter may not be plugged in)"
fi

# Check scripts
echo "[*] Checking scripts..."
if [ -f "deauth_attack.py" ]; then
    echo "[+] deauth_attack.py found"
else
    echo "[-] deauth_attack.py not found!"
    ERRORS=$((ERRORS+1))
fi

if [ -f "find_led_panel.py" ]; then
    echo "[+] find_led_panel.py found"
else
    echo "[-] find_led_panel.py not found!"
    ERRORS=$((ERRORS+1))
fi

echo
echo "========================================"
if [ $ERRORS -eq 0 ]; then
    echo "[+] Setup verification PASSED!"
    echo "[*] You're ready to use the tools"
else
    echo "[-] Setup verification FAILED ($ERRORS errors)"
    echo "[*] Please fix the errors above"
fi
echo "========================================"

exit $ERRORS

