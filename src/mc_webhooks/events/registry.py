"""Registry for event processors."""

from typing import Dict, Type

class Registry:
    """Registry singleton for event processors."""
    
    _registry: Dict[str, Type] = {}

    @classmethod
    def add(cls, event_type, processor_cls: Type) -> None:
        """
        Add an event processor to the registry.

        Args:
            event_type: The type of event the processor handles.
            processor_cls: The processor class to register.
        """
        cls._registry[event_type] = processor_cls

    @classmethod
    def get(cls, event_type: str) -> Type:
        """
        Get an event processor class by event type.
        
        Args:
            event_type: The type of event.

        Returns:
            The registered processor class.

        Raises:
            KeyError: If no processor is registered for the given event type.
        """
        if event_type not in cls._registry:
            raise KeyError(f"No processor registered for event type: {event_type}")
        return cls._registry[event_type]
    
    @classmethod
    def all(cls) -> Dict[str, Type]:
        """
        Get all registered event processors.

        Returns:
            A dictionary of event types to processor classes.
        """
        return cls._registry.copy()