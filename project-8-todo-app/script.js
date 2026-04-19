// To-Do List App
// Author: Salman Alhidamkara

let tasks = [];

// Load tasks dari localStorage
function loadTasks() {
    const storedTasks = localStorage.getItem('tasks');
    if (storedTasks) {
        tasks = JSON.parse(storedTasks);
    }
    renderTasks();
}

// Simpan tasks ke localStorage
function saveTasks() {
    localStorage.setItem('tasks', JSON.stringify(tasks));
}

// Render daftar tugas
function renderTasks() {
    const taskList = document.getElementById('taskList');
    const filter = document.querySelector('.filter-btn.active').dataset.filter;
    
    let filteredTasks = tasks;
    if (filter === 'active') {
        filteredTasks = tasks.filter(task => !task.completed);
    } else if (filter === 'completed') {
        filteredTasks = tasks.filter(task => task.completed);
    }
    
    if (filteredTasks.length === 0) {
        taskList.innerHTML = '<p style="text-align: center; color: #999;">Belum ada tugas</p>';
    } else {
        taskList.innerHTML = filteredTasks.map(task => `
            <li class="task-item ${task.completed ? 'completed' : ''}" data-id="${task.id}">
                <input type="checkbox" class="task-check" ${task.completed ? 'checked' : ''}>
                <span class="task-text">${escapeHtml(task.text)}</span>
                <button class="edit-btn">✏️</button>
                <button class="delete-btn">🗑️</button>
            </li>
        `).join('');
    }
    
    updateStats();
}

// Escape HTML untuk mencegah XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Update statistik
function updateStats() {
    const total = tasks.length;
    const completed = tasks.filter(task => task.completed).length;
    const active = total - completed;
    
    document.getElementById('stats').innerHTML = `
        Total: ${total} | Selesai: ${completed} | Belum Selesai: ${active}
    `;
}

// Tambah tugas baru
function addTask() {
    const input = document.getElementById('taskInput');
    const text = input.value.trim();
    
    if (text === '') {
        alert('Masukkan tugas terlebih dahulu');
        return;
    }
    
    const newTask = {
        id: Date.now(),
        text: text,
        completed: false
    };
    
    tasks.push(newTask);
    saveTasks();
    renderTasks();
    
    input.value = '';
    input.focus();
}

// Edit tugas
function editTask(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;
    
    const newText = prompt('Edit tugas:', task.text);
    if (newText !== null && newText.trim() !== '') {
        task.text = newText.trim();
        saveTasks();
        renderTasks();
    }
}

// Hapus tugas
function deleteTask(taskId) {
    if (confirm('Yakin ingin menghapus tugas ini?')) {
        tasks = tasks.filter(task => task.id !== taskId);
        saveTasks();
        renderTasks();
    }
}

// Toggle status tugas (selesai/belum)
function toggleTask(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (task) {
        task.completed = !task.completed;
        saveTasks();
        renderTasks();
    }
}

// Event delegation untuk task list
document.getElementById('taskList').addEventListener('click', (e) => {
    const taskItem = e.target.closest('.task-item');
    if (!taskItem) return;
    
    const taskId = parseInt(taskItem.dataset.id);
    
    if (e.target.classList.contains('task-check')) {
        toggleTask(taskId);
    } else if (e.target.classList.contains('edit-btn')) {
        editTask(taskId);
    } else if (e.target.classList.contains('delete-btn')) {
        deleteTask(taskId);
    }
});

// Filter buttons
document.querySelectorAll('.filter-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderTasks();
    });
});

// Add task button
document.getElementById('addBtn').addEventListener('click', addTask);

// Enter key untuk menambah tugas
document.getElementById('taskInput').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        addTask();
    }
});

// Initialize
loadTasks();
