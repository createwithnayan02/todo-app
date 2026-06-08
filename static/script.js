

function markDone(id) {
    fetch(`/done/${id}`)
        .then(() => location.reload());
}

function deleteTask(id) {
    fetch(`/delete/${id}`)
        .then(() => location.reload());
}
