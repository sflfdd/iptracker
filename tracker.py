from flask import Flask, request, redirect
import requests
from bot import handle_tracking_data
import asyncio
import os
from telegram import Bot
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.bot = Bot(token=os.getenv('BOT_TOKEN'))

@app.route('/')
def home():
    return "Bot is running!"

@app.route('/track/<tracking_id>')
def track(tracking_id):
    try:
        # Get IP address
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        
        # Make request to FreeIPAPI
        api_url = f'https://freeipapi.com/api/json/{ip}'
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }
        
        response = requests.get(api_url, headers=headers)
        
        if response.status_code == 200:
            ip_data = response.json()
            # Handle the tracking data
            asyncio.run(handle_tracking_data(tracking_id, ip_data, app.bot))
        else:
            print(f"API Error: {response.status_code}")
            ip_data = {"error": "Failed to get IP data"}
            
    except Exception as e:
        print(f"Error: {str(e)}")
        ip_data = {"error": str(e)}
    
    # Redirect to a safe page
    return redirect("https://google.com")

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port) 