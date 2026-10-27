const form = document.querySelector('#login-form'), dashboard = document.querySelector('#dashboard');
async function refresh() {
  const response = await fetch('/api/session');
  const {authenticated} = await response.json();
  form.hidden = authenticated; dashboard.hidden = !authenticated;
}
form.onsubmit = async event => {
  event.preventDefault();
  const error = document.querySelector('#login-error'); error.textContent = '';
  try {
    const response = await fetch('/api/login', {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({username:form.username.value,password:form.password.value})});
    const data = await response.json();
    if (!response.ok) error.textContent = data.error;
    else await refresh();
  } catch (_) { error.textContent = 'Сервер недоступен'; }
};
document.querySelector('#logout').onclick = async () => {
  await fetch('/api/logout', {method:'POST', headers:{'Content-Type':'application/json'}, body:'{}'});
  form.reset(); await refresh();
};
refresh();
