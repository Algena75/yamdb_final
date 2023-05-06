### Сервис позволяющий пользователям оценивать и писать свои рецензии на любые категории творчества
api_yamdb

![yamdb_workflow.yml](https://github.com/Algena75/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Команда разработчиков:
Самсонов Дмитрий
Никита Ковалев
Алексей Наумов

## Проект развернут на сервере:
http://158.160.98.187/

## Используемые технолологии:

Django v.2.2
djangorestframework v.3.12.4
PyJWT v.2.1.0
PostgreSQL 13.0
Docker 23.0.4

## Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:Algena75/yamdb_final.git
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Перейдите в директорию /api_yamdb/ и установите зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Установите Docker и Docker Compose:

```
sudo apt install docker-ce docker-compose -y
```

Создайте образ:

```
docker build -t infra .
```

Перейдите в директорию /infra/. В файле .env необходимо указать переменные окружения для доступа к БД.
Соберите контейнеры:

```
docker-compose up -d (для пересборки добавьте параметр --build)
```

После сборки и запуска контейнеров поочередно выполните миграции, создайте суперюзера и соберите статику проекта:

```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py collectstatic --no-input
```

## Аутентификация токена:

Самостоятельная регистрация и подтверждение адреса электронной почты:

```
http://127.0.0.1/api/v1/auth/signup/
```

Получить/обновить токен:

```
http://127.0.0.1/api/v1/auth/token/
```

## Примеры запросов к Api:

Получение ревью по id тайтла.

```
http://127.0.0.1/api/v1/titles/1/reviews/
```
Получение списка комментариев на ревью
```
http://127.0.0.1/api/v1/titles/1/reviews/1/comments/
```
