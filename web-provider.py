from flask import Flask, request, send_file, make_response, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import requests
import csv
import time
import re
from urllib.parse import urlencode

from utils.checktype import trainType
from utils.trainlogger.main import addTrain
from utils.trainset import setNumber

app = Flask(__name__)
CORS(app, resources={
    "/csv/*": {"origins": "*"},
    "/auth/discord": {"origins": "*"},
    "/log-train": {"origins": "*"}
})

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"]
)

# Configuration
DISCORD_TOKEN_URL = "https://discord.com/api/oauth2/token"
DISCORD_USER_URL = "https://discord.com/api/users/@me"

from dotenv import load_dotenv
load_dotenv()
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
CSV_DIR = os.getenv("CSV_DIR")
MAP_DIR = os.getenv("MAP_DIR")

# Existing endpoints remain unchanged...

@app.route('/csv/<filename>', methods=['GET', 'OPTIONS'])
@limiter.limit("100/day")
def serve_csv(filename):
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Accept, ngrok-skip-browser-warning'
        print("Handled OPTIONS preflight request for /csv")
        return response

    file_path = os.path.join(CSV_DIR, filename)
    print(f"Requested file: {filename}")
    print(f"Full path: {file_path}")
    print(f"Path exists: {os.path.exists(file_path)}")
    print(f"Is CSV: {file_path.endswith('.csv')}")
    print(f"Files in directory: {os.listdir(CSV_DIR)}")
    
    if os.path.exists(file_path) and file_path.endswith('.csv'):
        response = send_file(file_path, mimetype='text/csv')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = make_response(f"File not found or not a CSV at {file_path}", 404)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

@app.route('/map/<filename>', methods=['GET', 'OPTIONS'])
@limiter.limit("100/day")
def serve_map(filename):
    filename = filename + "-map.png"
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Accept, ngrok-skip-browser-warning'
        print("Handled OPTIONS preflight request for /map")
        return response

    file_path = os.path.join(MAP_DIR, filename)
    print(f"Requested file: {filename}")
    print(f"Full path: {file_path}")
    print(f"Path exists: {os.path.exists(file_path)}")
    print(f"Is PNG: {file_path.endswith('.png')}")
    print(f"Files in directory: {os.listdir(CSV_DIR)}")
    
    if os.path.exists(file_path) and file_path.endswith('.png'):
        response = send_file(file_path, mimetype='image/png')
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    else:
        response = make_response(f"File not found or not a PNG at {file_path}", 404)
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

@app.route('/auth/discord', methods=['POST', 'OPTIONS'])
@limiter.limit("50/day;10/hour")
def discord_auth():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        print("Handled OPTIONS preflight request for /auth/discord")
        return response

    data = request.get_json()
    if not data or 'code' not in data or 'redirect_uri' not in data:
        return jsonify({"error": "Missing code or redirect_uri"}), 400

    code = data['code']
    redirect_uri = data['redirect_uri']

    token_payload = {
        'client_id': DISCORD_CLIENT_ID,
        'client_secret': DISCORD_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': redirect_uri
    }

    try:
        token_response = requests.post(DISCORD_TOKEN_URL, data=token_payload, headers={
            'Content-Type': 'application/x-www-form-urlencoded'
        })
        token_response.raise_for_status()
        token_data = token_response.json()
        access_token = token_data.get('access_token')

        if not access_token:
            return jsonify({"error": "Failed to obtain access token"}), 500

        user_response = requests.get(DISCORD_USER_URL, headers={
            'Authorization': f'Bearer {access_token}'
        })
        user_response.raise_for_status()
        user_data = user_response.json()
        username = user_data.get('username')

        if not username:
            return jsonify({"error": "Failed to obtain username"}), 500

        response = jsonify({"access_token": access_token, "username": username})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response

    except requests.RequestException as e:
        print(f"Error during Discord auth: {e}")
        return jsonify({"error": "Authentication failed"}), 500

# New train logging endpoint
@app.route('/log-train', methods=['POST', 'OPTIONS'])
@limiter.limit("50/day;10/hour")
def log_train():
    if request.method == 'OPTIONS':
        response = make_response()
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, ngrok-skip-browser-warning'
        print("Handled OPTIONS preflight request for /log-train")
        return response

    # Check authorization
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Unauthorized: Missing or invalid token"}), 401
    access_token = auth_header.split(' ')[1]

    # Verify token with Discord
    try:
        user_response = requests.get(DISCORD_USER_URL, headers={'Authorization': f'Bearer {access_token}'})
        user_response.raise_for_status()
        user_data = user_response.json()
        username = user_data.get('username')
        if not username:
            return jsonify({"error": "Invalid token: Username not found"}), 401
    except requests.RequestException:
        return jsonify({"error": "Invalid or expired token"}), 401

    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    required_fields = ['number', 'date', 'line', 'start', 'end', 'traintype', 'notes', 'hidemessage', 'username']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    # Extract data
    number = data['number'].strip().upper()
    date = data['date'].strip().lower()
    line = data['line']
    start = data['start'].title()
    end = data['end'].title()
    traintype = data['traintype']
    notes = data['notes'].strip()
    hidemessage = data['hidemessage']
    username = data['username']

    # Process the train log
    try:
        log_id = process_train_log(username, line, number, start, end, date, traintype, notes)
        response = jsonify({"logId": log_id, "message": "Train logged successfully"})
        response.headers['Access-Control-Allow-Origin'] = '*'
        return response
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

# Train logging logic (adapted from Discord bot)
def process_train_log(username, line, number, start, end, date, traintype, notes):
    # Date handling
    if date == 'today':
        savedate = time.strftime("%Y-%m-%d", time.localtime())
    else:
        try:
            savedate = time.strptime(date, "%d/%m/%Y")
            savedate = time.strftime("%Y-%m-%d", savedate)
        except ValueError:
            raise ValueError(f"Invalid date: '{date}'. Use 'today' or 'DD/MM/YYYY' format.")

    # Train type and set logic
    set = 'Unknown'
    type = 'Unknown'

    if traintype != 'auto':
        type = traintype
        if traintype == "Tait":
            set = '381M-208T-230D-317M'
        else:
            # check if its a known train type and find the set, but if its not known just use the number
            checkTT = trainType(number.upper())
            if checkTT == traintype:
                set = setNumber(number.upper())
                if set == None:
                    set = traintype
            else:
                set = number.upper()
    else:
        # if the user puts a vlocity with he letters VL
        if number.upper().startswith('VL') and len(number) == 6:
            print('vlocity with vl')
            number = number.strip('VL').replace(' ', '')
        
        # checking if train number is valid
        if number != 'Unknown':
            set = setNumber(number.upper())
        if set == None:
            raise ValueError(f'Invalid train number: `{number.upper()}`')
        type = trainType(number.upper())

    # Clean notes
    if notes:
        notes = re.sub(r'[^\x00-\x7F]+', '', notes)  # Remove emojis
        notes = notes.replace('\n', ' ').strip()
        notes = f'"{notes}"'  # Quote for CSV compatibility

    # Generate log ID and save to CSV
    log_id = addTrain(username, set, type, savedate, line, start.title(), end.title(), notes)
    return log_id

if __name__ == '__main__':
    app.run(debug=True)