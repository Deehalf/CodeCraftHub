"""
CodeCraftHub - Simple Flask REST API using a JSON file as storage.

Features:
- Full CRUD for "courses"
- Data stored in courses.json (auto-created if missing)
- Basic validation and helpful error messages
"""

import json
import os
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)

DATA_FILE = "courses.json"
VALID_STATUSES = ["Not Started", "In Progress", "Completed"]


# -----------------------------
# Helper functions for JSON I/O
# -----------------------------

def load_courses():
    """
    Load all courses from the JSON file.
    If the file does not exist, create it with an empty list.
    """
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "w") as f:
                json.dump([], f)
        except OSError:
            # If we can't create the file, return an empty list
            # and let the API respond with an error later if needed.
            return []

    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        # If file can't be read or JSON is corrupted, treat as empty list
        return []


def save_courses(courses):
    """
    Save the list of courses to the JSON file.
    Raises an exception if writing fails.
    """
    try:
        with open(DATA_FILE, "w") as f:
            json.dump(courses, f, indent=4)
    except OSError as e:
        # Re-raise so the route can handle it and return a proper error
        raise e


def get_next_id(courses):
    """
    Generate the next course ID.
    If there are no courses, start at 1.
    Otherwise, take the max existing ID and add 1.
    """
    if not courses:
        return 1
    return max(course["id"] for course in courses) + 1


def validate_course_payload(data, require_all_fields=True):
    """
    Validate the incoming JSON payload for a course.

    - require_all_fields=True: used for POST (all fields required)
    - require_all_fields=False: used for PUT (can update partially, but here
      we still require all main fields to keep it simple for beginners).

    Returns:
        (is_valid: bool, error_message: str or None)
    """
    required_fields = ["name", "description", "target_date", "status"]

    # Check required fields
    if require_all_fields:
        missing = [field for field in required_fields if field not in data]
        if missing:
            return False, f"Missing required fields: {', '.join(missing)}"

    # Validate status if present
    status = data.get("status")
    if status is not None and status not in VALID_STATUSES:
        return False, (
            f"Invalid status value. Must be one of: {', '.join(VALID_STATUSES)}"
        )

    # Validate target_date format if present
    target_date = data.get("target_date")
    if target_date is not None:
        try:
            datetime.strptime(target_date, "%Y-%m-%d")
        except ValueError:
            return False, "Invalid target_date format. Use YYYY-MM-DD."

    return True, None


# -----------------------------
# REST API endpoints
# Base path: /api/courses
# -----------------------------

@app.route("/api/courses", methods=["POST"])
def create_course():
    """
    Create a new course.
    Expected JSON body:
    {
        "name": "Course name",
        "description": "Course description",
        "target_date": "YYYY-MM-DD",
        "status": "Not Started" | "In Progress" | "Completed"
    }
    """
    # Ensure we received JSON
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()

    # Validate payload
    is_valid, error_msg = validate_course_payload(data, require_all_fields=True)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    courses = load_courses()
    new_course = {
        "id": get_next_id(courses),
        "name": data["name"],
        "description": data["description"],
        "target_date": data["target_date"],
        "status": data["status"],
        # created_at is auto-generated timestamp in ISO format
        "created_at": datetime.utcnow().isoformat()
    }

    courses.append(new_course)

    try:
        save_courses(courses)
    except OSError:
        return jsonify({"error": "Failed to save course data"}), 500

    return jsonify(new_course), 201


@app.route("/api/courses", methods=["GET"])
def get_courses():
    """
    Get all courses.
    """
    courses = load_courses()
    return jsonify(courses), 200


@app.route("/api/courses/stats", methods=["GET"])
def get_course_stats():
    """
    Get course statistics:
    - Total courses
    - Number of courses by status
    """
    courses = load_courses()

    by_status = {status: 0 for status in VALID_STATUSES}
    for course in courses:
        status = course.get("status")
        if status in by_status:
            by_status[status] += 1

    stats = {
        "total_courses": len(courses),
        "by_status": by_status,
    }

    return jsonify(stats), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
def get_course(course_id):
    """
    Get a specific course by ID.
    """
    courses = load_courses()
    course = next((c for c in courses if c["id"] == course_id), None)

    if course is None:
        return jsonify({"error": "Course not found"}), 404

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    """
    Update an existing course by ID.
    Expected JSON body (all fields required for simplicity):
    {
        "name": "...",
        "description": "...",
        "target_date": "YYYY-MM-DD",
        "status": "Not Started" | "In Progress" | "Completed"
    }
    """
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400

    data = request.get_json()

    # Validate payload
    is_valid, error_msg = validate_course_payload(data, require_all_fields=True)
    if not is_valid:
        return jsonify({"error": error_msg}), 400

    courses = load_courses()
    for i, course in enumerate(courses):
        if course["id"] == course_id:
            # Keep created_at and id, update the rest
            courses[i] = {
                "id": course["id"],
                "name": data["name"],
                "description": data["description"],
                "target_date": data["target_date"],
                "status": data["status"],
                "created_at": course["created_at"],
            }

            try:
                save_courses(courses)
            except OSError:
                return jsonify({"error": "Failed to save course data"}), 500

            return jsonify(courses[i]), 200

    return jsonify({"error": "Course not found"}), 404


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    """
    Delete a course by ID.
    """
    courses = load_courses()
    new_courses = [c for c in courses if c["id"] != course_id]

    if len(new_courses) == len(courses):
        # No course was removed → ID not found
        return jsonify({"error": "Course not found"}), 404

    try:
        save_courses(new_courses)
    except OSError:
        return jsonify({"error": "Failed to save course data"}), 500

    return jsonify({"message": "Course deleted successfully"}), 200


# -----------------------------
# Entry point
# -----------------------------

if __name__ == "__main__":
    # debug=True is useful for development; remove or set to False in production
    app.run(debug=True)
