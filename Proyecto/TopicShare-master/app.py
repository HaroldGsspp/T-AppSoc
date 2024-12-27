from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory data storage
tasks = []
comments = []

# Route: Create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    task_id = len(tasks) + 1
    task = {
        "id": task_id,
        "title": data.get("title"),
        "description": data.get("description"),
        "assigned_to": data.get("assigned_to"),
        "status": "pending"
    }
    tasks.append(task)
    return jsonify(task), 201

# Route: Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks), 200

# Route: Add a comment to a task
@app.route('/tasks/<int:task_id>/comments', methods=['POST'])
def add_comment(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.get_json()
    comment_id = len(comments) + 1
    comment = {
        "id": comment_id,
        "task_id": task_id,
        "user": data.get("user"),
        "comment": data.get("comment"),
        "timestamp": datetime.utcnow().isoformat()
    }
    comments.append(comment)
    return jsonify(comment), 201

# Route: Get all comments for a task
@app.route('/tasks/<int:task_id>/comments', methods=['GET'])
def get_comments(task_id):
    task_comments = [c for c in comments if c['task_id'] == task_id]
    return jsonify(task_comments), 200

# Microservice: Simulate email notifications
@app.route('/notify', methods=['POST'])
def notify():
    data = request.get_json()
    email = data.get("email")
    message = data.get("message")
    print(f"Sending email to {email}: {message}")
    return jsonify({"status": "Email sent successfully"}), 200

if __name__ == '__main__':
    app.run(debug=True)