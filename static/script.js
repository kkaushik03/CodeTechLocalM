let token = '';

document.getElementById('login-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    const response = await fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    if (response.ok) {
        token = data.access_token;
        document.getElementById('login-message').innerText = 'Login successful!';
        document.getElementById('login-section').style.display = 'none';
        document.getElementById('upload-section').style.display = 'block';
        document.getElementById('reports-section').style.display = 'block';
        loadReports();
    } else {
        document.getElementById('login-message').innerText = data.msg || 'Login failed';
    }
});

document.getElementById('upload-form').addEventListener('submit', async function (e) {
    e.preventDefault();
    const fileInput = document.getElementById('file-input');
    if (!fileInput.files.length) return;

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('/upload', {
        method: 'POST',
        headers: { 'Authorization': 'Bearer ' + token },
        body: formData
    });

    const data = await response.json();
    if (response.ok) {
        document.getElementById('upload-message').innerText = 'File uploaded and processed. Report ID: ' + data.id;
        loadReports();
    } else {
        document.getElementById('upload-message').innerText = data.error || 'Upload failed';
    }
});

document.getElementById('refresh-reports').addEventListener('click', loadReports);

async function loadReports() {
    const response = await fetch('/reports', {
        headers: { 'Authorization': 'Bearer ' + token }
    });
    const data = await response.json();
    const list = document.getElementById('reports-list');
    list.innerHTML = '';
    if (response.ok) {
        data.reports.forEach(reportId => {
            const li = document.createElement('li');
            li.innerText = reportId;
            list.appendChild(li);
        });
    } else {
        list.innerText = data.error || 'Failed to load reports';
    }
}