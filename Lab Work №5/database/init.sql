CREATE TABLE IF NOT EXISTS projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,         -- название проекта
    date DATE NOT NULL,                  -- дата мероприятия
    location VARCHAR(255) NOT NULL,       -- площадка / место проведения
    description TEXT                       -- описание, комментарии
);
