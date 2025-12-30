#!/bin/bash
set -e
set -o pipefail

# ============================================
# Eleana DEB package builder
# ============================================

APP_NAME="eleanapy"
SRC_DIR="$HOME/eleanapy"
MAIN_PY="../main.py"

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

echo "==> Found Eleana build in $SRC_DIR"

# --- STEP 1: Detect version from main.py ---
if [ ! -f "$MAIN_PY" ]; then
    echo "WARNING: $MAIN_PY not found, using default version 1.0.0"
    ELEANA_VERSION="1.0.0"
else
    ELEANA_VERSION=$(grep -Po 'ELEANA_VERSION\s*=\s*\K[0-9.]+' "$MAIN_PY")
    if [ -z "$ELEANA_VERSION" ]; then
        echo "WARNING: ELEANA_VERSION not found in $MAIN_PY, using 1.0.0"
        ELEANA_VERSION="1.0.0"
    fi
fi

echo "==> Using Eleana version: $ELEANA_VERSION"

# --- STEP 2: Prepare package structure ---
PKGROOT="$(pwd)/${APP_NAME}-deb"
rm -rf "$PKGROOT"
mkdir -p "$PKGROOT"/{DEBIAN,usr/lib/$APP_NAME,usr/bin}

# --- STEP 3: Copy entire application dynamically ---
cp -r "$SRC_DIR"/* "$PKGROOT/usr/lib/$APP_NAME/"

# --- STEP 4: Create symlink to binary ---
ln -sf /usr/lib/$APP_NAME/$APP_NAME "$PKGROOT/usr/bin/$APP_NAME"

# --- STEP 5: Create DEBIAN/control file ---
cat > "$PKGROOT/DEBIAN/control" <<EOF
Package: $APP_NAME
Version: $ELEANA_VERSION
Section: science
Priority: optional
Architecture: amd64
Depends: libc6, libx11-6, libglib2.0-0
Maintainer: Your Name <you@email>
Description: Eleana - EPR data analysis tool
 Scientific application for EPR data analysis and simulation.
EOF

# --- STEP 6: Set permissions ---
chmod 755 "$PKGROOT/DEBIAN"
chmod 644 "$PKGROOT/DEBIAN/control"
chmod -R 755 "$PKGROOT/usr"
chmod +x "$PKGROOT/usr/lib/$APP_NAME/$APP_NAME"

# --- STEP 7: Build DEB package ---
dpkg-deb --build "$PKGROOT"
DEB_NAME="${APP_NAME}_${ELEANA_VERSION}_amd64.deb"
mv "$PKGROOT.deb" "$DEB_NAME"
rm -rf eleanapy-deb

echo "==> DEB package created: $DEB_NAME"
echo "You can install it with: sudo dpkg -i $DEB_NAME"
echo "To remove pyinstaller package type:"
echo "rm -rf ~/eleanapy"

