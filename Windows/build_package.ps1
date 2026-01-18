# --- STEP 0: Przygotuj eleana.iss z szablonu ---
$CfgPath = Join-Path $PSScriptRoot "eleana.cfg"
$IssPath = Join-Path $PSScriptRoot "eleana.iss"

Copy-Item -Path $CfgPath -Destination $IssPath -Force
Write-Host "eleana.iss copied from template eleana.cfg"



Write-Host "=== PATCHING eleana.iss ==="

$IssPath = Join-Path $PSScriptRoot "eleana.iss"

if (-not (Test-Path $IssPath)) {
    throw "eleana.iss NOT FOUND at $IssPath"
}

# --- Read version from main.py ---
$MainPyPath = Join-Path $PSScriptRoot "..\main.py"

if (-not (Test-Path $MainPyPath)) {
    throw "main.py NOT FOUND at $MainPyPath"
}

$VersionMatch = Select-String `
    -Path $MainPyPath `
    -Pattern '^\s*ELEANA_VERSION\s*=\s*([0-9.]+)'

if (-not $VersionMatch) {
    throw "ELEANA_VERSION not found in main.py"
}

$EleanaVersion = $VersionMatch.Matches[0].Groups[1].Value
Write-Host "Version detected: $EleanaVersion"

# --- Patch iss ---
$Content = Get-Content $IssPath -Raw

$NewContent = $Content -replace `
    '#define\s+EleanaVersion\s+".*?"',
    "#define EleanaVersion `"$EleanaVersion`""

#if ($Content -eq $NewContent) {
#    throw "eleana.iss was NOT modified (regex did not match)"
#}

Set-Content -Path $IssPath -Value $NewContent -Encoding UTF8

Write-Host "eleana.iss updated successfully"
Write-Host "============================"

# ============================================
# Eleana build script - Windows PowerShell
# ============================================

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# --- CONFIG ---
$ProjectSrc = Join-Path $PSScriptRoot ".."        
$ProjectDst = Join-Path $env:TEMP "eleana_pyinstaller"
$VenvDir = Join-Path $env:TEMP "eleana_venv"
$InstallDir = Join-Path $PSScriptRoot "eleanapy"

# --- STEP 0a: Patch DEVEL = False in main.py ---
$MainPySource = Join-Path $ProjectSrc "main.py"
if (Test-Path $MainPySource) {
    (Get-Content $MainPySource) |
        ForEach-Object { $_ -replace 'DEVEL\s*=\s*True', 'DEVEL = False' } |
        Set-Content $MainPySource
    Write-Host "==> Set DEVEL = False in source main.py"
} else {
    Write-Warning "main.py not found at $MainPySource"
}

# --- STEP 0b: Patch eleana.iss with version ---
$IssPath = Join-Path $PSScriptRoot "eleana.iss"
if (-not (Test-Path $IssPath)) {
    throw "eleana.iss NOT FOUND at $IssPath"
}

$VersionMatch = Select-String -Path $MainPySource -Pattern 'ELEANA_VERSION\s*=\s*([0-9.]+)'
if (-not $VersionMatch) { throw "ELEANA_VERSION not found in main.py" }

$EleanaVersion = $VersionMatch.Matches[0].Groups[1].Value
Write-Host "Version detected: $EleanaVersion"

$Content = Get-Content $IssPath -Raw
$NewContent = $Content -replace '#define\s+EleanaVersion\s+".*?"', "#define EleanaVersion `"$EleanaVersion`""
#if ($Content -eq $NewContent) { throw "eleana.iss was NOT modified (regex did not match)" }

Set-Content -Path $IssPath -Value $NewContent -Encoding UTF8
Write-Host "eleana.iss updated successfully"
Write-Host "============================"

# --- STEP 1: Remove old copy and make fresh copy ---
Write-Host "==> Copying project..."
if (Test-Path $ProjectDst) { Remove-Item -Recurse -Force $ProjectDst -ErrorAction SilentlyContinue }
Copy-Item -Recurse $ProjectSrc $ProjectDst

# --- STEP 2: Create virtual environment ---
if (-Not (Test-Path $VenvDir)) {
    Write-Host "==> Creating virtual environment..."
    python -m venv $VenvDir
}

# --- STEP 3: Activate venv ---
$VenvActivate = Join-Path $VenvDir "Scripts\Activate.ps1"
Write-Host "==> Activating virtual environment..."
. $VenvActivate

# --- STEP 4: Upgrade pip and install PyInstaller ---
Write-Host "==> Installing build tools..."
python -m pip install --upgrade pip
pip install pyinstaller

# --- STEP 5: Install project dependencies ---
Write-Host "==> Installing project dependencies..."
Set-Location $ProjectDst
pip install -r requirements.txt

# --- STEP 6: Backup main.py and rename for PyInstaller ---
Copy-Item main.py main.py.bak -Force
Rename-Item main.py eleana.py -Force

# --- STEP 7: Build with PyInstaller ---
$DistName = "Eleana_$EleanaVersion"
Write-Host "==> Building package with PyInstaller..."

$PyInstallerArgs = @(
    "eleana.py"

    "--name", $DistName
    "--clean"
    "--noconfirm"
    "--onedir"
    "--windowed"
    "--icon", "$PSScriptRoot\eleanapy.ico"

    # === collect-all +==
    "--collect-all", "numpy"
    "--collect-all", "scipy"
    "--collect-all", "lmfit"
    "--collect-all", "pygubu"

    # === hidden imports ===
    "--hidden-import", "scipy.special._cdflib"
    "--hidden-import", "customtkinter"
    "--hidden-import", "pygubu.plugins.customtkinter"
    "--hidden-import", "pygubu.plugins.pygubu.flodgauge_bo"
    "--hidden-import", "PIL._tkinter_finder"
    "--hidden-import", "numexpr"
    "--hidden-import", "sympy.utilities.lambdify"

    # === App data ===
    "--add-data", "assets;assets"
    "--add-data", "modules;modules"
    "--add-data", "subprogs;subprogs"
    "--add-data", "pixmaps;pixmaps"
    "--add-data", "widgets;widgets"
)

pyinstaller @PyInstallerArgs


# --- STEP 8: Rename executable ---
$DistPath = Join-Path $ProjectDst "dist\$DistName"
$ExeSrc = Join-Path $DistPath "$DistName.exe"
$ExeDst = Join-Path $DistPath "eleanapy.exe"
Rename-Item $ExeSrc $ExeDst -Force
Write-Host "==> Executable renamed to 'eleanapy.exe'"

# --- STEP 9: Move build to $InstallDir ---
if (Test-Path $InstallDir) { Remove-Item -Recurse -Force $InstallDir -ErrorAction SilentlyContinue }
Move-Item $DistPath $InstallDir
Write-Host "==> Built package moved to $InstallDir"

# --- STEP 10: Restore project state ---
Set-Location $ProjectDst
Rename-Item eleana.py main.py -Force
Move-Item main.py.bak main.py -Force

# --- STEP 11: Cleanup ---
Set-Location $PSScriptRoot
Start-Sleep -Seconds 1
Remove-Item -Recurse -Force $ProjectDst -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force $VenvDir -ErrorAction SilentlyContinue

Write-Host ""
Write-Host "==> Cleanup finished."
Write-Host ""
Write-Host "Executable is ready at: $InstallDir\eleanapy.exe"
Write-Host "==> Trying to complie the package using Inno Setup 6"

# Path to compiler
$ISCC = "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"

# Path to eleana.iss
$ISSFile = Join-Path $PSScriptRoot "eleana.iss"

# Compile
& "$ISCC" "$ISSFile"

Write-Host "Compilaton successful. Please find the installation package in ./Output directory."
 
