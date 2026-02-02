"""Configuration settings for the webhook listener."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""

    # Server settings
    host: str = "127.0.0.1"
    port: int = 8000
    webhook_endpoint: str = "/webhook"
    log_level: str = "INFO"

    # Redis settings
    redis_url: str | None = None
    redis_db: int = 0
    
    # Notification settings
    discord_webhook_url: str = ""
    
    # Event Processer settings
    player_private_cmds: str = '["/w", "/msg", "/tell"]' # JSON array of commands to treat as private
    player_private_chat_prefixes: str = '["->"]' # JSON array of chat prefixes to treat as private

    class Config:
        """Pydantic config."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False