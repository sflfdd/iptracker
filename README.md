# IP Tracker Bot

A Telegram bot that generates tracking links and provides information about visitors who click on them.

## Features

- Generate tracking links
- Get visitor information:
  - IP Address
  - Country
  - City
  - ISP
  - Timezone

## Setup

1. Install requirements:
```bash
pip install -r requirements.txt
```

2. Set environment variables:
- BOT_TOKEN: Your Telegram bot token
- BASE_URL: Your deployment URL

3. Run the bot:
```bash
python bot.py
```

## Commands

- `/start` - Start the bot
- `/generate` - Generate a tracking link
- `/help` - Show help message

## Deployment

This bot can be deployed on:
- Render
- PythonAnywhere
- Heroku
- Any other Python hosting platform

## Security

- Never share your bot token
- Keep sensitive data in environment variables
- Use HTTPS for all connections 