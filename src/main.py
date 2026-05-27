"""
Main entry point for GusOps PyCare application.
"""

import sys
import os
import threading
from pathlib import Path
from typing import Optional

# Add src directory to path for PyInstaller compatibility
if getattr(sys, 'frozen', False):
    # Running in PyInstaller bundle
    bundle_dir = Path(sys._MEIPASS)
    sys.path.insert(0, str(bundle_dir))
else:
    # Running in development
    src_dir = Path(__file__).parent
    sys.path.insert(0, str(src_dir))

# Import modules - direct imports work after path adjustment
from logger import logger
from config_manager import ConfigManager
from scheduler import ReminderScheduler
from dialog import ReminderDialog
from tray_icon import TrayIcon


class PyCareApp:
    """Main application class for GusOps PyCare."""
    
    def __init__(self):
        """Initialize the application."""
        self.config_manager: Optional[ConfigManager] = None
        self.scheduler: Optional[ReminderScheduler] = None
        self.tray_icon: Optional[TrayIcon] = None
        self.running = False
    
    def run(self) -> None:
        """Run the application."""
        logger.info("=" * 50)
        logger.info("GusOps PyCare - Screen Time Reminder")
        logger.info("=" * 50)
        
        try:
            # Load configuration
            logger.info("Loading configuration...")
            self.config_manager = ConfigManager()
            
            # Display configuration summary
            self._print_config_summary()
            
            # Initialize scheduler
            interval = self.config_manager.get_interval_seconds()
            messages = self.config_manager.get_messages()
            self.scheduler = ReminderScheduler(
                interval_seconds=interval,
                messages=messages,
                callback=self._show_reminder
            )
            
            # Start scheduler
            self.scheduler.start()
            self.running = True
            
            # Create and run system tray icon (blocking)
            logger.info("Starting system tray icon...")
            logger.info("Right-click the tray icon and select 'Exit' to quit.")
            logger.info("-" * 50)
            
            self.tray_icon = TrayIcon(on_exit=self._on_exit)
            self.tray_icon.create_icon()  # Blocks until exit
            
        except KeyboardInterrupt:
            logger.info("\nReceived interrupt signal.")
            self._shutdown()
        except Exception as e:
            logger.error(f"Error: {e}", exc_info=True)
            self._shutdown()
            sys.exit(1)
    
    def _print_config_summary(self) -> None:
        """Print configuration summary to console."""
        interval_min = self.config_manager.get_interval_minutes()
        duration_sec = self.config_manager.get_display_duration()
        messages = self.config_manager.get_messages()
        
        print(f"\nConfiguration:")
        print(f"  Reminder interval: {interval_min} minutes")
        print(f"  Display duration: {duration_sec} seconds")
        print(f"  Number of messages: {len(messages)}")
        print(f"  Messages will be shown in sequence.\n")
    
    def _show_reminder(self, message: str) -> None:
        """
        Show a reminder dialog.
        
        Args:
            message: The message to display
        """
        logger.info(f"_show_reminder called with message: {message[:50]}...")
        # Get display config and duration
        display_config = self.config_manager.get_display_config()
        duration = self.config_manager.get_display_duration()
        
        # Create and show dialog in main thread
        # Note: This runs synchronously and blocks until dismissed
        try:
            dialog = ReminderDialog(message, display_config, duration)
            dialog.show()
            logger.info("Dialog show() method returned")
        except Exception as e:
            logger.error(f"Error creating/showing dialog: {e}", exc_info=True)
    
    def _on_exit(self) -> None:
        """Handle application exit."""
        self._shutdown()
    
        logger.info("\nShutting down GusOps PyCare...")
        self.running = False
        
        # Stop scheduler
        if self.scheduler:
            self.scheduler.stop()
        
        # Stop tray icon
        if self.tray_icon:
            self.tray_icon.stop()
        
        logger.info("Goodbye!")
        # Stop tray icon
        if self.tray_icon:
            self.tray_icon.stop()
        
        print("Goodbye!")


def main():
    """Entry point for the application."""
    app = PyCareApp()
    app.run()


if __name__ == '__main__':
    main()
