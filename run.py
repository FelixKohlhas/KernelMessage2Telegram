#!/usr/bin/env python3

import subprocess
import requests
import argparse
import sys
import json

# Send Telegram message
def send_telegram_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"[!] Failed to send message: {e}")

# Monitor kernel messages using journalctl
def monitor_kernel_messages(token, chat_id, min_priority):
    print("[*] Monitoring kernel messages...")

    cmd = ['sudo', 'journalctl', '-kf', '-p', f'0..{min_priority}', '--output=short']
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        for line in iter(process.stdout.readline, ''):
            line = line.strip()
            if line:
                print(f"[LOG] {line}")
                send_telegram_message(token, chat_id, f"⚠️ *Kernel Alert:* `{line}`")
    except KeyboardInterrupt:
        print("\n[!] Monitoring stopped.")
    except Exception as e:
        print(f"[!] Error: {e}")

def load_config(config_path):
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config.get('token'), config.get('chat_id')
    except FileNotFoundError:
        print(f"[!] Config file not found: {config_path}")
        return None, None
    except json.JSONDecodeError:
        print(f"[!] Error decoding JSON from config file: {config_path}")
        return None, None

# Main
def main():
    parser = argparse.ArgumentParser(description="Live monitor kernel messages and send high severity logs to Telegram.")
    parser.add_argument('--token', default=None, help='Telegram bot token')
    parser.add_argument('--chat-id', default=None, help='Telegram chat ID to send messages to')
    parser.add_argument('--priority', default='3', help='Minimum priority (0=emerg, 1=alert, 2=crit, 3=err)')
    parser.add_argument('--config', default='/usr/local/etc/telegram_key.json', help='Path to the telegram key JSON file')

    args = parser.parse_args()

    if not args.token or not args.chat_id:
        token, chat_id = load_config(args.config)
    if args.token:
        token = args.token
    if args.chat_id:
        chat_id = args.chat_id
    if not token or not chat_id:
        print("[!] Telegram token and chat ID are required.")
        return

    try:
        priority = int(args.priority)
        if not (0 <= priority <= 3):
            raise ValueError
    except ValueError:
        print("[!] Priority must be an integer between 0 (emerg) and 3 (err).")
        sys.exit(1)

    monitor_kernel_messages(token, chat_id, priority)

if __name__ == "__main__":
    main()