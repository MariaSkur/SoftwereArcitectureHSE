document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('project-form');
    const projectsList = document.getElementById('projects-list');
    const API_URL = '/api/projects'; // проксируется через nginx

    // Загружаем все проекты при старте
    fetchProjects();

    // Обработчик отправки формы
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        const name = document.getElementById('name').value;
        const date = document.getElementById('date').value;
        const location = document.getElementById('location').value;
        const description = document.getElementById('description').value;

        const project = { name, date, location, description };

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(project)
            });
            if (!response.ok) throw new Error('Ошибка при добавлении');
            const newProject = await response.json();
            // Очистить форму
            form.reset();
            // Обновить список
            await fetchProjects();
        } catch (err) {
            console.error(err);
            alert('Не удалось добавить проект');
        }
    });

    // Функция загрузки проектов и отображения
    async function fetchProjects() {
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error('Ошибка загрузки');
            const projects = await response.json();
            renderProjects(projects);
        } catch (err) {
            console.error(err);
            projectsList.innerHTML = '<p>Не удалось загрузить проекты</p>';
        }
    }

    // Отображение списка проектов
    function renderProjects(projects) {
        if (!projects.length) {
            projectsList.innerHTML = '<p>Нет проектов. Добавьте первый!</p>';
            return;
        }
        projectsList.innerHTML = projects.map(project => `
            <div class="project-item">
                <h3>${escapeHtml(project.name)}</h3>
                <p><strong>Дата:</strong> ${escapeHtml(project.date)}</p>
                <p><strong>Место:</strong> ${escapeHtml(project.location)}</p>
                <p><strong>Описание:</strong> ${escapeHtml(project.description)}</p>
            </div>
        `).join('');
    }

    // Простая защита от XSS
    function escapeHtml(str) {
        if (!str) return '';
        return str.replace(/[&<>]/g, function(m) {
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        });
    }
});
