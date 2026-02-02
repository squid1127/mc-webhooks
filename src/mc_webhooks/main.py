"""Main entry point using Typer CLI."""

import typer
import uvicorn
from dotenv import load_dotenv

from .logging_config import setup_logging, get_logger
from .config import Settings
from .server import create_app

logger = get_logger(__name__)

app = typer.Typer(help="Webhook listener service")


@app.command()
def run(
    host: str | None = typer.Option(
        None,
        "--host",
        "-h",
        help="Host to bind to",
    ),
    port: int | None = typer.Option(
        None,
        "--port",
        "-p",
        help="Port to bind to",
    ),
    endpoint: str | None = typer.Option(
        None,
        "--endpoint",
        "-e",
        help="Webhook endpoint path",
    ),
    log_level: str | None = typer.Option(
        None,
        "--log-level",
        "-l",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    ),
    redis_url: str | None = typer.Option(
        None,
        "--redis-url",
        help="Redis connection URL",
    ),
    discord_webhook_url: str | None = typer.Option(
        None,
        "--discord-webhook-url",
        help="Discord webhook URL for notifications",
    ),
) -> None:
    """Start the webhook listener server."""
    
    # Load settings from env vars and defaults first
    settings = Settings()
    
    # Override with CLI args only if explicitly provided
    if host is not None:
        settings.host = host
    if port is not None:
        settings.port = port
    if endpoint is not None:
        settings.webhook_endpoint = endpoint
    if log_level is not None:
        settings.log_level = log_level
    if redis_url is not None:
        settings.redis_url = redis_url
    if discord_webhook_url is not None:
        settings.discord_webhook_url = discord_webhook_url
    
    # Setup logging
    setup_logging(level=settings.log_level)
    logger.info("Starting webhook listener")

    logger.info(f"Server will listen on {settings.host}:{settings.port}")
    logger.info(f"Webhook endpoint: {settings.webhook_endpoint}")
    logger.info(f"Redis URL: {settings.redis_url}")

    if settings.redis_url is None:
        logger.warning("Redis URL not provided; Redis features will be disabled.")
    if not settings.discord_webhook_url:
        logger.warning("Discord webhook URL not provided; notifications will be disabled.")

    # Create FastAPI app
    fastapi_app = create_app(settings=settings)

    # Run server
    uvicorn.run(
        fastapi_app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower(),
    )


if __name__ == "__main__":
    app()
