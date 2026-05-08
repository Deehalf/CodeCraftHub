import json
import os

DATA_FILE = "courses.json"

def load_courses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_courses(courses):
    with open(DATA_FILE, "w") as f:
        json.dump(courses, f, indent=4)
