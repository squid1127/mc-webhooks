# mc-webhooks

A simple, modular, async webhook listener for Minecraft server events using [this plugin](https://modrinth.com/plugin/minecraftserverapi/), built with FastAPI and Typer. It receives event data from a Minecraft server, processes it, and sends notifications to Discord.

## Overview

This project provides a webhook server that listens for events from a Minecraft server (e.g., player chat, commands). It's designed to be extensible, allowing you to add new event handlers easily.

- **FastAPI Server**: An asynchronous web server to receive webhooks.
- **Typer CLI**: A command-line interface for starting and configuring the server.
- **Event Handling**: A modular system for processing different types of events.
- **Discord Notifications**: Sends formatted messages to a Discord channel for specific events.
- **Redis Integration**: Can be connected to a Redis instance for data storage (optional).

## Usage

### Using Command-Line Arguments

You can start the server and configure it directly from the command line.

```bash
poetry run mcwh \
  --host 0.0.0.0 \
  --port 8080 \
  --discord-webhook-url "https://discord.com/api/webhooks/..."
```

### Using an Environment File

For a more permanent configuration, you can create a `.env` file in the project root.

```env
# .env
HOST=0.0.0.0
PORT=8080
LOG_LEVEL=DEBUG
DISCORD_WEBHOOK_URL="https://discord.com/api/webhooks/..."
PLAYER_PRIVATE_CMDS='["/login", "/register"]'
```

Then, run the server:

```bash
poetry run mcwh
```

## Configuration

The application can be configured via command-line arguments or environment variables. CLI arguments take precedence over environment variables.

| Feature               | CLI Argument            | Environment Variable           | Default Value             |
| --------------------- | ----------------------- | ------------------------------ | ------------------------- |
| Host                  | `--host`, `-h`          | `HOST`                         | `127.0.0.1`               |
| Port                  | `--port`, `-p`          | `PORT`                         | `8000`                    |
| Webhook Endpoint      | `--endpoint`, `-e`      | `WEBHOOK_ENDPOINT`             | `/webhook`                |
| Log Level             | `--log-level`, `-l`     | `LOG_LEVEL`                    | `INFO`                    |
| Redis URL (Optional)  | `--redis-url`           | `REDIS_URL`                    | N/A (Disabled)            |
| Redis DB              |                         | `REDIS_DB`                     | `0`                       |
| Discord Webhook URL   | `--discord-webhook-url` | `DISCORD_WEBHOOK_URL`          | `""`                      |
| Private Commands      |                         | `PLAYER_PRIVATE_CMDS`          | `["/w", "/msg", "/tell"]` |
| Private Chat Prefixes |                         | `PLAYER_PRIVATE_CHAT_PREFIXES` | `["->"]`                  |

## Development

Install development dependencies:

```bash
poetry install --with dev
```

Run tests:

```bash
poetry run pytest
```

Format and lint code:

```bash
poetry run black src/
poetry run ruff check src/
```
