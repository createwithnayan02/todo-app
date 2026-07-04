
function markDone(id) {
    fetch(`/done/${id}`)
        .then(() => location.reload());
}

function deleteTask(id) {
    fetch(`/delete/${id}`)
        .then(() => location.reload());
}

function openSidebar() {
    document.getElementById("sidebar").style.width = "250px";
}

function closeSidebar() {
    document.getElementById("sidebar").style.width = "0";
}

const textarea = document.querySelector(".task-textarea");

textarea.addEventListener("input", function () {
    this.style.height = "auto";
    this.style.height = this.scrollHeight + "px";
});