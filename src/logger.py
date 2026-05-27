"""
Logging configuration for GusOps PyCare.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime
from logging.handlers import RotatingFileHandler


def setup_logger(name: str = "pycare") -> logging.Logger:
    """
    Set up application logger with both file and console output.
    
    Args:
        name: Logger name
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # Avoid duplicate handlers if logger already configured
    if logger.handlers:
        return logger
    
    # Create logs directory
    if getattr(sys, 'frozen', False):
        # Running as exe - put logs next to executable
        logs_dir = Path(sys.executable).parent / 'logs'
    else:
        # Running as script - put logs in project root
        logs_dir = Path(__file__).parent.parent / 'logs'
    
    logs_dir.mkdir(exist_ok=True)
    
    # Create log filename with date
    log_file = logs_dir / f"pycare_{datetime.now().strftime('%Y%m%d')}.log"
    
    # File handler with rotation (max 5MB per file, keep 5 files)
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,  # 5MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(file_formatter)
    
    # Console handler for immediate feedback
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )
    console_handler.setFormatter(console_formatter)
    
    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    
    logger.info(f"Logger initialized. Log file: {log_file}")
    
    return logger


# Create default logger
logger = setup_logger()
