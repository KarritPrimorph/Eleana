#!/bin/bash
set -e
set -o pipefail

# ============================================
# Eleana build script - Linux version
# ============================================

# --- Python version check ---
PYTHON_BIN=$(command -v python3)

if [ -z "$PYTHON_BIN" ]; then
    echo "ERROR: python3 not found"
    exit 1
fi

PY_VERSION=$($PYTHON_BIN - <<'EOF'
import sys
print(f"{sys.version_info.major}.{sys.version_info.minor}")
EOF
)

REQUIRED_MIN="3.11"

verlte() { printf '%s\n%s' "$1" "$2" | sort -V | head -n1; }

if [ "$(verlte "$PY_VERSION" "$REQUIRED_MIN")" != "$REQUIRED_MIN" ]; then
    echo "ERROR: Python >= $REQUIRED_MIN required, found $PY_VERSION"
    exit 1
fi

echo "==> Using Python $PY_VERSION at $PYTHON_BIN"

# --- CONFIG ---
PROJECT_SRC=../
PROJECT_DST=/tmp/eleana_pyinstaller
VENV_DIR=/tmp/eleana_venv

# --- STEP 0: Remove old copy and make fresh copy ---
echo "==> Copying project..."
rm -rf "$PROJECT_DST"
cp -R "$PROJECT_SRC" "$PROJECT_DST"

# --- STEP 1: Create venv ---
if [ ! -d "$VENV_DIR" ]; then
    echo "==> Creating virtual environment..."
    "$PYTHON_BIN" -m venv "$VENV_DIR"
fi

# --- STEP 2: Activate venv ---
echo "==> Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# --- STEP 3: Install build tools ---
pip install --upgrade pip
pip install pyinstaller

echo "PyInstaller path: $(which pyinstaller)"

# --- STEP 4: Install project dependencies ---
cd "$PROJECT_DST"
pip install -r requirements.txt

# --- STEP 5: Prepare for build ---
ELEANA_VERSION=$(grep -Po 'ELEANA_VERSION\s*=\s*\K[0-9.]+' main.py)

if [ -z "$ELEANA_VERSION" ]; then
    echo "ERROR: ELEANA_VERSION not found in main.py"
    exit 1
fi

DIST_NAME="Eleana_${ELEANA_VERSION}"

rm -rf build dist *.spec

# Backup original main.py
cp main.py main.py.bak

# Set DEVEL = False
sed -i 's/^\s*DEVEL\s*=\s*True\s*$/DEVEL = False/' main.py

# Rename entrypoint
mv main.py eleana.py

# --- STEP 6: Build with PyInstaller ---
echo "==> Building package..."
pyinstaller eleana.py \
  --name "$DIST_NAME" \
  --clean \
  --noconfirm \
  --onedir \
  --hidden-import=customtkinter \
  --hidden-import=pygubu.plugins.customtkinter \
  --hidden-import=PIL._tkinter_finder \
  --add-data "assets:assets" \
  --add-data "modules:modules" \
  --add-data "subprogs:subprogs" \
  --add-data "pixmaps:pixmaps" \
  --add-data "widgets:widgets"

# --- STEP 7: Fix executable name ---
cd "dist/$DIST_NAME"
mv "$DIST_NAME" eleanapy
chmod +x eleanapy
echo "==> Executable renamed to 'eleanapy'"

# --- STEP 8: Move build to HOME ---
cd ..
rm -rf ~/eleanapy
mv "$DIST_NAME" ~/eleanapy
echo "==> Built package moved to ~/eleanapy"

# --- STEP 9: Restore project state ---
cd "$PROJECT_DST"
mv main.py.bak main.py

# --- STEP 10: Cleanup ---
rm -rf "$PROJECT_DST"
rm -rf "$VENV_DIR"
echo
echo "==> Cleanup finished."
echo
echo "To create DEB package type:"
echo "./create_deb.sh"
echo
echo "To install Eleana directly to /usr/local (Generic Linux) type:"
echo "./install_generic.sh"