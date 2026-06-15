from flask import Flask, render_template, request, redirect
from datetime import datetime
import os
import sqlite3

app = Flask(__name__)

FILE_NAME = "text.txt"
def init_db():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        category TEXT,
                   
        status TEXT,
        date TEXT
    )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def splash():
    return render_template("splash.html")

@app.route("/add-task")
def add_task_page():
    return render_template("add_task.html")


@app.route("/home")
def home():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE status='pending' ")
    pending_rows = cursor.fetchall()

    cursor.execute("SELECT* FROM tasks WHERE status='completed' ")
    completed_rows =cursor.fetchall()

    conn.close()

    category_icons = {
    "Learning": "📚",
    "Work": "💼",
    "Health": "💪",
    "Shopping": "🛍",
    "Personal": "🏠",
    "Hobby": "🎨",
    "Finance": "💰",
    "Meeting": "📅",
    "Design": "🖌️",
    "Special Event": "🎉",
    "Other": "📌"
}

    pending_tasks = []
    for row in pending_rows:
        pending_tasks.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "status": row[3],
            "date": row[4],
            "icon": category_icons.get(row[2], "📌")
        })
        pending_count = len(pending_tasks)

    completed_tasks=[]
    for row in completed_rows:
        completed_tasks.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "status": row[3],
            "date": row[4],
            "icon": category_icons.get(row[2], "📌")
        })

    return render_template("home.html", pending_tasks=pending_tasks, completed_tasks=completed_tasks, pending_count=pending_count)

@app.route("/done/<int:id>")
def mark_done(id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("UPDATE tasks SET status='completed' WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/home")

@app.route("/delete/<int:id>")
def delete_task(id):
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/home")

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    category = request.form.get("category")
    print("Task:", task)
    print("Category:", category)

    if task:
        category=category or "other"
        date = datetime.now().strftime("%Y-%m-%d")

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO tasks (name, category, status, date) VALUES (?, ?, ?, ?)",
            (task, category, "pending", date)
        )

        conn.commit()
        conn.close()

    return redirect("/home")
    
if __name__ == "__main__":
    init_db()
    app.run(debug=True)

