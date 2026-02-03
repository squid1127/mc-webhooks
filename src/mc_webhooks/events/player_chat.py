"""Player chat event"""
import json
from discord import Embed, Color
from .registry import Registry
from ..event import EventProcessor, Event


class PlayerChatEventProcessor(EventProcessor):
    """Processes player chat events."""
    
    event_types = ["player_chat"]
    
    def __post_init__(self):
        # Load private commands from settings
        self.private_prefixes: list[str] = json.loads(self.context.settings.player_private_chat_prefixes)
        
    def filter_private_messages(self, command: str) -> str:
        """Filter out private commands from being displayed."""
        for private_prefix in self.private_prefixes:
            if command.startswith(private_prefix):
                return f"{private_prefix} **[REDACTED]**"
        return command
        
    async def process_event(self, event: Event) -> None:
        """
        Process the player chat event.
        
        Args:
            event: The event to process.
        """
        player = event.payload.get("player", "Unknown")
        message = event.payload.get("message", "-# [Empty message]")
        
        embed = Embed(
            description=self.filter_private_messages(message),
            color=Color.blue(),
        )
        embed.set_author(name=player + " | Message")
        
        await self.context.notifier.send_embed(embed)
        
        self.context.logger.info(f"Processed player chat event from {player}")
        
        await self.context.redis.publish(
            "mc_webhooks:events:player_chat",
            {"player": player, "message": message}
        )
        
# Register the event processor
Registry.add(PlayerChatEventProcessor)
