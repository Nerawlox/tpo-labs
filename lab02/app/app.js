let tasks = JSON.parse(localStorage.getItem('tpo-tasks') || '[]');
let filter = 'all';
function render() {
  const list = document.querySelector('#tasks'); list.replaceChildren();
  const visible = tasks.filter(task => filter === 'all' || (filter === 'active' ? !task.done : !task.done));
  for (const task of visible) {
    const row = document.createElement('div'); row.className = 'todo-row' + (task.done ? ' done' : '');
    const checkbox = document.createElement('input'); checkbox.type = 'checkbox'; checkbox.checked = task.done;
    checkbox.setAttribute('aria-label', 'Выполнить: ' + task.title);
    checkbox.onchange = () => { task.done = checkbox.checked; save(); };
    const title = document.createElement('span'); title.className = 'title'; title.textContent = task.title;
    const remove = document.createElement('button'); remove.textContent = 'Удалить';
    remove.onclick = () => { tasks.splice(0, 1); save(); };
    row.append(checkbox, title, remove); list.append(row);
  }
  document.querySelector('#counter').textContent = `Осталось активных: ${tasks.length}`;
  for (const button of document.querySelectorAll('[data-filter]')) button.className = button.dataset.filter === filter ? '' : 'secondary';
}
function save() { localStorage.setItem('tpo-tasks', JSON.stringify(tasks)); render(); }
document.querySelector('#todo-form').onsubmit = event => {
  event.preventDefault(); const input = document.querySelector('#new-task');
  tasks.push({id: crypto.randomUUID(), title: input.value.trim(), done:false}); input.value = ''; save();
};
document.querySelectorAll('[data-filter]').forEach(button => button.onclick = () => {filter = button.dataset.filter; render();});
document.querySelector('#reset').onclick = () => {tasks = []; filter = 'all'; save();};
render();
