#!/usr/bin/env python3
"""
CyberHawk Recon - REAL Professional Reconnaissance Tool
Authors: IAIICT PROJECT DCT PROJECT GROUP 10
"""

import argparse
import socket
import requests
import json
import re
import sys
import time
import threading
from datetime import datetime
from colorama import init, Fore, Style, Back
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
import warnings

warnings.filterwarnings("ignore")
urllib3.disable_warnings()
init(autoreset=True)

class CyberHawkReal:
    """REAL Professional Reconnaissance Tool"""
    
    VERSION = "4.0.0"
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        self.results = {}
        self.threads = 50
    
    def banner(self):
        banner_text = f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                         ║
║{Fore.RED}     ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗{Fore.CYAN}     ║
║{Fore.RED}    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║  ██║██╔══██╗██║    ██║██║ ██╔╝{Fore.CYAN}              ║
║{Fore.RED}    -------------------------------------------------------------------------╝{Fore.CYAN}               ║
║{Fore.RED}    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔══██║██╔══██║██║███╗██║██╔═██╗{Fore.CYAN}               ║
║{Fore.RED}    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║  ██║██║  ██║╚███╔███╔╝██║  ██╗{Fore.CYAN}               ║
║{Fore.RED}     ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝{Fore.CYAN}               ║
║                                                                                                  ║
║{Fore.YELLOW}                         CYBERHAWK RECON - REAL EDITION                                     {Fore.CYAN}║
║{Fore.YELLOW}                    Professional Reconnaissance | Real Results Only                          {Fore.CYAN}║
║{Fore.YELLOW}                                    v{self.VERSION}                                              {Fore.CYAN}║
║{Fore.YELLOW}                         IAIICT PROJECT DCT PROJECT GROUP 10                               {Fore.CYAN}║
║                                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner_text)
    
    def show_help(self):
        print(f"""
{Fore.CYAN}╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                         CYBERHAWK RECON - COMMAND REFERENCE                                         ║
╠══════════════════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                                  ║
║  {Fore.GREEN}COMMAND{Fore.CYAN}                              {Fore.GREEN}DESCRIPTION{Fore.CYAN}                                                      ║
║  {Fore.CYAN}──────────────────────────────────────────────────────────────────────────────────────║
║                                                                                                  ║
║  {Fore.YELLOW}basic{Fore.CYAN}                                Basic reconnaissance (ports + headers)                                      ║
║  {Fore.YELLOW}  cyberhawk -t example.com --basic{Fore.CYAN}                                                                                ║
║                                                                                                  ║
║  {Fore.YELLOW}ports{Fore.CYAN}                               Port scan on target IP                                                  ║
║  {Fore.YELLOW}  cyberhawk -t example.com --ports{Fore.CYAN}                                                                              ║
║                                                                                                  ║
║  {Fore.YELLOW}subdomains{Fore.CYAN}                            Find subdomains                                                          ║
║  {Fore.YELLOW}  cyberhawk -t example.com --subdomains{Fore.CYAN}                                                                          ║
║                                                                                                  ║
║  {Fore.YELLOW}crawl{Fore.CYAN}                               Web crawling for hidden directories                                          ║
║  {Fore.YELLOW}  cyberhawk -t example.com --crawl{Fore.CYAN}                                                                            ║
║                                                                                                  ║
║  {Fore.YELLOW}vulns{Fore.CYAN}                              Vulnerability scan                                                      ║
║  {Fore.YELLOW}  cyberhawk -t example.com --vulns{Fore.CYAN}                                                                             ║
║                                                                                                  ║
║  {Fore.YELLOW}tech{Fore.CYAN}                               Detect technology stack                                                ║
║  {Fore.YELLOW}  cyberhawk -t example.com --tech{Fore.CYAN}                                                                             ║
║                                                                                                  ║
║  {Fore.YELLOW}all{Fore.CYAN}                                Run ALL reconnaissance modules                                            ║
║  {Fore.YELLOW}  cyberhawk -t example.com --all{Fore.CYAN}                                                                              ║
║                                                                                                  ║
║  {Fore.YELLOW}json{Fore.CYAN}                               Export results to JSON file                                            ║
║  {Fore.YELLOW}  cyberhawk -t example.com --all --json -o report.json{Fore.CYAN}                                                         ║
║                                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════════════════╝
""")
    
    def resolve(self, target):
        try:
            ip = socket.gethostbyname(target)
            print(f"{Fore.GREEN}[✓] Resolved: {target} → {ip}{Style.RESET_ALL}")
            return ip
        except:
            print(f"{Fore.RED}[✗] Failed to resolve{Style.RESET_ALL}")
            return None
    
    def scan_ports(self, ip, ports=None):
        """Real port scanning - COMPLETE version"""
        if not ports:
            ports = [20,21,22,23,25,53,80,110,111,135,139,143,389,443,445,465,587,636,993,995,1433,1521,1723,3306,3389,5432,5900,6379,8000,8080,8443,8888,9000,9200,9929,31337]
        
        services = {
            20: 'FTP-Data', 21: 'FTP', 22: 'SSH', 23: 'Telnet', 25: 'SMTP',
            53: 'DNS', 80: 'HTTP', 110: 'POP3', 111: 'RPC', 135: 'RPC',
            139: 'NetBIOS', 143: 'IMAP', 389: 'LDAP', 443: 'HTTPS', 445: 'SMB',
            465: 'SMTPS', 587: 'SMTP', 636: 'LDAPS', 993: 'IMAPS', 995: 'POP3S',
            1433: 'MSSQL', 1521: 'Oracle', 1723: 'PPTP', 3306: 'MySQL',
            3389: 'RDP', 5432: 'PostgreSQL', 5900: 'VNC', 6379: 'Redis',
            8000: 'HTTP-Alt', 8080: 'HTTP-Proxy', 8443: 'HTTPS-Alt', 8888: 'HTTP-Alt',
            9000: 'HTTP-Alt', 9200: 'Elasticsearch', 9929: 'Nping-echo', 31337: 'Nmap-Test'
        }
        
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🔌 PORT SCANNING - {ip}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'PORT':<8} {'STATE':<10} {'SERVICE'}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}")
        
        open_ports = []
        
        def scan_port(port):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, port))
                sock.close()
                if result == 0:
                    return port
            except:
                pass
            return None
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(scan_port, port): port for port in ports}
            for future in as_completed(futures):
                port = future.result()
                if port:
                    open_ports.append(port)
                    service = services.get(port, 'Unknown')
                    print(f"{Fore.GREEN}{port:<8} {Fore.GREEN}open{Fore.CYAN}      {service}{Style.RESET_ALL}")
        
        print(f"{Fore.CYAN}{'-'*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Found {len(open_ports)} open ports{Style.RESET_ALL}")
        return open_ports
    
    def find_subdomains(self, domain):
        """Real subdomain discovery"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🌐 SUBDOMAIN DISCOVERY - {domain}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        subdomains = set()
        
        # Passive API - HackerTarget
        print(f"{Fore.BLUE}[*] Querying HackerTarget API...{Style.RESET_ALL}")
        try:
            resp = requests.get(f"https://api.hackertarget.com/hostsearch/?q={domain}", timeout=15)
            for line in resp.text.split('\n'):
                if ',' in line:
                    sub = line.split(',')[0].strip()
                    if sub.endswith(domain):
                        subdomains.add(sub)
            print(f"{Fore.GREEN}    └── Found {len(subdomains)} subdomains{Style.RESET_ALL}")
        except:
            print(f"{Fore.YELLOW}    └── API failed{Style.RESET_ALL}")
        
        if subdomains:
            print(f"\n{Fore.BLUE}[*] Validating subdomains...{Style.RESET_ALL}")
            alive = []
            for sub in list(subdomains)[:30]:
                try:
                    ip = socket.gethostbyname(sub)
                    print(f"{Fore.GREEN}[+] {sub} → {ip}{Style.RESET_ALL}")
                    alive.append(sub)
                except:
                    print(f"{Fore.YELLOW}[!] {sub} → No DNS{Style.RESET_ALL}")
            
            print(f"{Fore.GREEN}[✓] Found {len(alive)} alive subdomains{Style.RESET_ALL}")
            return alive
        
        return []
    
    def web_crawl(self, domain):
        """Real web crawling"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🕷️ WEB CRAWLING - {domain}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        directories = ['admin', 'login', 'wp-admin', 'dashboard', 'cpanel', 'backup', 'config',
                       'api', 'v1', 'v2', 'robots.txt', 'sitemap.xml', '.env', '.git', 'phpinfo.php']
        
        base_url = f"https://{domain}"
        print(f"{Fore.BLUE}[*] Checking {len(directories)} paths...{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
        
        found = []
        for path in directories:
            url = f"{base_url}/{path}"
            try:
                resp = self.session.get(url, timeout=5, verify=False)
                if resp.status_code == 200:
                    found.append(url)
                    print(f"{Fore.GREEN}[200] {url}{Style.RESET_ALL}")
                elif resp.status_code in [301, 302, 403]:
                    found.append(url)
                    print(f"{Fore.YELLOW}[{resp.status_code}] {url}{Style.RESET_ALL}")
            except:
                pass
        
        print(f"{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Found {len(found)} accessible paths{Style.RESET_ALL}")
        return found
    
    def scan_vulnerabilities(self, domain):
        """Real vulnerability scanning"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🚨 VULNERABILITY SCANNING - {domain}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        vulnerabilities = []
        base_url = f"https://{domain}"
        
        # Check security headers
        print(f"{Fore.BLUE}[*] Checking security headers...{Style.RESET_ALL}")
        try:
            resp = self.session.get(base_url, timeout=10, verify=False)
            headers = resp.headers
            
            security_checks = ['Strict-Transport-Security', 'Content-Security-Policy', 'X-Frame-Options', 'X-Content-Type-Options']
            missing = [h for h in security_checks if h not in headers]
            
            if missing:
                for m in missing:
                    print(f"{Fore.YELLOW}[!] Missing: {m}{Style.RESET_ALL}")
                    vulnerabilities.append({'type': f'Missing {m}', 'severity': 'MEDIUM'})
            else:
                print(f"{Fore.GREEN}[✓] All security headers present{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}[!] Could not connect{Style.RESET_ALL}")
        
        # Check for exposed files
        print(f"\n{Fore.BLUE}[*] Checking for exposed files...{Style.RESET_ALL}")
        sensitive_files = ['.env', '.git/config', 'robots.txt', 'phpinfo.php']
        for file_path in sensitive_files:
            url = f"{base_url}/{file_path}"
            try:
                resp = self.session.get(url, timeout=5, verify=False)
                if resp.status_code == 200:
                    print(f"{Fore.RED}[!] EXPOSED: {url}{Style.RESET_ALL}")
                    vulnerabilities.append({'type': f'Exposed file: {file_path}', 'severity': 'HIGH', 'url': url})
            except:
                pass
        
        print(f"\n{Fore.GREEN}[✓] Found {len(vulnerabilities)} potential issues{Style.RESET_ALL}")
        return vulnerabilities
    
    def detect_technology(self, domain):
        """Real technology detection"""
        print(f"\n{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}💻 TECHNOLOGY DETECTION - {domain}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        try:
            resp = self.session.get(f"https://{domain}", timeout=10, verify=False)
            server = resp.headers.get('Server', 'Unknown')
            print(f"{Fore.GREEN}[+] Web Server: {server}{Style.RESET_ALL}")
            
            html = resp.text.lower()
            if 'wp-content' in html:
                print(f"{Fore.GREEN}[+] CMS: WordPress{Style.RESET_ALL}")
            if 'drupal' in html:
                print(f"{Fore.GREEN}[+] CMS: Drupal{Style.RESET_ALL}")
            if 'react' in html:
                print(f"{Fore.GREEN}[+] Framework: React{Style.RESET_ALL}")
        except:
            print(f"{Fore.RED}[!] Could not detect technology{Style.RESET_ALL}")
    
    def run(self, args):
        self.banner()
        
        if args.help:
            self.show_help()
            return
        
        if not args.target:
            print(f"{Fore.RED}[!] Please specify a target (-t domain.com){Style.RESET_ALL}")
            self.show_help()
            return
        
        self.threads = args.threads
        print(f"{Fore.YELLOW}[>] Target: {args.target}{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[>] Threads: {self.threads}{Style.RESET_ALL}")
        
        ip = self.resolve(args.target)
        if not ip:
            return
        
        if args.ports:
            self.scan_ports(ip)
        
        if args.subdomains:
            self.find_subdomains(args.target)
        
        if args.crawl:
            self.web_crawl(args.target)
        
        if args.vulns:
            self.scan_vulnerabilities(args.target)
        
        if args.tech:
            self.detect_technology(args.target)
        
        if args.basic:
            self.scan_ports(ip)
            self.detect_technology(args.target)
        
        if args.all:
            self.scan_ports(ip)
            self.find_subdomains(args.target)
            self.web_crawl(args.target)
            self.scan_vulnerabilities(args.target)
            self.detect_technology(args.target)
        
        print(f"\n{Fore.GREEN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{Style.BRIGHT}                    SCAN COMPLETE{Style.RESET_ALL}")
        print(f"{Fore.GREEN}{'='*70}{Style.RESET_ALL}")

def main():
    parser = argparse.ArgumentParser(description='CyberHawk Recon', add_help=False)
    parser.add_argument('-t', '--target', help='Target domain')
    parser.add_argument('--threads', type=int, default=50, help='Threads (default: 50)')
    parser.add_argument('--basic', action='store_true', help='Basic reconnaissance')
    parser.add_argument('--ports', action='store_true', help='Port scan')
    parser.add_argument('--subdomains', action='store_true', help='Find subdomains')
    parser.add_argument('--crawl', action='store_true', help='Web crawl')
    parser.add_argument('--vulns', action='store_true', help='Vulnerability scan')
    parser.add_argument('--tech', action='store_true', help='Detect technology')
    parser.add_argument('--all', action='store_true', help='Run all modules')
    parser.add_argument('-h', '--help', action='store_true', help='Show help')
    
    args = parser.parse_args()
    
    tool = CyberHawkReal()
    tool.run(args)

if __name__ == "__main__":
    main()
