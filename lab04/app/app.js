const form = document.querySelector('#contact-form');
form.onsubmit = async event => {
  event.preventDefault();
  const success = document.querySelector('#success'); success.hidden = true;
  for (const field of ['name','email','message']) document.querySelector(`#${field}-error`).textContent = '';
  try {
    const response = await fetch('/api/contact', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(Object.fromEntries(new FormData(form)))});
    const data = await response.json();
    if (!response.ok) {
      for (const [field,text] of Object.entries(data.errors || {})) document.querySelector(`#${field}-error`).textContent = text;
    } else { success.textContent = data.message; success.hidden = false; }
  } catch (_) {document.querySelector('#message-error').textContent = 'Сервер недоступен';}
};
