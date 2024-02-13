# SqlAlchemy

Позволяет описывать структуру БД и взаимодействие с ней на ЯП Python.

## Преимущества

- Безопасность (экранизация параметров)
- Производительность (может применять повторно план выполнения запроса в случае повторного запроса)
- Переносимость (без труда можно перейти на другую СУБД, не меняя код, потому что это некая абстракция)
- Легче читать, проверять, так как это python код, объекты (типизация)
- Самая популярная ORM
- Единый стиль написания запросов
- Удобно работать с вложенными структурами

## Ресурсы

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

## Создание движка

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

## Session

Когда мы входим в сессию, открывается транзакция

Предоставляет удобный интерфейс для выполнения запросов, добавления, изменения и удаления данных в базе данных.

- позволяет начать, фиксировать или откатывать транзакцию в зависимости от рез-та
- отслеживает изменения в объекте и авто. генерирует SQL запросы
- кэширует запросы и рез-ты выпол-ия
- эффективно управляет соединением с БД

## Фабрика сессий: работа с сессиями

Это - фабрика сессий, генерирующая объекты сессий. Предоставляет удобный способ создания сессий с параметрами (движком и др.). Позволяет избежать повтора (DRY).

```python
session_factory = sessionmaker(engine)
```

## Использование контекстного менеджера with

Преимущества:
- Автоматическое управление транзакциями (Например, с помощью контекстного менеджера session в SQLAlchemy вы можете автоматически открывать, фиксировать и откатывать транзакции, обеспечивая целостность данных.)
- Корректное открытие и закрытие соединений с БД
- Безопасное обращение с ресурсами - даже в случае исключения, гарантируется что закрытие будет завершено правильно
- Читаемость кода

## Создание соединения с БД

Для создания нового соединения с базой у engine есть 2 метода:
- .begin()
    - начинает новую транзакцию
    - возвращает объект транзакции
    - автоматически фиксирует (commit) или откатывает (rollback), в зависимости от рез-та операции в блоке кода
- .connect()
    - явно создается соединение
    - метод возвращает объект соединения, с помощью которого можно выполнять запросы к БД

Отличие в том, что begin() после выхода из контекстного менеджера делает commit, а connect() - rollback

Т.к. явное лучше не явного, лучше использовать connect() и явно прописывать conn.commit():

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

## Сырой запрос через text

```python
with engine.connect() as conn:
    res = conn.execute(text("SELECT VERSION()"))
    print(res)
    conn.commit()
```

## Получение одной строки

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
- автоматическое генерирование запросов на создание и изменение
- облегчает работу с миграциями

## Императивный стиль / SQLAlchemy Core

### Описание

- В императивном стиле таблицы определяются непосредственно с использованием языка Python.
- Вы создаете объекты таблиц, столбцов, индексов и ограничений напрямую в коде Python с помощью классов и методов SQLAlchemy.
- Этот стиль более прямолинеен и ближе к стандартному программированию на Python.

### Пример создания таблицы

```python
workers_table = Table(
    "workers",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("username", String),
)
```

### Методы объекта Table

- Имя таблицы:
`workers_table.name`

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

#### SQL выражения

- sqlalchemy.schema.Table.select()
- sqlalchemy.schema.Table.delete()
- sqlalchemy.schema.Table.insert()
- sqlalchemy.schema.Table.update()
- sqlalchemy.schema.Table.join()
- sqlalchemy.schema.Table.outerjoin()

#### Удаление отдельной таблицы

Также можно создать/удалить отдельно таблицу, вызвав метод класса Table *create*/*drop*

```python
workers_table.create(engine)
```

### INSERT/Вставка данных

#### Сырой запрос
```python
file_path = Path(__file__).parent / 'test_data.sql'
with open(file_path) as sql_file:
	sql_stmt = sql_file.read()
	with engine.connect() as conn:
		conn.execute(text(sql_stmt))
		conn.commit()
```

#### С помощью Query Builder / строителя запросов

```python
sql_stmt = insert(models.workers_table).values([
		{"username": "John"},
		{"username": "Michael"},
	])
with engine.connect() as conn:
	conn.execute(sql_stmt)
	conn.commit()
```

### SELECT запрос

```python
with engine.connect() as conn:
	query = select(models.workers_table)
	result = conn.execute(query)
	print(result.all())
```

`.all()` - возвращает все строки не в виде объекта, а в виде списка кортежей
`.scalars().all()` - возвращает первый столбец в каждой строке (полезно при SELECT запросе через ORM)

### UPDATE запрос

#### Сырой запрос

```python
def update_worker(worker_id: int = 1, username: str = "Emanuel"):
	with engine.connect() as conn:
		stmt = text("UPDATE workers SET username=:username where id=:id")
		stmt = stmt.bindparams(username=username, id=worker_id)
		conn.execute(stmt)
		conn.commit()
```

⚠️**Важно** Всегда использовать bindparams для предотвращения sql-инъекций

#### С помощью Query Builder / строителя запросов

```python
def update_worker(worker_id: int = 1, username: str = "Emanuel"):
    with engine.connect() as conn:
        stmt = (
            update(models.workers_table)
            .values(username=username)
            # .where(models.workers_table.c.id == worker_id)
            # .filter(models.workers_table.c.id == worker_id)
            .filter_by(id=worker_id)
        )
        conn.execute(stmt)
        conn.commit()
```

Фильтр where можно задавать следующими способами:
- `.where()` - столбцы указываются в формате <table>.c.<column> `.where(workers_table.c.id == 1)`
- `.filter()` - синоним для .where() `.filter(workers_table.c.username == 'John')`
- `.filter_by()` - столбцы указываются в kwarg стиле (без указания названия таблицы) `.filter_by(id=2)`

## Декларативный стиль / SQLAlchemy ORM

### Описание

Декларативный означает что код описывает что должно быть сделано, но не как должно.

- В декларативном стиле определение таблиц выносится в классы Python, которые являются подклассами специального класса, предоставляемого SQLAlchemy (declarative_base).
- Вы описываете структуру таблицы, используя декларативный синтаксис, а SQLAlchemy автоматически создает объекты таблиц на основе этих классов.
- Описываем желаемый результат (структуру таблицы) в терминах объектов и их свойств, а не пишем прямые инструкции о том, как создать результат.

**DeclarativeBase** - базовый класс для объявления моделей данных в декларативном стиле

### Создание базового класса Base
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

### INSERT/Вставка данных

```python
with session_factory() as session:
    worker_bobr = Workers(username="bobr")
    worker_volk = Workers(username="volk")
    # session.add(worker_bobr)
    # session.add(worker_volk)
    session.add_all([worker_bobr, worker_volk])
    session.commit()
```

### SELECT

#### Получение одной записи

Если в таблице первичный ключ только один:
```python
worker_id = 1
worker_jack = session.get(Workers, worker_id)
```

Если в таблице первичных ключей несколько:
- можно передать кортеж:
```python
worker_jack = session.get(Workers, (1, "John"))
```
- можно передать словарь
```python
worker_jack = session.get(Workers, {"id": 1, "username": "John"})
```

#### Получение нескольких записей

```python
with session_factory() as session:
	query = select(Workers)
	result = session.execute(query)
	print(result.scalars().all())
```

Разница с Core в том, что sqlalchemy получит данные и превратит их в модели (в инстансы/экземпляры модели Workers)

#### Использование функции агрегирования, приведение типа, объединения и условия contains,

```sql
SELECT resumes.workload, CAST(avg(resumes.compensation) AS INTEGER) AS avg_compensation
FROM resumes
WHERE (resumes.title LIKE '%' || 'Python' || '%') AND resumes.compensation > 40000
GROUP BY resumes.workload
```

```python
def select_resumes_avg_compensation(like_language: str = "Python"):
	with session_factory() as session:
		query = (
			select(
				Resumes.workload,
				func.cast(func.avg(Resumes.compensation), Integer).label("avg_compensation")
			)
			.select_from(Resumes)
			.filter(and_(
				Resumes.title.contains(like_language),
				Resumes.compensation > 40000
			))
			.group_by(Resumes.workload)
		)
		print(query.compile(compile_kwargs={"literal_binds": True}))
		res = session.execute(query)
		result = res.all()
		print(result)
		print(result[0].avg_compensation)
```

#### Сложные запросы

```sql
WITH helper2 AS (
  SELECT
    *,
    compensation - avg_workload_compensation AS compensation_diff
  FROM
    (
      SELECT
        w.id,
        w.username,
        r.compensation,
        r.workload,
        avg (r.compensation) OVER (PARTITION BY workload) :: int AS avg_workload_compensation
      FROM
        resumes r
        JOIN workers w ON r.worker_id = w.id
    ) helper1
)
SELECT
  *
FROM
  helper2
ORDER BY
  compensation_diff DESC;
```

### UPDATE/Обновление
```python
def update_worker(worker_id: int = 1, username: str = "emanuel"):
    with session_factory() as session:
        worker_michael = session.get(Workers, worker_id)
        worker_michael.username = username
        session.commit()
```

**⚠️ Важно**

При обновлении с использованием ORM делается 2 запроса: сначала на получение строки, далее на обновление

### Синхронизация изменений с базой данных: Session Flush

#### Описание

Используется для синхронизации всех изменений объектов модели с базой данных, но без фиксации транзакции.

Отправляет все ожидающие команды (например, добавление, изменение, удаление записей) в базу данных, но не фиксирует изменения, как это делает session.commit().

#### Причины использования flush

- предварительная проверка целостности (все ли данные прошли валидацию полей БД)
- повышение производительности (когда имеется большой объем данных, которые должны быть выполнены при фиксации изменений)
- Обновление автоматически генерируемых значений (например auto-increment id, или created_at, updated_at)

### Сброс состояния объектов: expire и expire_all

#### Описание

Используется для сброса изменений до фиксации.

#### Expire all
Новый запрос в БД будет сделан только если после expire_all() будет обращение к аттрибутам экземпляра

```python
worker_michael = session.get(Workers, worker_id)
worker_michael.username = username
session.expire_all()
print(worker_michael.username) # здесь будет сделан запрос
session.commit()
```

### Актуализация данных: Refresh

Используется для получения самых актуальных данных

```python
worker_michael = session.get(Workers, worker_id)
worker_michael.username = username
session.refresh(worker_michael)
session.commit()
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

Действие, которое будет выполняться при удалении родительской записи (на которую ссылается внешний ключ):

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

Т.к. мы не можем быть уверены, что обновление всегда будет происходить при помощи ORM модели, лучшим решением будет в postgres обновлять это поле при помощи триггера

```sql
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

#### Рядом с моделями

```python
from typing import Annotated

intpk = Annotated[int, mapped_column(primary_key=True)]

class Workers(Base):
    ...
    id: Mapped[intpk]
```

#### Рядом с классом Base

**database.py**

```python
from typing import Annotated

str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
	type_annotation_map = {
		str_256: String(256)
	}
```

**models.py**

```python
from database import Base, str_256
from sqlalchemy.orm import Mapped

class Resumes(Base):
	...
	title: Mapped[str_256]
```

## Relationships

#### Lazy Load / ленивая загрузка

Данные подгружаются только тогда, когда нужны. Заранее связанные данные Join'ом не загружаются.

Проблема N+один - для любых N загруженных объектов обращение к их атрибутам в режиме ленивой загрузки выполнит N+1 операторов SELECT

Например:

Загрузили N работников

Далее обратились к резюме первого работника: result[0].resumes

Выполнятся N+1 запросов, потому что для каждого работника выполнится еще по одному запросу для получения резюме

⚠️**Важно**
Ленивая загрузка НЕ работает в асинхронном варианте

```python
class Workers(Base):
	...
	resumes: Mapped[list["Resumes"]] = relationship()
```

```python
class Resumes(Base):
	...
	worker: Mapped["Workers"] = relationship()
```

```python
def select_workers_lazy_relationship():
	with session_factory() as session:
		query = select(Workers)
		res = session.execute(query)
		result = res.scalars().all()
		print(result[0].resumes)
```

#### Joined Load

Не подходит для one-to-many или many-to-many (потому что из БД выгружаются лишние, дублирующие данные)

Подходит для many-to-one или one-to-one.

```python
def select_workers_joined_relationship():
	with session_factory() as session:
		query = (
			select(Workers)
			.options(joinedload(Workers.resumes))
		)
		res = session.execute(query)
		result = res.unique().scalars().all()
		print(result[0].resumes)
```

#### Select in load

Подходит для one-to-many или many-to-many

```python
def select_workers_selectin_relationship():
	with session_factory() as session:
		query = select(Workers).options(selectinload(Workers.resumes))
		res = session.execute(query)
		result = res.unique().scalars().all()
		print(result[0].resumes)
```

#### __repr__ метод в базовом классе Base для ORM моделей

```python
class Base(DeclarativeBase):
	"""Включить в __repr__ метод вывод <кол-во> первых колонок"""
	include_repr_columns_num = 3
	"""Включить в __repr__ метод вывод перечисленных колонок, помимо :include_repr_columns_num"""
	include_repr_columns = ()

	def __repr__(self):
		columns = []

		for idx, column in enumerate(self.__table__.columns.keys()):
			if (
				idx < self.include_repr_columns_num
				or column in self.include_repr_columns
			):
				columns.append(column)

		cols = [f"{c}={getattr(self, c)}" for c in columns]
		cols_str = ",".join(cols)
		return f'<{self.__class__.__name__} {cols_str}>'

class Resumes(Base):
	...
	include_repr_columns = ("workload", )
```

#### Фильтрация при работе с Relationships

Для joinedload он включит фильтрацию в ON

```python
query = select(Workers).options(joinedload(Workers.resumes.and_(Resumes.workload == Workload.parttime)))
```

```sql
FROM workers LEFT OUTER JOIN resumes AS resumes_1 ON workers.id = resumes_1.worker_id AND resumes_1.workload = 'parttime'
```

#### Различие join и joinedload

Основное различие между join и joinedload заключается в том, что join используется для объединения таблиц при выполнении запросов SQL, в то время как joinedload используется для эффективной загрузки связанных объектов в память в рамках одного запроса к базе данных в SQLAlchemy.

#### Ссылки в Relationship

##### Самая простая реализация

```python
class Workers(Base):
	...
	resumes: Mapped[list["Resumes"]] = relationship()


class Resumes(Base):
	...
	worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
	
	worker: Mapped["Workers"] = relationship()
```

##### back_populates и backref

Используются для определения двунаправленных отношений (bidirectional relationships) между моделями данных.

Различие:
- **back_populates** определяется в обеих моделях данных, участвующих в отношении,
- в то время как **backref** определяется только в одной модели данных и автоматически создает обратное отношение.

Рекомендуется использовать **back_populates**

```python
class Workers(Base):
	...
	resumes: Mapped[list["Resumes"]] = relationship(
		back_populates="worker"
	)


class Resumes(Base):
	...
	worker_id: Mapped[int] = mapped_column(ForeignKey("workers.id", ondelete="CASCADE"))
	
	worker: Mapped["Workers"] = relationship(
		back_populates="resumes"
	)
```

#### Явное указание условий соединения и сортировки

```python
class Workers(Base):
	...
	resumes_parttime: Mapped[list["Resumes"]] = relationship(
		back_populates="worker",
		primaryjoin="and_(Workers.id == Resumes.worker_id, Resumes.workload == 'parttime')",
		order_by="Resumes.id.desc()"
	)
```

#### Загрузка связанных объектов при .join

Для этого необходимо указать опцию `contains_eager`

При использовании contains_eager(Workers.resumes) вы говорите SQLAlchemy загрузить связанные объекты Resumes вместе с объектами Workers в рамках одного запроса.

Полезно, когда вы знаете, что нужно получить связанные объекты вместе с основными объектами и хотите избежать доп. запросов к БД.

```python
def select_workers_contains_eager():
	with session_factory() as session:
		query = (
			select(Workers)
			.join(Workers.resumes)
			.options(contains_eager(Workers.resumes))
		)
		res = session.execute(query)
		result = res.unique().scalars().all()
```

#### Лимитированная выборка связанных данных

- `scalar_subquery()`
Преобразует результат запроса в скалярное значение (одно значение) вместо списка или кортежа.
Это означает, что подзапрос будет возвращать только одно значение, а не список значений или строки.

- `correlate()`
Используется для корреляции подзапроса с основным запросом, что позволяет использовать значения из основного запроса в подзапросе.
В данном случае метод correlate(Workers) указывает, что подзапрос должен быть скоррелирован с таблицей Workers, что позволяет использовать значения из Workers внутри подзапроса.
Необходимо для фильтрации по Workers.id

```python
sub_query = (
	select(Resumes.id.label("parttime_resume_id"))
	.filter(Resumes.worker_id == Workers.id)  # Нужно для join'а в query
	.order_by(Workers.id.desc())
	.limit(2)
	.scalar_subquery()
	.correlate(Workers)
)
query = (
	select(Workers)
	.join(Resumes, Resumes.id.in_(sub_query))
	.options(contains_eager(Workers.resumes))
)
```

#### Index и CheckConstraint

```python
from sqlalchemy import CheckConstraint
from sqlalchemy import Index

class Resumes(Base):
    ...
    __table_args__ = (
		Index("resumes_title_idx", "title"),
		CheckConstraint("compensation > 0", name="resumes_check_compensation_gt_0")
	)
```