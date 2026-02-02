"""Player command event"""
from discord import Embed, Color
import json
from .registry import Registry
from ..event import EventProcessor, Event

class PlayerCmdEventProcessor(EventProcessor):
    """Processes player command events."""
    
    def __post_init__(self):
        self.private_commands: list[str] = json.loads(self.context.settings.player_private_cmds)
        
    def filter_private_command(self, command: str) -> str:
        """Filter out private commands from being displayed."""
        command_root = command.split(" ")[0].lower()
        for private_cmd in self.private_commands:
            if command_root == private_cmd.lower():
                return f"{private_cmd} [REDACTED]"
        return command
        
    async def process_event(self, event: Event) -> None:
        """
        Process the player command event.
        
        Args:
            event: The event to process.
        """
        player = event.payload.get("player", "Unknown")
        command = event.payload.get("command", "[Empty command]")
        
        
        
        embed = Embed(
            description=f"`{self.filter_private_command(command)}`",
            color=Color.yellow(),
        )
        embed.set_author(name=player + " | Command")
        
        await self.context.notifier.send_embed(embed)
        
        self.context.logger.info(f"Processed player command event from {player}")
        
# Register the event processor
Registry.add("player_command", PlayerCmdEventProcessor)
