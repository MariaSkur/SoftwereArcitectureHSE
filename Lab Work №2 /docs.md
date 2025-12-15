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

<img width="2084" height="1099" alt="image" src="https://github.com/user-attachments/assets/6d0cd1cd-eb1d-4bc5-97ed-a04a513b7416" />

```PlantUML
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Диаграмма компонентов: Backend API (Application)

Container(backend_api, "Backend API", "Java/Spring Boot", "Основная бизнес-логика системы")

Container_Boundary(api_boundary, "Backend API") {
    Component(api_gateway, "API Gateway", "Spring Cloud Gateway", "Маршрутизация и балансировка запросов")
    
    Component(user_controller, "UserController", "REST Controller", "Обработка запросов пользователей")
    Component(team_controller, "TeamController", "REST Controller", "Управление командами")
    Component(venue_controller, "VenueController", "REST Controller", "Поиск и фильтрация площадок")
    Component(budget_controller, "BudgetController", "REST Controller", "Работа со сметами расходов")
    Component(voting_controller, "VotingController", "REST Controller", "Управление голосованиями")
    
    Component(team_service, "TeamManagementService", "Spring Service", "Логика управления командами")
    Component(venue_service, "VenueSearchService", "Spring Service", "Логика поиска площадок")
    Component(budget_service, "BudgetComparisonService", "Spring Service", "Логика сравнения бюджетов")
    Component(collaboration_service, "CollaborationService", "Spring Service", "Логика сбора мнений")
    
    Component(user_repo, "UserRepository", "Spring Data JPA", "Доступ к данным пользователей")
    Component(venue_repo, "VenueRepository", "Spring Data JPA", "Доступ к данным площадок")
    Component(team_repo, "TeamRepository", "Spring Data JPA", "Доступ к данным команд")
    Component(budget_repo, "BudgetRepository", "Spring Data JPA", "Доступ к данным смет")
    
    Component(notification_client, "NotificationClient", "Java Client", "Клиент для Email/SMS сервиса")
    Component(payment_client, "PaymentGatewayClient", "Java Client", "Клиент для платежного шлюза")
    Component(scraping_client, "ScrapingServiceClient", "Java Client", "Клиент для сервиса кластеризации")
}

ContainerDb(database, "Database", "PostgreSQL")
Container(message_queue, "Message Queue", "RabbitMQ")
Container(notification_service, "Email/SMS сервис", "External")
Container(payment_gateway, "Платежный шлюз", "External")
Container(scraping_service, "Scraping/Synchronization Service", "Python")

' Взаимодействия между компонентами внутри Backend API
Rel(api_gateway, user_controller, "Маршрутизирует запросы", "HTTP")
Rel(api_gateway, team_controller, "Маршрутизирует запросы", "HTTP")
Rel(api_gateway, venue_controller, "Маршрутизирует запросы", "HTTP")
Rel(api_gateway, budget_controller, "Маршрутизирует запросы", "HTTP")
Rel(api_gateway, voting_controller, "Маршрутизирует запросы", "HTTP")

Rel(user_controller, team_service, "Вызывает методы сервиса", "Java method")
Rel(team_controller, team_service, "Вызывает методы сервиса", "Java method")
Rel(venue_controller, venue_service, "Вызывает методы сервиса", "Java method")
Rel(budget_controller, budget_service, "Вызывает методы сервиса", "Java method")
Rel(voting_controller, collaboration_service, "Вызывает методы сервиса", "Java method")

Rel(team_service, user_repo, "Использует для доступа к данным", "Java method")
Rel(venue_service, venue_repo, "Использует для доступа к данным", "Java method")
Rel(team_service, team_repo, "Использует для доступа к данным", "Java method")
Rel(budget_service, budget_repo, "Использует для доступа к данным", "Java method")
Rel(collaboration_service, user_repo, "Использует для доступа к данным", "Java method")

Rel(team_service, notification_client, "Отправляет приглашения в команду", "Java method")
Rel(collaboration_service, notification_client, "Отправляет уведомления о голосованиях", "Java method")
Rel(budget_service, payment_client, "Инициирует платежи за аренду", "Java method")
Rel(venue_service, scraping_client, "Запрашивает кластеризацию площадок", "Java method")

' Внешние взаимодействия
Rel(user_repo, database, "Выполняет SQL-запросы", "JDBC")
Rel(venue_repo, database, "Выполняет SQL-запросы", "JDBC")
Rel(team_repo, database, "Выполняет SQL-запросы", "JDBC")
Rel(budget_repo, database, "Выполняет SQL-запросы", "JDBC")

Rel(notification_client, notification_service, "Отправляет уведомления", "SMTP/API")
Rel(payment_client, payment_gateway, "Инициирует платежи", "HTTPS")
Rel(scraping_client, scraping_service, "Запрашивает обработку данных", "REST")

Rel(team_service, message_queue, "Публикует события создания команды", "AMQP")
Rel(venue_service, message_queue, "Публикует события добавления площадки", "AMQP")

@enduml
```

## Scraping/Synchronization Service

<img width="1090" height="1158" alt="image" src="https://github.com/user-attachments/assets/68ad39b6-7385-41ae-a51b-8e7e31da6b2e" />

```PlantUML
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Диаграмма компонентов: Scraping/Synchronization Service

Container(background_service, "Scraping/Synchronization Service", "Python", "Фоновый сервис кластеризации и синхронизации")

Container_Boundary(service_boundary, "Scraping/Synchronization Service") {
    Component(event_listener, "Event Listeners", "Python + pika/redis", "Слушает события из Message Queue")
    Component(scheduled_trigger, "ScheduledSyncTrigger", "Python Celery", "Планировщик периодических задач")
    
    Component(sync_orchestrator, "DataSynchronizationOrchestrator", "Python Service", "Координатор процессов синхронизации")
    Component(api_client, "ExternalApiClient", "Python Requests", "Клиент для внешних API агрегаторов")
    Component(data_enricher, "DataEnrichmentProcessor", "Python Service", "Обработка и обогащение данных")
    
    Component(clustering_engine, "ClusteringEngine", "Python + scikit-learn", "ML-алгоритмы кластеризации")
    
    Component(data_publisher, "ProcessedDataPublisher", "Python Service", "Публикация обработанных данных")
}

ContainerDb(database, "Database", "PostgreSQL")
Container(message_queue, "Message Queue", "RabbitMQ")
System_Ext(aggregator_api, "Внешние API агрегаторов", "REST API")
System_Ext(backend_api, "Backend API", "Java/Spring Boot")

' Внутренние взаимодействия
Rel(event_listener, sync_orchestrator, "Передает событие о новой площадке", "Python call")
Rel(scheduled_trigger, sync_orchestrator, "Запускает периодическую синхронизацию", "Python call")

Rel(sync_orchestrator, api_client, "Запрашивает сбор данных", "Python call")
Rel(api_client, aggregator_api, "Получает данные о площадках", "REST/HTTPS")

Rel(sync_orchestrator, data_enricher, "Передает данные для обработки", "Python call")
Rel(data_enricher, clustering_engine, "Запрашивает кластеризацию данных", "Python call")

Rel(data_enricher, data_publisher, "Передает обработанные данные", "Python call")

' Внешние взаимодействия
Rel(event_listener, message_queue, "Слушает события (новая_площадка, обновление)", "AMQP")
Rel(data_publisher, database, "Записывает обогащенные данные о площадках", "SQLAlchemy")
Rel(data_publisher, backend_api, "Отправляет результаты кластеризации", "REST/HTTPS")
Rel(data_publisher, message_queue, "Публикует события об обновлении данных", "AMQP")

' Комментарии для пояснения
note right of clustering_engine
  <b>Алгоритмы кластеризации:</b>
  - k-means для категоризации
  - NLP для анализа описаний
  - CV для анализа фото
end note

note right of data_enricher
  <b>Пометка данных:</b>
  Если информации недостаточно,
  устанавливает флаг
  "requires_contact"
end note

@enduml
```
