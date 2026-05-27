"""
Scheduler for managing reminder timing and triggering.
"""

import threading
import time
from typing import Callable, List, Optional
from datetime import datetime

from src.logger import logger


class ReminderScheduler:
    """Manages timing and scheduling of reminder displays."""
    
    def __init__(self, interval_seconds: float, messages: List[str], 
                 callback: Callable[[str], None]):
        """
        Initialize the scheduler.
        
        Args:
            interval_seconds: Time between reminders in seconds
            messages: List of messages to show in sequence
            callback: Function to call when it's time to show a reminder
        """
        self.interval_seconds = interval_seconds
        self.messages = messages
        self.callback = callback
        
        self.current_message_index = 0
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.stop_event = threading.Event()
    
    def start(self) -> None:
        """Start the scheduler in a background thread."""
        if self.running:
            return
        
        self.running = True
        self.stop_event.clear()
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        logger.info(f"Scheduler started. Reminders every {self.interval_seconds/60:.1f} minutes.")
    
    def stop(self) -> None:
        """Stop the scheduler."""
        if not self.running:
            return
        
        logger.info("Stopping scheduler...")
        self.running = False
        self.stop_event.set()
        
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
    
    def _run(self) -> None:
        """Main scheduler loop running in background thread."""
        # Show first reminder immediately on startup
        logger.info("Scheduler thread started, preparing to show initial reminder...")
        if self.running and not self.stop_event.is_set():
            message = self._get_next_message()
            logger.info(f"Showing initial reminder: {message[:50]}...")
            try:
                self.callback(message)
                logger.info("Initial reminder callback executed successfully")
            except Exception as e:
                logger.error(f"Error showing initial reminder: {e}", exc_info=True)
        
        # Continue with regular interval-based reminders
        while self.running and not self.stop_event.is_set():
            # Wait for the interval
            if self.stop_event.wait(self.interval_seconds):
                # Stop event was set
                break
            
            if not self.running:
                break
            
            # Get the next message in sequence
            message = self._get_next_message()
            
            # Log the reminder
            logger.info(f"Showing scheduled reminder: {message[:50]}...")
            
            # Trigger the callback
            try:
                self.callback(message)
                logger.info("Scheduled reminder callback executed successfully")
            except Exception as e:
                logger.error(f"Error showing scheduled reminder: {e}", exc_info=True)
    
    def _get_next_message(self) -> str:
        """Get the next message in the sequence."""
        if not self.messages:
            return "Take a break!"
        
        message = self.messages[self.current_message_index]
        
        # Move to next message in sequence
        self.current_message_index = (self.current_message_index + 1) % len(self.messages)
        
        return message
    
    def reset_sequence(self) -> None:
        """Reset message sequence to the beginning."""
        self.current_message_index = 0
