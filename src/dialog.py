"""
Fullscreen dialog window for displaying reminder messages.
"""

import tkinter as tk
from datetime import datetime
from typing import Dict, Any, Optional
import platform
import threading

from logger import logger


class ReminderDialog:
    """Fullscreen dialog for displaying reminder messages."""
    
    def __init__(self, message: str, display_config: Dict[str, Any], 
                 duration_seconds: float, parent: Optional[tk.Tk] = None):
        """
        Initialize the reminder dialog.
        
        Args:
            message: The reminder message to display
            display_config: Display configuration dictionary
            duration_seconds: How long to show the dialog before auto-dismiss
            parent: Parent Tk root (if None, creates new root)
        """
        self.message = message
        self.display_config = display_config
        self.duration_seconds = duration_seconds
        self.parent = parent
        self.window: Optional[tk.Toplevel] = None
        self.dismissed = False
    
    def show(self) -> None:
        """Display the fullscreen dialog (thread-safe)."""
        logger.info("Dialog show() called")
        # Create window in a thread-safe manner
        if self.parent:
            # Use parent root (thread-safe with after)
            logger.info("Using parent-based dialog (Toplevel)")
            self.parent.after(0, self._create_window)
        else:
            # Create new root and run in separate thread
            logger.info("Creating dialog in separate thread")
            thread = threading.Thread(target=self._show_in_thread, daemon=True)
            thread.start()
            logger.info(f"Dialog thread started: {thread.name}")
    
    def _show_in_thread(self) -> None:
        """Create and show dialog in a separate thread with its own Tk root."""
        try:
            logger.info("Creating Tk root in dialog thread...")
            root = tk.Tk()
            self.window = root
            logger.info("Tk root created, setting up window...")
            self._setup_window(root)
            logger.info("Window setup complete, creating content...")
            self._create_content(root)
            logger.info("Content created, scheduling auto-dismiss...")
            self._schedule_auto_dismiss(root)
            logger.info("Updating window to ensure it's visible...")
            root.update_idletasks()
            root.update()
            logger.info("Starting dialog mainloop...")
            root.mainloop()
            logger.info("Dialog mainloop ended")
        except Exception as e:
            logger.error(f"Error in dialog thread: {e}", exc_info=True)
    
    def _create_window(self) -> None:
        """Create the dialog window as a Toplevel."""
        self.window = tk.Toplevel(self.parent)
        self._setup_window(self.window)
        self._create_content(self.window)
        self._schedule_auto_dismiss(self.window)
    
    def _setup_window(self, window: tk.Misc) -> None:
        """Configure the window for fullscreen overlay."""
        # Remove window decorations
        window.overrideredirect(True)
        
        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Set window to fullscreen
        window.geometry(f"{screen_width}x{screen_height}+0+0")
        
        # Configure background color
        bg_color = self.display_config.get('background_color', '#000000')
        window.configure(bg=bg_color)
        
        # Set window to always be on top (override-redirect already set)
        window.attributes('-topmost', True)
        
        # Bind escape key and click to dismiss
        window.bind('<Escape>', lambda e: self._dismiss())
        window.bind('<Button-1>', lambda e: self._dismiss())
        window.bind('<space>', lambda e: self._dismiss())
    
    def _create_content(self, window: tk.Misc) -> None:
        """Create and layout the dialog content."""
        # Get display settings
        text_color = self.display_config.get('text_color', '#FFFFFF')
        font_family = self.display_config.get('font_family', 'Arial')
        font_size = self.display_config.get('font_size', 32)
        show_datetime = self.display_config.get('show_datetime', True)
        datetime_format = self.display_config.get('datetime_format', 
                                                   '%Y-%m-%d %H:%M:%S')
        
        # Create main frame
        main_frame = tk.Frame(window, bg=window['bg'])
        main_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Date and time label (if enabled)
        if show_datetime:
            current_datetime = datetime.now().strftime(datetime_format)
            datetime_label = tk.Label(
                main_frame,
                text=current_datetime,
                font=(font_family, font_size // 2),
                fg=text_color,
                bg=window['bg']
            )
            datetime_label.pack(pady=(0, 40))
        
        # Message label
        message_label = tk.Label(
            main_frame,
            text=self.message,
            font=(font_family, font_size, 'bold'),
            fg=text_color,
            bg=window['bg'],
            wraplength=window.winfo_screenwidth() - 200,
            justify='center'
        )
        message_label.pack(pady=20)
        
        # Dismiss instruction
        # No dismiss instructions shown (per user request)
    
    def _schedule_auto_dismiss(self, window: tk.Misc) -> None:
        """Schedule automatic dismissal after duration."""
        # Convert seconds to milliseconds for tkinter
        delay_ms = int(self.duration_seconds * 1000)
        logger.info(f"Scheduling auto-dismiss in {self.duration_seconds} seconds ({delay_ms}ms)")
        window.after(delay_ms, self._dismiss)
    
    def _dismiss(self) -> None:
        """Dismiss the dialog."""
        logger.info(f"_dismiss called. dismissed={self.dismissed}, window={self.window is not None}")
        if not self.dismissed and self.window:
            self.dismissed = True
            logger.info("Dismissing dialog...")
            try:
                self.window.quit()
                self.window.destroy()
                logger.info("Dialog dismissed successfully")
            except Exception as e:
                logger.error(f"Error dismissing dialog: {e}")
                pass  # Window already closed
