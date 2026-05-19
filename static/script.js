const input = document.getElementById("task-input");
const addBtn = document.getElementById("add-btn");
const taskList = document.querySelector('ul');

// Load tasks from LocalStorage
let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

// Display tasks on screen
function displayTasks() {
    taskList.innerHTML = "";

    tasks.forEach((task, index) => {
        // show only pending task
        if (task.status === "completed")return;

        const li = document.createElement("li");
        li.textContent = task.title;
        // done button 
        const doneBtn = document.createElement("button");
        doneBtn.textContent="done";
        doneBtn.className="done-btn";
        doneBtn.onclick = () => markDone(index);

        // delete button
        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "Delete";
        deleteBtn.className = "delete-btn";
        deleteBtn.onclick = () => deleteTask(index);

        li.appendChild(doneBtn);
        li.appendChild(deleteBtn)
        taskList.appendChild(li);
    });
}

// Add new task
addBtn.addEventListener("click", () => {
    if (input.value === "") return;

    const newTask = {
        title: input.value,
        status: "pending",
        createdAt: new Date().toLocaleString(),
        completedAt: null
    };

    tasks.push(newTask);
    localStorage.setItem("tasks", JSON.stringify(tasks));

    input.value = "";
    displayTasks();
});

// Delete task , mark done


function markDone(id) {
    fetch(`/done/${id}`)
        .then(() => location.reload());
}

function deleteTask(id) {
    fetch(`/delete/${id}`)
        .then(() => location.reload());
}
