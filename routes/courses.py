from flask import Blueprint, request, jsonify
from services.storage import load_courses, save_courses

courses_bp = Blueprint("courses", __name__)

@courses_bp.get("/courses")
def get_courses():
    return jsonify(load_courses())

@courses_bp.get("/courses/<int:course_id>")
def get_course(course_id):
    courses = load_courses()
    course = next((c for c in courses if c["id"] == course_id), None)
    return jsonify(course or {}), (200 if course else 404)

@courses_bp.post("/courses")
def create_course():
    courses = load_courses()
    new_course = request.json
    new_course["id"] = (courses[-1]["id"] + 1) if courses else 1
    courses.append(new_course)
    save_courses(courses)
    return jsonify(new_course), 201

@courses_bp.put("/courses/<int:course_id>")
def update_course(course_id):
    courses = load_courses()
    for i, c in enumerate(courses):
        if c["id"] == course_id:
            courses[i] = {**c, **request.json}
            save_courses(courses)
            return jsonify(courses[i])
    return jsonify({"error": "Course not found"}), 404

@courses_bp.delete("/courses/<int:course_id>")
def delete_course(course_id):
    courses = load_courses()
    new_courses = [c for c in courses if c["id"] != course_id]
    if len(new_courses) == len(courses):
        return jsonify({"error": "Course not found"}), 404
    save_courses(new_courses)
    return jsonify({"message": "Course deleted"})
