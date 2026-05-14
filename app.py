<<<<<<< HEAD
from flask import Flask, render_template, request, redirect
from datetime import datetime
import os

app = Flask(__name__)

FILE_NAME = "text.txt"


def read_tasks():
    if not os.path.exists(FILE_NAME):
        return []
    with open(FILE_NAME, "r") as file:
        return file.readlines()


def add_task_to_file(task):
    with open(FILE_NAME, "a") as file:
        file.write(task + "\n")


@app.route("/")
def splash():
    return render_template("splash.html")   # 👈 splash back


@app.route("/home")
def home():
    raw_tasks = read_tasks()
    tasks = []

    for task in raw_tasks:
        parts = task.strip().split("|")
        if len(parts) == 4:
            tasks.append({
                "name": parts[0],
                "category": parts[1],
                "status": parts[2],
                "date": parts[3]
            })

    return render_template("home.html", tasks=tasks)


from datetime import datetime

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    category = request.form.get("category")

    if task and category:
        date = datetime.now().strftime("%Y-%m-%d")
        new_task = f"{task}|{category}|pending|{date}"
        add_task_to_file(new_task)

    return redirect("/home")
    


if __name__ == "__main__":
    app.run(debug=True)
=======
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

FILE_NAME = "text.txt"


# Read tasks from file
def read_tasks():
    with open(FILE_NAME, "r") as file:
        return file.readlines()


# Write one task to file
def add_task_to_file(task):
    with open(FILE_NAME, "a") as file:
        file.write(task + "\n")


@app.route("/")
def index():
    tasks = read_tasks()
    tasks = [task.strip() for task in tasks]  # remove \n
    return render_template("index.html", tasks=tasks)


@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        add_task_to_file(task)
    return redirect("/")
    

if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 99d6e7c1718d9580bfa65baf8e5a75eadc45c4e6
