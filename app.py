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
