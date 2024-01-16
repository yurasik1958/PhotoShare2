PhotoShare - REST API для зберігання та управління фотоальбомів.
API побудований з використанням інфраструктури FastAPI та SQLAlchemy для управління базою даних.

Коористувачі та фотоальбоми зберігаються в базі даних PostgreSQL.
Світлини з альбомів зберігаються з використанням сервісу Cloudinary.

API має можливість виконувати наступні дії:

1. Зарееструватися новому користувачу з верифікацією його електронної пошти.
2. Залогінитися користувачу (пройти автентифікацію).


Зареестрованому користувачу після успішної автентифікаціі доступно:

1. Додати нову світлину з описом у свій фотоальбом.
2. Видалити світлину зі свого фотоальбому.
3. Редагувати опис світлини у своєму фотоальбомі.
4. Перегляд світлин зі свого альбому як списком, так і окремо будь яку світлину.
5. Додавати до 5 тегів під світлину.
6. Виконувати базові операції трансформації над світлинами, які дозволяє сервіс Cloudinary.
7. Користувачі можуть коментувати світлину один одного.
8. Користувач може редагувати свій коментар, але не видаляти.
9. Адміністратори та модератори можуть видаляти коментарі.
10. Адміністратори можуть виконувати всі операціі зі світлинами користувачів.

Додатково в застосунку:
1. Для всіх оерацій з контактами обмежена кількість запитів (не більше 10 за 1 хвилину).
2. Додано та увімкнено CORS для застосунку.
3. Реалізована можливість оновлення аватара користувача з використанням сервісу Cloudinary.
4. Реалізовано механізм кешування поточного користувача під час авторизації за допомогою бази даних Redis.
5. Усі змінні середовища зберігаються у файлі ".env". Файл доданий у ".gitignore".


Для встановлення застосунку потрібно:
1. Python = 3.10 и вище.
2. Встановити Poetry (дивись інструкцию по встановленню Poetry).
3. Запустити Poetry, виконавши в кореневій папці проекту:
    - poetry shell
4. Виконати встановлення необхідних для проекту модулів Python, виконавши в кореневій папці проекту:
    - poetry install
5. Після закінчення встановлення пакетів створити файл налаштувань ".env" за зразком фалу ".example.env", та налаштувати параметри доступу:
    - до бази даних Postgres (Redis не використовується)
    - до поштового сервера та поштової сриньки, з якої будуть відправлятися запити на верифікацию emal користовача, при його ствоенні (SignUp)
    - до сервісу Cloudinary, де будуть фізично зберігатися світлини.
6. Для створення необхідних таблиць у базі даних віконати міграцию, виконавши:
    - alembic upgrade head
5. Після успішної міграції запустити локальний сервер Uvicorn:
    uvicorn main:app --host 0.0.0.0 --port 8080 --reload
6. У ВЕБ-браузері зайти на стартову сторінку застосунку за адресою:
    http://localhost:8080
7. Зі стартової сторінки можна перейти до "Swagger Docs" та на сторінку перегляду результатів покриття застосунку тестами "Coverage Tests".

При розгортанні застосунку на зовнішніх/хмарних сереверах встановлювати згідно інструкцій тих серверів.