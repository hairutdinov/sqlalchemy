# SqlAlchemy

Позволяет описывать структуру БД и взаимодействие с ней на ЯП Python.

## Преимущества

- Безопасность (экранизация параметров)
- Производительность (может применять повторно план выполнения запроса в случае повторного запроса)
- Переносимость (без труда можно перейти на другую СУБД, не меняя код, потому что это некая абстракция)
- Легче читать, проверять, так как это python код, объекты
- Самая популярная ORM

### Ресурсы

- https://lectureswww.readthedocs.io/6.www.sync/2.codding/9.databases/2.sqlalchemy/0.engine.html#create-engine
- https://pythonru.com/biblioteki/ustanovka-i-podklyuchenie-sqlalchemy-k-baze-dannyh

## Схема устройства / Диаграмма уровней SQLAlchemy

ORM (англ. object-relational mapping, рус. объектно-реляционное отображение) — представление БД и сущностей в виде Объектов, создавая "виртуальную объектную БД"

￼￼![SQL Alchemy Layers](https://lectureswww.readthedocs.io/_images/sqlalchemy_layers_ru.png "SQL Alchemy Layers")

### 1-ый слой

DBAPI (Database Application Programming Interface) - движок/драйвер/диалект - это библиотеки: psycopg2 (для PostgreSQL), или MySQL-Python (MySQL), которые соответствуют некоторому API (которая едина для всех) и имеют следующие особенности и функции:
- Подключение к БД - предоставляет способы подключения к разным типам БД
- Выполнение запросов
- Получение результата
- Управление транзакциями
- Параметризованные запросы

### 2-ой слой

Основная часть SQLAlchemy / SQLAlchemy Core - работает с соединениями с БД (открывает, закрывает, отправляет запросы в DBAPI, формирует запросы)

### 3-ий слой

Подсистема объектно-реляционного отображения

### Диалект SQLAlchemy


SQL — это стандартный язык для работы с базами данных. Но и он отличается от базы к базе. Производители БД добавляют свои особенности.

Для обработки таких различий и нужен диалект.
Диалект определяет поведение БД - отвечает за обработку SQL инструкций.

После установки соответствующего драйвера диалект обрабатывает все отличия, что позволяет сосредоточиться на создании самого приложения.


## Database Connection


**Создаем движок**
- url - строка подключения к БД
    - DSN (Data Source Name) - это строка или набор параметров, используемых для определения и настройки подключения к базе данных или другому источнику данных. В отличие от URL, который чаще всего используется в контексте веб-приложений и имеет строго определенный формат, DSN обычно предоставляет более гибкий и специфический для конкретной базы данных способ определения соединения.
    - формат: dialect+driver://username:password@host:port/database
- echo - должен ли SQLAlchemy выводить в консоль SQL-запросы, которые он генерирует
- pool_size -  размер пула соединений к базе данных. Пул соединений - это набор предварительно созданных и готовых к использованию соединений к базе данных. Установка размера пула позволяет контролировать количество одновременно открытых соединений к базе данных.
- max_overflow - Этот аргумент устанавливает максимальное количество "лишних" (overflow) соединений, которые могут быть созданы сверх установленного размера пула соединений. Если количество запросов к базе данных превышает размер пула, SQLAlchemy может создать дополнительные соединения до достижения значения max_overflow. Это позволяет обеспечить более гибкое управление соединениями в периоды пиковой нагрузки.

```python
engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10
)

```

### Использование контекстного менеджера


Преимущества:
- Автоматическое управление транзакциями (Например, с помощью контекстного менеджера session в SQLAlchemy вы можете автоматически открывать, фиксировать и откатывать транзакции, обеспечивая целостность данных.)
- Корректное открытие и закрытие соединений с БД
- Безопасное обращение с ресурсами - даже в случае исключения, гарантируется что закрытие будет завершено правильно
- Читаемость кода


## Первый запрос


Для создании нового соединения с базой у engine есть 2 метода:
- .begin()
    - начинает новую транзакцию
    - возвращает объект транзакции
    - автоматически фиксирует (commit) или откатывает (rollback), в зависимости от рез-та операции в блоке кода
- .connect()
    - явно создается соединение
    - метод возвращает объект соединения, с помощью которого можно выполнять запросы к БД

Отличие в том, что begin() после выхода из контекстного менеджера делает commit, а connect() - rollback

Т.к. явное лучше не явного, лучше использовать connect() и явно прописывать conn.commit():

```python
with engine.connect() as conn:
    res = conn.execute(text("SELECT VERSION()"))
    print(res)
    conn.commit()
```

Чтобы вернуть одну строчку, можно использовать на результате res метод .one()/.first() (но в запросе все равно вытащиться все строки и one() будет работать на уже полученных данных, хранящихся в RAM), или все строчки - .all()

- .one():
    - Метод .one() ожидает, что запрос вернет ровно один результат.
    - Если запрос возвращает несколько строк или ни одной строки, .one() вызовет исключение MultipleResultsFound или NoResultFound соответственно.
    - Этот метод полезен, когда вы уверены, что ваш запрос вернет ровно один результат.
- .first():
    - Метод .first() возвращает первую строку результата запроса.
    - Если запрос не вернет ни одной строки, то метод вернет None.
    - Этот метод удобен, когда вы хотите получить только первую строку результата или когда вы не уверены, что запрос вернет хотя бы одну строку.

## Объект MetaData

Причины создания:
- для определения структуры базы данных (таблицы, столбцы, индексы и ограничения)
- автоматическое генерирования запросов на создание и изменение
- облегчает работу с миграциями

### Описание таблиц в императивном стиле

- В императивном стиле таблицы определяются непосредственно с использованием языка Python.
- Вы создаете объекты таблиц, столбцов, индексов и ограничений напрямую в коде Python с помощью классов и методов SQLAlchemy.
- Этот стиль более прямолинеен и ближе к стандартному программированию на Python.

```python
workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)
```

## Описание таблиц в декларативном стиль

Декларативный означает что код описывает что должно быть сделано, но не как должно.

- В декларативном стиле определение таблиц выносится в классы Python, которые являются подклассами специального класса, предоставляемого SQLAlchemy (declarative_base).
- Вы описываете структуру таблицы, используя декларативный синтаксис, а SQLAlchemy автоматически создает объекты таблиц на основе этих классов.
- Описываем желаемый результат (структуру таблицы) в терминах объектов и их свойств, а не пишем прямые инструкции о том, как создать результат.

**DeclarativeBase** - базовый класс для объявления моделей данных в декларативном стиле

```python
from sqlalchemy.orm import DeclarativeBase
class Base(DeclarativeBase):
    pass
```

### Создание всех таблиц
```python
Base.metadata.create_all(engine)
```

### Удаление всех таблиц
```python
Base.metadata.drop_all(engine)
```

### Вставка данных в таблицу

```python
with session_factory() as session:
    worker_bobr = Workers(username="bobr")
    worker_volk = Workers(username="volk")
    # session.add(worker_bobr)
    # session.add(worker_volk)
    session.add_all([worker_bobr, worker_volk])
    session.commit()
```

#### Session Factory создается так:

```python
session_factory = sessionmaker(engine)
```


### Указание необязательности поля
```python
# Способ 1
compensation: Mapped[int] = mapped_column(nullable=True)
# Способ 2
compensation: Mapped[Optional[int]]
# Способ 3
compensation: Mapped[int | None]
```

### Enum поле

```python
from enum import Enum

class Workload(Enum):
    parttime = "parttime"
    fulltime = "fulltime"

class Resumes(Base):
	...
	workload: Mapped[Workload]
```

### Вторичный ключ

```python
class Workers(Base):
    ...
    id: Mapped[int] = mapped_column(primary_key=True)


class Resumes(Base):
	# Способ 1
	worker_id = Mapped[int] = mapped_column(ForeignKey("workers.id"))
	# Способ 2
	worker_id = Mapped[int] = mapped_column(ForeignKey(Workers.id))
```

Лучше использовать строчную запись вторичного ключа: `"workers.id"`

Действие, которое будет выполняться при удалении родительской записи (на которую ссылкается внешний ключ):

```python
ForeignKey("workers.id", ondelete="CASCADE")
```

Варианты ondelete:
- CASCADE
- RESTRICT
- SET NULL
- NO ACTION

### Поле created_at

```python
created_at = Mapped[datetime] = mapped_column(server_default=func.now())
```

Но лучше by default вставлять время без часового пояса (utc)

```python
created_at = Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
```

### Поле updated_at

```python
updated_at = Mapped[datetime] = mapped_column(
	server_default=text("TIMEZONE('utc', now())"),
	onupdate=datetime.utcnow()
)
```

Т.к. мы не можем быть уверены, что обновление всегда будет происходить при помощи ORM модели, лучшим решением будет в postgres обнолять это поле при помощи триггера

```python
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
	NEW.updated_at = TIMEZONE('utc', NOW());
	RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_updated_at
BEFORE UPDATE ON <your_table_name>
FOR EACH ROW
EXECUTE FUNCTION update_updated_at();
```

### Кастомные типы

```python
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]

class Workers(Base):
    ...
    id: Mapped[intpk]
```

### Кастомные типы рядом с классом Base

##### database.py
```python
from typing import Annotated

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
	type_annotation_map = {
		str_256: String(256)
	}
```

##### models.py

```python
from database import Base, str_256
from sqlalchemy.orm import Mapped

class Resumes(Base):
	...
	title: Mapped[str_256]
```

## Вставка данных

### Сырой запрос
```python
file_path = Path(__file__).parent / 'test_data.sql'
with open(file_path) as sql_file:
	sql_stmt = sql_file.read()
	with engine.connect() as conn:
		conn.execute(text(sql_stmt))
		conn.commit()
```

### С помощью Query Builder / строителя запросов

```python
sql_stmt = insert(models.workers_table).values([
        {"username": "Bobr"},
        {"username": "Volk"},
    ])
    with engine.connect() as conn:
        conn.execute(sql_stmt)
        conn.commit()
```

## Методы объекта Table

- Имя таблицы:
```python
workers_table.name
```

- Поля таблицы:
```python
print(workers_table.c)
```

- Инспектирования полей таблицы:

```python
print(workers_table.c.username)
```

- Name и Type полей таблицы:

```python
print(workers_table.c.username.name)
print(workers_table.c.username.type)
```

- Первичные ключи:

```python
print(workers_table.primary_key)
```

### SQL выражения

- sqlalchemy.schema.Table.select()
- sqlalchemy.schema.Table.delete()
- sqlalchemy.schema.Table.insert()
- sqlalchemy.schema.Table.update()
- sqlalchemy.schema.Table.join()
- sqlalchemy.schema.Table.outerjoin()

Также можно создать/удалить отдельно таблицу, вызвав метод класса Table *create*/*drop*

```python
workers_table.create(engine)
```
## Отражение / Reflection

Автоматическое создание объекта модели на основе существующей структуры БД.

Когда вы отражаете базу данных в SQLAlchemy, библиотека анализирует метаданные базы данных (таблицы, столбцы, индексы и ограничения) и автоматически создает соответствующие объекты модели

```python
metadata2 = MetaData()
workers_reflection = Table("workers", metadata2, autoload_with=engine)
print(workers_reflection.primary_key)
```

Или можно сделать отражение всей БД

```python
metadata2 = MetaData()
metadata2.reflect(bind=engine)
tables = metadata2.tables
workers_table = metadata2.tables["workers"]
print(tables.keys())
```

[Перейти к документации](https://docs.sqlalchemy.org/en/20/core/reflection.html)

## Интроспекция / Introspection

Анализ схемы БД во время выполнения

```python
from sqlalchemy import inspect
inspector = inspect(engine)
print(inspector.get_table_names())
print(inspector.get_columns('workers'))
```

[Перейти к документации](https://docs.sqlalchemy.org/en/20/core/inspection.html#sqlalchemy.inspect)

## Session

Когда мы входим в сессию, открывается транзакция

Предоставляет удобный интерфейс для выполнения запросов, добавления, изменения и удаления данных в базе данных.

- позволяет начать, фиксировать или откатывать транзакцию в зависимости от рез-та
- отслеживает изменения в объекте и авто. генерирует SQL запросы
- кэширует запросы и рез-ты выпол-ия
- эффиктивно управляят соединением с БД

### sessionmaker
Это - фабрика сессий, генерирующая объекты сессий. Предоставляет удобный способ создания сессий с параметрами (движком и др.). Позволяет избежать повтора (DRY).
