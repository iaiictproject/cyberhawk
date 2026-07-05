
<div align="center">

![CyberHawk Recon](https://img.shields.io/badge/CyberHawk-Recon-red?style=for-the-badge)
![Version](https://img.shields.io/badge/version-4.0.0-blue?style=for-the-badge)
![Python](https://img.shields.io/badge/python-3.6+-green?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Termux%20%7C%20Windows-lightgrey?style=for-the-badge)
![Status](https://img.shields.io/badge/status-active-success?style=for-the-badge)

# 🦅 CyberHawk Recon

**Professional Reconnaissance Tool for Security Researchers & Penetration Testers**

[![GitHub stars](https://img.shields.io/github/stars/iaiictproject/cyberhawk?style=social)](https://github.com/iaiictproject/cyberhawk/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/iaiictproject/cyberhawk?style=social)](https://github.com/iaiictproject/cyberhawk/network/members)

[Installation](#-installation) • [Quick Start](#-quick-start) • [Features](#-features) • [Usage](#-usage) • [Examples](#-examples) • [Documentation](#-documentation)

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

- ⚡ **Multi-threaded Scanning**: Configurable thread pool for faster results
- 📊 **Real-time Progress**: Live feedback during scanning operations
- 🔌 **Service Detection**: Identifies services running on open ports
- 🛡️ **Security Headers Analysis**: Checks for missing security headers
- 📁 **Exposed File Detection**: Finds sensitive files like .env, .git, robots.txt
- 🌐 **Subdomain Validation**: DNS resolution to confirm active subdomains
- 💻 **Technology Fingerprinting**: Identifies CMS, frameworks, and web servers
- 🎨 **Color-coded Output**: Easy-to-read console output with color coding
- 📝 **JSON Export**: Export results for further analysis


## 📦 Installation

### 📱 **Termux (Android)**

<details>
<summary><b>Click to expand Termux Installation Guide</b></summary>

#### Step-by-Step Installation

# 1. Update Termux packages
pkg update && pkg upgrade -y

# 2. Install required dependencies
pkg install python git -y

# 3. Install Python packages
pkg install python-pip -y

# 4. Clone the repository
git clone https://github.com/iaiictproject/cyberhawk.git

# 5. Navigate to the directory
cd cyberhawk

# 6. Install Python dependencies
pip install -r requirements.txt

# 7. Make executable
chmod +x cyberhawk.py

# 8. Run the tool
python cyberhawk.py -h


#### One-Click Installation Script

Copy and paste this entire command:


pkg update && pkg upgrade -y && pkg install python git python-pip -y && git clone https://github.com/iaiictproject/cyberhawk.git && cd cyberhawk && pip install -r requirements.txt && chmod +x cyberhawk.py && echo -e "\n\033[32m✓ CyberHawk installed successfully!\033[0m" && python cyberhawk.py -h


#### Troubleshooting Termux

If you encounter issues:

# Fix pip issues
pkg install python-pip
pip install --upgrade pip

# Fix permission issues
termux-setup-storage

# If Python version issues
pkg install python3


</details>



### 🐧 **Linux (Ubuntu/Debian/Kali/Parrot)**

<details>
<summary><b>Click to expand Linux Installation Guide</b></summary>

#### Step-by-Step Installation


# 1. Update system packages
sudo apt update && sudo apt upgrade -y

# 2. Install Python and pip if not installed
sudo apt install python3 python3-pip git -y

# 3. Clone the repository
git clone https://github.com/iaiictproject/cyberhawk.git

# 4. Navigate to the directory
cd cyberhawk

# 5. Install Python dependencies
pip3 install -r requirements.txt

# 6. Make executable
chmod +x cyberhawk.py

# 7. (Optional) Install globally
sudo cp cyberhawk.py /usr/local/bin/cyberhawk

# 8. Run the tool
python3 cyberhawk.py -h


#### One-Click Installation Script

Copy and paste this entire command:


sudo apt update && sudo apt upgrade -y && sudo apt install python3 python3-pip git -y && git clone https://github.com/iaiictproject/cyberhawk.git && cd cyberhawk && pip3 install -r requirements.txt && chmod +x cyberhawk.py && echo -e "\n\033[32m✓ CyberHawk installed successfully!\033[0m" && python3 cyberhawk.py -h


#### 📦 Arch Linux Installation


# Install dependencies
sudo pacman -S python python-pip git

# Clone and install
git clone https://github.com/iaiictproject/cyberhawk.git
cd cyberhawk
pip install -r requirements.txt
chmod +x cyberhawk.py

# Run
python cyberhawk.py -h


#### 🔴 Fedora/RHEL/CentOS


# Install dependencies
sudo dnf install python3 python3-pip git -y

# Clone and install
git clone https://github.com/iaiictproject/cyberhawk.git
cd cyberhawk
pip3 install -r requirements.txt
chmod +x cyberhawk.py

# Run
python3 cyberhawk.py -h


</details>


### 💻 **Windows**

<details>
<summary><b>Click to expand Windows Installation Guide</b></summary>

#### Option 1: Using Command Prompt (CMD)


# 1. Install Python from https://www.python.org/downloads/
# Make sure to check "Add Python to PATH" during installation

# 2. Open Command Prompt as Administrator

# 3. Install Git from https://git-scm.com/download/win

# 4. Clone repository
git clone https://github.com/iaiictproject/cyberhawk.git

# 5. Navigate to directory
cd cyberhawk

# 6. Install dependencies
pip install -r requirements.txt

# 7. Run the tool
python cyberhawk.py -h


#### Option 2: Using PowerShell

# Run PowerShell as Administrator

# Install Python dependencies
pip install requests colorama urllib3

# Clone repository
git clone https://github.com/iaiictproject/cyberhawk.git

# Navigate
cd cyberhawk

# Run
python cyberhawk.py -h


#### Option 3: Complete Batch Script

Create a file `install.bat` with:

@echo off
echo Installing CyberHawk Recon...
echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found! Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Clone repository...
git clone https://github.com/iaiictproject/cyberhawk.git
cd cyberhawk

echo.
echo CyberHawk installed successfully!
echo.
echo Run: python cyberhawk.py -h
pause

#### 💡 Windows Tips

- Use **Windows Terminal** for better experience
- Run as Administrator for full functionality
- Disable Windows Defender temporarily if issues occur

</details>

### 🐍 **Docker Installation** (Bonus)

<details>
<summary><b>Click to expand Docker Installation</b></summary>

# Build Docker image
docker build -t cyberhawk .

# Run the container
docker run -it cyberhawk

# Or run with target
docker run -it cyberhawk python cyberhawk.py -t example.com --all


Create `Dockerfile`:

FROM python:3.9-alpine

RUN apk add --no-cache git

WORKDIR /app

RUN git clone https://github.com/iaiictproject/cyberhawk.git .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "cyberhawk.py"]
CMD ["-h"]

</details>


## 🚀 Quick Start

### One-Click Installation (All Platforms)

#### **Termux (Android)**

pkg update && pkg upgrade -y && pkg install python git python-pip -y && git clone https://github.com/iaiictproject/cyberhawk.git && cd cyberhawk && pip install -r requirements.txt && chmod +x cyberhawk.py && python cyberhawk.py -h


#### **Linux (Ubuntu/Debian/Kali)**
sudo apt update && sudo apt upgrade -y && sudo apt install python3 python3-pip git -y && git clone https://github.com/iaiictproject/cyberhawk.git && cd cyberhawk && pip3 install -r requirements.txt && chmod +x cyberhawk.py && python3 cyberhawk.py -h


#### **Windows (PowerShell)**
git clone https://github.com/iaiictproject/cyberhawk.git; cd cyberhawk; pip install -r requirements.txt; python cyberhawk.py -h

## 🛠️ Usage

### Basic Syntax


python cyberhawk.py -t <target> [options]


### Available Options

| Option | Description | Example |
|--------|-------------|---------|
| `-t, --target` | Target domain | `-t example.com` |
| `--threads` | Number of threads (default: 50) | `--threads 100` |
| `--basic` | Run basic reconnaissance | `--basic` |
| `--ports` | Perform port scanning | `--ports` |
| `--subdomains` | Discover subdomains | `--subdomains` |
| `--crawl` | Web crawl for hidden paths | `--crawl` |
| `--vulns` | Scan for vulnerabilities | `--vulns` |
| `--tech` | Detect technology stack | `--tech` |
| `--all` | Run all modules | `--all` |
| `-h, --help` | Show help menu | `-h` |



## 📊 Examples

### 🎯 Basic Reconnaissance


python cyberhawk.py -t example.com --basic


### 🎯 Complete Reconnaissance


python cyberhawk.py -t example.com --all

### 🎯 Custom Thread Count


python cyberhawk.py -t example.com --all --threads 100


### 🎯 Subdomain Discovery Only


python cyberhawk.py -t example.com --subdomains


### 🎯 Vulnerability Assessment


python cyberhawk.py -t example.com --vulns


### 🎯 Technology Fingerprinting


python cyberhawk.py -t example.com --tech


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

### 📜 Usage Policy

1. **Only use on targets you own or have explicit permission to test**
2. **Do not use for illegal activities**
3. **Respect privacy and data protection laws**
4. **Use responsibly and ethically**



## 🤝 Contributing

We welcome contributions! Here's how you can help:

### Development Process

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request`

### Development Guidelines

- ✅ Follow PEP 8 style guide
- ✅ Add comments for complex logic
- ✅ Update documentation for new features
- ✅ Test thoroughly before submitting
- ✅ Write meaningful commit messages

### 🐛 Report Issues

Found a bug? [Open an issue](https://github.com/iaiictproject/cyberhawk/issues) with:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- System information



## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.


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




## 🙏 Acknowledgments

- IAIICT Project DCT Project Group 10
- Open-source security community
- All contributors and testers
- HackerTarget API for subdomain discovery


## 📞 Contact & Support

### 📧 Email
- **Project Team**: project.dct@iaiict.edu
- **Support**: support@iaiict.edu

### 🌐 Social Links
- **GitHub**: [@iaiictproject](https://github.com/iaiictproject)
- **Twitter**: [@IAIICT](https://twitter.com/IAIICT)
- **Website**: [www.iaiict.edu](https://www.iaiict.edu)

### 💬 Community
- Join our [Discord Server](https://discord.gg/cyberhawk)
- Follow on [LinkedIn](https://linkedin.com/company/iaiict)



## 📚 Documentation

- [User Guide](docs/USER_GUIDE.md)
- [API Reference](docs/API.md)
- [FAQ](docs/FAQ.md)
- [Contributing Guide](CONTRIBUTING.md)


## 📊 Project Stats

![GitHub contributors](https://img.shields.io/github/contributors/iaiictproject/cyberhawk)
![GitHub last commit](https://img.shields.io/github/last-commit/iaiictproject/cyberhawk)
![GitHub issues](https://img.shields.io/github/issues/iaiictproject/cyberhawk)
![GitHub pull requests](https://img.shields.io/github/issues-pr/iaiictproject/cyberhawk)



<div align="center">
  <sub>Built with ❤️ by IAIICT PROJECT DCT PROJECT GROUP 10</sub>
  <br>
  <sub>⭐ Star this repo if you find it useful! ⭐</sub>
</div>



## 📁 Additional Files

### **requirements.txt**

requests>=2.28.0
colorama>=0.4.6
urllib3>=1.26.0


### **install.sh** (Linux/Termux One-Click Installer)
#!/bin/bash

# CyberHawk Installer Script
# Auto-detects platform (Linux/Termux)

echo "🦅 CyberHawk Recon Installer"
echo "=============================="
echo ""

# Detect platform
if [ -d "$PREFIX" ]; then
    # Termux
    echo "📱 Detected: Termux (Android)"
    pkg update && pkg upgrade -y
    pkg install python git python-pip -y
else
    # Linux
    echo "🐧 Detected: Linux"
    sudo apt update && sudo apt upgrade -y
    sudo apt install python3 python3-pip git -y
fi

echo ""
echo "📦 Cloning repository..."
git clone https://github.com/iaiictproject/cyberhawk.git

cd cyberhawk

echo "📥 Installing dependencies..."
if [ -d "$PREFIX" ]; then
    pip install -r requirements.txt
else
    pip3 install -r requirements.txt
fi

echo "🔧 Setting permissions..."
chmod +x cyberhawk.py

echo ""
echo "✅ CyberHawk installed successfully!"
echo ""
echo "🚀 Quick start:"
echo "  python cyberhawk.py -t example.com --all"
echo ""
echo "📖 Help:"
echo "  python cyberhawk.py -h"


### **install.bat** (Windows Installer)
@echo off
color 0A
echo ========================================
echo    🦅 CyberHawk Recon Installer
echo ========================================
echo.

echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)

echo [OK] Python found
echo.

echo Installing Git...
where git >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Git not found!
    echo Download Git from: https://git-scm.com/download/win
    pause
)

echo Cloning repository...
git clone https://github.com/iaiictproject/cyberhawk.git
cd cyberhawk

echo Installing dependencies
pip install -r requirements.txt

echo.
echo ========================================
echo    ✅ Installation Complete!
echo ========================================
echo.
echo Quick Start:
echo   python cyberhawk.py -t example.com --all
echo.
echo Help:
echo   python cyberhawk.py -h
echo.
pause

### **Dockerfile** (Optional)
FROM python:3.9-slim

LABEL maintainer="IAIICT PROJECT DCT PROJECT GROUP 10"
LABEL version="4.0.0"
LABEL description="CyberHawk Recon - Professional Reconnaissance Tool"

RUN apt-get update && apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN git clone https://github.com/iaiictproject/cyberhawk.git .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python", "cyberhawk.py"]
CMD ["-h"]


