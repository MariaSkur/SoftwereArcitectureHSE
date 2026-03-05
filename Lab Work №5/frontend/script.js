const API_URL = 'http://localhost:5000/api/projects';

async function loadProjects() {
    const response = await fetch(API_URL);
    const projects = await response.json();
    const list = document.getElementById('projects-list');
    list.innerHTML = '';
    projects.forEach(project => {
        const div = document.createElement('div');
        div.className = 'project';
        div.innerHTML = `
            <h3>${project.name}</h3>
            <p><strong>Дата:</strong> ${project.date}</p>
            <p><strong>Площадка:</strong> ${project.location}</p>
            <p>${project.description}</p>
            <button onclick="deleteProject(${project.id})">Удалить</button>
        `;
        list.appendChild(div);
    });
}

document.getElementById('project-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const formData = {
        name: document.getElementById('name').value,
        date: document.getElementById('date').value,
        location: document.getElementById('location').value,
        description: document.getElementById('description').value
    };
    await fetch(API_URL, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData)
    });
    loadProjects();
    e.target.reset();
});

async function deleteProject(id) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    loadProjects();
}

loadProjects();
