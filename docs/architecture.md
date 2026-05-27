# py-care Architecture

## System Architecture

### Component Overview

```
┌─────────────────────────────────────────────────┐
│                   main.py                       │
│            (Application Entry Point)            │
└─────────────────┬───────────────────────────────┘
                  │
                  ├──────────────┬──────────────┬────────────────┐
                  │              │              │                │
         ┌────────▼────────┐ ┌──▼────────┐ ┌──▼───────────┐ ┌─▼─────────┐
         │ config_manager  │ │ scheduler │ │   dialog     │ │ tray_icon │
         │                 │ │           │ │              │ │ (optional)│
         └────────┬────────┘ └──┬────────┘ └──────────────┘ └───────────┘
                  │              │
         ┌────────▼────────┐    │
         │   config.yaml   │    │
         └─────────────────┘    │
                                │
                         (Timer Thread)
```

## Module Responsibilities

### main.py
- Application initialization
- Command-line argument parsing
- OS detection and platform-specific setup
- Event loop management
- Graceful shutdown handling

### config_manager.py
- Load and parse YAML configuration
- Validate configuration values
- Provide default values
- Watch for config file changes (optional)
- Handle configuration errors gracefully

### scheduler.py
- Background timing thread
- Calculate next reminder time
- Handle system sleep/wake events
- Idle time detection (optional)
- Trigger dialog display at intervals

### dialog.py
- Create fullscreen overlay window
- Display messages with styling
- Handle keyboard/mouse input for dismissal
- Platform-specific fullscreen implementation
- Multi-monitor support

### tray_icon.py (Optional)
- System tray integration
- Menu for pause/resume/settings/quit
- Status indicators

## Data Flow

1. **Startup**:
   - main.py loads config via config_manager
   - Scheduler initialized with interval from config
   - System tray icon created (if enabled)

2. **Runtime**:
   - Scheduler runs in background thread
   - When interval elapsed, scheduler triggers dialog
   - Dialog selects message from config list
   - Dialog displays fullscreen overlay
   - User dismisses dialog
   - Scheduler resets timer

3. **Shutdown**:
   - User quits via tray icon or keyboard shortcut
   - Scheduler thread stops gracefully
   - Resources cleaned up

## Platform-Specific Considerations

### Windows
- Use `win32gui` (pywin32) or tkinter's built-in methods
- Handle taskbar overlay with topmost flag
- Startup: Create shortcut in `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`

### macOS
- Handle dock and menu bar with NSWindow properties
- May need PyObjC for full control
- Startup: Create plist in `~/Library/LaunchAgents`

## Threading Model

- **Main Thread**: GUI event loop (tkinter)
- **Scheduler Thread**: Timer and scheduling logic
- **Communication**: Queue or Event for thread-safe dialog triggering

## Error Handling

- Invalid config: Use defaults and log warning
- Display errors: Fallback to simpler dialog
- Platform-specific errors: Graceful degradation
- Logging to file for debugging

## Future Enhancements

- GUI config editor
- Statistics tracking (reminders shown, completion rate)
- Custom sound notifications
- Reminder profiles for different times of day
- Integration with calendar/meeting apps (skip reminders during meetings)
