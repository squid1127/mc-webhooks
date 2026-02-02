"""Handle incoming webhook events and process them based on their type."""

from .events import Registry
from .event import Event, EventProcessor
from .app_context import AppContext

class EventHandler:
    """Handles incoming webhook events and delegates processing to the appropriate event processors."""
    
    def __init__(self, context: AppContext):
        """
        Initialize the event handler with application context.
        
        Args:
            context: Application context providing access to all services.
        """
        self.context = context
        self.event_processors: dict[str, EventProcessor] = {}
        
        for event_type, processor_cls in Registry.all().items():
            self.event_processors[event_type] = processor_cls(event_type, context)
        
        
    async def handle_event(self, event_type: str, payload: dict) -> None:
        """
        Handle an incoming event by delegating to the appropriate event processor.
        
        Args:
            event_type: The type of the incoming event.
            payload: The payload of the incoming event.
        """
        processor = self.event_processors.get(event_type)
        if not processor:
            # No processor registered for this event type
            return
        
        event = Event(event_type=event_type, payload=payload)
        await processor.process_event(event)