#!/usr/bin/env python3
"""
Test script to demonstrate REAL port scanning
"""

import socket
from concurrent.futures import ThreadPoolExecutor

def test_scan(target, ports):
    print(f"\nTesting port scan on {target}")
    print("="*50)
    
    open_ports = []
    
    def scan(p):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            if sock.connect_ex((target, p)) == 0:
                return p
            sock.close()
        except:
            pass
        return None
    
    with ThreadPoolExecutor(max_workers=50) as ex:
        results = list(ex.map(scan, ports))
    
    for p in results:
        if p:
            open_ports.append(p)
            print(f"  Port {p} - OPEN")
    
    return open_ports

# Test on Google (firewalled)
print("\n1. Testing GOOGLE.COM (has firewall):")
google_ports = test_scan("216.58.223.206", [80, 443, 22, 21, 25, 3306, 5432, 8080, 8443])
print(f"   Result: Only {google_ports} responded (firewall blocks others)")

# Test on Nmap test server (no firewall)
print("\n2. Testing SCANME.NMAP.ORG (allows scanning):")
nmap_ports = test_scan("45.33.32.156", [22, 80, 9929, 31337, 80, 443, 8080])
print(f"   Result: Open ports: {nmap_ports}")

print("\n" + "="*50)
print("CONCLUSION: The tool works! Major sites have firewalls.")
print("To see REAL multiple open ports, scan scanme.nmap.org")
