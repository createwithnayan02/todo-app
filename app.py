from asyncio import tasks
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

    cursor.execute("SELECT * FROM tasks WHERE status='pending'")
    pending_rows = cursor.fetchall()

    conn.close()

    category_icons = {
        "Learning": "📚",
        "Work": "💼",
        "Health": "🏃",
        "Shopping": "🛒",
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

    return render_template(
        "home.html",
        pending_tasks=pending_tasks,
        pending_count=pending_count
    )

@app.route("/history")

def history():
    conn = sqlite3.connect("tasks.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM tasks WHERE status='completed' ")
    completed_rows = cursor.fetchall()

    conn.close()

    category_icons = {
        "Learning": "📚",
        "Work": "💼",
        "Health": "🏃",
        "Shopping": "🛒",
        "Personal": "🏠",
        "Hobby": "🎨",
        "Finance": "💰",
        "Meeting": "📅",
        "Design": "🖌️",
        "Special Event": "🎉",
        "Other": "📌"
    }

    completed_tasks = []
    for row in completed_rows:
        completed_tasks.append({
            "id": row[0],
            "name": row[1],
            "category": row[2],
            "status": row[3],
            "date": row[4],
            "icon": category_icons.get(row[2], "📌")
        })
        completed_count = len(completed_tasks)

    return render_template("history.html", completed_tasks=completed_tasks,
                            completed_count=completed_count)

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


CATEGORY_KEYWORDS = {

    "Learning": [
        "study", "learn", "learning", "exam", "test", "assignment",
        "homework", "college", "school", "class", "lecture",
        "course", "tutorial", "practice", "revision", "java",
        "python", "c++", "sql", "coding", "programming",
        "project", "research", "book", "notes", "reading"
    ],

    "Work": [
        "work", "office", "client", "project", "report",
        "deadline", "presentation", "document", "email",
        "task", "meeting notes", "proposal", "job",
        "internship", "resume", "linkedin", "career"
    ],

    "Meeting": [
        "meeting", "call", "zoom", "discussion",
        "conference", "interview", "appointment",
        "standup", "review meeting", "team meeting"
    ],

    "Health": [
        "gym", "exercise", "workout", "run", "running",
        "walk", "walking", "yoga", "doctor", "hospital",
        "medicine", "meditation", "fitness", "health",
        "diet", "protein", "sleep", "cycling", "swimming"
    ],

    "Shopping": [
        "buy", "purchase", "shopping", "shop", "order",
        "milk", "groceries", "vegetables", "fruits",
        "market", "mall", "amazon", "flipkart",
        "clothes", "shoes", "laptop", "phone",
        "grocery", "food", "snacks", "book online"
    ],

    "Finance": [
        "bill", "payment", "bank", "salary", "upi",
        "investment", "stock", "mutual fund", "sip",
        "money", "budget", "tax", "insurance",
        "emi", "loan", "rent", "electricity bill", "bill",
        "recharge", "wallet"
    ],

    "Personal": [
        "family", "mom", "mother", "dad", "father",
        "brother", "sister", "friend", "home",
        "clean room", "house", "personal",
        "call mom", "call dad", "visit family"
    ],

    "Hobby": [
        "dance", "dancing", "guitar", "music",
        "painting", "drawing", "art", "singing",
        "photography", "gaming", "game", "reading novel",
        "writing", "poetry", "sketch", "craft"
    ],

    "Special Event": [
        "birthday", "wedding", "anniversary",
        "celebration", "party", "festival",
        "event", "ceremony", "function",
        "engagement", "holiday"
    ],

    "Design": [
        "design", "ui", "ux", "wireframe",
        "prototype", "figma", "logo",
        "poster", "banner", "mockup",
        "illustration"
    ],

    "Other": []
}

def get_category(task):
    task = task.lower()

    for category, keywords in CATEGORY_KEYWORDS.items():

        for keyword in keywords:

            if keyword in task:
                return category

    return "Other"

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

    conn.commit()
    conn.close()

    return redirect("/home")


@app.route("/add", methods=["POST"])
def add():

    tasks_text = request.form.get("tasks")

    if tasks_text:

        task_list = tasks_text.split("\n")

        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect("tasks.db")
        cursor = conn.cursor()

        for task in task_list:

            task = task.strip()

            if task:

                category = get_category(task)

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

