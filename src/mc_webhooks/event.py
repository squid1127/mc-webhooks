"""Base event types for webhook processing."""

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, TYPE_CHECKING
from abc import ABC, abstractmethod

from datetime import datetime

if TYPE_CHECKING:
    from .app_context import AppContext


@dataclass(frozen=True, order=True)
class Event:
    """Represents a generic webhook event."""

    event_type: str
    payload: Dict[str, Any]
    received_at: datetime = field(default_factory=datetime.utcnow)
    
class EventProcessor(ABC):
    """Processes incoming events."""
    
    def __init__(self, event_type: str, context: "AppContext"):
        """
        Initialize the event processor.
        
        Args:
            event_type: The type of event this processor handles.
            context: Application context providing access to all services (redis, notifier, etc).
        """
        self._event_type = event_type
        self.context = context
        self.__post_init__()

    def __post_init__(self) -> None:
        """Post-initialization hook for subclasses."""
        pass
            
    # Convenience properties for backwards compatibility / readability
    @property
    def redis(self):
        """Access to Redis client."""
        return self.context.redis
    
    @property
    def notifier(self):
        """Access to Notifier."""
        return self.context.notifier
    
    @property
    def logger(self):
        """Access to Logger."""
        return self.context.logger
        
    @abstractmethod
    async def process_event(self, event: Event) -> None:
        """
        Process the given event.
        
        Args:
            event: The event to process.
        """
        pass
    
    @property
    def event_type(self) -> str:
        """The type of event this processor handles."""
        return self._event_type
