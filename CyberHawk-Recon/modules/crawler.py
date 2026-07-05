#!/usr/bin/env python3
"""
Advanced Web Crawler - Find hidden directories, files, endpoints
"""

import requests
import threading
import time
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style
import sys
import re

class WebCrawler:
    def __init__(self, target, threads=100, timeout=3):
        self.target = target
        self.threads = threads
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'CyberHawk-Recon/3.0'}
        self.found = []
        self.visited = set()
    
    def crawl_with_wordlist(self, base_url, wordlist):
        """Crawl with custom wordlist"""
        return self.crawl(base_url)
    
    def crawl(self, base_url):
        """Default crawl"""
        wordlist = self.load_directory_wordlist()
        total = len(wordlist)
        
        print(f"\n{Fore.CYAN}┌─────────────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│                    WEB CRAWLER & DIRECTORY DISCOVERY                 │{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├─────────────────────────────────────────────────────────────────────┤{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Target:{Fore.CYAN} {base_url}{' ' * (53 - len(base_url))}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Words:{Fore.CYAN} {total}{' ' * 55}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Threads:{Fore.CYAN} {self.threads}{' ' * 52}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'STATUS':<8} {'URL':<55} {'SIZE':<8}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
        
        found_dirs = []
        
        for word in wordlist[:500]:
            url = urljoin(base_url, word)
            if not url.endswith('/') and '.' not in word.split('/')[-1]:
                url += '/'
            
            try:
                resp = self.session.get(url, timeout=self.timeout, verify=False)
                if resp.status_code in [200, 201, 202, 203, 204, 301, 302, 403]:
                    found_dirs.append({'url': url, 'status': resp.status_code, 'size': len(resp.content)})
                    status_color = Fore.GREEN if resp.status_code == 200 else Fore.YELLOW
                    size_info = f"{len(resp.content)}b" if len(resp.content) < 1024 else f"{len(resp.content)/1024:.1f}kb"
                    print(f"{status_color}[{resp.status_code}]{Style.RESET_ALL} {Fore.WHITE}{url:<55}{Style.RESET_ALL} {Fore.CYAN}{size_info:>8}{Style.RESET_ALL}")
            except:
                pass
        
        return found_dirs
    
    def crawl_javascript(self, base_url):
        """Extract endpoints from JavaScript files"""
        endpoints = set()
        
        try:
            resp = self.session.get(base_url, timeout=5, verify=False)
            js_pattern = r'(?:src|href)=["\']([^"\']+\.js[^"\']*)["\']'
            js_files = re.findall(js_pattern, resp.text, re.I)
            
            for js_file in js_files[:10]:
                if not js_file.startswith('http'):
                    js_file = urljoin(base_url, js_file)
                
                try:
                    js_resp = self.session.get(js_file, timeout=5, verify=False)
                    # Look for API endpoints
                    api_patterns = [
                        r'["\'](/api/[a-zA-Z0-9/_-]+)["\']',
                        r'["\'](/v\d+/[a-zA-Z0-9/_-]+)["\']',
                        r'url:\s*["\']([^"\']+)["\']',
                        r'fetch\(["\']([^"\']+)["\']'
                    ]
                    
                    for pattern in api_patterns:
                        matches = re.findall(pattern, js_resp.text, re.I)
                        for match in matches:
                            if len(match) > 3:
                                endpoints.add(match[:100])
                except:
                    pass
        except:
            pass
        
        return list(endpoints)[:30]
    
    def load_directory_wordlist(self):
        return [
            'admin', 'login', 'wp-admin', 'dashboard', 'cpanel', 'backup', 'config',
            'api', 'v1', 'v2', 'v3', 'docs', 'uploads', 'assets', 'static', 'js', 'css',
            '.env', '.git', 'robots.txt', 'sitemap.xml', 'phpinfo.php'
        ]
