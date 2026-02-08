# Диаграмма контейнеров

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

# Диаграмма последовательностей
<img width="1919" height="874" alt="image" src="https://github.com/user-attachments/assets/b299c3c5-e0dd-4cbc-b886-86e8489ffc0a" />


```PlantUML
@startuml
title Сравнение вариантов бюджета мероприятия

actor Организатор
participant "Web App" as Web
participant "BudgetController" as Controller
participant "BudgetComparisonService" as ComparisonService
participant "TeamService" as TeamService
participant "BudgetRepository" as Repository
database "PostgreSQL\n(Budget DB)" as DB
participant "EmailClient" as Email
participant "Email Service" as ExternalEmail

Организатор -> Web: Запрос сравнения бюджетных вариантов
Web -> Controller: POST /api/budgets/compare
Controller -> ComparisonService: compareBudgetOptions(budgetIds, userId)

ComparisonService -> Repository: findById(budgetId1)
Repository -> DB: SELECT * FROM budgets WHERE id = budgetId1
DB --> Repository: Budget 1
Repository --> ComparisonService: Budget 1

ComparisonService -> Repository: findById(budgetId2)
Repository -> DB: SELECT * FROM budgets WHERE id = budgetId2
DB --> Repository: Budget 2
Repository --> ComparisonService: Budget 2

ComparisonService -> ComparisonService: calculateDifferences(budget1, budget2)
ComparisonService -> ComparisonService: generateComparisonReport()

alt Есть команда мероприятия
    ComparisonService -> TeamService: getTeamMembers(eventId)
    TeamService --> ComparisonService: List<User>
    ComparisonService -> Email: sendComparisonToTeam(report, teamMembers)
    Email -> ExternalEmail: Отправка email
end

ComparisonService --> Controller: ComparisonResult
Controller --> Web: HTTP 200 + JSON
Web --> Организатор: Отображение результатов сравнения

@enduml

```

Пояснение: Диаграмма последовательностей показывает процесс сравнения двух вариантов бюджета мероприятия. Организатор инициирует сравнение через веб-интерфейс. Система получает данные о бюджетах, вычисляет различия, генерирует отчет и при необходимости отправляет его команде по email.

# Модель БД
<img width="1129" height="1189" alt="image" src="https://github.com/user-attachments/assets/70115fdc-a2ec-4114-b8bd-2882ceba476f" />

```PlantUML
@startuml
title Модель базы данных системы

class User {
    +Long id
    +String email
    +String name
    +String role
    +Date createdAt
    +__constructors__()
    +__getters/setters__()
}

class Team {
    +Long id
    +String name
    +Long ownerId
    +Date createdAt
    +__constructors__()
    +__getters/setters__()
}

class TeamMember {
    +Long id
    +Long teamId
    +Long userId
    +String role
    +Date joinedAt
    +__constructors__()
    +__getters/setters__()
}

class Venue {
    +Long id
    +String name
    +String address
    +String venueType
    +Integer capacity
    +BigDecimal pricePerHour
    +String contactPerson
    +Boolean requiresContact
    +Date createdAt
    +__constructors__()
    +__getters/setters__()
}

class Event {
    +Long id
    +String title
    +String description
    +Long venueId
    +Long teamId
    +Date eventDate
    +Integer durationHours
    +String status
    +Date createdAt
    +__constructors__()
    +__getters/setters__()
}

class Budget {
    +Long id
    +String name
    +Long eventId
    +BigDecimal venueCost
    +BigDecimal equipmentCost
    +BigDecimal cateringCost
    +BigDecimal marketingCost
    +BigDecimal otherCosts
    +BigDecimal total
    +Boolean isActive
    +Date createdAt
    +__constructors__()
    +__getters/setters__()
    +calculateTotal()
}

class BudgetVote {
    +Long id
    +Long budgetId
    +Long userId
    +String voteType
    +String comment
    +Date votedAt
    +__constructors__()
    +__getters/setters__()
}

' Связи
User "1" -- "*" TeamMember : имеет
Team "1" -- "*" TeamMember : включает
Team "1" -- "*" Event : организует
Venue "1" -- "*" Event : используется для
Event "1" -- "*" Budget : имеет варианты
Budget "1" -- "*" BudgetVote : получает оценки
User "1" -- "*" BudgetVote : голосует

note top of Budget : Метод calculateTotal() суммирует\nвсе статьи расходов
note right of Venue : requiresContact - флаг, указывающий\nна необходимость связи\nс представителем площадки

@enduml
```

Пояснение: Модель базы данных включает 7 основных сущностей:

User - пользователи системы

Team - команды организаторов

TeamMember - связь пользователей с командами

Venue - площадки для мероприятий (с флагом requiresContact для решения проблемы неполных данных)

Event - мероприятия

Budget - варианты бюджета с методом расчета общей суммы

BudgetVote - голоса участников команды по вариантам бюджета

# Применение основных принципов разработки

## 1. BudgetComparisonService.java 
```java
@Service
public class BudgetComparisonService {

    private final BudgetRepository budgetRepository;
    private final TeamService teamService;
    private final EmailClient emailClient;

    // SOLID (DIP): зависимости передаются через конструктор
    public BudgetComparisonService(BudgetRepository budgetRepository,
                                   TeamService teamService,
                                   EmailClient emailClient) {
        this.budgetRepository = budgetRepository;
        this.teamService = teamService;
        this.emailClient = emailClient;
    }

    // SOLID (SRP): сервис отвечает только за сравнение бюджетов
    public ComparisonResult compareBudgetOptions(List<Long> budgetIds, Long userId) {
        validateInput(budgetIds);

        List<Budget> budgets = loadBudgets(budgetIds);
        Budget baseBudget = budgets.get(0);

        List<BudgetComparison> comparisons = budgets.stream()
                .skip(1)
                .map(budget -> compareBudgets(baseBudget, budget))
                .toList();

        ComparisonResult result = new ComparisonResult(baseBudget, comparisons);

        notifyTeamIfNeeded(baseBudget.getEventId(), result);

        return result;
    }

    // DRY: единая точка загрузки бюджетов
    private List<Budget> loadBudgets(List<Long> budgetIds) {
        List<Budget> budgets = budgetRepository.findAllById(budgetIds);
        if (budgets.size() < 2) {
            throw new IllegalArgumentException("At least two budgets are required");
        }
        return budgets;
    }

    // SOLID (OCP): добавление новых статей расходов без изменения логики сервиса
    private BudgetComparison compareBudgets(Budget base, Budget other) {
        Map<ExpenseType, BigDecimal> differences = new EnumMap<>(ExpenseType.class);

        for (ExpenseType type : ExpenseType.values()) {
            differences.put(type, type.calculateDifference(base, other));
        }

        return new BudgetComparison(other, differences);
    }

    // YAGNI: уведомления отправляются только при наличии команды
    private void notifyTeamIfNeeded(Long eventId, ComparisonResult result) {
        if (eventId == null) {
            return;
        }

        List<User> teamMembers = teamService.getTeamMembers(eventId);
        if (teamMembers.isEmpty()) {
            return;
        }

        String report = generateReport(result);
        emailClient.sendToTeam(report, teamMembers);
    }

    // KISS: простой и читаемый формат отчёта
    private String generateReport(ComparisonResult result) {
        StringBuilder report = new StringBuilder("Сравнение бюджетов\n");
        report.append("Базовый бюджет: ")
              .append(result.getPrimaryBudget().getName())
              .append("\n\n");

        for (BudgetComparison comparison : result.getComparisons()) {
            report.append("Сравнение с: ")
                  .append(comparison.getBudget().getName())
                  .append("\n");

            comparison.getDifferences().forEach((type, value) ->
                    report.append(type.getLabel())
                          .append(": ")
                          .append(value)
                          .append("\n")
            );

            report.append("\n");
        }

        return report.toString();
    }

    private void validateInput(List<Long> budgetIds) {
        if (budgetIds == null || budgetIds.size() < 2) {
            throw new IllegalArgumentException("At least 2 budget IDs required");
        }
    }
}

```

## 2. VenueService.java 
```java
@Service
public class VenueService {

    private final VenueRepository venueRepository;

    public VenueService(VenueRepository venueRepository) {
        this.venueRepository = venueRepository;
    }

    // SOLID (SRP): поиск площадок
    public List<Venue> findVenuesForEvent(VenueSearchCriteria criteria) {
        validateCriteria(criteria);

        return venueRepository
                .findByTypeAndCapacityGreaterThanEqual(
                        criteria.getVenueType(),
                        criteria.getMinCapacity()
                )
                .stream()
                .filter(venue -> matchesCriteria(venue, criteria))
                .sorted(Comparator.comparing(Venue::getPricePerHour))
                .toList();
    }

    // KISS + DRY
    private boolean matchesCriteria(Venue venue, VenueSearchCriteria criteria) {
        if (venue.getPricePerHour().compareTo(criteria.getMaxPrice()) > 0) {
            return false;
        }
        return criteria.isIncludeUnverified() || !venue.isRequiresContact();
    }

    private void validateCriteria(VenueSearchCriteria criteria) {
        if (criteria == null) {
            throw new IllegalArgumentException("Search criteria must not be null");
        }
    }
}

```
## 3. Budget.java 
```java
@Entity
@Table(name = "budgets")
public class Budget {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String name;
    private Long eventId;

    @Column(precision = 10, scale = 2)
    private BigDecimal venueCost = BigDecimal.ZERO;

    @Column(precision = 10, scale = 2)
    private BigDecimal equipmentCost = BigDecimal.ZERO;

    @Column(precision = 10, scale = 2)
    private BigDecimal cateringCost = BigDecimal.ZERO;

    @Column(precision = 10, scale = 2)
    private BigDecimal marketingCost = BigDecimal.ZERO;

    @Column(precision = 10, scale = 2)
    private BigDecimal otherCosts = BigDecimal.ZERO;

    @Column(precision = 10, scale = 2)
    private BigDecimal total = BigDecimal.ZERO;

    @PrePersist
    @PreUpdate
    public void calculateTotal() {
        total = venueCost
                .add(equipmentCost)
                .add(cateringCost)
                .add(marketingCost)
                .add(otherCosts);
    }

    // SOLID (OCP + LSP)
    public void addExpense(ExpenseType type, BigDecimal amount) {
        switch (type) {
            case VENUE -> venueCost = venueCost.add(amount);
            case EQUIPMENT -> equipmentCost = equipmentCost.add(amount);
            case CATERING -> cateringCost = cateringCost.add(amount);
        }
        calculateTotal();
    }

    // getters/setters
}

```
# Дополнительные принципы разработки
## 1. BDUF (Big Design Up Front) - отказ

__Краткое описание принципа:__
BDUF предполагает детальное проектирование всей системы заранее, до начала реализации, с фиксированием архитектуры, моделей данных и алгоритмов.

__Обоснование отказа:__

 - __Неопределённость требований.__
В системе управления мероприятиями отсутствуют стабильные и полностью сформулированные требования, особенно в части обработки и кластеризации площадок. Алгоритмы и модели данных могут быть определены только после получения реальных данных и пользовательской обратной связи.
 - __Необходимость гибкости.__
Система должна адаптироваться к изменяющимся сценариям использования, появлению новых источников данных и внешних сервисов. Жёсткое проектирование на старте затруднило бы внесение изменений.
 - __Следование принципу YAGNI.__
Проектирование сложных механизмов (например, интеллектуальной обработки площадок) заранее нецелесообразно, так как их необходимость на текущем этапе не подтверждена.

__Вывод:__
От принципа BDUF осознанно отказались в пользу итеративного развития и постепенного уточнения архитектуры.

## 2. SoC (Separation of Concerns) — применение

__Краткое описание принципа:__
SoC предполагает разделение системы на независимые части, каждая из которых отвечает за строго определённую область ответственности.

__Обоснование применения:__

 - __Архитектурное разделение.__
Применена многоуровневая архитектура:
     - Controller — обработка HTTP-запросов
     - Service — бизнес-логика
     - Repository — доступ к данным

 - __Доменное разделение.__
Бизнес-логика разделена по предметным областям:
     - VenueService — работа с площадками
     - BudgetComparisonService — сравнение бюджетов
     - TeamService — управление командами

 - __Инфраструктурное разделение.__
Взаимодействие с внешними сервисами (email) вынесено в EmailClient, что изолирует инфраструктурную логику от бизнес-правил.

__Вывод:__
Принцип SoC полностью соблюдён и является базовым для архитектуры системы.

## 3. MVP (Minimum Viable Product) — применение

__Краткое описание принципа:__
MVP предполагает реализацию минимального набора функций, достаточного для проверки ценности продукта и получения обратной связи от пользователей.

__Обоснование применения:__

 - __Фокус на ключевой функциональности.__
В первой версии реализованы только основные сценарии:
     - поиск площадок
     - создание и сравнение бюджетов
     - командное взаимодействие

 - __Отложенная сложность.__
Сложные механизмы (например, ML-кластеризация площадок) намеренно не реализованы. Вместо этого используется простая и понятная логика (флаг requiresContact).

 - __Быстрая обратная связь.__
MVP позволяет оперативно проверить гипотезы и скорректировать развитие системы на основе реального использования.

__Реализация MVP в системе:__
 - фильтрация площадок по цене и вместимости
 - базовое сравнение бюджетов
 - простая командная коммуникация
 - ручное обновление информации о площадках

__Вывод:__
Принцип MVP применён осознанно и соответствует целям раннего этапа разработки.

## 4. PoC (Proof of Concept) — отказ 

__Краткое описание принципа:__
PoC используется для экспериментальной проверки технической реализуемости идеи или технологии до начала полноценной разработки.

__Обоснование отказа:__

 - __Отсутствие исследовательской задачи.__
В рамках данной системы не требуется доказывать техническую возможность реализации ключевого функционала — все используемые технологии (REST API, базы данных, email-уведомления) являются стандартными и хорошо изученными.

 - __Чётко сформулированная цель разработки.__
Проект направлен на создание прикладного программного продукта, а не на эксперимент или исследование новых технологий.

 - __Соответствие принципу MVP.__
Разработка ведётся сразу в виде рабочего продукта, а не отдельного экспериментального прототипа.

 - __Избыточность PoC.__
Создание PoC для таких задач, как поиск, фильтрация или сравнение данных, не даёт дополнительной ценности и лишь увеличивает затраты времени.

__Вывод:__
Применение PoC признано нецелесообразным, поэтому от него осознанно отказались.
