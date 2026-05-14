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

// Delete task
function deleteTask(index) {
    tasks.splice(index, 1);
    localStorage.setItem("tasks", JSON.stringify(tasks));
    displayTasks();
}

// Initial load
displayTasks();

function  markDone(index) {
    tasks[index].status="completed";
    tasks[index].completedAt= new Date().toLocaleDateString();
    
    localStorage.setItem("tasks",JSON.stringify(tasks));
    displayTasks();
    
}
