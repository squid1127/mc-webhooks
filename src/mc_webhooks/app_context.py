"""Application context containing all shared services."""

from dataclasses import dataclass
from .redis import RedisClient
from .notify import Notifier
from .logging_config import get_logger
from .config import Settings

@dataclass
class AppContext:
    """
    Application context providing access to all shared services.
    
    This object is passed to event processors and other components to avoid
    circular imports and tight coupling. Services can be added here without
    changing function signatures across the codebase.
    """
    
    notifier: Notifier
    settings: Settings
    redis: RedisClient | None
    logger: object | None = None
    
    def __post_init__(self):
        """Initialize default logger if not provided."""
        if self.logger is None:
            self.logger = get_logger(__name__)
