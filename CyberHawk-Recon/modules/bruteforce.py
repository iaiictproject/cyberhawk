#!/usr/bin/env python3
"""
Advanced Subdomain Bruteforce Engine - Find Hidden Subdomains
Like gobuster/ffuf but for subdomains
Authors: IAIICT PROJECT DCT PROJECT GROUP 10
"""

import socket
import dns.resolver
import requests
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from colorama import Fore, Style
from tqdm import tqdm
import sys

class SubdomainBruteforceEngine:
    """Find hidden subdomains that aren't in public databases"""
    
    def __init__(self, domain, threads=200, timeout=3):
        self.domain = domain
        self.threads = threads
        self.timeout = timeout
        self.found = []
        self.resolved_cache = {}
        self.lock = threading.Lock()
        
        # DNS resolvers for reliability
        self.resolvers = ['8.8.8.8', '8.8.4.4', '1.1.1.1', '1.0.0.1', '9.9.9.9']
    
    def load_massive_wordlist(self):
        """Load comprehensive subdomain wordlist (10,000+ entries)"""
        wordlist = [
            # Common prefixes
            'www', 'mail', 'webmail', 'ftp', 'smtp', 'pop3', 'imap', 'ns1', 'ns2', 'ns3',
            'admin', 'administrator', 'blog', 'dev', 'development', 'staging', 'stage',
            'test', 'testing', 'qa', 'quality', 'uat', 'acceptance', 'preprod', 'preproduction',
            'demo', 'demo2', 'sandbox', 'playground', 'lab', 'labs', 'internal', 'external',
            
            # Technical
            'api', 'rest', 'graphql', 'v1', 'v2', 'v3', 'v4', 'latest', 'current', 'stable',
            'app', 'apps', 'application', 'web', 'site', 'portal', 'dashboard', 'console',
            'cdn', 'static', 'assets', 'resources', 'media', 'images', 'img', 'css', 'js',
            'upload', 'download', 'files', 'data', 'content', 'docs', 'documentation',
            
            # Infrastructure
            'db', 'database', 'mysql', 'postgres', 'postgresql', 'mongo', 'mongodb', 'redis',
            'elastic', 'elasticsearch', 'kibana', 'logstash', 'grafana', 'prometheus',
            'jenkins', 'gitlab', 'github', 'bitbucket', 'git', 'repo', 'code', 'build',
            'ci', 'cd', 'pipeline', 'deploy', 'deployment', 'artifact', 'docker', 'kubernetes',
            'k8s', 'openshift', 'rancher', 'nomad', 'terraform', 'ansible', 'puppet', 'chef',
            
            # Security
            'vpn', 'remote', 'secure', 'security', 'auth', 'authentication', 'login', 'signin',
            'oauth', 'sso', 'identity', 'idp', 'mfa', '2fa', 'verify', 'cert', 'certificate',
            'ssl', 'tls', 'encrypt', 'encryption', 'decrypt', 'firewall', 'waf', 'ids', 'ips',
            'monitor', 'monitoring', 'status', 'health', 'healthcheck', 'ready', 'live', 'metrics',
            'stats', 'analytics', 'logs', 'logging', 'trace', 'debug', 'profiler',
            
            # Business
            'corp', 'corporate', 'company', 'business', 'enterprise', 'intranet', 'extranet',
            'hr', 'human-resources', 'finance', 'accounting', 'legal', 'compliance', 'risk',
            'audit', 'procurement', 'purchasing', 'sales', 'marketing', 'advertising', 'pr',
            'support', 'help', 'helpdesk', 'service-desk', 'ticket', 'kb', 'knowledge-base',
            'wiki', 'training', 'learn', 'education', 'academy', 'university', 'campus',
            
            # Cloud
            'aws', 'azure', 'gcp', 'google-cloud', 'amazon', 'microsoft', 'cloud', 'cloudfront',
            'cloudflare', 'fastly', 'akamai', 's3', 'ec2', 'rds', 'lambda', 'cloudwatch',
            'cloudtrail', 'iam', 'kms', 'secrets', 'vault', 'storage', 'bucket',
            
            # Development patterns
            'dev-', 'test-', 'stage-', 'prod-', 'api-', 'app-', 'web-', 'mobile-',
            '-dev', '-test', '-stage', '-prod', '-api', '-app', '-web', '-mobile',
            'dev1', 'dev2', 'test1', 'test2', 'stage1', 'prod1', 'prod2',
            '01', '02', '03', '04', '05', '10', '11', '12',
            
            # Additional common subdomains
            'analytics', 'tracking', 'pixel', 'tag', 'events', 'collector',
            'auth0', 'okta', 'onelogin', 'authy', 'duo',
            'statuspage', 'uptime', 'healthz', 'readyz', 'livez',
            'backup', 'backups', 'archive', 'archives', 'snapshot', 'snapshots',
            'cache', 'caching', 'proxy', 'reverse-proxy', 'load-balancer', 'lb',
            'gateway', 'api-gateway', 'ingress', 'egress', 'bastion', 'jump',
            'ci', 'cd', 'cicd', 'jenkins', 'gitlab-ci', 'github-actions', 'circleci',
            'travis', 'drone', 'concourse', 'teamcity', 'bamboo', 'spinnaker',
            'argo', 'flux', 'helm', 'chart', 'registry', 'harbor', 'quay',
            'elastic', 'kibana', 'logstash', 'beats', 'filebeat', 'metricbeat',
            'packetbeat', 'heartbeat', 'auditbeat', 'winlogbeat', 'fluentd',
            'fluentbit', 'logstash', 'graylog', 'splunk', 'sumologic', 'datadog',
            'newrelic', 'dynatrace', 'appdynamics', 'instana', 'honeycomb',
            'sentry', 'rollbar', 'bugsnag', 'raygun', 'airbrake'
        ]
        
        # Remove duplicates and generate variations
        wordlist = list(set(wordlist))
        
        # Try to load external wordlist if exists
        try:
            with open('wordlists/subdomains.txt', 'r') as f:
                external = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                wordlist.extend(external)
                wordlist = list(set(wordlist))
        except:
            pass
        
        return wordlist
    
    def check_subdomain(self, sub):
        """Check if subdomain resolves"""
        full = f"{sub}.{self.domain}"
        
        # Check cache
        if full in self.resolved_cache:
            return self.resolved_cache[full] if self.resolved_cache[full] else None
        
        try:
            ip = socket.gethostbyname(full)
            with self.lock:
                self.resolved_cache[full] = ip
            return (full, ip)
        except:
            with self.lock:
                self.resolved_cache[full] = None
            return None
    
    def bruteforce(self, wordlist=None):
        """Run bruteforce with real-time display"""
        if not wordlist:
            wordlist = self.load_massive_wordlist()
        
        total = len(wordlist)
        found = []
        
        print(f"\n{Fore.CYAN}┌─────────────────────────────────────────────────────────────────────┐{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│                    SUBDOMAIN BRUTEFORCE ENGINE                       │{Style.RESET_ALL}")
        print(f"{Fore.CYAN}├─────────────────────────────────────────────────────────────────────┤{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Target:{Fore.CYAN} {self.domain}{' ' * (50 - len(self.domain))}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Words:{Fore.CYAN} {total}{' ' * 55}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}│ {Fore.WHITE}Threads:{Fore.CYAN} {self.threads}{' ' * 52}│{Style.RESET_ALL}")
        print(f"{Fore.CYAN}└─────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}")
        
        print(f"\n{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'STATUS':<10} {'SUBDOMAIN':<45} {'IP':<15}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
        
        start_time = time.time()
        
        with ThreadPoolExecutor(max_workers=self.threads) as executor:
            futures = {executor.submit(self.check_subdomain, word): word for word in wordlist}
            
            for future in as_completed(futures):
                result = future.result()
                if result:
                    full, ip = result
                    found.append(full)
                    print(f"{Fore.GREEN}[FOUND]{Style.RESET_ALL} {Fore.WHITE}{full:<45}{Style.RESET_ALL} {Fore.CYAN}→ {ip}{Style.RESET_ALL}")
                
                # Progress update
                completed = len([f for f in futures if f.done()])
                if completed % 100 == 0:
                    rate = completed / (time.time() - start_time) if (time.time() - start_time) > 0 else 0
                    sys.stdout.write(f"\r{Fore.YELLOW}[*] Progress: {completed}/{total} ({rate:.0f}/s) | Found: {len(found)}{Style.RESET_ALL}")
                    sys.stdout.flush()
        
        elapsed = time.time() - start_time
        print(f"\n\n{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[✓] Bruteforce complete! Found {len(found)} subdomains in {elapsed:.1f}s{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'─'*70}{Style.RESET_ALL}")
        
        return found
    
    def smart_bruteforce(self, initial_finds):
        """Learn from found subdomains and generate targeted wordlist"""
        if not initial_finds:
            return []
        
        patterns = set()
        for sub in initial_finds:
            # Extract parts that might be patterns
            parts = sub.replace(f".{self.domain}", "").split('.')
            for part in parts:
                if len(part) > 3 and part not in ['www', 'mail', 'api']:
                    patterns.add(part)
        
        # Generate pattern-based words
        smart_words = []
        for pattern in patterns:
            smart_words.append(pattern)
            smart_words.append(f"{pattern}-api")
            smart_words.append(f"api-{pattern}")
            smart_words.append(f"{pattern}-dev")
            smart_words.append(f"dev-{pattern}")
            smart_words.append(f"{pattern}-test")
            smart_words.append(f"test-{pattern}")
            smart_words.append(f"{pattern}-staging")
            smart_words.append(f"staging-{pattern}")
            smart_words.append(f"{pattern}-prod")
            smart_words.append(f"prod-{pattern}")
            smart_words.append(f"{pattern}1")
            smart_words.append(f"{pattern}2")
            smart_words.append(f"{pattern}01")
            smart_words.append(f"{pattern}02")
        
        smart_words = list(set(smart_words))
        
        if smart_words:
            print(f"\n{Fore.BLUE}[*] Smart bruteforce with {len(smart_words)} pattern-based words...{Style.RESET_ALL}")
            return self.bruteforce(smart_words)
        
        return []
