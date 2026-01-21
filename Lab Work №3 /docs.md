# Диаграмма контейнеров

<img width="575" height="969" alt="image" src="https://github.com/user-attachments/assets/659d7a0a-56a3-4ba9-a86f-54b9821a8cb8" />

 
```PlantUML
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

title Диаграмма контейнеров: Система для организаторов мероприятий

Person(organizer, "Организатор", "Основной пользователь системы")
Person(team_member, "Участник команды", "Участвует в обсуждениях и голосованиях")

System_Boundary(system_boundary, "Система для организаторов мероприятий") {
    Container(web_app, "Web Application", "React.js", "SPA для всех пользователей системы")
    Container(backend_api, "Backend API", "Spring Boot", "Ядро системы: REST API и бизнес-логика", $tags="focus")
    ContainerDb(database, "Database", "PostgreSQL", "Хранит пользователей, площадки, команды, бюджеты")
}

System_Ext(email_service, "Email сервис", "SMTP/API")

Rel(organizer, web_app, "Использует для управления мероприятиями", "HTTPS")
Rel(team_member, web_app, "Участвует в командной работе", "HTTPS")
Rel(web_app, backend_api, "Вызывает REST API", "HTTPS/JSON")
Rel(backend_api, database, "Читает/записывает данные", "JDBC")
Rel(backend_api, email_service, "Отправляет уведомления", "SMTP/API")

@enduml
```

Пояснение: Диаграмма показывает высокоуровневую архитектуру системы с акцентом на Backend API, который будет детализирован в диаграмме компонентов. Web Application взаимодействует с Backend API через REST, а Backend API управляет данными в PostgreSQL и отправляет уведомления через внешний Email сервис.

# Диаграмма компонентов
<img width="1112" height="853" alt="image" src="https://github.com/user-attachments/assets/549d971d-54b9-4eb6-9489-a5982142a071" />

```PlantUML
@startuml
!include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Component.puml

title Диаграмма компонентов: Backend API

Container(backend_api, "Backend API", "Spring Boot", "Основная бизнес-логика системы")

Container_Boundary(api_boundary, "Backend API") {
    Component(venue_controller, "VenueController", "REST Controller", "Обработка запросов по площадкам")
    Component(budget_controller, "BudgetController", "REST Controller", "Обработка запросов по бюджетам")
    
    Component(venue_service, "VenueService", "Spring Service", "Логика работы с площадками")
    Component(budget_comparison_service, "BudgetComparisonService", "Spring Service", "Логика сравнения бюджетов")
    Component(team_service, "TeamService", "Spring Service", "Логика работы с командами")
    
    Component(venue_repository, "VenueRepository", "JPA Repository", "Доступ к данным площадок")
    Component(budget_repository, "BudgetRepository", "JPA Repository", "Доступ к данным бюджетов")
    Component(team_repository, "TeamRepository", "JPA Repository", "Доступ к данным команд")
    
    Component(email_client, "EmailClient", "Adapter", "Отправка email уведомлений")
}

ContainerDb(database, "Database", "PostgreSQL")
System_Ext(email_service, "Email сервис", "SMTP")

' Взаимодействия
Rel(venue_controller, venue_service, "Вызывает методы", "Java method")
Rel(budget_controller, budget_comparison_service, "Вызывает методы", "Java method")
Rel(budget_controller, team_service, "Вызывает методы", "Java method")

Rel(venue_service, venue_repository, "Использует для доступа к данным", "Java method")
Rel(budget_comparison_service, budget_repository, "Использует для доступа к данным", "Java method")
Rel(team_service, team_repository, "Использует для доступа к данным", "Java method")

Rel(team_service, email_client, "Отправляет уведомления", "Java method")

Rel(venue_repository, database, "Выполняет SQL запросы", "JDBC")
Rel(budget_repository, database, "Выполняет SQL запросы", "JDBC")
Rel(team_repository, database, "Выполняет SQL запросы", "JDBC")

Rel(email_client, email_service, "Отправляет email", "SMTP")

@enduml
```

Пояснение: Диаграмма компонентов показывает внутреннюю структуру Backend API. Контроллеры обрабатывают HTTP-запросы, сервисы содержат бизнес-логику, репозитории обеспечивают доступ к данным. Для демонстрации принципов разработки будут показаны код BudgetComparisonService (сравнение бюджетов) и VenueService (работа с площадками).

# Диаграмма последовательностей
<img width="1606" height="741" alt="image" src="https://github.com/user-attachments/assets/5ff8985e-8d10-4ed1-a501-928872769161" />

```PlantUML
@startuml
title Сравнение вариантов бюджета мероприятия

actor Организатор
participant "Web App" as Web
participant "BudgetController" as Controller
participant "BudgetComparisonService" as ComparisonService
participant "TeamService" as TeamService
participant "BudgetRepository" as Repository
participant "EmailClient" as Email
participant "Email Service" as ExternalEmail

Организатор -> Web: Запрос сравнения бюджетных вариантов
Web -> Controller: POST /api/budgets/compare
Controller -> ComparisonService: compareBudgetOptions(budgetIds, userId)
ComparisonService -> Repository: findById(budgetId1)
Repository --> ComparisonService: Budget 1
ComparisonService -> Repository: findById(budgetId2)
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

## 1. BudgetComparisonService.java (SOLID, DRY, KISS)
```java
@Service
public class BudgetComparisonService {
    
    private final BudgetRepository budgetRepository;
    private final TeamService teamService;
    private final EmailClient emailClient;
    
    // Принцип SOLID: Dependency Injection (Dependency Inversion Principle)
    public BudgetComparisonService(BudgetRepository budgetRepository, 
                                   TeamService teamService, 
                                   EmailClient emailClient) {
        this.budgetRepository = budgetRepository;
        this.teamService = teamService;
        this.emailClient = emailClient;
    }
    
    // Принцип SOLID: Single Responsibility Principle
    // Класс отвечает только за сравнение бюджетов
    public ComparisonResult compareBudgetOptions(List<Long> budgetIds, Long userId) {
        // Принцип KISS: простой и понятный метод
        validateInput(budgetIds);
        
        List<Budget> budgets = budgetRepository.findAllById(budgetIds);
        if (budgets.size() < 2) {
            throw new IllegalArgumentException("Need at least 2 budgets for comparison");
        }
        
        Budget primary = budgets.get(0);
        List<BudgetComparison> comparisons = new ArrayList<>();
        
        // Принцип DRY: повторное использование метода calculateDifferences
        for (int i = 1; i < budgets.size(); i++) {
            comparisons.add(calculateDifferences(primary, budgets.get(i)));
        }
        
        ComparisonResult result = new ComparisonResult(primary, comparisons);
        
        // Принцип YAGNI: отправка email только если есть команда
        Optional<Long> eventId = primary.getEventId();
        eventId.ifPresent(id -> notifyTeamIfNeeded(id, result));
        
        return result;
    }
    
    // Принцип SOLID: Open/Closed Principle
    // Метод закрыт для модификации, но открыт для расширения
    private BudgetComparison calculateDifferences(Budget base, Budget other) {
        Map<String, BigDecimal> differences = new HashMap<>();
        
        // Принцип DRY: избегаем дублирования кода расчета разниц
        differences.put("venueCost", calculateDifference(base.getVenueCost(), other.getVenueCost()));
        differences.put("equipmentCost", calculateDifference(base.getEquipmentCost(), other.getEquipmentCost()));
        differences.put("cateringCost", calculateDifference(base.getCateringCost(), other.getCateringCost()));
        differences.put("total", calculateDifference(base.getTotal(), other.getTotal()));
        
        return new BudgetComparison(other, differences);
    }
    
    // Принцип DRY: выделенный метод для расчета разницы
    private BigDecimal calculateDifference(BigDecimal base, BigDecimal other) {
        return other.subtract(base);
    }
    
    // Принцип YAGNI: условная отправка уведомлений
    private void notifyTeamIfNeeded(Long eventId, ComparisonResult result) {
        // Отправляем уведомления только если в мероприятии есть команда
        List<User> teamMembers = teamService.getTeamMembers(eventId);
        if (!teamMembers.isEmpty()) {
            String report = generateComparisonReport(result);
            emailClient.sendToTeam(report, teamMembers);
        }
    }
    
    // Принцип KISS: простой генератор отчета
    private String generateComparisonReport(ComparisonResult result) {
        StringBuilder report = new StringBuilder();
        report.append("Сравнение бюджетных вариантов\n");
        report.append("Основной вариант: ").append(result.getPrimaryBudget().getName()).append("\n");
        
        for (BudgetComparison comparison : result.getComparisons()) {
            report.append("Сравнение с: ").append(comparison.getBudget().getName()).append("\n");
            report.append("Разница в стоимости площадки: ").append(comparison.getDifferences().get("venueCost")).append("\n");
            report.append("Общая разница: ").append(comparison.getDifferences().get("total")).append("\n");
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

## 2. VenueService.java (SOLID, KISS)
```java
@Service
public class VenueService {
    
    private final VenueRepository venueRepository;
    
    public VenueService(VenueRepository venueRepository) {
        this.venueRepository = venueRepository;
    }
    
    // Принцип SOLID: Single Responsibility Principle
    // Метод отвечает только за поиск площадок с учетом требований
    public List<Venue> findVenuesForEvent(VenueSearchCriteria criteria) {
        // Принцип KISS: простой и понятный алгоритм поиска
        List<Venue> allVenues = venueRepository.findByTypeAndCapacityGreaterThanEqual(
            criteria.getVenueType(), 
            criteria.getMinCapacity()
        );
        
        return filterAndSortVenues(allVenues, criteria);
    }
    
    // Принцип SOLID: Open/Closed Principle
    // Фильтрацию можно расширять через новые стратегии
    private List<Venue> filterAndSortVenues(List<Venue> venues, VenueSearchCriteria criteria) {
        return venues.stream()
            .filter(venue -> venue.getPricePerHour().compareTo(criteria.getMaxPrice()) <= 0)
            .filter(venue -> !venue.isRequiresContact() || criteria.isIncludeUnverified())
            .sorted(Comparator.comparing(Venue::getPricePerHour))
            .collect(Collectors.toList());
    }
    
    // Принцип YAGNI: не добавляем сложную логику кластеризации на данном этапе
    public void flagVenuesRequiringContact() {
        // Простая реализация - флаг выставляется при создании/обновлении
        // В будущем можно добавить ML-кластеризацию
    }
}

// Принцип SOLID: Interface Segregation Principle
// Разделенный интерфейс для критериев поиска
public interface VenueSearchCriteria {
    String getVenueType();
    Integer getMinCapacity();
    BigDecimal getMaxPrice();
    boolean isIncludeUnverified();
}

// Простая реализация
@Data
public class BasicVenueSearchCriteria implements VenueSearchCriteria {
    private String venueType;
    private Integer minCapacity;
    private BigDecimal maxPrice;
    private boolean includeUnverified;
}
```
## 3. Budget.java (SOLID, DRY)
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
    
    private boolean isActive;
    private Date createdAt;
    
    // Принцип DRY: вычисление тотала в одном месте
    @PrePersist
    @PreUpdate
    public void calculateTotal() {
        this.total = venueCost
            .add(equipmentCost)
            .add(cateringCost)
            .add(marketingCost)
            .add(otherCosts);
    }
    
    // Принцип SOLID: Liskov Substitution Principle
    // Метод для добавления новой статьи расходов без изменения существующего кода
    public void addCustomExpense(String category, BigDecimal amount) {
        // Можно расширять без изменения основной логики
        if ("venueCost".equals(category)) {
            this.venueCost = this.venueCost.add(amount);
        } else if ("equipmentCost".equals(category)) {
            this.equipmentCost = this.equipmentCost.add(amount);
        }
        // Добавляем другие категории по мере необходимости (YAGNI)
        calculateTotal(); // Пересчитываем общую сумму
    }
    
    // Геттеры и сеттеры
    // ...
}
```
# Дополнительные принципы разработки
## 1. BDUF (Big Design Up Front) - Отказ
Обоснование отказа:

Неопределенность требований к кластеризации площадок: Проблема недостатка информации о площадках требует итеративного подхода, так как точные алгоритмы кластеризации могут быть определены только после анализа реальных данных.

Гибкость для изменений: Система для мероприятий должна адаптироваться к меняющимся требованиям пользователей и появлению новых сервисов-агрегаторов.

Принцип YAGNI: Не стоит проектировать сложные системы сбора данных заранее, когда можно начать с простого решения и расширять его по мере необходимости.

Вместо BDUF применяем: Итеративный подход с минимально жизнеспособным продуктом (MVP).

## 2. SoC (Separation of Concerns) - Применение
Обоснование применения:

Архитектурное разделение: Система четко разделена на уровни (Controller → Service → Repository), каждый из которых отвечает за свою зону ответственности.

Доменное разделение: Разные сервисы отвечают за разные домены (VenueService - площадки, BudgetComparisonService - бюджеты, TeamService - команды).

Инфраструктурное разделение: EmailClient изолирует логику отправки email от бизнес-логики.

Пример в коде: BudgetComparisonService отвечает только за сравнение бюджетов, а отправкой email занимается EmailClient.

## 3. MVP (Minimum Viable Product) - Применение
Обоснование применения:

Фокус на основных функциях: Первая версия системы включает только базовый функционал: поиск площадок, создание бюджета, сравнение вариантов, командное взаимодействие.

Отложенная сложность: Сложная ML-кластеризация площадок отложена на будущие итерации. Вместо этого используется простой флаг requiresContact.

Быстрая обратная связь: MVP позволяет быстро получить обратную связь от организаторов мероприятий и адаптировать развитие системы.

Реализация MVP:

Базовая фильтрация площадок по цене и вместимости

Простое сравнение бюджетов без сложной аналитики

Базовая система голосований в команде

Ручное обновление информации о площадках

## 4. PoC (Proof of Concept) - Применение для кластеризации
Обоснование применения:

Доказательство возможности кластеризации: Прежде чем внедрять сложную систему ML-кластеризации, нужно доказать, что автоматическая категоризация площадок возможна на основе доступных данных.

Оценка качества данных: PoC поможет оценить, достаточно ли данных в открытых источниках для автоматического обогащения информации о площадках.

Определение технических требований: Позволит оценить необходимые вычислительные ресурсы и сложность реализации.

### План PoC для кластеризации:

Собрать выборку данных о площадках из разных источников

Реализовать простые алгоритмы классификации (по ключевым словам, ценам, локациям)

Оценить точность автоматической категоризации

Определить, какие данные действительно требуют ручного уточнения

На основе результатов PoC принять решение о полноценной реализации

Вывод: Применение комбинации MVP (для основной системы), SoC (для архитектуры) и PoC (для сложных функций) позволяет создать гибкую, поддерживаемую систему, способную развиваться по мере появления новых требований и возможностей, избегая рисков, связанных с подходом BDUF.
