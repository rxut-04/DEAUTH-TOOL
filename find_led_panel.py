#!/usr/bin/env python3
"""
LED Panel Network Scanner
Scans for WiFi networks and helps identify the LED panel
"""

from scapy.all import *
import sys
import time
from collections import defaultdict

def scan_networks(interface, duration=30):
    """
    Scan for WiFi networks and display detailed information
    """
    print(f"[*] Scanning for networks on {interface}...")
    print(f"[*] Duration: {duration} seconds")
    print(f"[*] Make sure your interface is in monitor mode!\n")
    print("=" * 80)
    
    networks = defaultdict(dict)
    
    def packet_handler(packet):
        if packet.haslayer(Dot11):
            # Beacon frames (access points advertising themselves)
            if packet.type == 0 and packet.subtype == 8:
                try:
                    ssid = packet[Dot11Elt].info.decode('utf-8', errors='ignore')
                    bssid = packet[Dot11].addr2
                    
                    if ssid and bssid:
                        # Get signal strength if available
                        rssi = None
                        if packet.haslayer(RadioTap):
                            rssi = packet[RadioTap].dBm_AntSignal
                        
                        # Get channel
                        channel = None
                        if packet.haslayer(Dot11Elt):
                            for elt in packet[Dot11Elt]:
                                if elt.ID == 3:  # DS Parameter Set (channel)
                                    channel = ord(elt.info)
                        
                        # Store network info
                        if bssid not in networks or networks[bssid].get('rssi', -100) < (rssi or -100):
                            networks[bssid] = {
                                'ssid': ssid,
                                'bssid': bssid,
                                'rssi': rssi,
                                'channel': channel,
                                'count': networks[bssid].get('count', 0) + 1
                            }
                            
                            # Print immediately
                            rssi_str = f"{rssi} dBm" if rssi else "N/A"
                            channel_str = f"Ch {channel}" if channel else "N/A"
                            print(f"[+] {ssid:30s} | {bssid:17s} | {rssi_str:10s} | {channel_str}")
                except Exception as e:
                    pass
    
    try:
        sniff(iface=interface, prn=packet_handler, timeout=duration)
    except KeyboardInterrupt:
        print("\n[*] Scan interrupted by user")
    except Exception as e:
        print(f"[-] Error: {e}")
        return None
    
    print("=" * 80)
    print(f"\n[+] Found {len(networks)} unique networks\n")
    
    # Sort by signal strength
    sorted_networks = sorted(networks.items(), 
                            key=lambda x: x[1].get('rssi', -100), 
                            reverse=True)
    
    print("Top networks (by signal strength):")
    print("-" * 80)
    for bssid, info in sorted_networks[:10]:
        rssi_str = f"{info['rssi']} dBm" if info['rssi'] else "N/A"
        channel_str = f"Ch {info['channel']}" if info['channel'] else "N/A"
        print(f"SSID: {info['ssid']:30s}")
        print(f"  BSSID: {bssid}")
        print(f"  Signal: {rssi_str:10s} | Channel: {channel_str}")
        print()
    
    # Look for LED panel indicators
    print("\n[*] Looking for potential LED panel networks...")
    print("-" * 80)
    led_keywords = ['led', 'panel', 'display', 'sign', 'climate', 'change']
    found_led = False
    
    for bssid, info in sorted_networks:
        ssid_lower = info['ssid'].lower()
        for keyword in led_keywords:
            if keyword in ssid_lower:
                print(f"[!] Potential LED Panel:")
                print(f"    SSID: {info['ssid']}")
                print(f"    BSSID: {bssid}")
                print(f"    Signal: {rssi_str}")
                print()
                found_led = True
                break
    
    if not found_led:
        print("[!] No obvious LED panel networks found")
        print("[!] Look for networks with unusual names or strong signals")
    
    return networks


def main():
    if len(sys.argv) < 2:
        print("Usage: python find_led_panel.py <interface> [duration]")
        print("Example: python find_led_panel.py wlan0mon 30")
        sys.exit(1)
    
    interface = sys.argv[1]
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    
    print("=" * 80)
    print("LED Panel Network Scanner")
    print("=" * 80)
    print()
    
    networks = scan_networks(interface, duration)
    
    if networks:
        print("\n[*] To attack a network, use:")
        print(f"    python deauth_attack.py -i {interface} -t <BSSID>")


if __name__ == "__main__":
    main()

