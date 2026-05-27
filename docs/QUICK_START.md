# Quick Start Guide

## First Time Setup

### 1. Install Dependencies

Open a terminal in the project directory and run:

```powershell
# Windows (PowerShell)
pip install -r requirements.txt
```

```bash
# macOS/Linux
pip3 install -r requirements.txt
```

### 2. Verify Installation

Check that all packages are installed:

```powershell
pip list | Select-String -Pattern "PyYAML|pystray|Pillow"
```

You should see:
- PyYAML (version 6.0.1 or higher)
- pystray (version 0.19.5 or higher)
- Pillow (version 10.0.0 or higher)

### 3. Test Configuration

The default `config.yaml` is already set up with:
- Reminders every **20 minutes**
- Auto-dismiss after **10 seconds**
- 6 pre-configured messages

To customize, edit `config.yaml` before running.

### 4. Run the Application

```powershell
# From project root
python src/main.py
```

### 5. Using the App

**System Tray**:
- Look for the py-care icon in your system tray (bottom-right on Windows)
- Right-click the icon → "Exit" to quit

**When Reminder Appears**:
- Fullscreen black dialog with white text
- Shows current date/time (24-hour format)
- Displays one message from your sequence
- Auto-dismisses after 10 seconds (configurable)
- Or press ESC, SPACE, or click to dismiss immediately

## Customization Examples

### Change Reminder Frequency

Edit `config.yaml`:

```yaml
reminder:
  interval_minutes: 30  # Change from 20 to 30 minutes
```

### Change Auto-Dismiss Duration

```yaml
reminder:
  display_duration_seconds: 15  # Change from 10 to 15 seconds
```

### Add Your Own Messages

```yaml
reminder:
  messages:
    - "Time for a coffee break!"
    - "Check your posture - are you slouching?"
    - "Blink your eyes 10 times slowly"
    - "Stand up and stretch for 30 seconds"
```

### Change Text Size

```yaml
display:
  font_size: 40  # Larger text (default is 32)
```

### Change Colors

```yaml
display:
  background_color: "#1a1a1a"  # Dark gray instead of black
  text_color: "#00ff00"        # Green text instead of white
```

## Troubleshooting

### "Module not found" error

```powershell
pip install --upgrade -r requirements.txt
```

### Reminder doesn't cover taskbar (Windows)

This is expected behavior in some Windows security configurations. The app uses maximum available permissions for standard Python applications.

### Can't see tray icon

- Check if tray icons are hidden
- Windows: Click the up arrow (^) in system tray
- Look for the blue circle icon with "C"

### Config changes not applied

- Stop the app (right-click tray icon → Exit)
- Edit config.yaml
- Start the app again

### Application crashes on start

Check the terminal output for error messages. Common issues:
- Invalid YAML syntax in config.yaml
- Missing dependencies
- Python version < 3.8

## Running on Startup (Optional)

### Windows

1. Create a shortcut to the app:
   ```powershell
   # In project directory
   $WshShell = New-Object -ComObject WScript.Shell
   $Shortcut = $WshShell.CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\py-care.lnk")
   $Shortcut.TargetPath = "pythonw.exe"
   $Shortcut.Arguments = "$PWD\src\main.py"
   $Shortcut.WorkingDirectory = "$PWD"
   $Shortcut.Save()
   ```

2. The app will now start automatically when you log in

### macOS

1. Open System Preferences → Users & Groups
2. Click Login Items
3. Click + and add Python or create a startup script

## Next Steps

- Test the first reminder (default: 20 minutes)
- Adjust timing and messages to your preference
- Consider adding custom icons (see [../README.md](../README.md) and [../assets/icons/README.md](../assets/icons/README.md))
- Share feedback or contribute improvements!

---

**Need help?** Check the main [README.md](../README.md) or [TECHNICAL_DECISIONS.md](../TECHNICAL_DECISIONS.md)
