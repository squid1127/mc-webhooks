"""Player chat event"""
import json
from discord import Embed, Color
from .registry import Registry
from ..event import EventProcessor, Event


class PlayerJoinLeaveEventProcessor(EventProcessor):
    """Processes player chat events."""
    
    event_types = ["player_login", "player_quit"]
        
    async def process_event(self, event: Event) -> None:
        """
        Process the player chat event.
        
        Args:
            event: The event to process.
        """
        player = event.payload.get("player", "Unknown")
        joined = event.event_type == "player_login"
        
        embed = Embed(            color=Color.blurple(),
        )
        embed.set_author(name=player + " | " + ("Joined" if joined else "Left"))
        
        await self.context.notifier.send_embed(embed)
        
        self.context.logger.info(f"Processed player join/leave event from {player}")
        
        await self.context.redis.publish(
            f"mc_webhooks:events:player_{'join' if joined else 'leave'}",
            {"player": player}
        )
        
# Register the event processor
Registry.add(PlayerJoinLeaveEventProcessor)