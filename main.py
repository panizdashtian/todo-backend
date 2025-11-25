from flask import Flask, request, jsonify

app = Flask(__name__)

# دیتابیس ساده با لیست
users = {}
tasks = []
task_id_counter = 1


# --- Signup ---
@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if username in users:
        return jsonify({"message": "User already exists"}), 400

    users[username] = password
    return jsonify({"message": "Signup successful"}), 201


# --- Login ---
@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if users.get(username) != password:
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Login successful"}), 200


# --- Create Task ---
@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_counter
    data = request.json

    task = {
        "id": task_id_counter,
        "title": data.get("title"),
        "done": False
    }
    task_id_counter += 1
    tasks.append(task)

    return jsonify(task), 201


# --- Get Tasks ---
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(tasks), 200


# --- Mark as Done ---
@app.route("/tasks/<int:task_id>/done", methods=["PUT"])
def mark_done(task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            return jsonify(task), 200
    return jsonify({"message": "Task not found"}), 404


if __name__ == "__main__":
    app.run(debug=True)