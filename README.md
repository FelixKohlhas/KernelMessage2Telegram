# KernelMessage2Telegram

## Description
This script monitors kernel messages in real-time using `journalctl` and sends high-severity logs to a specified Telegram chat. It is useful for system administrators who want to be alerted about critical kernel events.

## Features
- Monitors kernel messages with a specified priority range.
- Sends alerts to a Telegram chat using a bot.
- Configurable via command-line arguments or a JSON configuration file.

## Requirements
- Python 3.x
- `requests` library
- `journalctl` (requires `sudo` privileges)

## Installation
1. Clone this repository or download the script.
2. Install the required Python library:
   ```bash
   pip install requests
   ```
3. Ensure you have `journalctl` installed and accessible.

## Usage
Run the script with the following options:

```bash
python3 run.py [--token TOKEN] [--chat-id CHAT_ID] [--priority PRIORITY] [--config CONFIG_PATH]
```

### Options
- `--token`: Telegram bot token (optional if provided in the config file).
- `--chat-id`: Telegram chat ID to send messages to (optional if provided in the config file).
- `--priority`: Minimum priority level for kernel messages (default: `3`).
  - `0`: Emergency
  - `1`: Alert
  - `2`: Critical
  - `3`: Error
- `--config`: Path to the JSON configuration file (default: `/usr/local/etc/telegram_key.json`).

### Example
```bash
python3 run.py --token YOUR_BOT_TOKEN --chat-id YOUR_CHAT_ID --priority 2
```

## Configuration File
You can use a JSON file to store the Telegram bot token and chat ID. The default path is `/usr/local/etc/telegram_key.json`. The file should have the following structure:

```json
{
  "token": "YOUR_BOT_TOKEN",
  "chat_id": "YOUR_CHAT_ID"
}
```

## Notes
- The script requires `sudo` privileges to access kernel messages via `journalctl`.
- Ensure your Telegram bot has been created and the chat ID is correct.