"""
Configuration manager for GusOps PyCare.
Loads and validates YAML configuration file.
Prioritizes external config files over bundled defaults.
"""

import os
import sys
import yaml
from pathlib import Path
from typing import Dict, Any, List, Optional


class ConfigManager:
    """Manages application configuration from YAML file."""
    
    DEFAULT_CONFIG = {
        'reminder': {
            'interval_minutes': 20,
            'display_duration_seconds': 10,
            'messages': [
                "Time to take a break! Look away from your screen.",
                "Stay hydrated! Drink some water.",
                "Stretch your body. Move around for a minute.",
            ]
        },
        'display': {
            'background_color': '#000000',
            'text_color': '#FFFFFF',
            'font_family': 'Arial',
            'font_size': 32,
            'show_datetime': True,
            'datetime_format': '%Y-%m-%d %H:%M:%S'
        }
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the config manager.
        
        Args:
            config_path: Path to config.yaml. If None, searches in order:
                1. Next to executable (for packaged apps)
                2. User's home directory (~/.py-care/config.yaml)
                3. Project root (for development)
                4. Bundled default (PyInstaller package)
        """
        if config_path is None:
            config_path = self._find_config_file()
        
        self.config_path = Path(config_path) if config_path else None
        self.config = self._load_config()
    
    def _find_config_file(self) -> Optional[str]:
        """
        Find config file in ord or not self.config_path.exists():
            if self.config_path:
            
        Returns:
            Path to config file, or None if not found (will use defaults)
        """
        config_filename = 'config.yaml'
        
        # 1. Check next to executable (highest priority for packaged apps)
        if getattr(sys, 'frozen', False):
            # Running as compiled executable
            exe_dir = Path(sys.executable).parent
            exe_config = exe_dir / config_filename
            if exe_config.exists():
                print(f"Using config from executable directory: {exe_config}")
                return str(exe_config)
        
        # 2. Check user's home directory
        user_config_dir = Path.home() / '.py-care'
        user_config = user_config_dir / config_filename
        if user_config.exists():
            print(f"Using config from user directory: {user_config}")
            return str(user_config)
        
        # 3. Check project root (for development)
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller temp folder - check there for bundled default
            bundled_config = Path(sys._MEIPASS) / config_filename
            if bundled_config.exists():
                print(f"Using bundled config: {bundled_config}")
                return str(bundled_config)
        else:
            # Development mode - check project root
            project_root = Path(__file__).parent.parent
            dev_config = project_root / config_filename
            if dev_config.exists():
                print(f"Using config from project root: {dev_config}")
                return str(dev_config)
        
        # If no config file found, will use DEFAULT_CONFIG
        print("No config file found, using default configuration")
        return None
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file with fallback to defaults."""
        if self.config_path is None or not self.config_path.exists():
            if self.config_path:
                print(f"Warning: Config file not found at {self.config_path}")
            print("Using default configuration.")
            return self.DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = yaml.safe_load(f)
            
            # Merge with defaults to handle missing keys
            merged_config = self._merge_with_defaults(config)
            self._validate_config(merged_config)
            return merged_config
            
        except yaml.YAMLError as e:
            print(f"Error parsing config file: {e}")
            print("Using default configuration.")
            return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            print(f"Error loading config: {e}")
            print("Using default configuration.")
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_with_defaults(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Merge loaded config with defaults for missing keys. Supports messages at root or under reminder."""
        merged = self.DEFAULT_CONFIG.copy()
        if config:
            # If messages are at root, move them under reminder
            if 'messages' in config and isinstance(config['messages'], list):
                if 'reminder' not in config or not isinstance(config['reminder'], dict):
                    config['reminder'] = {}
                config['reminder']['messages'] = config['messages']
            # Deep merge for nested dictionaries
            for key in merged:
                if key in config and isinstance(config[key], dict):
                    merged[key].update(config[key])
                elif key in config:
                    merged[key] = config[key]
        return merged
    
    def _validate_config(self, config: Dict[str, Any]) -> None:
        """Validate configuration values."""
        # Validate interval
        interval = config['reminder']['interval_minutes']
        if not isinstance(interval, (int, float)) or interval <= 0:
            raise ValueError(f"Invalid interval_minutes: {interval}")
        
        # Validate display duration
        duration = config['reminder']['display_duration_seconds']
        if not isinstance(duration, (int, float)) or duration <= 0:
            raise ValueError(f"Invalid display_duration_seconds: {duration}")
        
        # Validate messages
        messages = config['reminder']['messages']
        if not isinstance(messages, list) or len(messages) == 0:
            raise ValueError("Messages list cannot be empty")
        
        # Validate font size
        font_size = config['display']['font_size']
        if not isinstance(font_size, int) or font_size <= 0:
            raise ValueError(f"Invalid font_size: {font_size}")
    
    def get_interval_minutes(self) -> float:
        """Get reminder interval in minutes."""
        return self.config['reminder']['interval_minutes']
    
    def get_interval_seconds(self) -> float:
        """Get reminder interval in seconds."""
        return self.config['reminder']['interval_minutes'] * 60
    
    def get_display_duration(self) -> float:
        """Get dialog display duration in seconds."""
        return self.config['reminder']['display_duration_seconds']
    
    def get_messages(self) -> List[str]:
        """Get list of reminder messages."""
        return self.config['reminder']['messages']
    
    def get_display_config(self) -> Dict[str, Any]:
        """Get display configuration."""
        return self.config['display']
    
    def reload(self) -> None:
        """Reload configuration from file."""
        self.config = self._load_config()
