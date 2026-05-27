display:
# GusOps PyCare

Simple fullscreen reminder app for Windows and Mac.

## Features

- 🖥️ **Fullscreen Reminders**: Black screen with white text covers your entire display
- ⏰ **Customizable Intervals**: Set how often reminders appear (default: 20 minutes)
- 📝 **Sequential Messages**: Display different messages in sequence
- 🕐 **24-Hour Time Display**: Shows current date and time on each reminder
- ⚡ **Auto-Dismiss**: Reminders automatically disappear after set duration
- 🎯 **System Tray**: Runs quietly in background, exit via tray icon
- ⚙️ **YAML Configuration**: Easy-to-edit configuration file

## Usage

1. **Run the app:**
   - From source:
     ```bash
     python src/main.py
     ```
   - Or run the packaged exe from `dist/windows/py-care.exe` (Windows build).

2. **How it works:**
   - Starts in the background with a tray icon.
   - Shows fullscreen reminders at your configured interval.
   - Dismiss reminders with `ESC` or `SPACE`, or wait for auto-dismiss.
   - Right-click the tray icon and select "Exit" to quit.

## Configuration

Edit `config.yaml` to set interval, duration, messages, and appearance. Example:

```yaml
reminder:
  interval_minutes: 20
  display_duration_seconds: 10
  messages:
    - "Look away from the screen."
    - "Stretch your body."

├── assets/
  background_color: "#000000"
  text_color: "#FFFFFF"
  font_family: "Arial"
  font_size: 32
  datetime_font_size: 24
  show_datetime: true
```

## Build (Windows)

1. Create a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Build the exe:
   ```bash
   .\build\build-windows.ps1
   ```
4. Find the exe in `dist/windows/py-care.exe`.
│   └── icons/               # Icon files (.ico, .png)
├── docs/
│   ├── architecture.md      # Architecture documentation
│   └── QUICK_START.md       # Quick start guide
├── tests/                   # Unit tests
├── config.yaml              # Configuration file
├── requirements.txt         # Python dependencies
├── setup.py                 # Installation script
├── TECHNICAL_DECISIONS.md   # Technical documentation
├── README.md
└── LICENSE
```

### VS Code Extensions (Recommended)

- **Python** (ms-python.python)
- **Pylance** (ms-python.vscode-pylance)
- **Python Debugger** (ms-python.debugpy)
- **Black Formatter** (ms-python.black-formatter)
- **Ruff** (charliermarsh.ruff)
- **YAML** (redhat.vscode-yaml)

## Troubleshooting

### Dialog doesn't cover taskbar/dock
- Windows: Ensure you have appropriate window permissions
- Mac: Grant accessibility permissions to Terminal/Python in System Preferences

### Config file not loading
- Check that `config.yaml` exists in the project root
- Verify YAML syntax (use a YAML validator)
- Check console output for error messages

### Tray icon not appearing
- Ensure `pystray` and `Pillow` are installed
- Check system tray settings (hidden icons)

## Building Executables

To create distributable executables for Windows and macOS:

```powershell
# Windows
pip install -r requirements-build.txt
.\build\build-windows.ps1

# macOS
pip3 install -r requirements-build.txt
chmod +x build/build-macos.sh
./build/build-macos.sh
```

See [docs/BUILDING.md](docs/BUILDING.md) for complete build instructions.

**Distribution structure:**
- `dist/windows/py-care/` - Windows executable and dependencies
- `dist/macos/py-care.app` - macOS application bundle

Users can place their custom `config.yaml` next to the executable to override defaults.

## License

See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

---

## Project Notes (2026)

- **Dialog Dismissal:** Reminders auto-dismiss after the configured duration. No explicit close/dismiss instructions are shown. Users can use OS-level shortcuts (Alt+F4, tab away) if needed.
- **Date/Time Format:** The reminder dialog displays the current date and time using your system's locale. For example, Spanish: "27 de mayo de 2026"; English: "May 27th 2026".
- **dist/ Folder:** The `dist/` folder is tracked in the repository and contains downloadable executables and sample config files for users.
- **logs/ Folder:** The `logs/` folder is ignored and not included in the repository.
- **build/py-care-windows/:** This build artifact folder is ignored; only build scripts/specs are tracked.
- **Config File:** Messages can be defined at the root or under `reminder` in `config.yaml`.

---
