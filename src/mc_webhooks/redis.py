"""Redis client management."""

import json
from typing import Any, Optional

import redis.asyncio as redis

from .logging_config import get_logger

logger = get_logger(__name__)


class RedisClient:
    """Manages Redis connection."""

    def __init__(self, redis_url: str = "redis://localhost", db: int = 0):
        """
        Initialize Redis client.

        Args:
            redis_url: Redis connection URL.
            db: Database number.
        """
        self.redis_url = redis_url
        self.db = db
        self._client: Optional[redis.Redis] = None

    async def connect(self) -> None:
        """Establish connection to Redis."""
        try:
            # redis.asyncio returns a ready-to-use async Redis client
            self._client = redis.from_url(
                self.redis_url, db=self.db, decode_responses=True
            )
            await self._client.ping()
            logger.info(f"Connected to Redis at {self.redis_url}")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self._client:
            # Close async client
            try:
                # redis 5 provides aclose() for asyncio clients
                await self._client.aclose()
            except AttributeError:
                # Fallback for older versions
                await self._client.close()
            logger.info("Disconnected from Redis")

    async def publish(self, channel: str, message: dict | Any) -> None:
        """
        Publish a message to a Redis channel.

        Args:
            channel: The Redis channel to publish to.
            message: The message to publish (will be JSON-encoded).
        Raises:
            RuntimeError: If the Redis client is not connected.
            json.JSONDecodeError: If message serialization fails.
        """
        if not self._client:
            raise RuntimeError("Redis client is not connected.")
        await self._client.publish(channel, json.dumps(message))
        logger.debug(f"Published message to channel '{channel}': {message}")

    @property
    def client(self) -> Optional[redis.Redis]:
        """Get the Redis client instance."""
        return self._client
