"""Event processing modules & registry."""

# Registry
from .registry import Registry

# Event processors - imported to trigger registration
from .player_chat import PlayerChatEventProcessor
from .player_command import PlayerCmdEventProcessor
from .player_join_leave import PlayerJoinLeaveEventProcessor

__all__ = ["Registry"]