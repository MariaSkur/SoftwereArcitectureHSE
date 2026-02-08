# Диаграмма системного контекста
<img width="721" height="874" alt="image" src="https://github.com/user-attachments/assets/938675db-e67e-4ef5-bbbb-c57a076ec877" />


```PlantUML
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Context.puml

title Системный контекст: Система для организаторов мероприятий

Person(organizer, "Организатор мероприятия", "Основной пользователь системы, планирует мероприятия, формирует команду и бюджет")
Person(team_member, "Участник команды", "Член команды организаторов, участвует в обсуждениях и голосованиях")
Person(venue_admin, "Администратор культурных площадок", "Представитель ДК или государственной площадки, управляет информацией о площадке")

System(system, "Система для организаторов мероприятий", "Обеспечивает поиск площадок, управление бюджетом, командную работу и сбор мнений")

System_Ext(aggregator_api, "Внешние API агрегаторов площадок", "Сервисы типа Авито для поиска коммерческих площадок")
System_Ext(notification_service, "Email/SMS сервис", "Сервис отправки уведомлений")
System_Ext(payment_gateway, "Платежный шлюз", "Сервис обработки онлайн-платежей")

Rel(organizer, system, "Управляет проектами, ищет площадки, формирует бюджет", "HTTPS")
Rel(team_member, system, "Участвует в обсуждениях, голосует, просматривает варианты", "HTTPS")
Rel(venue_admin, system, "Обновляет информацию о площадке, расписание, цены", "HTTPS")
Rel(system, aggregator_api, "Получает данные о доступных коммерческих площадках", "API/HTTPS")
Rel(system, notification_service, "Отправляет уведомления команде", "SMTP/API")
Rel(system, payment_gateway, "Проводит платежи за аренду", "HTTPS")

@enduml
```

# Диаграмма контейнеров с пояснениями по выбору базового архитектурного стиля / архитектуры уровня приложений
## Выбор архитектуры уровня приложений
Выбранная архитектура для Backend API: Многослойная архитектура (Layered Architecture) с элементами Гексагональной архитектуры (Hexagonal Architecture).

Обоснование:
1. Сложность бизнес-логики: Система содержит несколько взаимосвязанных бизнес-процессов:
* Поиск и сравнение площадок с учетом кластеризации
* Формирование и комбинирование вариантов бюджета
* Управление командными взаимодействиями и сбором мнений
* Интеграция с внешними системами (платежи, уведомления)

Многослойная архитектура обеспечивает четкое разделение ответственности между уровнями (контроллеры, сервисы, репозитории), что упрощает поддержку сложной логики.

2. Интеграция с внешними системами: Гексагональный подход (порты и адаптеры) позволяет:
* Изолировать бизнес-логику от деталей интеграции с внешними API
* Легко добавлять новые источники данных о площадках
* Заменять реализацию интеграций (например, перейти на другой платежный шлюз) без изменения бизнес-логики
* Тестировать бизнес-логику с mock-адаптерами

3. Управление транзакциями и согласованностью данных: При работе с бюджетами и командными решениями важна согласованность данных. Многослойная архитектура с четким разделением на:
* Уровень представления (REST контроллеры)
* Уровень бизнес-логики (сервисы)
* Уровень доступа к данным (репозитории)

позволяет корректно управлять транзакционными границами и обеспечивать целостность данных.

4. Тестируемость: Разделение на слои с четкими интерфейсами позволяет:
* Тестировать бизнес-логику изолированно от инфраструктурных деталей
* Использовать модульные и интеграционные тесты на разных уровнях
* Легко создавать тестовые дубликаты для внешних зависимостей

5. Поддержка разных клиентов: Веб-приложение является единственным клиентом, но архитектура позволяет в будущем:
* Добавить мобильное приложение без изменения бизнес-логики
* Предоставлять API для сторонних интеграций
* Создавать различные представления данных для разных ролей пользователей

6. Обработка асинхронных событий: Для обработки событий от Data Processing Service используется паттерн "Observer" через Message Queue, что позволяет:
* Реагировать на обновления данных о площадках в реальном времени
* Обрабатывать результаты кластеризации без блокировки пользовательского интерфейса
* Обеспечивать отказоустойчивость при обработке длительных операций

Выбранная архитектура для Web Application: Компонентно-ориентированная архитектура (Component-Based Architecture) с использованием шаблона Presentational/Container Components.

Обоснование:

1. Сложность пользовательского интерфейса: Веб-приложение включает множество взаимосвязанных компонентов:
*  Интерактивные карты для поиска площадок
* Динамические формы для составления и сравнения бюджетов
* Система голосований и обсуждений для команд
* Панели управления для администраторов площадок
* Компонентный подход позволяет создавать переиспользуемые, тестируемые UI-компоненты.

2. Разделение ответственности в UI: Паттерн Presentational/Container Components обеспечивает:
* Presentational components: отвечают только за отображение, не содержат бизнес-логики
* Container components: управляют состоянием и взаимодействием с Backend API

Это упрощает тестирование и повторное использование компонентов.

3. Управление состоянием приложения: Для сложных взаимодействий (сравнение бюджетов, командные обсуждения) используется централизованное управление состоянием (например, Redux или Vuex), что позволяет:
* Синхронизировать состояние между различными компонентами
* Отслеживать изменения состояния для отладки
* Реализовывать сложные бизнес-правила на уровне UI

4. Адаптивность и доступность: Веб-приложение должно работать на различных устройствах с разными разрешениями экранов. Компонентный подход с использованием responsive design позволяет:
* Создавать адаптивные компоненты, работающие на мобильных и десктопных устройствах
* Обеспечивать доступность для пользователей с ограниченными возможностями
* Оптимизировать производительность за счет ленивой загрузки компонентов

5. Интеграция с Backend API: Архитектура поддерживает эффективное взаимодействие с REST API через:
* Слой сервисов для абстрагирования API-вызовов
* Обработку состояний загрузки и ошибок
* Кэширование данных для улучшения производительности
* Оптимистичные обновления для лучшего UX

Данный выбор архитектурных решений обеспечивает баланс между производительностью, масштабируемостью, поддерживаемостью и соответствием функциональным требованиям системы для организаторов мероприятий.


## Диаграмма контейнеров


<img width="1026" height="1227" alt="image" src="https://github.com/user-attachments/assets/78714c10-014b-459f-88e2-978830044420" />

```PlantUML
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

title Диаграмма контейнеров: Система для организаторов мероприятий

Person(organizer, "Организатор", "Основной пользователь системы")
Person(team_member, "Участник команды", "Участвует в обсуждениях и голосованиях")
Person(venue_admin, "Администратор площадок", "Управляет информацией о площадках")

System_Boundary(system_boundary, "Система для организаторов мероприятий") {
    Container(web_app, "Web Application", "React.js/Vue.js", "SPA для всех пользователей системы")
    Container(backend_api, "Backend API", "Spring Boot", "Ядро системы: бизнес-логика и REST API")
    ContainerDb(database, "Database", "PostgreSQL", "Хранит пользователей, площадки, команды, бюджеты, голосования")
    Container(data_service, "Data Processing Service", "Python", "Сбор, кластеризация и обогащение данных о площадках")
    ContainerQueue(message_queue, "Message Queue", "RabbitMQ", "Асинхронное взаимодействие сервисов")
}

System_Ext(aggregator_api, "API агрегаторов", "REST API (Авито и аналоги)")
System_Ext(email_service, "Email сервис", "SMTP/API")
System_Ext(payment_gateway, "Платежный шлюз", "HTTPS API")

' Основные взаимодействия пользователей
Rel(organizer, web_app, "Использует для управления мероприятиями", "HTTPS")
Rel(team_member, web_app, "Участвует в командной работе", "HTTPS")
Rel(venue_admin, web_app, "Управляет данными площадок", "HTTPS")

' Внутренние взаимодействия
Rel(web_app, backend_api, "Вызывает REST API", "HTTPS/JSON")
Rel(backend_api, database, "Читает/записывает данные", "JDBC")
Rel(backend_api, data_service, "Запрашивает обработку данных", "REST API")
Rel(backend_api, message_queue, "Публикует события", "AMQP")
Rel(data_service, message_queue, "Слушает события обработки", "AMQP")

' Внешние взаимодействия
Rel(data_service, aggregator_api, "Собирает данные о площадках", "REST API")
Rel(backend_api, email_service, "Отправляет уведомления", "SMTP/API")
Rel(backend_api, payment_gateway, "Инициирует платежи", "HTTPS API")

' Дополнительные взаимодействия
Rel(data_service, database, "Обновляет данные о площадках", "SQLAlchemy")

@enduml
```

# Диаграмма компонентов 
## Backend API

<img width="2404" height="1557" alt="image" src="https://github.com/user-attachments/assets/b4ed33cc-4550-4234-bf21-47f6b53a3516" />


```PlantUML
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Диаграмма компонентов: Бэкенд API


Container_Boundary(backend_boundary, "Бэкенд API") {
    Component(api_gateway, "API Gateway", "Spring Cloud Gateway", "Маршрутизация и балансировка запросов")
    
    ' Контроллеры (точки входа)
    Component(user_controller, "UserController", "REST Controller", "Вход: HTTP запросы на /api/users/**")
    Component(project_controller, "ProjectController", "REST Controller", "Вход: HTTP запросы на /api/projects/**")
    Component(team_controller, "TeamController", "REST Controller", "Вход: HTTP запросы на /api/teams/**")
    Component(venue_controller, "VenueController", "REST Controller", "Вход: HTTP запросы на /api/venues/**")
    Component(budget_controller, "BudgetController", "REST Controller", "Вход: HTTP запросы на /api/budgets/**")
    Component(voting_controller, "VotingController", "REST Controller", "Вход: HTTP запросы на /api/votings/**")
    
    ' Сервисы бизнес-логики
    Component(user_service, "UserService", "Spring Service", "Вход: DTO от контроллеров, события от очереди")
    Component(project_service, "ProjectService", "Spring Service", "Вход: Данные проектов, критерии поиска")
    Component(team_service, "TeamService", "Spring Service", "Вход: Запросы на управление командой")
    Component(venue_service, "VenueService", "Spring Service", "Вход: Параметры поиска, данные для сравнения")
    Component(budget_service, "BudgetService", "Spring Service", "Вход: Бюджетные статьи, ограничения")
    Component(collaboration_service, "CollaborationService", "Spring Service", "Вход: Голоса, комментарии, предпочтения")
    
    ' Репозитории доступа к данным
    Component(user_repository, "UserRepository", "Spring Data JPA", "Вход: Entity объекты, критерии поиска")
    Component(project_repository, "ProjectRepository", "Spring Data JPA", "Вход: Entity проектов, фильтры")
    Component(team_repository, "TeamRepository", "Spring Data JPA", "Вход: Entity команд, условия выборки")
    Component(venue_repository, "VenueRepository", "Spring Data JPA", "Вход: Entity площадок, геоданные")
    Component(budget_repository, "BudgetRepository", "Spring Data JPA", "Вход: Entity бюджетов, агрегации")
    
    ' Клиенты внешних сервисов
    Component(notification_client, "NotificationClient", "Java Client", "Вход: Данные для уведомлений, шаблоны")
    Component(payment_client, "PaymentClient", "Java Client", "Вход: Платежные данные, суммы")
    Component(venue_service_client, "VenueServiceClient", "Java Client", "Вход: Параметры поиска, данные для обогащения")
    
    ' Обработчики событий
    Component(message_consumer, "MessageConsumer", "Spring AMQP", "Вход: События из очереди (JSON)")
}

' Внешние системы и хранилища
ContainerDb(main_database, "Основная база данных", "PostgreSQL")
ContainerQueue(message_queue, "Очередь сообщений", "RabbitMQ")
Container(web_app, "Веб-приложение", "React.js/Vue.js")
System_Ext(notification_service, "Сервис уведомлений", "External")
System_Ext(payment_gateway, "Платежный шлюз", "External")
System_Ext(venue_processing_service, "Сервис обработки площадок", "Python")


Rel(web_app, api_gateway, "Входные HTTP запросы:\n• REST API вызовы\n• JWT токены аутентификации\n• JSON данные", "HTTPS/JSON")
Rel(api_gateway, user_controller, "Маршрутизированные запросы:\n• POST /api/users/register\n• GET /api/users/profile", "HTTP")
Rel(api_gateway, project_controller, "Маршрутизированные запросы:\n• POST /api/projects\n• GET /api/projects/search", "HTTP")
Rel(api_gateway, team_controller, "Маршрутизированные запросы:\n• POST /api/teams/invite\n• PUT /api/teams/members", "HTTP")
Rel(api_gateway, venue_controller, "Маршрутизированные запросы:\n• GET /api/venues/search\n• POST /api/venues/compare", "HTTP")
Rel(api_gateway, budget_controller, "Маршрутизированные запросы:\n• POST /api/budgets\n• GET /api/budgets/compare", "HTTP")
Rel(api_gateway, voting_controller, "Маршрутизированные запросы:\n• POST /api/votings/vote\n• GET /api/votings/results", "HTTP")

Rel(message_queue, message_consumer, "Входящие события:\n• venue_data_updated\n• team_invitation_sent\n• payment_processed", "AMQP/JSON")
Rel(message_consumer, venue_service, "Обработанные события:\n• Обновления данных площадок\n• Результаты кластеризации", "Java event")
Rel(message_consumer, team_service, "Обработанные события:\n• Подтверждения приглашений\n• Изменения состава команды", "Java event")

Rel(user_controller, user_service, "DTO пользователей:\n• UserRegistrationDTO\n• UserProfileUpdateDTO", "Java method")
Rel(project_controller, project_service, "DTO проектов:\n• ProjectCreateDTO\n• ProjectSearchCriteria", "Java method")
Rel(team_controller, team_service, "DTO команд:\n• TeamInvitationDTO\n• TeamMemberUpdateDTO", "Java method")
Rel(venue_controller, venue_service, "DTO площадок:\n• VenueSearchDTO\n• VenueComparisonRequest", "Java method")
Rel(budget_controller, budget_service, "DTO бюджетов:\n• BudgetCreateDTO\n• BudgetComparisonRequest", "Java method")
Rel(voting_controller, collaboration_service, "DTO голосований:\n• VoteDTO\n• CommentCreateDTO", "Java method")

Rel(user_service, user_repository, "Entity и критерии:\n• User entity\n• Specification для поиска", "Java method")
Rel(project_service, project_repository, "Entity и критерии:\n• Project entity\n• Pageable запросы", "Java method")
Rel(team_service, team_repository, "Entity и критерии:\n• Team entity\n• Join условия", "Java method")
Rel(venue_service, venue_repository, "Entity и критерии:\n• Venue entity\n• Гео-запросы", "Java method")
Rel(budget_service, budget_repository, "Entity и критерии:\n• Budget entity\n• Агрегации по статьям", "Java method")

Rel(user_repository, main_database, "SQL запросы:\n• INSERT/UPDATE пользователей\n• SELECT с JOIN", "JDBC/SQL")
Rel(project_repository, main_database, "SQL запросы:\n• Транзакции проектов\n• Сложные запросы с подзапросами", "JDBC/SQL")
Rel(team_repository, main_database, "SQL запросы:\n• Управление связями\n• Оптимизированные выборки", "JDBC/SQL")
Rel(venue_repository, main_database, "SQL запросы:\n• Пространственные запросы\n• Полнотекстовый поиск", "JDBC/SQL")
Rel(budget_repository, main_database, "SQL запросы:\n• Агрегатные функции\n• Window функции", "JDBC/SQL")

Rel(team_service, notification_client, "Данные для уведомлений:\n• Email получателя\n• Шаблон приглашения\n• Контекстные данные", "Java method")
Rel(collaboration_service, notification_client, "Данные для уведомлений:\n• Список участников\n• Данные голосования\n• Ссылки", "Java method")
Rel(budget_service, payment_client, "Платежные данные:\n• Сумма и валюта\n• Описание платежа\n• Return URL", "Java method")
Rel(venue_service, venue_service_client, "Запросы на обработку:\n• Критерии поиска\n• Данные для обогащения\n• Параметры кластеризации", "Java method")

Rel(notification_client, notification_service, "Запросы на отправку:\n• SMTP/API вызовы\n• JSON payload", "SMTP/API/JSON")
Rel(payment_client, payment_gateway, "Платежные запросы:\n• HTTPS вызовы\n• Зашифрованные данные", "HTTPS API/JSON")
Rel(venue_service_client, venue_processing_service, "Запросы на обработку:\n• REST API вызовы\n• Пакетные данные", "REST API/JSON")

Rel(team_service, message_queue, "Исходящие события:\n• team_created\n• member_added\n• invitation_accepted", "AMQP/JSON")
Rel(venue_service, message_queue, "Исходящие события:\n• venue_search_requested\n• comparison_completed", "AMQP/JSON")
Rel(budget_service, message_queue, "Исходящие события:\n• budget_created\n• payment_initiated\n• threshold_exceeded", "AMQP/JSON")

@enduml
```

## Диаграмма компонентов: VenueService

<img width="2518" height="1044" alt="image" src="https://github.com/user-attachments/assets/7be851be-783e-47f1-b3b6-617701002388" />


```PlantUML
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Диаграмма компонентов: VenueService (детализация с входами)


  Component(venue_controller, "VenueController", "REST Controller", "HTTP вход для работы с площадками")
  Component(message_consumer, "MessageConsumer", "Spring AMQP Listener", "Асинхронные события из очереди")

  Container_Boundary(venue_service_boundary, "VenueService") {

      Component(venue_service_facade, "VenueService", "Spring Service", "Фасад бизнес-логики площадок")

      Component(search_engine, "VenueSearchEngine", "Spring Service", "Поиск площадок")
      Component(comparison_engine, "VenueComparisonEngine", "Spring Service", "Сравнение площадок")
      Component(recommendation_engine, "VenueRecommendationEngine", "Spring Service", "Рекомендации")

      Component(availability_checker, "AvailabilityChecker", "Spring Service", "Проверка доступности дат")
      Component(price_analyzer, "PriceAnalyzer", "Spring Service", "Анализ цен и бюджета")

      Component(data_enricher, "VenueDataEnricher", "Spring Service", "Обогащение данных")
      Component(validation_service, "VenueValidationService", "Spring Validator", "Валидация входных данных")
      Component(cache_manager, "VenueCacheManager", "Spring Cache", "Кэширование результатов")

      Component(event_publisher, "VenueEventPublisher", "Spring AMQP", "Публикация доменных событий")
  }



Component(venue_repository, "VenueRepository", "Spring Data JPA", "Доступ к данным площадок")
Component(venue_service_client, "VenueServiceClient", "Feign Client", "Вызов внешнего сервиса")

ContainerDb(main_database, "Основная БД", "PostgreSQL")
Container(cache_store, "Кэш", "Redis")
System_Ext(message_queue, "Очередь сообщений", "RabbitMQ")
System_Ext(venue_processing_service, "Сервис обработки площадок", "External")

Rel(venue_controller, venue_service_facade, "HTTP запросы /api/venues/**", "REST/JSON")
Rel(message_consumer, venue_service_facade, "События venue_*", "Java event")

Rel(venue_service_facade, validation_service, "Валидация DTO", "Java")
Rel(venue_service_facade, cache_manager, "Проверка кэша", "Java")
Rel(cache_manager, cache_store, "Чтение / запись", "Redis")

Rel(venue_service_facade, search_engine, "Поиск площадок", "Java")
Rel(search_engine, venue_repository, "JPA запросы", "JPA")
Rel(venue_repository, main_database, "SQL", "JDBC")

Rel(venue_service_facade, comparison_engine, "Сравнение", "Java")
Rel(venue_service_facade, recommendation_engine, "Рекомендации", "Java")

Rel(venue_service_facade, availability_checker, "Проверка доступности", "Java")
Rel(venue_service_facade, price_analyzer, "Анализ цен", "Java")

Rel(venue_service_facade, venue_service_client, "Запрос обогащения", "Feign")
Rel(venue_service_client, venue_processing_service, "REST вызов", "HTTP/JSON")
Rel(data_enricher, venue_service_facade, "Обогащённые данные", "Java")

Rel(venue_service_facade, event_publisher, "Доменные события", "Java")
Rel(event_publisher, message_queue, "Публикация событий", "AMQP")

@enduml

```
