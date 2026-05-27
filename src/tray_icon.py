"""
System tray icon for GusOps PyCare application.
"""

import pystray
import sys
from pathlib import Path
from PIL import Image, ImageDraw
from typing import Callable, Optional

try:
    from src.logger import logger
except ImportError:
    from logger import logger


class TrayIcon:
    """System tray icon with menu for application control."""
    
    def __init__(self, on_exit: Callable[[], None]):
        """
        Initialize the system tray icon.
        
        Args:
            on_exit: Callback function to execute when exit is clicked
        """
        self.on_exit = on_exit
        self.icon: Optional[pystray.Icon] = None
        self.eye_open_icon: Optional[Image.Image] = None
        self.eye_closed_icon: Optional[Image.Image] = None
        self.current_icon_open = True
        
    def create_icon(self) -> None:
        """Create and run the system tray icon."""
        logger.info("Creating system tray icon...")
        
        # Load or create icon images
        self.eye_open_icon = self._load_icon('eye.png')
        self.eye_closed_icon = self._load_icon('eye-closed.png')
        
        # Start with eye open
        icon_image = self.eye_open_icon
        
        # Create menu
        menu = pystray.Menu(
            pystray.MenuItem('GusOps PyCare', lambda: None, enabled=False),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem('Exit', self._on_exit_clicked)
        )
        
        # Create icon
        self.icon = pystray.Icon(
            'gusops-pycare',
            icon_image,
            'GusOps PyCare - Screen Time Reminder',
            menu
        )
        
        logger.info("System tray icon created, starting run loop...")
        # Run the icon (blocking call)
        self.icon.run()
    
    def toggle_icon(self) -> None:
        """Toggle between eye open and eye closed icons."""
        if not self.icon:
            return
            
        self.current_icon_open = not self.current_icon_open
        new_icon = self.eye_open_icon if self.current_icon_open else self.eye_closed_icon
        self.icon.icon = new_icon
        logger.debug(f"Icon toggled to: {'open' if self.current_icon_open else 'closed'}")
    
    def _load_icon(self, icon_name: str) -> Image.Image:
        """
        Load an icon from the assets folder or create a default one.
        
        Args:
            icon_name: Name of the icon file (e.g., 'eye.png')
            
        Returns:
            PIL Image object
        """
        try:
            # Determine the assets path
            if getattr(sys, 'frozen', False):
                # Running as exe - check next to executable first
                base_path = Path(sys.executable).parent
                icon_path = base_path / 'assets' / 'icons' / icon_name
                
                if not icon_path.exists():
                    # Try bundled resources
                    if hasattr(sys, '_MEIPASS'):
                        base_path = Path(sys._MEIPASS)
                        icon_path = base_path / 'assets' / 'icons' / icon_name
            else:
                # Running as script
                base_path = Path(__file__).parent.parent
                icon_path = base_path / 'assets' / 'icons' / icon_name
            
            if icon_path.exists():
                logger.info(f"Loading icon from: {icon_path}")
                return Image.open(icon_path).resize((64, 64), Image.Resampling.LANCZOS)
            else:
                logger.warning(f"Icon not found at {icon_path}, using default")
                return self._create_default_icon(icon_name)
                
        except Exception as e:
            logger.error(f"Error loading icon {icon_name}: {e}")
            return self._create_default_icon(icon_name)
    
    def _create_default_icon(self, icon_name: str = 'eye.png') -> Image.Image:
        """
        Create a default icon image.
        
        Args:
            icon_name: Name to determine which icon to create
            
        Returns:
            PIL Image object
        """
        # Create a 64x64 image with transparency
        size = 64
        image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        dc = ImageDraw.Draw(image)
        
        # Draw a blue circle
        margin = 8
        dc.ellipse(
            [margin, margin, size - margin, size - margin],
            fill='#4A90E2',
            outline='#2E5C8A',
            width=3
        )
        
        # Draw a letter based on icon type
        if 'closed' in icon_name.lower():
            letter = 'Z'  # Z for closed/sleeping
        else:
            letter = 'G'  # G for GusOps
            
        dc.text(
            (size // 2 - 8, size // 2 - 12),
            letter,
            fill='white',
            font=None
        )
        
        return image
    
    def _on_exit_clicked(self) -> None:
        """Handle exit menu item click."""
        logger.info("Exit requested from tray icon.")
        
        # Stop the icon
        if self.icon:
            self.icon.stop()
        
        # Call the exit callback
        self.on_exit()
    
    def stop(self) -> None:
        """Stop the tray icon."""
        if self.icon:
            logger.info("Stopping tray icon...")
            self.icon.stop()
