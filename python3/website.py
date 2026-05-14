from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os

app = Flask(__name__)
CORS(app) # This allows GitHub Pages to talk to your Pi

DATA_FILE = "database.json"

# Initialize database file if it's missing
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({"admin": {"code": "999", "coins": 999}, "users": {}}, f)

def load_data():
    with open(DATA_FILE, "r") as f: return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f, indent=4)

@app.route('/')
def home():
    return "API is running! Connect your GitHub Pages site to this URL."

@app.route('/login', methods=['POST'])
def login():
    data = load_data()
    req = request.json
    user, code = req.get("user"), req.get("code")
    
    if user == "admin" and code == data["admin"]["code"]:
        return jsonify({"status": "success", "role": "admin"})
    if user in data["users"] and data["users"][user]["code"] == code:
        return jsonify({"status": "success", "role": "user", "coins": data["users"][user]["coins"]})
    return jsonify({"status": "fail"}), 401

@app.route('/admin/update-coins', methods=['POST'])
def update_coins():
    data = load_data()
    req = request.json
    if req.get("admin_user") != "admin": return jsonify({"error": "Unauthorized"}), 403
    
    target = req.get("target_user")
    amount = int(req.get("amount", 0))

    if target not in data["users"]:
        data["users"][target] = {"code": "123", "coins": 0}
    
    data["users"][target]["coins"] = max(0, data["users"][target]["coins"] + amount)
    save_data(data)
    return jsonify({"message": f"Updated {target}'s coins!"})

@app.route('/process-url', methods=['POST'])
def process():
    data = load_data()
    req = request.json
    user, target_url = req.get("user"), req.get("url")

    if user in data["users"] and data["users"][user]["coins"] > 0:
        data["users"][user]["coins"] -= 1
        save_data(data)
        permalink = f"https://www.croxyproxy.com{target_url}"
        return jsonify({"permalink": permalink})
    return jsonify({"error": "No coins remaining"}), 403

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
