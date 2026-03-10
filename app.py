from db import init_db
from taskstore import TaskStore
from flask import Flask, request, jsonify
from datetime import datetime
from errors import ApiError, BadRequestError


#Create flask app
app = Flask(__name__)
store = TaskStore()

#Ensure database and tables exist before requests are made
init_db()

#Turn API exceptions into JSON
@app.errorhandler(ApiError)
def handle_api_error(error: ApiError):
    return jsonify({"error": error.message}), error.status_code

#Catch all other unexpected crashes
@app.errorhandler(Exception)
def handle_unexpected_error(error: Exception):
    app.logger.exception(error) #logs the full traceback server side
    return jsonify({"error": "internal server error"}), 500 #500 code based off flask docs

#Route to create a task
@app.post("/tasks")
def create_task():
    data = request.get_json() #Read client JSON body

    if not data:
        raise BadRequestError("Missing JSON body")
    
    text = data.get("text")
    tags = data.get("tags")
    due_str = data.get("due")

    if not isinstance(text, str):
        raise BadRequestError("text must be a string")

    if not isinstance(tags, list):
        raise BadRequestError("tags must be a list")

    if not isinstance(due_str, str):
        raise BadRequestError("due must be a string in ISO format")

    try:
        due = datetime.fromisoformat(due_str)
    except ValueError:
        raise BadRequestError("invalid due date format")

    task_id = store.create_task(text, tags, due)
    return jsonify({"id": task_id}), 201

#Route to get one task
@app.get("/task/<int:task_id>/")
def get_task(task_id: int):
    task = store.get_task(task_id)
    return jsonify(task.to_dict()), 200

#Route to get all tasks
@app.get("/task/")
def get_all_tasks():
    tasks = store.get_all_tasks()
    serialized = [] #tasks in dict format
    for task in tasks:
        serialized.append(task.to_dict())
    return jsonify(serialized), 200

#Route to delete task by id
@app.delete("/task/<int:task_id>/")
def delete_task(task_id: int):
    store.delete_task(task_id)
    return jsonify({"message": "task deleted"}), 200

#Route to get task by tag
@app.get("/tag/<string:tag>/")
def get_tasks_by_tag(tag: str):
    tasks = store.get_tasks_by_tag(tag)
    serialized = [] #tasks in dict format
    for task in tasks:
        serialized.append(task.to_dict())
    return jsonify(serialized), 200

#Route to get tasks by due date
@app.get("/due/<int:year>/<int:month>/<int:day>/")
def get_tasks_by_due_date(year: int, month: int, day: int):
    tasks = store.get_tasks_by_due_date(year, month, day)
    serialized = [] #tasks in dict format
    for task in tasks:
        serialized.append(task.to_dict())
    return jsonify(serialized), 200

#Route to update a task by id
@app.put("/task/<int:task_id>/")
def update_task(task_id: int):
    data = request.get_json() #Read client JSON body

    if not data:
        raise BadRequestError("Missing JSON body")

    text = data.get("text")
    tags = data.get("tags")
    due_str = data.get("due")

    if not isinstance(text, str):
        raise BadRequestError("text must be a string")

    if not isinstance(tags, list):
        raise BadRequestError("tags must be a list")

    if not isinstance(due_str, str):
        raise BadRequestError("due must be a string in ISO format")
    
    try:
        due = datetime.fromisoformat(due_str)
    except ValueError:
        raise BadRequestError("invalid due date format")

    store.update_task(task_id, text, tags, due)
    task = store.get_task(task_id)
    return jsonify(task.to_dict()), 200

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
