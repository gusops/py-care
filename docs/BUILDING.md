# Building Distributable Executables

This guide explains how to build distributable executables for Windows and macOS using PyInstaller.

## Overview

py-care uses **PyInstaller** to create standalone executables that include:
- ✅ All Python dependencies
- ✅ Default config.yaml file
- ✅ Application icons
- ✅ No Python installation required by users

### Config File Priority

The app automatically searches for config files in this order:
1. **Next to executable** (highest priority) - `./config.yaml`
2. **User home directory** - `~/.py-care/config.yaml`
3. **Bundled default** - Built into the executable
4. **Hard-coded defaults** - Last resort fallback

Users can place their customized `config.yaml` next to the executable to override defaults.

## Prerequisites

### Install Build Dependencies

```powershell
# Windows (PowerShell)
pip install -r requirements-build.txt
```

```bash
# macOS/Linux
pip3 install -r requirements-build.txt
```

This installs PyInstaller and other packaging tools.

## Building for Windows

### Automated Build (Recommended)

```powershell
# Run the build script
.\build\build-windows.ps1
```

This script will:
1. Check for PyInstaller
2. Clean previous builds
3. Build the executable
4. Organize files in `dist/windows/`
5. Copy config file
6. Display results

### Manual Build

```powershell
# Clean previous builds
Remove-Item -Recurse -Force build, dist

# Build with PyInstaller
pyinstaller py-care-windows.spec --clean --noconfirm

# Organize distribution
New-Item -ItemType Directory -Path "dist\windows" -Force
Move-Item -Path "dist\py-care" -Destination "dist\windows\"
Copy-Item -Path "config.yaml" -Destination "dist\windows\py-care\"
```

### Output Structure

```
dist/
└── windows/
    └── py-care/
        ├── py-care.exe         # Main executable
        ├── config.yaml         # Default config (user can edit)
        ├── assets/             # Icons
        └── (dependencies)      # DLLs and libraries
```

### Testing Windows Build

```powershell
cd dist\windows\py-care
.\py-care.exe
```

## Building for macOS

### Automated Build (Recommended)

```bash
# Make script executable
chmod +x build/build-macos.sh

# Run the build script
./build/build-macos.sh
```

### Manual Build

```bash
# Clean previous builds
rm -rf build dist

# Build with PyInstaller
pyinstaller py-care-macos.spec --clean --noconfirm

# Organize distribution
mkdir -p dist/macos
mv dist/py-care.app dist/macos/
cp config.yaml dist/macos/
```

### Output Structure

```
dist/
└── macos/
    ├── py-care.app         # macOS application bundle
    └── config.yaml         # Default config (user can edit)
```

### Testing macOS Build

```bash
open dist/macos/py-care.app
```

## Distribution

### Windows

#### Option 1: Zip Distribution
```powershell
# Create zip file
Compress-Archive -Path "dist\windows\py-care" -DestinationPath "py-care-windows.zip"
```

Users can:
1. Extract the zip
2. Edit `config.yaml` to customize
3. Run `py-care.exe`
4. (Optional) Create shortcut in Startup folder

#### Option 2: Installer (Advanced)
Use **Inno Setup** to create a proper Windows installer:
1. Install [Inno Setup](https://jrsoftware.org/isinfo.php)
2. Create `.iss` script
3. Package `dist/windows/py-care/` folder

### macOS

#### Option 1: Zip Distribution
```bash
# Create zip
cd dist/macos
zip -r py-care-macos.zip py-care.app config.yaml
```

#### Option 2: DMG Installer (Recommended)
```bash
# Install create-dmg
brew install create-dmg

# Create DMG
create-dmg \
  --volname "py-care" \
  --window-pos 200 120 \
  --window-size 600 400 \
  --icon-size 100 \
  --icon "py-care.app" 175 120 \
  --hide-extension "py-care.app" \
  --app-drop-link 425 120 \
  "py-care-installer.dmg" \
  "dist/macos/"
```

## Customization

### Changing Icon

1. **Windows**: Convert PNG to ICO format
   - Use online tools or `convert` command
   - Update `icon=` line in `py-care-windows.spec`

2. **macOS**: Use PNG or ICNS
   - Update `icon=` line in `py-care-macos.spec`

### Single-File Executable

To create a single-file executable instead of a folder:

Edit the .spec file and change:
```python
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,      # Add these three lines
    a.zipfiles,      # to the EXE section
    a.datas,         # (remove from COLLECT)
    exclude_binaries=False,  # Change to False
    # ... rest of config ...
)

# Remove COLLECT section entirely
```

**Trade-off**: Single file is easier to distribute but slightly slower to start.

## Troubleshooting

### "Module not found" errors
- Add missing modules to `hiddenimports` in .spec file
- Example: `hiddenimports=['missing_module']`

### Config file not found
- Ensure `config.yaml` is in `datas` section of .spec file
- Check config search logic in `src/config_manager.py`

### Large executable size
- Exclude unnecessary packages in .spec file `excludes` section
- Already excluded: matplotlib, numpy, pandas, scipy, pytest

### Antivirus false positives
- Code sign your executable (Windows: signtool, macOS: codesign)
- Submit to antivirus vendors for whitelisting

### macOS "App is damaged" message
- Remove quarantine: `xattr -cr dist/macos/py-care.app`
- Code sign the app for distribution

## Code Signing (Production)

### Windows
```powershell
# Requires code signing certificate
signtool sign /f certificate.pfx /p password /t http://timestamp.digicert.com dist\windows\py-care\py-care.exe
```

### macOS
```bash
# Requires Apple Developer account
codesign --deep --force --sign "Developer ID Application: Your Name" dist/macos/py-care.app
```

## Build Sizes

Typical sizes (approximate):
- **Windows**: 40-60 MB (folder), 30-40 MB (single file)
- **macOS**: 50-70 MB (.app bundle)

Size includes Python runtime, tkinter, and all dependencies.

## CI/CD Integration

Example GitHub Actions workflow:

```yaml
name: Build Executables
on: [push, pull_request]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt -r requirements-build.txt
      - run: .\build\build-windows.ps1
      - uses: actions/upload-artifact@v3
        with:
          name: windows-build
          path: dist/windows/

  build-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt -r requirements-build.txt
      - run: chmod +x build/build-macos.sh && ./build/build-macos.sh
      - uses: actions/upload-artifact@v3
        with:
          name: macos-build
          path: dist/macos/
```

## Next Steps

After building:
1. ✅ Test the executable thoroughly
2. ✅ Verify config file priority works correctly
3. ✅ Test on clean systems (no Python installed)
4. ✅ Create installation instructions for users
5. ✅ (Optional) Set up auto-updater
6. ✅ (Optional) Create installers (Inno Setup / DMG)
7. ✅ (Optional) Code sign for production distribution

---

**Your executables are now ready for distribution!**
