#!/bin/bash
set -e
set -o pipefail

# ============================================
# Eleana Installer for Generic Linux distribution
# ============================================

APP_NAME="eleanapy"
SRC_DIR="$HOME/eleanapy"
MAIN_PY="../eleanapy"

# --- STEP 0: Check if build exists ---
if [ ! -d "$SRC_DIR" ] || [ ! -x "$SRC_DIR/$APP_NAME" ]; then
    echo "WARNING: Directory $SRC_DIR or executable $APP_NAME not found."
    echo "You must first run build_package.sh to create the Eleana build."

    read -p "Do you want to run build_package.sh now? [y/N]: " run_build
    if [[ "$run_build" =~ ^[Yy]$ ]]; then
        if [ ! -f "./build_package.sh" ]; then
            echo "ERROR: ./build_package.sh not found. Cannot build."
            exit 1
        fi
        echo "==> Running build_package.sh..."
        bash ./build_package.sh
        echo "==> Build finished. Continuing DEB creation..."
    else
        echo "Exiting. Please run build_package.sh first."
        exit 1
    fi
fi


read -p "Do you want to install Eleana system-wide in /usr/local? [y/N]: " install_sys
if [[ "$install_sys" =~ ^[Yy]$ ]]; then
    echo "==> Installing Eleana system-wide..."

    sudo rm -rf /usr/local/eleanapy
    sudo cp -r ~/eleanapy /usr/local/eleanapy
    sudo ln -sf /usr/local/eleanapy/eleanapy /usr/local/bin/eleanapy
    sudo chmod +x /usr/local/eleanapy/eleanapy

    echo "==> Eleana installed. Run with: eleanapy"
else
    echo "==> System installation skipped."
fi
