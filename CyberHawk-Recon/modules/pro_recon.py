#!/usr/bin/env python3
"""
Professional Reconnaissance Engine - COMPLETE Version
Features: WAF Detection, Origin IP, Tech Stack, Endpoints, Subdomain Takeover
Authors: IAIICT PROJECT DCT PROJECT GROUP 10
"""

import requests
import socket
import dns.resolver
import re
import json
import hashlib
import ssl
import OpenSSL.crypto as crypto
from datetime import datetime
from colorama import Fore, Style
import urllib3
from concurrent.futures import ThreadPoolExecutor, as_completed

urllib3.disable_warnings()

class ProfessionalRecon:
    """Complete professional reconnaissance - All features working"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def detect_waf(self, domain):
        """Enhanced WAF Detection - Multiple methods"""
        waf_signatures = {
            'Cloudflare': ['cf-ray', 'cloudflare', '__cfduid', 'cf-cache-status'],
            'AWS WAF': ['x-amzn-RequestId', 'AWSALB', 'awselb'],
            'Sucuri': ['sucuri', 'x-sucuri-id', 'x-sucuri-cache'],
            'Akamai': ['akamai', 'x-akamai', 'akamai-x'],
            'Imperva': ['incap_ses', 'visid_incap', 'x-iinfo', '_incap'],
            'F5 BIG-IP': ['bigip', 'f5.com', 'X-F5-Edge'],
            'ModSecurity': ['mod_security', 'NOYB', 'Mod_Security'],
            'Wordfence': ['wordfence', 'wfvt', 'wfwaf'],
            'Barracuda': ['barracuda', 'cuda'],
            'Fortinet': ['fortigate', 'fortinet'],
            'CloudFront': ['cloudfront', 'x-amz-cf'],
            'Fastly': ['fastly', 'x-served-by', 'x-cache-hits'],
            'StackPath': ['stackpath', 'x-oc-cache'],
            'Edgecast': ['ecdn', 'edgecast']
        }
        
        detected = []
        
        try:
            # Method 1: HTTP Headers
            resp = self.session.get(f"https://{domain}", timeout=10, verify=False)
            headers = resp.headers
            html = resp.text.lower()
            
            for waf, signatures in waf_signatures.items():
                for sig in signatures:
                    if sig.lower() in str(headers).lower() or sig.lower() in html:
                        detected.append(waf)
                        break
            
            # Method 2: Cloudflare detection via DNS
            try:
                cf = socket.gethostbyname(f"{domain}.cdn.cloudflare.net")
                if cf:
                    detected.append('Cloudflare (CDN detected)')
            except:
                pass
            
            # Method 3: Response behavior
            test_payload = "/?id=1%20AND%201=1"
            try:
                test_resp = self.session.get(f"https://{domain}{test_payload}", timeout=10, verify=False)
                if test_resp.status_code == 403 or 'blocked' in test_resp.text.lower():
                    if 'WAF' not in detected:
                        detected.append('Generic WAF (Blocking behavior)')
            except:
                pass
            
        except:
            pass
        
        return {'detected': list(set(detected)), 'has_waf': len(detected) > 0}
    
    def find_origin_ip(self, domain):
        """Enhanced Origin IP Discovery - Multiple techniques"""
        origin_ips = set()
        
        # Technique 1: Historical DNS records
        try:
            url = f"https://api.hackertarget.com/hostsearch/?q={domain}"
            resp = self.session.get(url, timeout=10)
            for line in resp.text.split('\n'):
                if ',' in line:
                    parts = line.split(',')
                    if len(parts) > 1:
                        ip = parts[1].strip()
                        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
                            origin_ips.add(ip)
        except:
            pass
        
        # Technique 2: SSL Certificate analysis
        try:
            cert = ssl.get_server_certificate((domain, 443))
            x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            for i in range(x509.get_extension_count()):
                ext = x509.get_extension(i)
                if 'subjectAltName' in str(ext.get_short_name()):
                    for alt in str(ext).split(','):
                        if 'IP Address:' in alt:
                            ip = alt.split(':')[1].strip()
                            origin_ips.add(ip)
                        elif 'DNS:' in alt and domain not in alt:
                            try:
                                sub_ip = socket.gethostbyname(alt.split(':')[1].strip())
                                origin_ips.add(sub_ip)
                            except:
                                pass
        except:
            pass
        
        # Technique 3: Check common subdomains that bypass CDN
        bypass_subdomains = ['direct', 'origin', 'backend', 'internal', 'admin', 'dev', 
                            'api', 'live', 'static', 'media', 'cdn', 'www2', 'web', 'server']
        for sub in bypass_subdomains:
            try:
                ip = socket.gethostbyname(f"{sub}.{domain}")
                origin_ips.add(ip)
            except:
                pass
        
        # Technique 4: MX records (often point to origin)
        try:
            mx = dns.resolver.resolve(domain, 'MX')
            for record in mx:
                mx_domain = str(record.exchange).rstrip('.')
                try:
                    ip = socket.gethostbyname(mx_domain)
                    origin_ips.add(ip)
                except:
                    pass
        except:
            pass
        
        return {'origin_ips': list(origin_ips), 'count': len(origin_ips)}
    
    def get_technology_stack(self, domain):
        """Enhanced Technology Stack Detection"""
        tech = {
            'web_servers': [],
            'frameworks': [],
            'cms': [],
            'javascript': [],
            'analytics': [],
            'cdn': [],
            'cloud_providers': [],
            'languages': []
        }
        
        try:
            resp = self.session.get(f"https://{domain}", timeout=10, verify=False)
            headers = resp.headers
            html = resp.text.lower()
            
            # Web Servers
            server = headers.get('Server', '')
            if 'nginx' in server.lower():
                tech['web_servers'].append('Nginx')
            elif 'apache' in server.lower():
                tech['web_servers'].append('Apache')
            elif 'iis' in server.lower():
                tech['web_servers'].append('IIS')
            elif 'caddy' in server.lower():
                tech['web_servers'].append('Caddy')
            elif 'openresty' in server.lower():
                tech['web_servers'].append('OpenResty')
            
            # Programming Languages
            if '.php' in str(headers) or 'php' in server.lower():
                tech['languages'].append('PHP')
            if 'aspx' in str(headers) or '.net' in server.lower():
                tech['languages'].append('ASP.NET')
            if 'python' in server.lower() or 'django' in html:
                tech['languages'].append('Python')
            if 'node' in server.lower() or 'express' in html:
                tech['languages'].append('Node.js')
            if 'java' in server.lower() or 'jsp' in html:
                tech['languages'].append('Java')
            if 'ruby' in server.lower() or 'rails' in html:
                tech['languages'].append('Ruby')
            
            # CMS Detection
            cms_patterns = {
                'WordPress': ['/wp-content/', 'wordpress', 'wp-json', 'wp-includes'],
                'Drupal': ['drupal', 'sites/default', 'drupal.js'],
                'Joomla': ['joomla', 'com_content', 'media/joomla'],
                'Magento': ['magento', 'skin/frontend', 'mage/cookies'],
                'Shopify': ['shopify', 'myshopify.com', 'cdn.shopify'],
                'Wix': ['wix.com', 'wixstatic', 'wix-code'],
                'Squarespace': ['squarespace', 'static.squarespace'],
                'Webflow': ['webflow', 'cdn.webflow']
            }
            
            for cms, patterns in cms_patterns.items():
                for pattern in patterns:
                    if pattern in html:
                        tech['cms'].append(cms)
                        break
            
            # JavaScript Frameworks
            js_frameworks = {
                'React': ['react', 'react-dom', 'reactjs', 'react.min'],
                'Vue.js': ['vue', 'vue.js', 'vue.min', 'v-app'],
                'Angular': ['angular', 'ng-app', 'angularjs', 'ng-controller'],
                'jQuery': ['jquery', '$('],
                'Bootstrap': ['bootstrap', 'bootstrap.min'],
                'Tailwind': ['tailwind', 'tailwindcss']
            }
            
            for framework, patterns in js_frameworks.items():
                for pattern in patterns:
                    if pattern in html:
                        tech['javascript'].append(framework)
                        break
            
            # Analytics
            analytics = {
                'Google Analytics': ['google-analytics', 'gtag', 'ga('],
                'Facebook Pixel': ['facebook-pixel', 'fbq('],
                'Hotjar': ['hotjar', 'hj('],
                'Mixpanel': ['mixpanel', 'mpq('],
                'Segment': ['segment.com', 'analytics.js']
            }
            
            for service, patterns in analytics.items():
                for pattern in patterns:
                    if pattern in html:
                        tech['analytics'].append(service)
                        break
            
            # CDN Detection
            cdn_patterns = {
                'Cloudflare': ['cloudflare', 'cf-ray'],
                'Akamai': ['akamai', 'akamaihd'],
                'Fastly': ['fastly', 'x-fastly'],
                'CloudFront': ['cloudfront', 'amazonaws.com/cloudfront'],
                'Sucuri': ['sucuri', 'x-sucuri'],
                'StackPath': ['stackpath', 'highwinds']
            }
            
            for cdn, patterns in cdn_patterns.items():
                for pattern in patterns:
                    if pattern in str(headers).lower() or pattern in html:
                        tech['cdn'].append(cdn)
                        break
            
            # Cloud Providers
            cloud_providers = {
                'AWS': ['aws', 'amazonaws', 'ec2', 's3', 'elb'],
                'Azure': ['azure', 'azurewebsites', 'cloudapp'],
                'GCP': ['google cloud', 'appspot', 'cloud.google'],
                'DigitalOcean': ['digitalocean', 'do'],
                'Heroku': ['heroku', 'herokuapp']
            }
            
            for provider, patterns in cloud_providers.items():
                for pattern in patterns:
                    if pattern in str(headers).lower() or pattern in html:
                        tech['cloud_providers'].append(provider)
                        break
                        
        except:
            pass
        
        return tech
    
    def find_endpoints(self, domain):
        """Enhanced API Endpoint Discovery from JavaScript files"""
        endpoints = set()
        js_files = []
        
        try:
            resp = self.session.get(f"https://{domain}", timeout=10, verify=False)
            html = resp.text
            
            # Find JavaScript files
            js_patterns = [
                r'(?:src|href)=["\']([^"\']+\.js[^"\']*)["\']',
                r'(?:src|href)=["\'](//[^"\']+\.js[^"\']*)["\']',
                r'<script\s+[^>]*src=["\']([^"\']+\.js[^"\']*)["\'][^>]*>'
            ]
            
            for pattern in js_patterns:
                matches = re.findall(pattern, html, re.I)
                for match in matches:
                    if match.startswith('//'):
                        match = 'https:' + match
                    elif match.startswith('/') and not match.startswith('//'):
                        match = f"https://{domain}{match}"
                    if match.endswith('.js'):
                        js_files.append(match)
            
            js_files = list(set(js_files))[:30]
            
            # Analyze JavaScript files
            api_patterns = [
                r'["\'](https?://[^"\']*api[^"\']*)["\']',
                r'["\'](https?://[^"\']*v\d+[^"\']*)["\']',
                r'["\'](https?://[^"\']*graphql[^"\']*)["\']',
                r'["\'](https?://[^"\']*rest[^"\']*)["\']',
                r'url:\s*["\']([^"\']+)["\']',
                r'fetch\(["\']([^"\']+)["\']',
                r'\.get\(["\']([^"\']+)["\']',
                r'\.post\(["\']([^"\']+)["\']',
                r'axios\.(?:get|post|put|delete)\(["\']([^"\']+)["\']',
                r'/api/[a-zA-Z0-9/_-]+',
                r'/v\d+/[a-zA-Z0-9/_-]+'
            ]
            
            for js_url in js_files[:15]:
                try:
                    js_resp = self.session.get(js_url, timeout=5, verify=False)
                    content = js_resp.text
                    
                    for pattern in api_patterns:
                        matches = re.findall(pattern, content, re.I)
                        for match in matches:
                            if isinstance(match, str) and len(match) > 5:
                                if domain in match or match.startswith('/'):
                                    endpoints.add(match[:200] if len(match) > 200 else match)
                except:
                    pass
                    
        except:
            pass
        
        return {'endpoints': list(endpoints)[:50], 'total': len(endpoints)}
    
    def find_exposed_git(self, domain):
        """Check for exposed .git directory"""
        exposed = []
        
        git_paths = ['/.git/config', '/.git/HEAD', '/.git/index', '/.git/logs/HEAD', '/.gitignore']
        
        for path in git_paths:
            try:
                url = f"https://{domain}{path}"
                resp = self.session.get(url, timeout=5, verify=False)
                if resp.status_code == 200:
                    if 'repositoryformatversion' in resp.text or 'ref:' in resp.text or '.git' in resp.text:
                        exposed.append(url)
                        break
            except:
                pass
        
        if not exposed:
            try:
                url = f"http://{domain}/.git/config"
                resp = self.session.get(url, timeout=5, verify=False)
                if resp.status_code == 200 and 'repositoryformatversion' in resp.text:
                    exposed.append(url)
            except:
                pass
        
        return {'exposed': exposed, 'has_git': len(exposed) > 0}
    
    def find_backup_files(self, domain):
        """Find exposed backup and sensitive files"""
        backups = []
        
        sensitive_patterns = [
            '.env', '.env.backup', '.env.old', '.env.bak', '.env.local',
            'config.php', 'wp-config.php', 'config.yml', 'config.yaml', 'config.json',
            'database.sql', 'backup.sql', 'dump.sql', 'db_backup.sql',
            'appsettings.json', 'secrets.json', 'credentials.json', 'settings.json',
            'robots.txt', 'sitemap.xml', 'crossdomain.xml', 'security.txt',
            'phpinfo.php', 'info.php', 'test.php', 'debug.php',
            '.htaccess', '.htpasswd', '.gitignore', '.dockerignore',
            'Dockerfile', 'docker-compose.yml', 'Makefile'
        ]
        
        for pattern in sensitive_patterns:
            try:
                url = f"https://{domain}/{pattern}"
                resp = self.session.get(url, timeout=3, verify=False)
                if resp.status_code == 200:
                    sensitive_keywords = ['password', 'secret', 'key', 'token', 'api', 'db_', 'mysql', 'postgres']
                    is_sensitive = any(kw in resp.text.lower() for kw in sensitive_keywords)
                    backups.append({'url': url, 'type': pattern, 'sensitive': is_sensitive})
            except:
                pass
        
        return backups
    
    def check_subdomain_takeover(self, domain, subdomains):
        """Check for subdomain takeover vulnerabilities"""
        takeover_signatures = {
            'GitHub Pages': ['There isn\'t a GitHub Pages site here', 'Repository not found', '404 - Page not found'],
            'Heroku': ['No such app', 'Heroku | No such app', 'There\'s nothing here'],
            'AWS S3': ['NoSuchBucket', 'The specified bucket does not exist', 'Bucket not found'],
            'Azure': ['404 Web Site not found', 'Azure Websites', 'The resource you are looking for has been removed'],
            'Shopify': ['Sorry, this shop is currently unavailable', 'This store is unavailable'],
            'WordPress': ['Do you want to register', 'Coming Soon', 'Maintenance Mode'],
            'ReadTheDocs': ['Repository not found', 'Page not found'],
            'StatusPage': ['Page not found', 'There is no page here'],
            'CloudFront': ['Bad Request', 'The request could not be satisfied'],
            'Fastly': ['Fastly error: unknown domain', 'Domain not found']
        }
        
        takeover_candidates = []
        
        print(f"{Fore.BLUE}[*] Checking subdomain takeover for {len(subdomains)} subdomains...{Style.RESET_ALL}")
        
        def check_single(sub):
            vulnerabilities = []
            for service, signatures in takeover_signatures.items():
                for proto in ['https', 'http']:
                    try:
                        resp = self.session.get(f"{proto}://{sub}", timeout=5, verify=False)
                        for sig in signatures:
                            if sig.lower() in resp.text.lower():
                                vulnerabilities.append({
                                    'subdomain': sub,
                                    'service': service,
                                    'evidence': sig,
                                    'url': f"{proto}://{sub}",
                                    'risk': 'HIGH'
                                })
                                break
                        break
                    except:
                        continue
            return vulnerabilities
        
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = {executor.submit(check_single, sub): sub for sub in subdomains[:100]}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    takeover_candidates.extend(result)
                    for candidate in result:
                        print(f"{Fore.RED}    ⚠ {candidate['subdomain']} - {candidate['service']} takeover possible!{Style.RESET_ALL}")
        
        return takeover_candidates
    
    def comprehensive_recon(self, domain, subdomains=None):
        """Run all professional recon techniques"""
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}🎯 PROFESSIONAL RECONNAISSANCE REPORT{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        
        results = {}
        
        # 1. WAF Detection
        print(f"\n{Fore.BLUE}[*] WAF Detection...{Style.RESET_ALL}")
        waf = self.detect_waf(domain)
        results['waf'] = waf
        if waf['has_waf']:
            print(f"{Fore.YELLOW}    └── WAF Detected: {', '.join(waf['detected'])}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}    └── No WAF Detected (or detection bypassed){Style.RESET_ALL}")
        
        # 2. Origin IP Discovery
        print(f"\n{Fore.BLUE}[*] Origin IP Discovery...{Style.RESET_ALL}")
        origin = self.find_origin_ip(domain)
        results['origin_ips'] = origin
        if origin['origin_ips']:
            print(f"{Fore.YELLOW}    └── Found {origin['count']} potential origin IPs{Style.RESET_ALL}")
            for ip in origin['origin_ips'][:5]:
                print(f"{Fore.CYAN}        • {ip}{Style.RESET_ALL}")
            if origin['count'] > 5:
                print(f"{Fore.CYAN}        • ... and {origin['count'] - 5} more{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}    └── No origin IPs found (protected by CDN){Style.RESET_ALL}")
        
        # 3. Technology Stack
        print(f"\n{Fore.BLUE}[*] Technology Stack Detection...{Style.RESET_ALL}")
        tech = self.get_technology_stack(domain)
        results['technology'] = tech
        if tech['web_servers']:
            print(f"{Fore.GREEN}    └── Web Servers: {', '.join(tech['web_servers'])}{Style.RESET_ALL}")
        if tech['languages']:
            print(f"{Fore.GREEN}    └── Languages: {', '.join(tech['languages'])}{Style.RESET_ALL}")
        if tech['cms']:
            print(f"{Fore.GREEN}    └── CMS: {', '.join(tech['cms'])}{Style.RESET_ALL}")
        if tech['javascript']:
            print(f"{Fore.GREEN}    └── JS Frameworks: {', '.join(tech['javascript'])}{Style.RESET_ALL}")
        if tech['cdn']:
            print(f"{Fore.GREEN}    └── CDN: {', '.join(tech['cdn'])}{Style.RESET_ALL}")
        if tech['cloud_providers']:
            print(f"{Fore.GREEN}    └── Cloud: {', '.join(tech['cloud_providers'])}{Style.RESET_ALL}")
        
        # 4. API Endpoint Discovery
        print(f"\n{Fore.BLUE}[*] API Endpoint Discovery...{Style.RESET_ALL}")
        endpoints = self.find_endpoints(domain)
        results['endpoints'] = endpoints
        if endpoints['endpoints']:
            print(f"{Fore.GREEN}    └── Found {endpoints['total']} potential endpoints{Style.RESET_ALL}")
            for ep in endpoints['endpoints'][:5]:
                print(f"{Fore.CYAN}        • {ep[:80]}{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}    └── No endpoints found{Style.RESET_ALL}")
        
        # 5. Exposed Git
        print(f"\n{Fore.BLUE}[*] Exposed Git Repository Check...{Style.RESET_ALL}")
        git = self.find_exposed_git(domain)
        results['exposed_git'] = git
        if git['has_git']:
            print(f"{Fore.RED}    └── ⚠ EXPOSED .git directory!{Style.RESET_ALL}")
            for url in git['exposed']:
                print(f"{Fore.RED}        • {url}{Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}    └── No exposed .git found{Style.RESET_ALL}")
        
        # 6. Backup/Sensitive Files
        print(f"\n{Fore.BLUE}[*] Backup/Sensitive File Discovery...{Style.RESET_ALL}")
        backups = self.find_backup_files(domain)
        results['backup_files'] = backups
        sensitive = [b for b in backups if b.get('sensitive')]
        if sensitive:
            print(f"{Fore.RED}    └── ⚠ Found {len(sensitive)} sensitive files{Style.RESET_ALL}")
            for b in sensitive[:5]:
                print(f"{Fore.RED}        • {b['url']}{Style.RESET_ALL}")
        elif backups:
            print(f"{Fore.YELLOW}    └── Found {len(backups)} files (non-sensitive){Style.RESET_ALL}")
        else:
            print(f"{Fore.GREEN}    └── No backup files found{Style.RESET_ALL}")
        
        # 7. ASN Info
        print(f"\n{Fore.BLUE}[*] ASN & Network Information...{Style.RESET_ALL}")
        try:
            ip = socket.gethostbyname(domain)
            url = f"https://ipinfo.io/{ip}/json"
            resp = self.session.get(url, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                asn_info = {
                    'ip': ip,
                    'org': data.get('org', 'Unknown'),
                    'asn': data.get('asn', 'Unknown'),
                    'country': data.get('country', 'Unknown'),
                    'city': data.get('city', 'Unknown'),
                    'hostname': data.get('hostname', 'Unknown')
                }
                results['asn_info'] = asn_info
                print(f"{Fore.GREEN}    └── IP: {asn_info['ip']}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}    └── ASN: {asn_info['asn']} - {asn_info['org']}{Style.RESET_ALL}")
                print(f"{Fore.GREEN}    └── Location: {asn_info['city']}, {asn_info['country']}{Style.RESET_ALL}")
        except:
            pass
        
        # 8. Subdomain Takeover Check (if subdomains provided)
        if subdomains:
            print(f"\n{Fore.BLUE}[*] Subdomain Takeover Check...{Style.RESET_ALL}")
            takeovers = self.check_subdomain_takeover(domain, subdomains)
            results['subdomain_takeover'] = takeovers
            if takeovers:
                print(f"{Fore.RED}    └── Found {len(takeovers)} takeover candidates{Style.RESET_ALL}")
            else:
                print(f"{Fore.GREEN}    └── No takeover candidates found{Style.RESET_ALL}")
        
        return results
