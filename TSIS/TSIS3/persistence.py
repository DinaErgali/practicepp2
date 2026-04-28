import json
import os

SETTINGS_FILE = "settings.json"
LEADERBOARD_FILE = "leaderboard.json"

def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"sound": True, "color": "red", "difficulty": "medium"}
    with open(SETTINGS_FILE) as f:
        return json.load(f)

def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_scores():
    if not os.path.exists(LEADERBOARD_FILE):
        return []
    with open(LEADERBOARD_FILE) as f:
        return json.load(f)

def save_score(name, score, distance):
    scores = load_scores()
    scores.append({"name": name, "score": score, "distance": distance})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(scores, f, indent=4)