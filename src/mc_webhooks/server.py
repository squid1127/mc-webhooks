"""FastAPI webhook server."""

from typing import Any
from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
import json

from .logging_config import get_logger
from .redis import RedisClient
from .config import Settings
from .notify import Notifier
from .event_handler import EventHandler
from .app_context import AppContext

logger = get_logger(__name__)


class WebhookServer(FastAPI):
    def __init__(self, settings: Settings):
        super().__init__(
            title="MC Webhook Listener",
            description="Async webhook listener with Redis capabilities",
            version="0.1.0",
            lifespan=lifespan,
            redirect_slashes=False,
        )
        self._settings = settings
        if self.settings.redis_url:
            self._redis: RedisClient = RedisClient(
                redis_url=self.settings.redis_url, db=self.settings.redis_db
            )
        self._notifier: Notifier = Notifier(
            webhook_url=self.settings.discord_webhook_url
        )
        self._context: AppContext = AppContext(
            redis=self.redis,
            notifier=self.notifier,
            logger=logger,
            settings=self.settings,
        )
        self._event_handler: EventHandler = EventHandler(context=self._context)

    # Immutable properties
    @property
    def redis(self) -> RedisClient | None:
        if hasattr(self, "_redis"):
            return self._redis
        return None

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def notifier(self) -> Notifier:
        return self._notifier

    @property
    def context(self) -> AppContext:
        return self._context

    @property
    def event_handler(self) -> EventHandler:
        return self._event_handler


@asynccontextmanager
async def lifespan(app: WebhookServer):
    """Manage application lifespan (startup/shutdown)."""
    # Startup
    if app.redis:
        await app.redis.connect()
    logger.info("Application startup complete")
    yield
    # Shutdown
    if app.redis:
        await app.redis.disconnect()
    logger.info("Application shutdown complete")


def create_app(settings: Settings) -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI instance.
    """
    app = WebhookServer(
        settings=settings,
    )

    @app.post(app.settings.webhook_endpoint.rstrip("/"))
    @app.post(app.settings.webhook_endpoint.rstrip("/") + "/")
    async def receive_webhook(request: Request) -> dict:
        """
        Receive webhook POST request.

        Args:
            request: FastAPI request object.

        Returns:
            Response confirming webhook receipt.
        """

        try:
            # Get request body
            body: dict[str, Any] = await request.json()
            logger.info(f"Received webhook: {json.dumps(body)}")

            event_type = body.get("event")
            await app.event_handler.handle_event(event_type, body)

            return {
                "status": "success",
                "message": "Webhook received and processed",
            }
        except json.JSONDecodeError:
            logger.error("Invalid JSON in webhook request")
            logger.info(f"Received webhook: {await request.body()}")
            return {
                "status": "error",
                "message": "Invalid JSON payload",
            }
        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return {
                "status": "error",
                "message": "Internal server error",
            }

    @app.get("/health")
    async def health_check() -> dict:
        """Health check endpoint."""
        return {"status": "healthy"}

    return app
