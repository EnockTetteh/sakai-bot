import json
import os

STATE_FILE = "state.json"

def load_state():
    if not os.path.exists(STATE_FILE):
        return {"announcements": [], "assignments": [], "grades": [], "messages": []}
    with open(STATE_FILE, "r") as f:
        return json.load(f)

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def get_new_items(category, current_items, state):
    seen = set(state.get(category, []))
    new = [item for item in current_items if item not in seen]
    return new

def update_state(category, current_items, state):
    # Keep last 100 items per category to avoid file growing too large
    combined = list(set(state.get(category, []) + current_items))
    state[category] = combined[-100:]
    return state
