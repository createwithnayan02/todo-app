from flask import Flask, render_template, request, redirect
from datetime import datetime

app = Flask(__name__)

FILE_NAME = "text.txt"

@app.route("/home")
def home():
    tasks = read_tasks()
    return render_template("home.html", tasks=tasks)


# Read tasks from file
def read_tasks():
    try:
        with open(FILE_NAME, "r") as file:
            return file.readlines()
    except FileNotFoundError:
        return []


# Write task to file
def add_task_to_file(task):
    with open(FILE_NAME, "a") as file:
        file.write(task + "\n")

#splash 
@app.route("/")
def splash():
    return render_template("splash.html")

#add task
@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        date = datetime.now().strftime("%Y-%m-%d")
        new_task = f"{task}|pending|{date}"
        add_task_to_file(new_task)
    return redirect("/home")

if __name__ == "__main__" :
    app.run(debug=True)

