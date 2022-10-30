### yamdb_final
http://84.201.153.0/api/v1/

http://84.201.153.0/redoc/

![работай штука](https://github.com/Zizeka/yamdb_final/actions/workflows/yamdb_workflow.yaml/badge.svg)

Проект YaMDb собирает отзывы (Review) пользователей на произведения (Titles). Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий (Category) может быть расширен администратором (например, можно добавить категорию «Изобразительное искусство» или «Ювелирка»).
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
В каждой категории есть произведения: книги, фильмы или музыка. Например, в категории «Книги» могут быть произведения «Винни-Пух и все-все-все» и «Марсианские хроники», а в категории «Музыка» — песня «Давеча» группы «Насекомые» и вторая сюита Баха.
Произведению может быть присвоен жанр (Genre) из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы (Review) и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

### Авторы проекта: 

**[Чернов Алексей](https://github.com/AlexBlackNn)**. Управление пользователями (Auth и Users): система регистрации и аутентификации, права доступа, работа с токеном, система подтверждения через e-mail.

**[Анна Руотси](https://github.com/Zizeka)**.  Категории (Categories), жанры (Genres) и произведения (Titles): модели, представления и эндпойнты для них.

**[Анна Голушко](https://github.com/AnnaGolushko)**. Отзывы (Review) и комментарии (Comments): модели, представления, настраивает эндпойнты, определяет права доступа для запросов. Рейтинги произведений.

### Cписок используемых технологий:
Django 

Django-rest-framework

Docker

Gunicorn

nginx

Яндекс.Облако(Ubuntu 18.04)

PostgreSQL

GIT

### Как запустить проект:

Клонировать репозиторий и перейти в папку yatube_api

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

```
source env/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

### Последовательность загрузки данных важна!

Загрузить Пользователей в БД:

```
python manage.py load_users_data
```

Загрузить Жанры в БД:

```
python manage.py load_genre_data
```

Загрузить Категории в БД:
```
python manage.py load_category_data
```

Загрузить Произведения в БД:
```
python manage.py load_titles_data
```
Загрузить Ревью в БД:
```
python manage.py load_review_data
```
Загрузка Комментариев в БД
```
python manage.py load_comment_data
```

Загрузка связи Жанр Произведение 
```
python manage.py load_genre_title_data
```


Cоздать нового пользователя (в терминале появиться confirmation_code, например 619-f5cfa27f1dd04b07ba36)
```
POST http://127.0.0.1:8000/api/v1/auth/signup/
Content-Type: application/json

{
    "email": "Test_user@yamdb.fake",
    "username": "Test_user"
}
```

Передать пользователю токен (в терминале появиться {"token": "eyJ0eXAi.....})
```
POST http://127.0.0.1:8000/api/v1/auth/token/
Content-Type: application/json

{
    "confirmation_code": "619-f14dfe2a024b55d023a7",
    "username": "Test_user"
}
```

Запросить свою информацию
```
GET http://127.0.0.1:8000/api/v1/users/me/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0MTg2NjAzLCJqdGkiOiI0MGE0ZjRlNTg2ZTI0MTJiYjYyN2JhZGJhODViZTk4YyIsInVzZXJfaWQiOjN9.AQAhyAWsR2_koog8ofuWy9QEWSSYObvI6C-VSbjIprE
```

Редактировать информацию о себе
```
PATCH http://127.0.0.1:8000/api/v1/users/me/
Content-Type: application/json
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0MTg2NjAzLCJqdGkiOiI0MGE0ZjRlNTg2ZTI0MTJiYjYyN2JhZGJhODViZTk4YyIsInVzZXJfaWQiOjN9.AQAhyAWsR2_koog8ofuWy9QEWSSYObvI6C-VSbjIprE

{
  "first_name": "Test",
  "last_name": "User",
  "bio": "Some biography1"
}
```
Получение списка всех пользователей.
В админке, нужно дать права админа (role) прежде!
```
GET http://127.0.0.1:8000/api/v1/users/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0MTg2NjAzLCJqdGkiOiI0MGE0ZjRlNTg2ZTI0MTJiYjYyN2JhZGJhODViZTk4YyIsInVzZXJfaWQiOjN9.AQAhyAWsR2_koog8ofuWy9QEWSSYObvI6C-VSbjIprE
```

Получить пользователя по username.
```
GET http://127.0.0.1:8000/api/v1/users/Test_user/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0MTg2NjAzLCJqdGkiOiI0MGE0ZjRlNTg2ZTI0MTJiYjYyN2JhZGJhODViZTk4YyIsInVzZXJfaWQiOjN9.AQAhyAWsR2_koog8ofuWy9QEWSSYObvI6C-VSbjIprE
```

Изменение данных пользователя по username
```
PATCH http://127.0.0.1:8000/api/v1/users/Test_user/
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjU0MTg2NjAzLCJqdGkiOiI0MGE0ZjRlNTg2ZTI0MTJiYjYyN2JhZGJhODViZTk4YyIsInVzZXJfaWQiOjN9.AQAhyAWsR2_koog8ofuWy9QEWSSYObvI6C-VSbjIprE

{
    "first_name": "string1",
    "last_name": "string2"
}

```
### Шаблон наполнения .env

```
# указываем, с какой БД работаем
DB_ENGINE=django.db.backends.postgresql
# имя базы данных
DB_NAME=
# логин для подключения к базе данных
POSTGRES_USER=
# пароль для подключения к БД (установите свой)
POSTGRES_PASSWORD=
# название сервиса (контейнера)
DB_HOST=
# порт для подключения к БД
DB_PORT=
```

### Автоматизация развертывания серверного ПО
Для автоматизации развертывания ПО на боевых серверах используется среда виртуализации Docker, а также Docker-compose - инструмент для запуска многоконтейнерных приложений. Docker позволяет «упаковать» приложение со всем его окружением и зависимостями в контейнер, который может быть перенесён на любую Linux -систему, а также предоставляет среду по управлению контейнерами. Таким образом, для разворачивания серверного ПО достаточно чтобы на сервере с ОС семейства Linux были установлены среда Docker и инструмент Docker-compose.

Ниже представлен Dockerfile - файл с инструкцией по разворачиванию Docker-контейнера веб-приложения:
```
FROM python:3.7-slim

WORKDIR /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY . .

WORKDIR /app

CMD ["gunicorn", "api_yamdb.wsgi:application", "--bind", "0:8000" ]
```
В файле «docker-compose.yml» описываются запускаемые контейнеры: веб-приложения, СУБД PostgreSQL и сервера Nginx.
```
version: '3.8'

services:
  db:
    image: postgres:13.0-alpine

    volumes:
      - /var/lib/postgresql/data/
    env_file:
      - ./.env
  web:
    build: ../api_yamdb
    restart: always

    volumes:
    - static_value:/app/static/
    - media_value:/app/media/
    depends_on:
      - db
    env_file:
      - ./.env

  nginx:
    image: nginx:1.21.3-alpine

    ports:
      - "80:80"

    volumes:
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf

      - static_value:/var/html/static/

      - media_value:/var/html/media/

    depends_on:
      - web
volumes:
  static_value:
  media_value:
  ```
### Описание команд для запуска приложения в контейнерах
Для запуска проекта в контейнерах используем docker-compose : ```docker-compose up -d --build```, находясь в директории (infra_sp2) с ```docker-compose.yaml```

После сборки контейнеров выполяем:
```
# Выполняем миграции
docker-compose exec web python manage.py migrate
# Создаем суперппользователя
docker-compose exec web python manage.py createsuperuser
# Собираем статику со всего проекта
docker-compose exec web python manage.py collectstatic --no-input
# Для дампа данных из БД
docker-compose exec web python manage.py dumpdata > dump.json
```
### Для выгрузки данных из дампа (резервной копии) в БД
```
docker-compose exec web bash
# Сброс БД, суперюзеры так же удаляются
>>> python manage.py flush

>>> python3 manage.py shell  
        # выполнить в открывшемся терминале:
>>>>>> from django.contrib.contenttypes.models import ContentType
>>>>>> ContentType.objects.all().delete()
>>>>>> quit()

>>> python manage.py loaddata dump.json
```
### Описание команды для заполнения БД данными из csv:
python manage.py import_csv_to_db в контейнере web (docker-compose exec web bash)

Это - менеджмент команда.

Выгружаются данные из файлов директории api_yamdb/static

НО, прежде выполнить миграции! В случае изменения названий моделей/csv файлов и которых брать данне - изменить настройки в api_yamdb/reviews/management/commands/_settings_for_import.py, а именно:
```
NEED_TO_PARSE = {
'users.csv': User,
'category.csv': Category,
'genre.csv': Genre,
'titles.csv': Title,
'genre_title.csv': Genre_title,
'review.csv': Review,
'comments.csv': Comment,
}
```
=======
