# Лабораторная работа №6: Использование шаблонов проектирования
## Цель работы
Получить опыт применения шаблонов проектирования GoF и GRASP при написании кода программной системы на примере информационной системы для подбора площадок/
## Шаблоны проектирования GoF
## Порождающие шаблоны 
### 1. Factory Method (Фабричный метод)
Назначение: Определяет интерфейс для создания объекта, но оставляет подклассам решение о том, экземпляр какого класса создавать.
Применение в проекте: Создание различных типов проектов мероприятий (конференция, форум, тренинг). Каждый тип может иметь свои параметры по умолчанию.

```python
from abc import ABC, abstractmethod

class Project(ABC):
    def __init__(self, name, date, location):
        self.name = name
        self.date = date
        self.location = location
        self.budget = None

    @abstractmethod
    def get_type(self):
        pass

class ConferenceProject(Project):
    def get_type(self):
        return "Conference"

class ForumProject(Project):
    def get_type(self):
        return "Forum"

class TrainingProject(Project):
    def get_type(self):
        return "Training"

class ProjectFactory(ABC):
    @abstractmethod
    def create_project(self, name, date, location):
        pass

class ConferenceFactory(ProjectFactory):
    def create_project(self, name, date, location):
        return ConferenceProject(name, date, location)

class ForumFactory(ProjectFactory):
    def create_project(self, name, date, location):
        return ForumProject(name, date, location)

class TrainingFactory(ProjectFactory):
    def create_project(self, name, date, location):
        return TrainingProject(name, date, location)
```
<img width="1373" height="327" alt="image" src="https://github.com/user-attachments/assets/801dd588-5749-4a7a-bd57-2d78712d1269" />

### 2. Singleton (Одиночка)
Назначение: Гарантирует, что класс имеет только один экземпляр, и предоставляет глобальную точку доступа к нему.
Применение в проекте: Класс для управления конфигурацией приложения (настройки подключения к БД, внешние API).

```python
class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Инициализация конфигурации
            cls._instance.DB_HOST = "db"
            cls._instance.DB_NAME = "eventdb"
            cls._instance.DB_USER = "postgres"
            cls._instance.DB_PASSWORD = "postgres"
        return cls._instance
```

<img width="440" height="256" alt="image" src="https://github.com/user-attachments/assets/4bd0268d-5b4b-4ed3-8d76-74fe1d992564" />

### 3. Builder (Строитель)
Назначение: Отделяет конструирование сложного объекта от его представления, позволяя создавать разные представления.
Применение в проекте: Построение объекта "Проект" с множеством необязательных параметров (бюджет, команда, площадки, дополнительные опции).

```python
class Project:
    def __init__(self):
        self.name = None
        self.date = None
        self.location = None
        self.budget = None
        self.team = []
        self.venue = None
        self.options = {}

    def __str__(self):
        return f"Project({self.name}, {self.date}, {self.location})"

class ProjectBuilder:
    def __init__(self):
        self.project = Project()

    def set_name(self, name):
        self.project.name = name
        return self

    def set_date(self, date):
        self.project.date = date
        return self

    def set_location(self, location):
        self.project.location = location
        return self

    def set_budget(self, budget):
        self.project.budget = budget
        return self

    def add_team_member(self, member):
        self.project.team.append(member)
        return self

    def set_venue(self, venue):
        self.project.venue = venue
        return self

    def add_option(self, key, value):
        self.project.options[key] = value
        return self

    def build(self):
        return self.project
```
<img width="452" height="578" alt="image" src="https://github.com/user-attachments/assets/8f35dfaf-6e14-476a-ba5d-5f94b5f0b730" />

## Структурные шаблоны 
### 1. Adapter (Адаптер)
Назначение: Преобразует интерфейс одного класса в интерфейс другого, ожидаемый клиентом.
Применение в проекте: Интеграция с внешним API агрегатора площадок (например, API Авито), который имеет несовместимый интерфейс с нашей системой.

```python
# Внешний API (не наш)
class ExternalVenueAPI:
    def get_venues_by_city(self, city):
        # возвращает данные в своём формате
        return [{"title": "Hall", "price": 10000}]

# Целевой интерфейс
class VenueProvider(ABC):
    @abstractmethod
    def get_venues(self, city):
        pass

# Адаптер
class VenueAdapter(VenueProvider):
    def __init__(self, external_api):
        self.external_api = external_api

    def get_venues(self, city):
        raw_data = self.external_api.get_venues_by_city(city)
        # преобразование в формат системы
        return [{"name": item["title"], "cost": item["price"]} for item in raw_data]
```
<img width="449" height="623" alt="image" src="https://github.com/user-attachments/assets/b1a138b4-7d32-4173-83b6-3d5620ed0acc" />

### 2. Decorator (Декоратор)
Назначение: Динамически добавляет новые обязанности объекту.
Применение в проекте: Добавление функциональности логирования к сервису проектов без изменения его кода.

```python
from functools import wraps

class ProjectService:
    def get_project(self, project_id):
        # реальная логика
        return {"id": project_id, "name": "Test"}

# Декоратор в виде функции 
def logging_decorator(service):
    @wraps(service.get_project)
    def wrapper(project_id):
        print(f"Getting project {project_id}")
        result = service.get_project(project_id)
        print(f"Result: {result}")
        return result
    service.get_project = wrapper
    return service
```
<img width="465" height="334" alt="image" src="https://github.com/user-attachments/assets/80ddf523-5d18-4f74-8a06-5ab2990da1c8" />

### 3. Facade (Фасад)
Назначение: Предоставляет унифицированный интерфейс к подсистеме.
Применение в проекте: Упрощение работы с комплексной подсистемой создания проекта, включающей проверку доступности площадок, расчёт бюджета, добавление участников.

```python
class VenueManager:
    def check_availability(self, venue_id, date):
        # сложная логика
        return True

class BudgetCalculator:
    def calculate(self, venue_cost, team_size, options):
        # сложная логика
        return venue_cost * team_size

class TeamManager:
    def add_members(self, project_id, members):
        # логика добавления
        pass

class ProjectFacade:
    def __init__(self):
        self.venue_mgr = VenueManager()
        self.budget_calc = BudgetCalculator()
        self.team_mgr = TeamManager()

    def create_project(self, name, date, venue_id, members, options):
        if not self.venue_mgr.check_availability(venue_id, date):
            raise Exception("Venue not available")
        budget = self.budget_calc.calculate(10000, len(members), options)
        # создание проекта в БД
        project_id = 123
        self.team_mgr.add_members(project_id, members)
        return project_id
```
<img width="857" height="211" alt="image" src="https://github.com/user-attachments/assets/17b7977e-46fe-4735-bfa0-7912eef1179a" />

### 4. Proxy (Заместитель)
Назначение: Контролирует доступ к объекту, выполняя дополнительные действия.
Применение в проекте: Контроль доступа к данным проекта в зависимости от роли пользователя.

```python
class ProjectRepository:
    def get_project(self, project_id):
        # реальное получение из БД
        return {"id": project_id, "name": "Secret Project", "owner": "admin"}

class ProjectProxy:
    def __init__(self, repository, user_role):
        self._repository = repository
        self._user_role = user_role

    def get_project(self, project_id):
        if self._user_role != "admin":
            raise PermissionError("Access denied")
        return self._repository.get_project(project_id)
```
<img width="452" height="474" alt="image" src="https://github.com/user-attachments/assets/ec6adeef-7b66-4308-a89d-38b79ed53c1d" />

## Поведенческие шаблоны 
### 1. Observer (Наблюдатель)
Назначение: Определяет зависимость типа "один ко многим" между объектами так, что при изменении состояния одного все зависимые оповещаются.
Применение в проекте: Уведомление участников команды об изменениях в проекте (новый комментарий, изменение даты).

```python
from abc import ABC, abstractmethod

class Observer(ABC):
    @abstractmethod
    def update(self, message):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        self._observers.append(observer)

    def detach(self, observer):
        self._observers.remove(observer)

    def notify(self, message):
        for observer in self._observers:
            observer.update(message)

class Project(Subject):
    def __init__(self, name):
        super().__init__()
        self.name = name

    def change_date(self, new_date):
        # изменение даты
        self.notify(f"Дата проекта {self.name} изменена на {new_date}")

class TeamMember(Observer):
    def __init__(self, name):
        self.name = name

    def update(self, message):
        print(f"{self.name} получил уведомление: {message}")
```
<img width="387" height="902" alt="image" src="https://github.com/user-attachments/assets/598914f3-3633-42b2-a38f-c7e25c58e526" />

### 2. Strategy (Стратегия)
Назначение: Определяет семейство алгоритмов, инкапсулирует каждый и делает их взаимозаменяемыми.
Применение в проекте: Различные способы расчёта бюджета мероприятия (фиксированный, почасовой, с учётом скидок).

```python
from abc import ABC, abstractmethod

class BudgetStrategy(ABC):
    @abstractmethod
    def calculate(self, base_cost, hours, participants):
        pass

class FixedBudget(BudgetStrategy):
    def calculate(self, base_cost, hours, participants):
        return base_cost

class HourlyBudget(BudgetStrategy):
    def calculate(self, base_cost, hours, participants):
        return base_cost * hours

class DiscountBudget(BudgetStrategy):
    def __init__(self, discount):
        self.discount = discount

    def calculate(self, base_cost, hours, participants):
        return base_cost * hours * (1 - self.discount)

class BudgetCalculator:
    def __init__(self, strategy: BudgetStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy):
        self._strategy = strategy

    def calculate(self, base_cost, hours, participants):
        return self._strategy.calculate(base_cost, hours, participants)
```
<img width="951" height="307" alt="image" src="https://github.com/user-attachments/assets/306669ac-19b0-4faa-8fd8-b47cc73b50cd" />

### 3. Command (Команда)
Назначение: Инкапсулирует запрос как объект, позволяя параметризовать клиенты с различными запросами, ставить запросы в очередь или логировать их.
Применение в проекте: Выполнение операций над проектом с возможностью отмены (undo). Например, добавление участника.

```python
from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass

class AddMemberCommand(Command):
    def __init__(self, project, member):
        self.project = project
        self.member = member

    def execute(self):
        self.project.add_member(self.member)

    def undo(self):
        self.project.remove_member(self.member)

class Project:
    def __init__(self):
        self.members = []

    def add_member(self, member):
        self.members.append(member)
        print(f"Добавлен {member}")

    def remove_member(self, member):
        if member in self.members:
            self.members.remove(member)
            print(f"Удалён {member}")

class CommandHistory:
    def __init__(self):
        self._history = []

    def execute_command(self, command):
        command.execute()
        self._history.append(command)

    def undo_last(self):
        if self._history:
            command = self._history.pop()
            command.undo()
```
<img width="415" height="902" alt="image" src="https://github.com/user-attachments/assets/9b1193c1-1190-499b-a070-278047c29b6a" />

### 4. State (Состояние)
Назначение: Позволяет объекту изменять своё поведение при изменении внутреннего состояния.
Применение в проекте: Проект может находиться в состояниях: черновик, активен, завершён. Поведение методов зависит от состояния.

```python
from abc import ABC, abstractmethod

class ProjectContext:
    def __init__(self):
        self.state = DraftState(self)

    def set_state(self, state):
        self.state = state

    def publish(self):
        self.state.publish()

    def complete(self):
        self.state.complete()

class ProjectState(ABC):
    def __init__(self, context):
        self.context = context

    @abstractmethod
    def publish(self):
        pass

    @abstractmethod
    def complete(self):
        pass

class DraftState(ProjectState):
    def publish(self):
        print("Переход в активное состояние")
        self.context.set_state(ActiveState(self.context))

    def complete(self):
        print("Нельзя завершить черновик")

class ActiveState(ProjectState):
    def publish(self):
        print("Уже активен")

    def complete(self):
        print("Завершение проекта")
        self.context.set_state(CompletedState(self.context))

class CompletedState(ProjectState):
    def publish(self):
        print("Завершённый проект нельзя опубликовать")

    def complete(self):
        print("Уже завершён")
```
<img width="515" height="495" alt="image" src="https://github.com/user-attachments/assets/5531fef8-d402-49e1-bd08-809f8b5c5202" />

### 5. Template Method (Шаблонный метод)
Назначение: Определяет скелет алгоритма в операции, оставляя некоторые шаги подклассам.
Применение в проекте: Общий процесс создания проекта, который может быть переопределён для разных типов проектов.

```python
from abc import ABC, abstractmethod

class ProjectCreator(ABC):
    def create_project(self, data):
        self.validate_data(data)
        project = self.build_project(data)
        self.after_create(project)
        return project

    def validate_data(self, data):
        if not data.get("name") or not data.get("date"):
            raise ValueError("Invalid data")

    @abstractmethod
    def build_project(self, data):
        pass

    def after_create(self, project):
        print(f"Проект {project.name} создан")

class SimpleProjectCreator(ProjectCreator):
    def build_project(self, data):
        return Project(data["name"], data["date"], data.get("location", ""))

class ConferenceProjectCreator(ProjectCreator):
    def build_project(self, data):
        # дополнительная логика для конференции
        return ConferenceProject(data["name"], data["date"], data["location"])

    def after_create(self, project):
        super().after_create(project)
        print("Отправлено уведомление спонсорам")
```
<img width="528" height="249" alt="image" src="https://github.com/user-attachments/assets/19e7f596-dd5c-4a91-8e35-1f9ef13c2994" />

## Шаблоны проектирования GRASP
Роли классов 
### 1. Information Expert (Информационный эксперт)
Проблема: Какому классу назначить ответственность за выполнение некоторой операции?
Решение: Назначить ответственность классу, который обладает наибольшей информацией, необходимой для выполнения задачи.
Пример: Класс Project сам отвечает за расчёт своей длительности (если у него есть даты начала и окончания).

```python
class Project:
    def __init__(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date

    def get_duration(self):
        return (self.end_date - self.start_date).days
```
Результат: Уменьшение связанности, повышение инкапсуляции.
Связь: Часто используется с шаблоном Strategy для делегирования алгоритмов.

### 2. Creator (Создатель)
Проблема: Кто должен создавать экземпляры класса?
Решение: Класс B должен создавать класс A, если B агрегирует A, содержит A, записывает A, или тесно использует A.
Пример: Класс Project создаёт объекты BudgetItem (статьи бюджета).

```python
class BudgetItem:
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

class Project:
    def __init__(self):
        self.budget_items = []

    def add_budget_item(self, name, amount):
        item = BudgetItem(name, amount)  # Creator
        self.budget_items.append(item)
```
Результат: Упрощение управления жизненным циклом объектов.
Связь: Связан с порождающими шаблонами (Factory Method, Builder).

### 3. Controller (Контроллер)
Проблема: Как обрабатывать события, поступающие от пользовательского интерфейса?
Решение: Назначить класс-контроллер, который отвечает за обработку системных событий.
Пример: Класс ProjectController обрабатывает HTTP-запросы во Flask.

```python
@app.route('/api/projects', methods=['POST'])
def create_project():
    data = request.get_json()
    # контроллер делегирует выполнение сервису
    project_service.create_project(data)
    return jsonify({"status": "ok"})
```
Результат: Чёткое разделение между UI и бизнес-логикой.
Связь: Часто используется с Facade.

### 4. Low Coupling (Низкая связанность)
Проблема: Как уменьшить зависимость между классами?
Решение: Назначать ответственности так, чтобы связанность оставалась низкой.
Пример: Использование интерфейсов и внедрение зависимостей.

```python
class ProjectService:
    def __init__(self, repository):  # зависит от абстракции
        self.repository = repository

class ProjectRepository(ABC):
    @abstractmethod
    def save(self, project):
        pass
```
Результат: Лёгкость повторного использования и тестирования.
Связь: Связан с Dependency Inversion.

### 5. High Cohesion (Высокая связность)
Проблема: Как сделать классы сфокусированными и понятными?
Решение: Назначать ответственности так, чтобы они были тесно связаны и класс имел чёткое назначение.
Пример: Класс BudgetCalculator занимается только расчётами бюджета, а не работой с БД.

```python
class BudgetCalculator:
    def calculate(self, items):
        return sum(item.amount for item in items)
```
Результат: Лёгкость поддержки и понимания.
Связь: Противоположность "God object".

## Принципы разработки 
### 1. Open/Closed Principle (Открытости/Закрытости)
Проблема: Как сделать класс открытым для расширения, но закрытым для модификации?
Решение: Использовать абстракции и полиморфизм.
Пример: Добавление новых типов бюджетных стратегий без изменения существующего кода (см. Strategy).

```python
# Добавление новой стратегии не требует изменения BudgetCalculator
class PremiumBudget(BudgetStrategy):
    def calculate(self, base_cost, hours, participants):
        return base_cost * hours * 1.2
```
Результат: Гибкость и уменьшение риска внесения ошибок.
Связь: Реализуется через полиморфизм и шаблоны Strategy, Template Method.

### 2. Dependency Inversion Principle (Инверсия зависимостей)
Проблема: Как избежать зависимости от конкретных классов?
Решение: Зависеть от абстракций, а не от реализаций.
Пример: Внедрение зависимости через интерфейс репозитория.

```python
class ProjectService:
    def __init__(self, repo: ProjectRepository):  # зависит от абстракции
        self.repo = repo
```
Результат: Лёгкая замена реализаций (например, in-memory репозиторий на PostgreSQL).
Связь: Используется с IoC-контейнерами.

### 3. Interface Segregation Principle (Разделение интерфейса)
Проблема: Как избежать "жирных" интерфейсов, которые клиенты вынуждены реализовывать?
Решение: Разбивать интерфейсы на более мелкие, специфичные.
Пример: Разделение интерфейса для работы с проектами на ProjectReader и ProjectWriter.

```python
class ProjectReader(ABC):
    @abstractmethod
    def get(self, id):
        pass

class ProjectWriter(ABC):
    @abstractmethod
    def save(self, project):
        pass

class ProjectRepository(ProjectReader, ProjectWriter):
    # реализация
    pass
```
Результат: Уменьшение ненужных зависимостей.
Связь: Связан с Low Coupling.

## Свойство программы 
### Гибкость (Flexibility)
Проблема: Как сделать систему адаптируемой к изменениям требований?
Решение: Применение шаблонов проектирования (Strategy, Observer, Factory Method) позволяет легко добавлять новые варианты поведения без изменения существующего кода.
Пример: В проекте используется стратегия расчёта бюджета. Добавление нового алгоритма не требует правки классов, использующих стратегию.

```python
# Добавляем новую стратегию
class SeasonalBudget(BudgetStrategy):
    def calculate(self, base_cost, hours, participants):
        return base_cost * hours * 0.9  # сезонная скидка

# Использование без изменения BudgetCalculator
calculator.set_strategy(SeasonalBudget())
```
Результат: Система легко расширяется, что снижает стоимость сопровождения.
Связь: Обеспечивается применением Open/Closed, Dependency Inversion и соответствующих шаблонов GoF.

# Заключение
В данной лабораторной работе были применены 12 шаблонов проектирования GoF (3 порождающих, 4 структурных, 5 поведенческих) к информационной системе для подбора площадок. Также проанализированы и реализованы ключевые принципы GRASP: выделены 5 ролей классов, 3 принципа разработки и 1 свойство программы. Полученный код стал более гибким, расширяемым и поддерживаемым.
