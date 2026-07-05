

<div align="center">

![CyberHawk Recon](https://img.shields.io/badge/CyberHawk-Recon-red?style=for-the-badge)
![Version](https://img.shields.io/badge/version-4.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.6+-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)

**Professional Reconnaissance Tool for Security Researchers & Penetration Testers**

[Installation](#-installation) • [Features](#-features) • [Usage](#-usage) • [Examples](#-examples) • [Documentation](#-documentation)

</div>


## 📋 Overview

CyberHawk Recon is a comprehensive reconnaissance tool designed for security professionals and penetration testers. It provides real results through multiple scanning modules including port scanning, subdomain discovery, web crawling, vulnerability detection, and technology fingerprinting.

**Developed by:** IAIICT PROJECT DCT PROJECT GROUP 10

## ✨ Features

### 🔍 Core Modules

| Module | Description | Status |
|--------|-------------|--------|
| **Port Scanning** | Complete port scanning with service detection | ✅ Active |
| **Subdomain Discovery** | Passive & active subdomain enumeration | ✅ Active |
| **Web Crawling** | Hidden directory and file discovery | ✅ Active |
| **Vulnerability Scanning** | Security header analysis & exposed file detection | ✅ Active |
| **Technology Detection** | CMS, framework, and server fingerprinting | ✅ Active |

### 🚀 Key Capabilities

- **Multi-threaded Scanning**: Configurable thread pool for faster results
- **Real-time Progress**: Live feedback during scanning operations
- **Service Detection**: Identifies services running on open ports
- **Security Headers Analysis**: Checks for missing security headers
- **Exposed File Detection**: Finds sensitive files like .env, .git, robots.txt
- **Subdomain Validation**: DNS resolution to confirm active subdomains
- **Technology Fingerprinting**: Identifies CMS, frameworks, and web servers
- **Color-coded Output**: Easy-to-read console output with color coding

## 📦 Installation

### Prerequisites

- Python 3.6 or higher
- pip package manager

### Quick Install

# Clone the repository
git clone https://github.com/iaiictproject/cyberhawk.git
cd cyberhawk

# Install dependencies
pip install -r requirements.txt

# Make executable
chmod +x cyberhawk.py



## 🚀 Usage

### Basic Syntax

python cyberhawk.py -t <target> [options]


### Available Options

| Option | Description |
|--------|-------------|
| `-t, --target` | Target domain (e.g., example.com) |
| `--threads` | Number of threads (default: 50) |
| `--basic` | Run basic reconnaissance |
| `--ports` | Perform port scanning |
| `--subdomains` | Discover subdomains |
| `--crawl` | Web crawl for hidden paths |
| `--vulns` | Scan for vulnerabilities |
| `--tech` | Detect technology stack |
| `--all` | Run all modules |
| `-h, --help` | Show help menu |

## 📊 Examples

### 1. Basic Reconnaissance

python cyberhawk.py -t example.com --basic


Performs port scanning and technology detection.

### 2. Complete Reconnaissance

python cyberhawk.py -t example.com --all


Runs all modules: ports, subdomains, crawling, vulnerabilities, and tech detection.

### 3. Custom Thread Count


python cyberhawk.py -t example.com --all --threads 100


Increases thread pool for faster scanning.

### 4. Subdomain Discovery Only

python cyberhawk.py -t example.com --subdomains


Finds and validates subdomains.

### 5. Vulnerability Assessment


python cyberhawk.py -t example.com --vulns


Checks security headers and exposed files.

### 6. Technology Fingerprinting

python cyberhawk.py -t example.com --tech

Identifies web server, CMS, and frameworks.

## 📋 Sample Output


╔══════════════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                                         ║
║     ██████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗  ██╗ █████╗ ██╗    ██╗██╗  ██╗                     ║
║    ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗██║  ██║██╔══██╗██║    ██║██║ ██╔╝              ║
║    -------------------------------------------------------------------------╝               ║
║    ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗██╔══██║██╔══██║██║███╗██║██╔═██╗               ║
║    ╚██████╗   ██║   ██████╔╝███████╗██║  ██║██║  ██║██║  ██║╚███╔███╔╝██║  ██╗               ║
║     ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═╝               ║
║                                                                                                  ║
║                         CYBERHAWK RECON - REAL EDITION                                     ║
║                    Professional Reconnaissance | Real Results Only                          ║
║                                    v4.0.0                                              ║
║                         IAIICT PROJECT DCT PROJECT GROUP 10                               ║
║                                                                                                  ║
╚══════════════════════════════════════════════════════════════════════════════════════════════╝

[>] Target: example.com
[>] Threads: 50
[✓] Resolved: example.com → 93.184.216.34

======================================================================
🔌 PORT SCANNING - 93.184.216.34
======================================================================
PORT     STATE      SERVICE
----------------------------------------------------------------------
80       open       HTTP
443      open       HTTPS
----------------------------------------------------------------------
[✓] Found 2 open ports

======================================================================
🌐 SUBDOMAIN DISCOVERY - example.com
======================================================================
[*] Querying HackerTarget API...
    └── Found 3 subdomains

[*] Validating subdomains...
[+] www.example.com → 93.184.216.34
[+] mail.example.com → 93.184.216.35
[✓] Found 2 alive subdomains

======================================================================
🚨 VULNERABILITY SCANNING - example.com
======================================================================
[*] Checking security headers...
[!] Missing: Content-Security-Policy
[!] Missing: X-Frame-Options

[*] Checking for exposed files...
[!] EXPOSED: https://example.com/robots.txt

[✓] Found 3 potential issues

======================================================================
                    SCAN COMPLETE
======================================================================


## 🛡️ Legal Disclaimer

> **⚠️ IMPORTANT**: This tool is designed for educational purposes and authorized security testing only. Users are solely responsible for ensuring they have proper authorization before scanning any target. Unauthorized scanning may violate laws and regulations in your jurisdiction.

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request`

### Development Guidelines

- Follow PEP 8 style guide
- Add comments for complex logic
- Update documentation for new features
- Test thoroughly before submitting

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- IAIICT Project DCT Project Group 10
- Open-source security community
- Contributors and testers

## 📞 Contact

For issues, suggestions, or contributions:
- **Open an Issue**: [GitHub Issues](https://github.com/iaiictproject/cyberhawk/issues)
- **Email**: iaiictgroup10project@gmail.com



<div align="center">
  <sub>Built with ❤️ by IAIICT PROJECT DCT PROJECT GROUP 10</sub>
</div>


## 📁 Additional Files to Create

### 1. **requirements.txt**
Create this file in your repository root:


requests>=2.28.0
colorama>=0.4.6
urllib3>=1.26.0


### 2. **LICENSE**
Create a MIT License file:


MIT License

Copyright (c) 2024 IAIICT PROJECT DCT PROJECT GROUP 10

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.


### 3. **.gitignore**
Create a `.gitignore` file:

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
env/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs
*.log
*.out

# OS
.DS_Store
Thumbs.db

# Reports
reports/
results/
*.json

### 4. **setup.py** (Optional - for pip installation)
from setuptools import setup, find_packages

setup(
    name="cyberhawk-recon",
    version="4.0.0",
    author="IAIICT PROJECT DCT PROJECT GROUP 10",
    description="Professional Reconnaissance Tool for Security Researchers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/iaiictproject/cyberhawk",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Security",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.28.0",
        "colorama>=0.4.6",
        "urllib3>=1.26.0",
    ],
    entry_points={
        "console_scripts": [
            "cyberhawk=cyberhawk:main",
        ],
    },
)


## 🚀 Quick Setup Commands

After creating these files, run:

# Initialize git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit: CyberHawk Recon v4.0.0"

# Add remote
git remote add origin https://github.com/iaiictproject/cyberhawk.git

# Push to GitHub
git push -u origin main
