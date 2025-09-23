from flask import Flask, request, jsonify
from models import ToDoList, Task

app = Flask(__name__)
td = ToDoList()

@app.route("/tasks", methods=["GET"])
def list_tasks():
    return jsonify([t.to_row() for t in td.list()])

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    t = Task.create(
        data.get("title", ""),
        data.get("description", ""),
        data.get("priority", 2),
        data.get("due_date", "")
    )
    td.add(t)
    return jsonify(t.to_row()), 201

if __name__ == "__main__":
    app.run(debug=True)