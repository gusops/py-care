# py-care

A simple desktop app for Windows and Mac to reduce screen time fatigue. Balance your digital life with reminders to hydrate, look away, and move.

## Features

- 🖥️ **Fullscreen Reminders**: Black screen with white text covers your entire display
- ⏰ **Customizable Intervals**: Set how often reminders appear (default: 20 minutes)
- 📝 **Sequential Messages**: Display different messages in sequence
- 🕐 **24-Hour Time Display**: Shows current date and time on each reminder
- ⚡ **Auto-Dismiss**: Reminders automatically disappear after set duration
- 🎯 **System Tray**: Runs quietly in background, exit via tray icon
- ⚙️ **YAML Configuration**: Easy-to-edit configuration file

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11 or macOS 10.14+

### Steps

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd py-care
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or install in development mode:
   ```bash
   pip install -e .
   ```

## Usage

### Running the Application

```bash
python src/main.py
```

Or if installed:
```bash
py-care
```

The application will:
1. Start in the background
2. Display a tray icon in your system tray
3. Show fullscreen reminders at configured intervals
4. Right-click the tray icon and select "Exit" to quit

### Dismissing Reminders

When a reminder appears, you can dismiss it by:
- Pressing `ESC`
- Pressing `SPACE`
- Clicking anywhere on the screen
- Waiting for auto-dismiss (default: 10 seconds)

## Configuration

Edit `config.yaml` in the project root to customize:

```yaml
reminder:
  interval_minutes: 20              # Time between reminders
  display_duration_seconds: 10      # Auto-dismiss after this time
  messages:
    - "Your custom message 1"
    - "Your custom message 2"
    # Add more messages...

display:
  background_color: "#000000"       # Black background
  text_color: "#FFFFFF"             # White text
  font_family: "Arial"
  font_size: 32
  show_datetime: true
  datetime_format: "%Y-%m-%d %H:%M:%S"
```

### Message Behavior

- Messages display in **sequence** (not random)
- One message per reminder
- After the last message, cycles back to the first

## Custom Tray Icon

To use a custom icon:

1. Create or download a `.ico` file (recommended for Windows)
   - Recommended: Multi-size ICO with 16x16, 32x32, 64x64 pixels
   - Alternative: PNG file (256x256 or 512x512)

2. Save your icon file in the `assets/icons/` folder

3. Update the icon loading in `src/tray_icon.py` to use your custom file

See [assets/icons/README.md](assets/icons/README.md) for detailed instructions and design guidelines.

## Development

### Project Structure

```
py-care/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config_manager.py    # Configuration loader
│   ├── scheduler.py         # Reminder timing
│   ├── dialog.py            # Fullscreen dialog
│   └── tray_icon.py         # System tray icon
├── assets/
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

**Stay healthy, stay productive! 💙**
