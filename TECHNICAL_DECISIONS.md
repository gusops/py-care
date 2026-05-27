# Technical Decisions - py-care

## Project Overview
Cross-platform Python desktop application for Windows and Mac that displays fullscreen reminder dialogs at configurable intervals to reduce screen time fatigue.

## Technology Stack

### Core Libraries
- **tkinter** (built-in): Cross-platform GUI library, suitable for simple fullscreen dialogs
  - Alternative: **PyQt5/PyQt6** - More robust but adds external dependency
  - Alternative: **customtkinter** - Modern UI but may not support true fullscreen overlay
- **configparser** or **YAML**: Configuration file management
- **threading/schedule**: For timing and background execution

### Configuration Management
**Decision: YAML configuration file**
- Rationale: More readable than .ini, easier for users to edit, supports lists naturally
- Location: `config.yaml` in project root or user config directory
- Alternative: JSON (less user-friendly) or .ini (limited structure)

### Fullscreen Dialog Implementation
**Challenge: True fullscreen overlay covering taskbar/dock**
- Windows: Use `tkinter` with `overrideredirect(True)` + `topmost` + `fullscreen` state
- Mac: Similar approach, may need different flags for covering dock and menu bar
- Need to handle multi-monitor scenarios

### Project Structure
```
py-care/
├── src/
│   ├── __init__.py
│   ├── main.py               # Entry point
│   ├── dialog.py             # Dialog window implementation
│   ├── scheduler.py          # Timing and scheduling logic
│   ├── config_manager.py     # Config file loading
│   └── tray_icon.py          # System tray integration
├── assets/
│   └── icons/                # Icon files (.ico, .png)
├── docs/                     # Centralized documentation
│   ├── architecture.md
│   └── QUICK_START.md
├── tests/                    # Unit tests
├── config.yaml               # Default configuration
├── requirements.txt
├── setup.py                  # For installation
├── README.md
├── LICENSE
└── TECHNICAL_DECISIONS.md   # This file
```

## Implementation Considerations

### 1. Dialog Display
- **Color scheme**: Black background (#000000), white text (#FFFFFF)
- **Font**: Large, readable font (e.g., Arial 24pt)
- **Dismissal**: ESC key or click to close
- **Animation**: Optional fade-in/out (keep simple)

### 2. Timing Mechanism
- Background thread or event loop
- Configurable interval in minutes
- Should not block main application

### 3. Configuration Format
```yaml
# config.yaml example
reminder:
  interval_minutes: 20
  messages:
    - "Time to take a break! Look 20 feet away for 20 seconds."
    - "Stay hydrated! Drink some water."
    - "Stretch your body. Move around for a minute."
    - "Rest your eyes. Close them for a few seconds."
  
display:
  background_color: "#000000"
  text_color: "#FFFFFF"
  font_size: 24
  dismiss_key: "Escape"
```

### 4. Platform-Specific Handling
- Detect OS using `platform.system()`
- Windows: Handle taskbar overlay
- Mac: Handle dock and menu bar overlay
- Different window manager behaviors

### 5. Auto-Start Options
- Windows: Startup folder or registry entry
- Mac: Login items
- Provide helper script for setup

## Development Tools

### VS Code Extensions (Recommended)
1. **Python** (Microsoft) - Essential Python support
2. **Pylance** (Microsoft) - Fast language server
3. **Python Debugger** (Microsoft) - Debugging support
4. **autoDocstring** - Generate docstrings
5. **Python Indent** - Correct indentation
6. **YAML** - YAML file support
7. **GitLens** - Enhanced Git integration
8. **Black Formatter** - Code formatting
9. **Ruff** - Fast Python linter

## Requirements Finalized

### 1. User Interaction ✓
- ✅ Dialog auto-dismisses after configurable duration (in YAML)
- ✅ No snooze functionality
- ✅ No pause functionality
- ✅ ESC, SPACE, or click to manually dismiss

### 2. Message Display ✓
- ✅ Messages shown in sequence (not random)
- ✅ One message per reminder
- ✅ Include current date/time in 24-hour format on dialog
- ✅ Format: YYYY-MM-DD HH:MM:SS

### 3. System Tray Integration ✓
- ✅ App runs in system tray
- ✅ Tray icon with Exit button
- ✅ Icon format: .ICO preferred (Windows), .PNG also supported
- ✅ Recommended sizes: 16x16, 32x32, 64x64 in one .ico file

### 4. Timing Behavior ✓
- ✅ No timer reset on wake from sleep
- ✅ No idle time detection
- ✅ No quiet hours feature

### 5. Customization ✓
- ✅ Configuration via YAML file only (no GUI editor)
- ✅ Single profile (no multiple profiles)

### 6. Additional Features
- ❌ No sound notifications (visual only)
- ✅ Font size configurable in YAML
- ✅ Colors configurable in YAML

### 7. Logging
- ✅ Console logging of reminder times
- ❌ No analytics or tracking

## Next Steps
1. Clarify open questions with user
2. Create initial project structure
3. Implement basic dialog with tkinter
4. Add configuration management
5. Implement scheduling system
6. Test on both Windows and Mac
7. Add auto-start capability
8. Package for distribution

---

## 2026 Project State Updates

- **Dialog Dismissal:** Only auto-dismiss and OS-level close (Alt+F4/tab away) are supported. No explicit close/dismiss instructions are shown in the dialog.
- **Locale-Aware Date/Time:** Dialogs display the current date and time using the system's locale (e.g., "27 de mayo de 2026" for Spanish, "May 27th 2026" for English).
- **.gitignore Policy:** The `dist/` folder is tracked for user downloads. `logs/`, `.venv/`, `.vscode/`, and `build/py-care-windows/` are ignored and not tracked.
- **Config File Flexibility:** Messages can be defined at the root or under `reminder` in `config.yaml`.

---
