const historyList = document.getElementById("history-list");

let tasks = JSON.parse(localStorage.getItem("tasks")) || [];

function displayHistory() {
    historyList.innerHTML = "";

    tasks.forEach(task =>{
        if (task.status ==="completed"){
            const li = document.createElement("li");

            
           li.innerHTML = `
                <strong>${task.title}</strong><br>
                Created: ${task.createdAt}<br>
                Completed: ${task.completedAt}
            `;
        historyList.appendChild(li);
        }
    })
}
displayHistory();