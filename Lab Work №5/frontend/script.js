const API_URL = 'http://localhost:5000/api/events';

async function loadEvents() {
    const response = await fetch(API_URL);
    const events = await response.json();
    const list = document.getElementById('events-list');
    list.innerHTML = '';
    events.forEach(event => {
        const div = document.createElement('div');
        div.className = 'event';
        div.innerHTML = `
            <h3>${event.name}</h3>
            <p><strong>Date:</strong> ${event.date}</p>
            <p><strong>Location:</strong> ${event.location}</p>
            <p>${event.description}</p>
            <button onclick="deleteEvent(${event.id})">Delete</button>
        `;
        list.appendChild(div);
    });
}

document.getElementById('event-form').addEventListener('submit', async (e) => {
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
    loadEvents();
    e.target.reset();
});

async function deleteEvent(id) {
    await fetch(`${API_URL}/${id}`, { method: 'DELETE' });
    loadEvents();
}

loadEvents();
