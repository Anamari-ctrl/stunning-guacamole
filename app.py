import json

from flask import Flask
from flask import request

app = Flask(__name__)

tasks = {
    0: {
        "id": 0,
        "description": "clean the horse",
        "done": False
    },
    1: {
        "id": 1,
        "description": "feed the dog",
        "done": False
    }
}

task_id_counter = 2


@app.route("/")
@app.route("/tasks/")
def get_tasks():
    result = {
        "success": True,
        "data": list(tasks.values())
    }
    return json.dumps(result), 200


# for creation, we use POST
@app.route("/tasks", methods=["POST"])
def create_task():
    global task_id_counter
    body = json.loads(request.data)
    description = body.get("description",
                           "no description")  # <- better because doesn't throw error, it returns None if there is no key decription,
    # also we can give default message, another way would be body["description"] but it throws error
    task = {"id": task_id_counter, "description": description, "done": False}
    tasks[task_id_counter]= task
    task_id_counter += 1
    return json.dumps({"success": True, "data": task}), 201

@app.route("/tasks/<int:task_id>/")
def get_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"success": False, "error": "Task not found"}), 404
    return json.dumps({"success": True, "data": task}), 200

@app.route("/tasks/<int:task_id>/", methods=["POST"])
def update_task(task_id):
    task = tasks.get(task_id)
    if not task:
        return json.dumps({"success": False, "error": "Task not found"}), 404
    body = json.loads(request.data)
    task["description"] = body.get("description", "no updated description")
    task["done"] =



if __name__ == "__main__":
    app.run(debug=True)
