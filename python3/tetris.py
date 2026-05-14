from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# --- SAVE SCORE ---
@app.route('/highscore', methods=['POST'])
def save_score():
    try:
        data = request.json
        name = str(data.get('name', 'Anonymous'))[:16]
        score = int(data.get('score', 0))
        with open("highscores.txt", "a") as f:
            f.write(f"{name}: {score}\n")
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# --- GET WORLD RECORD ---
@app.route('/get_high_score', methods=['GET'])
def get_high_score():
    try:
        highest = 0
        leader = "None"
        with open("highscores.txt", "r") as f:
            for line in f:
                if ":" in line:
                    parts = line.strip().split(": ")
                    if len(parts) == 2:
                        name, score = parts[0], int(parts[1])
                        if score > highest:
                            highest, leader = score, name
        return jsonify({"name": leader, "score": highest}), 200
    except FileNotFoundError:
        return jsonify({"name": "No Record", "score": 0}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
