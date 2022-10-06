# Проект "Продуктовый помощник". FoodGram

IP-адрес проекта: 158.160.13.103

## Описание

На этом сервисе пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

## Шаблон заполнения .env файла

DB_ENGINE=*<тип БД>*

DB_NAME=*<имя базы данных>*

POSTGRES_USER=*<логин для подключения к базе данных>*

POSTGRES_PASSWORD=*<пароль для подключения к БД>*

DB_HOST=*<название сервиса (контейнера)>*

DB_PORT=*<порт для подключения к БД>*

SECRET_KEY=*<SECRET_KEY Django>*

## Установка

Клонировать репозиторий и перейти в него в командной строке:
```
git clone https://github.com/Julka3561/foodgram-project-react.git
```

```
cd infra
```

Запустить проект в контейнерах Docker

```
docker-compose up -d
```
Провести миграции: 

```
docker-compose exec backend python manage.py migrate
```

Создать суперпользователя:

```
docker-compose exec bakend python manage.py createsuperuser
```
Собрать статику:

```
docker-compose exec backend python manage.py collectstatic --no-input
```

## Заполнение базы данными

```
docker-compose exec backend python manage.py loaddata dump.json 
```
## Об авторе
Юля & Яндекс.Практикум

Copyright (c) 2022, Julia Vasileva

All rights reserved.

