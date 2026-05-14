const input = document.getElementById("task-input");
const addBtn = document.getElementById("add-btn");
const taskList = document.querySelector('ul');

// Add Delete buttons to existing tasks
document.querySelectorAll('ul li').forEach(li => {
    const deleteBtn = document.createElement('button');
    deleteBtn.textContent = 'Delete';
    deleteBtn.className = 'delete-btn';
    li.appendChild(deleteBtn);
});

// Add new task
addBtn.addEventListener("click", () => {
    if (input.value === "") return;

    const li = document.createElement("li");
    li.textContent = input.value;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.className = "delete-btn";
    li.appendChild(deleteBtn);

    taskList.appendChild(li);
    input.value = "";
});

// Delete task using event delegation
taskList.addEventListener("click", function(e) {
    if (e.target.classList.contains("delete-btn")) {
        e.target.parentElement.remove();
    }
});
