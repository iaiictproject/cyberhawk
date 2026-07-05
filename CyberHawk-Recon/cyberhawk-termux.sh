#!/data/data/com.termux/files/usr/bin/bash
# CyberHawk Recon - Termux Launcher
# Authors: IAIICT PROJECT DCT PROJECT GROUP 10

echo -e "\033[0;36m"
echo "╔═══════════════════════════════════════════════════════════════╗"
echo "║     CyberHawk Recon - Termux Edition                         ║"
echo "║     Professional Reconnaissance Tool                         ║"
echo "╚═══════════════════════════════════════════════════════════════╝"
echo -e "\033[0m"

# Check if python is installed
if ! command -v python &> /dev/null; then
    echo "[!] Python not found. Installing..."
    pkg install python -y
fi

# Run the tool
python cyberhawk.py "$@"
