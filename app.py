
from asyncio import tasks
from flask import Flask, render_template, request, redirect
from datetime import datetime
import os
import sqlite3
from datetime import datetime, timedelta
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
        "diet", "protein", "sleep", "cycling", "swimming","eat"
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
        "call mom", "call dad", "visit family","clean",
        "enjoy","bath", "rest","call","create"
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

    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting= "Good Morning"
    elif 12 <= current_hour < 17:
        greeting= "Good Afternoon"
    else:
        greeting= "Good Evening"



    conn = sqlite3.connect("tasks.db")
    cursor =conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks= cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='pending' ")
    pending_tasks = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status='completed'")
    completed_tasks = cursor.fetchone()[0]
  
    if total_tasks > 0:
        completed_percentage = round((completed_tasks / total_tasks) * 100)
    else:
        completed_percentage = 0

    today = datetime.now()
    seven_days_ago = today - timedelta(days=7)
    fourteen_days_ago = today - timedelta(days=14)

    today_str = today.strftime("%Y-%m-%d")
    seven_days_ago_str = seven_days_ago.strftime("%Y-%m-%d")
    fourteen_days_ago_str = fourteen_days_ago.strftime("%Y-%m-%d")

   
 # TODAY'S TASKS

    cursor.execute(
    """
    SELECT COUNT(*)
    FROM tasks
    WHERE DATE(date) = DATE(?)
    """,
    (today_str,)
)

    today_tasks = cursor.fetchone()[0]


# THIS WEEK TOTAL TASKS

    cursor.execute(
    """
    SELECT COUNT(*)
    FROM tasks
    WHERE DATE(date) BETWEEN DATE(?) AND DATE(?)
    """,
    (seven_days_ago_str, today_str)
)

    this_week_tasks = cursor.fetchone()[0]


# THIS WEEK CHART DATA

    cursor.execute(
    """
    SELECT strftime('%w', date), COUNT(*)
    FROM tasks
    WHERE DATE(date) BETWEEN DATE(?) AND DATE(?)
    GROUP BY strftime('%w', date)
    """,
    (seven_days_ago_str, today_str)
)

    this_week_data = cursor.fetchall()

    this_week_dict = dict(this_week_data)
 
    this_week_chart = [
    this_week_dict.get("1", 0),  # Monday
    this_week_dict.get("2", 0),  # Tuesday
    this_week_dict.get("3", 0),  # Wednesday
    this_week_dict.get("4", 0),  # Thursday
    this_week_dict.get("5", 0),  # Friday
    this_week_dict.get("6", 0),  # Saturday
    this_week_dict.get("0", 0)   # Sunday
]


# LAST WEEK TOTAL TASKS

    cursor.execute(
    """
    SELECT COUNT(*)
    FROM tasks
    WHERE DATE(date) BETWEEN DATE(?) AND DATE(?)
    """,
    (fourteen_days_ago_str, seven_days_ago_str)
)

    last_week_tasks = cursor.fetchone()[0]


# LAST WEEK CHART DATA

    cursor.execute(
    """
    SELECT strftime('%w', date), COUNT(*)
    FROM tasks
    WHERE DATE(date) BETWEEN DATE(?) AND DATE(?)
    GROUP BY strftime('%w', date)
    """,
    (fourteen_days_ago_str, seven_days_ago_str)
)

    last_week_data = cursor.fetchall()

    last_week_dict = dict(last_week_data)

    last_week_chart = [
    last_week_dict.get("1", 0),
    last_week_dict.get("2", 0),
    last_week_dict.get("3", 0),
    last_week_dict.get("4", 0),
    last_week_dict.get("5", 0),
    last_week_dict.get("6", 0),
    last_week_dict.get("0", 0)
]


# WEEKLY COMPARISON

   

    if last_week_tasks == 0:
     comparison = "🎉 New activity this week!"

    else:
     task_difference = this_week_tasks - last_week_tasks

    if task_difference > 0:
        comparison = f"📈 Completed {task_difference} more task{'s' if task_difference > 1 else ''} than last week"

    elif task_difference < 0:
          comparison = f"📉 Completed {abs(task_difference)} fewer task{'s' if abs(task_difference) > 1 else ''} than last week"

    else:
        comparison = "🤝 Same number of tasks as last week"

        

    
    work_tasks =0 
    Learning_tasks =0
    Health_tasks = 0
    Shopping_tasks = 0
    Personal_tasks = 0
    Hobby_tasks = 0
    Finance_tasks = 0
    Meeting_tasks = 0
    Design_tasks = 0
    Special_tasks =0
    Other_tasks = 0

    cursor.execute("SELECT category, COUNT(*) FROM tasks GROUP BY category")

    rows = cursor.fetchall()
    print(rows)
    cursor.execute("SELECT COUNT(*) FROM tasks")
    print(total_tasks)

    for row in rows:
        if row[0] =="Learning":
            Learning_tasks = row[1]
        elif row[0] == "Work":
            work_tasks = row[1]
        elif row[0] == "Health":
            Health_tasks = row[1]
        elif row[0] == "Shopping":
            Shopping_tasks = row[1]
        elif row[0] == "Personal":
            Personal_tasks = row[1]
        elif row[0] == "Hobby":
            Hobby_tasks = row[1]
        elif row[0] == "Finance":
            Finance_tasks = row[1]
        elif row[0] == "Meeting":
            Meeting_tasks = row[1]
        elif row[0] == "Design":
            Design_tasks = row[1]
        elif row[0] == "Special Event":
            Special_tasks = row[1]
        elif row[0] == "Other":
            Other_tasks = row[1]

    category_chart = [
        Learning_tasks,
        work_tasks,
        Personal_tasks,
        Health_tasks,
        Shopping_tasks,
        Hobby_tasks,
        Finance_tasks,
        Meeting_tasks,
        Design_tasks,
        Special_tasks,
        Other_tasks
]
    #achivement 
    achievements_status = [
    ("🎯 First Task", total_tasks >= 1),
    ("🔥 Getting Things Done", completed_tasks >= 10),
    ("⭐ Productivity Pro", completed_tasks >= 25),
    ("🚀 Task Champion", completed_tasks >= 50),
    ("💯 Completed 100 Tasks", completed_tasks >= 100),
    ("👑 FlowDo Master", completed_tasks >= 250)
    ]

    
        
    conn.close()
    
   
    return render_template(
        "dashboard.html",
        greeting=greeting,
        total_tasks=total_tasks,
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks,
        completed_percentage=completed_percentage,
        today_tasks=today_tasks,
        this_week_tasks=this_week_tasks,
        last_week_tasks=last_week_tasks,
        comparison=comparison,
        this_week_chart = this_week_chart,
        last_week_chart =last_week_chart,
        category_chart=category_chart,
        achievements_status = achievements_status
    )
       

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


