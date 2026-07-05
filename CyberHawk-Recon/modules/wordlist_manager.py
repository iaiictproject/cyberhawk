#!/usr/bin/env python3
"""
Wordlist Manager - Custom wordlists, pattern generation, management
Authors: IAIICT PROJECT DCT PROJECT GROUP 10
"""

import os
import re
from pathlib import Path

class WordlistManager:
    """Manage and generate custom wordlists"""
    
    def __init__(self, wordlist_dir="wordlists"):
        self.wordlist_dir = wordlist_dir
        os.makedirs(wordlist_dir, exist_ok=True)
    
    def load_wordlist(self, name):
        """Load a wordlist by name"""
        path = os.path.join(self.wordlist_dir, f"{name}.txt")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return [line.strip() for line in f if line.strip() and not line.startswith('#')]
        return None
    
    def save_wordlist(self, name, words):
        """Save a wordlist"""
        path = os.path.join(self.wordlist_dir, f"{name}.txt")
        with open(path, 'w') as f:
            f.write('\n'.join(sorted(set(words))))
        return path
    
    def generate_from_patterns(self, discovered):
        """Generate new wordlist from discovered subdomains"""
        patterns = set()
        
        for sub in discovered:
            # Extract parts
            parts = sub.split('.')
            for part in parts:
                if len(part) > 3 and part not in ['www', 'mail', 'api', 'admin']:
                    patterns.add(part)
                    
                    # Generate variations
                    patterns.add(f"{part}-api")
                    patterns.add(f"api-{part}")
                    patterns.add(f"{part}-dev")
                    patterns.add(f"dev-{part}")
                    patterns.add(f"{part}-test")
                    patterns.add(f"test-{part}")
                    patterns.add(f"{part}-staging")
                    patterns.add(f"{part}-prod")
                    patterns.add(f"{part}1")
                    patterns.add(f"{part}2")
                    patterns.add(f"{part}01")
                    patterns.add(f"{part}02")
        
        return list(patterns)
    
    def get_default_subdomains(self):
        """Return default subdomain wordlist"""
        return [
            'www', 'mail', 'webmail', 'ftp', 'smtp', 'pop3', 'imap', 'ns1', 'ns2',
            'admin', 'blog', 'dev', 'staging', 'test', 'api', 'cdn', 'vpn', 'portal',
            'app', 'secure', 'remote', 'support', 'shop', 'store', 'forum', 'docs',
            'git', 'jenkins', 'jira', 'dashboard', 'console', 'login', 'auth', 'sso',
            'monitor', 'status', 'health', 'metrics', 'logs', 'backup', 'db', 'database',
            'cache', 'worker', 'analytics', 'reports', 'data', 'static', 'assets',
            'media', 'images', 'upload', 'download', 'files'
        ]
    
    def get_default_directories(self):
        """Return default directory wordlist"""
        return [
            'admin', 'login', 'wp-admin', 'dashboard', 'cpanel', 'backup', 'config',
            'sql', 'dump', 'logs', 'temp', 'api', 'v1', 'v2', 'v3', 'docs',
            'uploads', 'images', 'assets', 'static', 'js', 'css', 'include', 'inc',
            'modules', 'plugins', 'themes', 'downloads', 'files', 'data', 'database'
        ]
    
    def merge_wordlists(self, *wordlists):
        """Merge multiple wordlists"""
        merged = set()
        for wl in wordlists:
            if wl:
                merged.update(wl)
        return list(merged)
    
    def list_wordlists(self):
        """List all available wordlists"""
        files = os.listdir(self.wordlist_dir) if os.path.exists(self.wordlist_dir) else []
        return [f.replace('.txt', '') for f in files if f.endswith('.txt')]
