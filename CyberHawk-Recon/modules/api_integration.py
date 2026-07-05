#!/usr/bin/env python3
"""
API Integration Module - Shodan, Censys, SecurityTrails, GitHub
Authors: IAIICT PROJECT DCT PROJECT GROUP 10
"""

import requests
import json
import base64
from colorama import Fore, Style
import urllib3

urllib3.disable_warnings()

# Try to load API keys from config file
try:
    import config
    SHODAN_API_KEY = getattr(config, 'SHODAN_API_KEY', None)
    CENSYS_API_ID = getattr(config, 'CENSYS_API_ID', None)
    CENSYS_API_SECRET = getattr(config, 'CENSYS_API_SECRET', None)
    SECURITYTRAILS_API_KEY = getattr(config, 'SECURITYTRAILS_API_KEY', None)
    URLSCAN_API_KEY = getattr(config, 'URLSCAN_API_KEY', None)
    FULLHUNT_API_KEY = getattr(config, 'FULLHUNT_API_KEY', None)
    LEAKIX_API_KEY = getattr(config, 'LEAKIX_API_KEY', None)
    ENABLE_SHODAN = getattr(config, 'ENABLE_SHODAN', True)
    ENABLE_CENSYS = getattr(config, 'ENABLE_CENSYS', True)
    ENABLE_SECURITYTRAILS = getattr(config, 'ENABLE_SECURITYTRAILS', True)
    ENABLE_URLSCAN = getattr(config, 'ENABLE_URLSCAN', True)
except:
    SHODAN_API_KEY = "NMer5F1XOwe1yp1wyEbZlqij9aM2bUfh"
    CENSYS_API_ID = "censys_2CMJ81nm_eieLravhJfCiZ1StUiL5fzY1"
    CENSYS_API_SECRET = ""
    SECURITYTRAILS_API_KEY = "H4dal2Ci7QO6ZL5Uh7DDt865VhbVUgIB"
    URLSCAN_API_KEY = "019e2835-fb1a-737a-a660-1addd3ae988f"
    FULLHUNT_API_KEY = "54fcc323-46f2-4feb-97bc-97bdf8567cad"
    LEAKIX_API_KEY = "ULAyds9M5hcIvciesq8fDvxwNyHuNHVrXP762rHKZrOyLK2_"
    ENABLE_SHODAN = True
    ENABLE_CENSYS = True
    ENABLE_SECURITYTRAILS = True
    ENABLE_URLSCAN = True

class APIIntegration:
    """Integration with external security APIs"""
    
    def __init__(self):
        self.SHODAN_API_KEY = SHODAN_API_KEY
        self.CENSYS_API_ID = CENSYS_API_ID
        self.CENSYS_API_SECRET = CENSYS_API_SECRET
        self.SECURITYTRAILS_API_KEY = SECURITYTRAILS_API_KEY
        self.URLSCAN_API_KEY = URLSCAN_API_KEY
        self.FULLHUNT_API_KEY = FULLHUNT_API_KEY
        self.LEAKIX_API_KEY = LEAKIX_API_KEY
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'CyberHawk-Recon/3.0'}
    
    def query_shodan(self, ip):
        """Query Shodan for IP intelligence"""
        if not self.SHODAN_API_KEY or not ENABLE_SHODAN:
            return None
        
        try:
            url = f"https://api.shodan.io/shodan/host/{ip}?key={self.SHODAN_API_KEY}"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return {
                    'hostnames': data.get('hostnames', [])[:5],
                    'ports': data.get('ports', [])[:10],
                    'vulnerabilities': data.get('vulns', []),
                    'tags': data.get('tags', []),
                    'org': data.get('org', 'Unknown')
                }
        except Exception as e:
            pass
        return None
    
    def query_securitytrails(self, domain):
        """Query SecurityTrails for domain data"""
        if not self.SECURITYTRAILS_API_KEY or not ENABLE_SECURITYTRAILS:
            return None
        
        try:
            url = f"https://api.securitytrails.com/v1/domain/{domain}/subdomains"
            headers = {'APIKEY': self.SECURITYTRAILS_API_KEY}
            resp = self.session.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                subs = data.get('subdomains', [])
                return {
                    'subdomains': subs[:20],
                    'count': len(subs)
                }
        except Exception as e:
            pass
        return None
    
    def query_censys(self, ip):
        """Query Censys for host data"""
        if not self.CENSYS_API_ID or not ENABLE_CENSYS:
            return None
        
        try:
            auth = base64.b64encode(f"{self.CENSYS_API_ID}:{self.CENSYS_API_SECRET}".encode()).decode()
            headers = {'Authorization': f'Basic {auth}'}
            url = f"https://search.censys.io/api/v2/hosts/{ip}"
            resp = self.session.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                result = data.get('result', {})
                return {
                    'services': len(result.get('services', [])),
                    'location': result.get('location', {}),
                    'autonomous_system': result.get('autonomous_system', {})
                }
        except Exception as e:
            pass
        return None
    
    def query_urlscan(self, domain):
        """Query URLScan.io for domain scans"""
        if not self.URLSCAN_API_KEY or not ENABLE_URLSCAN:
            return None
        
        try:
            url = f"https://urlscan.io/api/v1/search/?q=domain:{domain}"
            headers = {'API-Key': self.URLSCAN_API_KEY}
            resp = self.session.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                results = data.get('results', [])
                return {
                    'total_scans': len(results),
                    'malicious': any(r.get('malicious', False) for r in results),
                    'latest_scan': results[0].get('task', {}).get('time', 'N/A') if results else 'N/A'
                }
        except Exception as e:
            pass
        return None
    
    def query_github_secrets(self, domain):
        """Search GitHub for exposed secrets"""
        secrets = []
        
        # Search patterns for common secrets
        patterns = [
            f'"{domain}" "api_key"',
            f'"{domain}" "secret"',
            f'"{domain}" "password"',
            f'"{domain}" "token"',
            f'"{domain}" "private"'
        ]
        
        for pattern in patterns[:3]:
            try:
                url = f"https://api.github.com/search/code?q={pattern}"
                resp = self.session.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if data.get('total_count', 0) > 0:
                        secrets.append({
                            'pattern': pattern,
                            'count': data['total_count'],
                            'message': f'Found {data["total_count"]} potential matches'
                        })
            except:
                pass
        
        return secrets
    
    def comprehensive_api_scan(self, target, ips):
        """Run all API scans"""
        print(f"\n{Fore.BLUE}[*] Running API Intelligence Scans...{Style.RESET_ALL}")
        
        results = {}
        
        # SecurityTrails
        if ENABLE_SECURITYTRAILS and self.SECURITYTRAILS_API_KEY:
            print(f"{Fore.CYAN}    SecurityTrails...{Style.RESET_ALL}")
            st_result = self.query_securitytrails(target)
            if st_result:
                results['securitytrails'] = st_result
                print(f"{Fore.GREEN}        └── Found {st_result['count']} subdomains{Style.RESET_ALL}")
        
        # URLScan
        if ENABLE_URLSCAN and self.URLSCAN_API_KEY:
            print(f"{Fore.CYAN}    URLScan.io...{Style.RESET_ALL}")
            us_result = self.query_urlscan(target)
            if us_result:
                results['urlscan'] = us_result
                if us_result.get('malicious'):
                    print(f"{Fore.RED}        └── Malicious content detected!{Style.RESET_ALL}")
                else:
                    print(f"{Fore.GREEN}        └── {us_result['total_scans']} scans, clean{Style.RESET_ALL}")
        
        # Shodan and Censys for each IP
        if ips:
            for ip in ips[:3]:
                if ENABLE_SHODAN and self.SHODAN_API_KEY:
                    shodan_data = self.query_shodan(ip)
                    if shodan_data:
                        results[f'shodan_{ip}'] = shodan_data
                        vuln_count = len(shodan_data.get('vulnerabilities', []))
                        if vuln_count > 0:
                            print(f"{Fore.RED}        └── Shodan: {vuln_count} vulns on {ip}{Style.RESET_ALL}")
                
                if ENABLE_CENSYS and self.CENSYS_API_ID:
                    censys_data = self.query_censys(ip)
                    if censys_data:
                        results[f'censys_{ip}'] = censys_data
                        print(f"{Fore.CYAN}        └── Censys: {censys_data['services']} services on {ip}{Style.RESET_ALL}")
        
        # GitHub secrets
        print(f"{Fore.CYAN}    GitHub Secret Search...{Style.RESET_ALL}")
        github_secrets = self.query_github_secrets(target)
        if github_secrets:
            results['github_secrets'] = github_secrets
            for secret in github_secrets:
                if secret['count'] > 0:
                    print(f"{Fore.YELLOW}        └── {secret['message']}{Style.RESET_ALL}")
        
        return results
