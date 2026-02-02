"""Notification services for webhook events, using discord.py webhooks."""

from discord import Embed, Webhook, Client
from pathlib import Path
import aiohttp

class Notifier:
    """Base notifier class for sending notifications via Discord webhooks and other services."""

    def __init__(self, webhook_url: str | None = None):
        """
        Initialize the Discord notifier.

        Args:
            webhook_url: The Discord webhook URL to send notifications to, or None to disable.
        """
        self.webhook_url: str | None = webhook_url
        
    async def send_embed(self, embed: Embed) -> None:
        """
        Send an embed notification to the Discord channel.

        Args:
            embed: The Discord Embed object to send.
        """
        
        await self.send_message(content=None, embed=embed)

    async def send_message(self, content: str | None, **kwargs) -> None:
        """
        Send a message notification to the Discord channel.

        Args:
            content: The message content to send, or None for no content.
            **kwargs: Additional keyword arguments for the send method.
        """
        if not self.webhook_url:
            return  # Notifications are disabled

        async with aiohttp.ClientSession() as session:
            webhook = Webhook.from_url(self.webhook_url, session=session)
            await webhook.send(content=content, **kwargs)