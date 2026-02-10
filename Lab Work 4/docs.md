# Лабораторная работа №4
__Тема:__ Проектирование REST API

__Цель работы:__ Получить опыт проектирования программного интерфейса.

# Документация по API
## Общая информация
__Базовый URL API:__ http://127.0.0.1:8000/api/v1 

__Формат данных:__ JSON для запросов и ответов.

__Аутентификация:__ Для большинства операций требуется JWT-токен, передаваемый в заголовке Authorization: Bearer <token>. Исключение — публичные GET-запросы для просмотра площадок.

## Принятые проектные решения:
1. __RESTful-подход:__ Используются стандартные HTTP-методы (GET, POST, PUT, DELETE) и понятные, иерархические пути (endpoints) для ресурсов.
1. __Версионирование API:__ Версия API (v1) включена в URL для обеспечения обратной совместимости при будущих изменениях.
1. __Статус-коды HTTP:__ Используются семантически верные коды ответов (200, 201, 400, 404, 401, 403).
1. __Пагинация и фильтрация:__ Для коллекций реализована пагинация через query-параметры limit и offset. Фильтрация также выполняется через query-параметры.
1. __Единый формат ошибок:__ Все ошибки возвращаются в едином JSON-формате с полями code, message и details.
1. __Идентификаторы ресурсов:__ Используются UUID вместо автоинкрементных ID для безопасности и удобства при распределенной разработке.
1. __Вложенные ресурсы:__ Для логической группировки API для управления доступностью дат (/venues/{id}/availability) и запросами (/venues/{id}/requests) вложены в ресурс площадки.
1. __Частичное обновление:__ Метод PUT на /venues/{id} реализует логику полной замены ресурса. Для частичного обновления (например, только названия) можно было бы использовать PATCH, но в рамках требований лабораторной ограничимся PUT.


## Реализуемое API для ресурса "Помещения" (Venues)
__1. Получить список площадок (с фильтрацией)__
   - __Метод:__ ```GET```
   - __Путь:__ ```/venues```
   - __Описание:__ Возвращает список площадок с поддержкой фильтрации, сортировки и пагинации. Доступно без аутентификации для публичного просмотра.
   - __Обозначения:__
      - __data__ (array) - массив объектов площадок
      - ```id``` (string, UUID) - уникальный идентификатор площадки
      - ```name``` (string) - название площадки
      - ```type``` (string, enum) - тип помещения
      - ```district``` (string) - район города
      - ```address``` (string) - физический адрес
      - ```capacity``` (integer) - вместимость в количестве человек
      - ```price_per_hour``` (number) - стоимость аренды за час в рублях
      - ```description``` (string) - описание площадки
      - __meta__ (object) - метаинформация о запросе
      - ```total``` (integer) - общее количество площадок в базе
      - ```limit``` (integer) - количество записей на странице
      - ```offset``` (integer) - смещение для пагинации

   - __Тело запроса: Не требуется.__
   - __Успешный ответ (200 OK):__

```json
{
  "data": [
    {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "name": "Культурный центр 'Восток'",
      "type": "conference_hall",
      "district": "Центральный",
      "address": "ул. Ленина, 10",
      "capacity": 200,
      "price_per_hour": 5000,
      "description": "Современный зал с мультимедийным оборудованием."
    }
    // ... другие площадки
  ],
  "meta": {
    "total": 150,
    "limit": 20,
    "offset": 0
  }
}
```
   - __Возможные ошибки:__
      - ```400 Bad Request``` - неверные параметры запроса (например, ```min_capacity=abc```).
     
__2. Создать новую площадку (только для представителей площадок)__
   - __Метод:__ ```POST```
   - __Путь:__ ```/venues```
   - __Описание:__ Создает новую запись о площадке в системе. Требует аутентификации и прав представителя площадки (```role: venue_representative```).
   - __Обозначения:__
      - ```id``` (string, UUID) - уникальный идентификатор площадки
      - ```name``` (string) - название площадки
      - ```type``` (string, enum) - тип помещения
      - ```district``` (string) - район города
      - ```address``` (string) - физический адрес
      - ```capacity``` (integer) - вместимость в количестве человек
      - ```price_per_hour``` (number) - стоимость аренды за час в рублях
      - ```description``` (string) - описание площадки
      - ```equipment``` (array of strings) - массив доступного оборудования
      - ```created_by``` (string, UUID) - идентификатор пользователя-создателя
      - ```created_at``` (string, ISO 8601) - дата и время создания   
   - __Тело запроса (обязательное, JSON):__

```json
{
  "name": "Новая Арт-площадка 'Куб'",
  "type": "loft",
  "district": "Заречный",
  "address": "пр. Мира, 25",
  "capacity": 150,
  "price_per_hour": 7000,
  "description": "Просторный лофт для выставок и вечеринок.",
  "equipment": ["проектор", "звуковая система", "wi-fi"]
}
```
   - __Успешный ответ (201 Created):__

```json
{
  "data": {
    "id": "aa1bb2cc-3d4e-5f6a-7b8c-9d0e1f2a3b4c",
    "name": "Новая Арт-площадка 'Куб'",
    "type": "loft",
    "district": "Заречный",
    "address": "пр. Мира, 25",
    "capacity": 150,
    "price_per_hour": 7000,
    "description": "Просторный лофт для выставок и вечеринок.",
    "equipment": ["проектор", "звуковая система", "wi-fi"],
    "created_by": "user-uuid-here",
    "created_at": "2023-10-27T10:30:00Z"
  }
}
```
   - __Заголовки ответа:__ Location: ```/venues/aa1bb2cc-3d4e-5f6a-7b8c-9d0e1f2a3b4c```

   - __Возможные ошибки:__
      - ```401 Unauthorized``` - отсутствует или неверный токен аутентификации.
      - ```403 Forbidden``` - у пользователя нет прав на создание площадки.
      - ```400 Bad Request``` - невалидные данные (например, отсутствует ```name``` или ```capacity``` не число).

__3. Получить детальную информацию о конкретной площадке__
   - __Метод:__ ```GET```
   - __Путь:__ ```/venues/{id}```
   - __Описание:__ Возвращает полную информацию о площадке по её UUID. Доступно без аутентификации.
   - __Обозначения:__
      - ```id``` (string, UUID) - уникальный идентификатор площадки
      - ```name``` (string) - название площадки
      - ```type``` (string, enum) - тип помещения
      - ```district``` (string) - район города
      - ```address``` (string) - физический адрес
      - ```capacity``` (integer) - вместимость в количестве человек
      - ```price_per_hour``` (number) - стоимость аренды за час в рублях
      - ```description``` (string) - описание площадки
      - ```equipment``` (array of strings) - массив доступного оборудования
      - ```rules``` (string) - правила использования площадки
      - ```contact_phone``` (string) - контактный телефон
      - ```contact_email``` (string) - контактный email
      - ```photos``` (array of strings) - массив URL фотографий
      - ```created_at``` (string, ISO 8601) - дата создания
      - ```updated_at``` (string, ISO 8601) - дата последнего обновления
   - __Параметры пути:__

        - ```id``` (required, UUID): Идентификатор площадки.

   - __Тело запроса:__ Не требуется.

   - __Успешный ответ (200 OK):__
```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "name": "Культурный центр 'Восток'",
    "type": "conference_hall",
    "district": "Центральный",
    "address": "ул. Ленина, 10",
    "capacity": 200,
    "price_per_hour": 5000,
    "description": "Современный зал с мультимедийным оборудованием.",
    "equipment": ["проектор", "экран", "микрофоны", "стол президиума"],
    "rules": "Запрещены мероприятия после 23:00.",
    "contact_phone": "+7 (XXX) XXX-XX-XX",
    "contact_email": "east@culture.ru",
    "photos": ["photo1_url.jpg", "photo2_url.jpg"],
    "created_at": "2023-09-15T14:20:00Z",
    "updated_at": "2023-10-20T09:15:00Z"
  }
}
```
   - __Возможные ошибки:__

       - ```404 Not Found``` - площадка с указанным ID не найдена.

__4. Обновить информацию о площадке (полная замена)__
   - __Метод:__ ```PUT```

   - __Путь:__ ```/venues/{id}```

   - __Описание:__ Полностью обновляет ресурс площадки. Все поля, кроме id и служебных (```created_at```), должны быть переданы в запросе. Требует прав владельца площадки или администратора.

   - __Параметры пути:__

       - ```id``` (required, UUID): Идентификатор площадки.

   - __Тело запроса__ (обязательное, JSON): Аналогично телу запроса для ```POST```, но со всеми текущими значениями полей.

   - __Успешный ответ__ (200 OK): Возвращает обновленный объект площадки (формат аналогичен ответу ```GET /venues/{id}```).

   - __Возможные ошибки:__

       - ```401 Unauthorized```, ```403 Forbidden``` - проблемы с правами.

       - ```404 Not Found``` - площадка не найдена.

```400 Bad Request``` - невалидные данные.

__5. Удалить площадку__
   - __Метод:__ ```DELETE```

   - __Путь:__ ```/venues/{id}```

   - __Описание:__ Помечает площадку как удаленную (soft delete) или удаляет её физически. Требует прав владельца площадки или администратора.

   - __Параметры пути:__

       - ```id``` (required, UUID): Идентификатор площадки.

   - __Тело запроса:__ Не требуется.

   - __Успешный ответ (204 No Content):__ Тело ответа отсутствует.

   - __Возможные ошибки:__

      - ```401 Unauthorized```, ```403 Forbidden``` - проблемы с правами.

      - ```404 Not Found``` - площадка не найдена.

__6. Управление доступностью дат для площадки__
   - __Метод:__ ```POST```

   - __Путь:__ ```/venues/{id}/availability```

   - __Описание:__ Добавляет или обновляет информацию о доступности площадки на конкретную дату. Используется представителями площадок для блокировки/разблокировки дат.

   - __Параметры пути:__

       - ```id``` (required, UUID): Идентификатор площадки.
   - __Обозначения:__
       - ```venue_id``` (string, UUID) - идентификатор площадки
       - ```date``` (string, YYYY-MM-DD) - дата события
       - ```status``` (string, enum) - статус доступности
       - ```reason``` (string, optional) - причина недоступности
       - ```updated_by``` (string, UUID) - идентификатор пользователя
       - ```updated_at``` (string, ISO 8601) - время обновления   

   - __Тело запроса (обязательное, JSON):__

```json
{
  "date": "2023-12-25",
  "status": "unavailable",
  "reason": "Технический перерыв"
}
```
       - ```status```: ```available```, ```unavailable```, ```booked```.

   - __Успешный ответ (201 Created):__

```json
{
  "data": {
    "venue_id": "550e8400-e29b-41d4-a716-446655440000",
    "date": "2023-12-25",
    "status": "unavailable",
    "reason": "Технический перерыв",
    "updated_by": "user-uuid-here",
    "updated_at": "2023-10-27T11:45:00Z"
  }
}
```
   - __Возможные ошибки:__ Стандартные (401, 403, 404, 400).

__7. Создать запрос на бронирование__
   - __Метод:__ ```POST```
   - __Путь:__ ```/api/v1/venue-requests```
   - __Описание:__ Организатор отправляет запрос на бронирование площадки.
   - __Обозначения:__
       - ```id``` (string, UUID) - уникальный идентификатор запроса
       - ```venue_id``` (string, UUID) - идентификатор запрашиваемой площадки
       - ```event_date``` (string, YYYY-MM-DD) - желаемая дата мероприятия
       - ```event_name``` (string) - название мероприятия
       - ```contact_person``` (string) - контактное лицо
       - ```contact_email``` (string) - email организатора
       - ```notes``` (string, optional) - дополнительные заметки
       - ```status``` (string, enum) - статус запроса
       - ```created_at``` (string, ISO 8601) - время создания
       - ```response``` (string or null) - ответ от представителя
   - __Тело запроса (JSON):__

```json
{
  "venue_id": "550e8400-e29b-41d4-a716-446655440000",
  "event_date": "2023-12-25",
  "event_name": "Новогодний корпоратив",
  "contact_person": "Иванов Иван",
  "contact_email": "ivanov@example.com",
  "notes": "Нужна сцена и звуковое оборудование"
}
```

   - __Успешный ответ (201 Created):__

```json
{
  "data": {
    "id": "request-uuid-here",
    "venue_id": "550e8400-e29b-41d4-a716-446655440000",
    "event_date": "2023-12-25",
    "event_name": "Новогодний корпоратив",
    "contact_person": "Иванов Иван",
    "contact_email": "ivanov@example.com",
    "notes": "Нужна сцена и звуковое оборудование",
    "status": "pending",
    "created_at": "2023-11-01T10:30:00Z",
    "response": null
  },
  "message": "Запрос на бронирование успешно создан"
}
```

   - __Ошибки:__
       - ```400 Bad Request``` - площадка не найдена
       - ```422 Unprocessable Entity``` - невалидные данные
    
__8. Создать команду__
   - __Метод:__ ```POST```
   - __Путь:__ ```/api/v1/teams```
   - __Описание:__ Создать новую команду для организации мероприятий.
   - __Поля:__
       - ```name``` (обязательное, string): Название команды (3-100 символов)
       - ```description``` (опциональное, string): Описание команды (максимум 500 символов)
       - ```members``` (обязательное, array): Список участников команды (минимум 1 участник)

   - __Поля участника (TeamMember):__
       - ```user_id``` (обязательное, string): Уникальный идентификатор пользователя
       - ```name``` (обязательное, string): Имя участника (2-50 символов)
       - ```role``` (обязательное, string): Роль в команде. Допустимые значения: organizer, editor, viewer
       - ```email``` (обязательное, string): Email участника (должен быть валидным email)
   - __Тело запроса (JSON):__

```json
{
  "name": "Команда конференции",
  "description": "Организация IT-конференции",
  "members": [
    {
      "user_id": "user-001",
      "name": "Иванов Иван",
      "role": "organizer",
      "email": "ivanov@example.com"
    }
  ]
}
```

   - __Успешный ответ (201 Created):__

```json
{
  "data": {
    "id": "team-uuid-here",
    "name": "Команда конференции",
    "description": "Организация IT-конференции",
    "members": [
      {
        "user_id": "user-001",
        "name": "Иванов Иван",
        "role": "organizer",
        "email": "ivanov@example.com"
      }
    ],
    "created_at": "2023-11-01T11:00:00Z",
    "created_by": "current-user"
  },
  "message": "Команда успешно создана"
}
```
   - __Возможные ошибки:__
      - ```400 Bad Request``` - невалидные данные (например, отсутствует ```name```, пустой список ```members```, невалидный email).
      - ```401 Unauthorized``` - отсутствует или неверный токен аутентификации.
      - ```403 Forbidden``` - у пользователя нет прав на создание команд.
      - ```409 Conflict``` - команда с таким названием уже существует.
      - ```422 Unprocessable Entity``` - неправильный формат JSON или неверные типы данных (например, role не из допустимых значений).
      - ```429 Too Many Requests``` - превышен лимит запросов на создание команд.
      - ```500 Internal Server Error``` - внутренняя ошибка сервера.

## Дополнительные API (для полноты картины системы):
```GET /projects``` - список проектов организатора.

```POST /projects``` - создать новый проект.

```GET /projects/{id}/venues``` - получить площадки, добавленные в проект.

```POST /venues/{id}/requests``` - отправить запрос представителю площадки (от организатора).

```GET /teams``` - список команд пользователя.

```POST /venues/{id}/vote``` - проголосовать за площадку в контексте проекта.

# Реализация # 

<img width="1621" height="1008" alt="image" src="https://github.com/user-attachments/assets/ed785a41-016a-4456-b2e9-036f54b525a4" />

<img width="1619" height="1029" alt="image" src="https://github.com/user-attachments/assets/bd0967d6-9915-4faa-80ba-7d2134641c67" />
<img width="1614" height="1137" alt="image" src="https://github.com/user-attachments/assets/97927757-b585-4af8-b6b3-dfc9cde461f8" />
<img width="1619" height="1079" alt="image" src="https://github.com/user-attachments/assets/9f95817b-0f84-4af5-98c2-3dce4c919bef" />
<img width="1820" height="979" alt="image" src="https://github.com/user-attachments/assets/9518693c-f3c2-4b04-850b-1eebb8eff617" />
<img width="1820" height="977" alt="image" src="https://github.com/user-attachments/assets/4124a623-caaa-4ac8-adf0-a0e033eefa9d" />
<img width="1820" height="987" alt="image" src="https://github.com/user-attachments/assets/10801ce7-2411-4799-9fb7-0288887a7cec" />
<img width="1821" height="972" alt="image" src="https://github.com/user-attachments/assets/378c7e61-ba25-4cbc-8650-b590dbeaea4c" />
<img width="1818" height="975" alt="image" src="https://github.com/user-attachments/assets/297b3957-1485-48bd-ae6e-05fa4616957e" />
<img width="1818" height="970" alt="image" src="https://github.com/user-attachments/assets/cc5806ac-a7b4-4fca-8da3-7f4df0c67a28" />
<img width="1817" height="1022" alt="image" src="https://github.com/user-attachments/assets/0b7a2a45-6e6d-49a7-a7a5-381777d937a4" />


# Тесты #

<img width="1754" height="735" alt="image" src="https://github.com/user-attachments/assets/4ba51b1c-247f-4352-adb6-e13f12ff4313" />
<img width="1759" height="727" alt="image" src="https://github.com/user-attachments/assets/50aa1bca-37cd-4663-a4b1-5b93ee32c9e2" />
<img width="1819" height="1001" alt="image" src="https://github.com/user-attachments/assets/8f5510d0-31f1-493a-a01b-0d03a0e061f8" />

<img width="1807" height="722" alt="image" src="https://github.com/user-attachments/assets/e44814b7-1aeb-4064-bb92-787136f82682" />
<img width="1823" height="917" alt="image" src="https://github.com/user-attachments/assets/babd1382-e883-4b83-8939-d5c050d68bce" />
<img width="1810" height="920" alt="image" src="https://github.com/user-attachments/assets/ddd93a4e-c772-4cfd-a55f-9fe6e120322b" />
<img width="1816" height="922" alt="image" src="https://github.com/user-attachments/assets/9a0339f5-231e-49f6-a59b-dee0ca16dbac" />
<img width="1813" height="884" alt="image" src="https://github.com/user-attachments/assets/2de72753-689f-4e82-8776-3fc920937b04" />
<img width="1815" height="927" alt="image" src="https://github.com/user-attachments/assets/e9d3d7f2-0731-4d54-b865-6fa443c0752e" />
<img width="1816" height="913" alt="image" src="https://github.com/user-attachments/assets/dcd50b91-30b3-4bff-b28a-c1be8f3c1a36" />
<img width="1809" height="922" alt="image" src="https://github.com/user-attachments/assets/f12e18f0-dbe0-41d9-b850-6766b8fafe38" />
<img width="1813" height="910" alt="image" src="https://github.com/user-attachments/assets/2a8090db-2ac0-46e5-b97c-5882aff1e387" />
<img width="1794" height="911" alt="image" src="https://github.com/user-attachments/assets/91025685-b16b-46de-8f89-8a982491e57e" />
<img width="1443" height="849" alt="image" src="https://github.com/user-attachments/assets/438066a8-3948-4357-be9e-bbeefc2c54f3" />
