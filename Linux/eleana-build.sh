#!/bin/bash
set -e  # exit on error
set -o pipefail

# ============================================
# Eleana build script - Linux version
# ============================================

# --- CONFIG ---
PROJECT_SRC=~/PycharmProjects/Eleana
PROJECT_DST=~/Eleana
VENV_DIR=~/venvs/eleana

# --- STEP 0: Remove old copy and make fresh copy ---
echo "==> Copying project..."
rm -rf "$PROJECT_DST"
cp -R "$PROJECT_SRC" "$PROJECT_DST"

# --- STEP 1: Create venv if not exists ---
if [ ! -d "$VENV_DIR" ]; then
    echo "==> Creating virtual environment..."
    python3.12 -m venv "$VENV_DIR"
fi

# --- STEP 2: Activate venv ---
echo "==> Activating virtual environment..."
source "$VENV_DIR/bin/activate"

# --- STEP 3: Check Python & pip ---
echo "Python path: $(which python)"
pip install --upgrade pip
pip install pyinstaller

echo "PyInstaller path: $(which pyinstaller)"

# --- STEP 4: Install project dependencies ---
cd "$PROJECT_DST"
pip install -r requirements.txt

# --- STEP 5: Test application ---
echo "==> Testing application..."
python ./main.py || echo "Warning: application did not exit cleanly, but continuing..."

# --- STEP 6: Prepare for build ---
ELEANA_VERSION=$(grep -Po 'ELEANA_VERSION\s*=\s*\K[0-9.]+' main.py)
DIST_NAME="Eleana_${ELEANA_VERSION}"

# Clean old build
rm -rf build dist *.spec

# Backup original main.py
cp main.py main.py.bak

# Set DEVEL = False
sed -i 's/DEVEL = True/DEVEL = False/' main.py

# Rename main.py to eleana.py
mv main.py eleana.py

# --- STEP 7: Run PyInstaller ---
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

# --- STEP 8: Test build ---
cd "dist/$DIST_NAME"
echo "==> Testing built application..."
./"$DIST_NAME" || echo "Warning: built application did not exit cleanly."

# --- STEP 9: Rename package folder ---
cd ..
mv "$DIST_NAME" eleana

# --- STEP 10: Restore original main.py ---
cd "$PROJECT_DST"
mv main.py.bak main.py

echo "==> Build finished. Package folder: $PROJECT_DST/dist/eleana"
