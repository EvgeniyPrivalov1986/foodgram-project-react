### praktikum_diplom

## Стек технологий

 - Python
 - Django
 - Django REST Framework
 - PostgreSQL
 - Nginx
 - Gunicorn
 - Docker
 - GitHub%20Actions
 - Yandex.Cloud

## Описание проекта
# Foodgram - «Продуктовый помощник»

Это онлайн-сервис и API для него. На этом сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект использует базу данных PostgreSQL. Проект запускается в трёх контейнерах (nginx, PostgreSQL и Django) (контейнер frontend используется лишь для подготовки файлов) через docker-compose на сервере.

## Запуск проекта с помощью Docker

1. Склонируйте репозиторий на локальную машину.

    ```
    git clone git@github.com:EvgeniyPrivalov1986/foodgram-project-react.git
    ```

2. Создайте .env файл в директории backend/foodgram/, в котором должны содержаться следующие переменные для подключения к базе PostgreSQL:

    ```
    DB_ENGINE=django.db.backends.postgresql
    DB_NAME=postgres
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432    
    ```

3. Перейдите в директорию infra/ и выполните команду для создания и запуска контейнеров.
    ```
    sudo docker compose up -d --build
    ```
4. В контейнере backend выполните миграции, создайте суперпользователя и соберите статику.

    ```
    sudo docker compose exec backend python manage.py migrate
    sudo docker compose exec backend python manage.py createsuperuser
    sudo docker compose exec backend python manage.py collectstatic --no-input 
    ```

5. Загрузите в бд заранее подготовленные ингредиенты.

    ```
    sudo docker compose exec backend python manage.py load_ingredients
    ```

6. Проект доступен по следующим адресам:
    -  http://localhost/ - главная страница сайта;
    -  http://localhost/admin/ - админ панель;
    -  http://localhost/api/ - API проекта;
    -  http://localhost/api/docs/redoc.html - документация к API;

---
## Автор
**[Евгений Привалов](https://github.com/EvgeniyPrivalov1986)** - создание api, деплой на сервер.
