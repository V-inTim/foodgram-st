# Foodgram
«Фудграм» — сайт-проект курса Яндекс Практикум.

## Стек технологий
Django, DRF, Nginx, Docker, PostgreSQL

## Запуск проекта
### через django
```
// 1. клонирование репозитория
git clone https://github.com/V-inTim/foodgram-st
cd foodgram-st/backend

// 2. создание и активация виртуального окружения
python3 -m venv venv  
source ./env/bin/activate

// 3. установка зависимостей
pip install -r requirements.txt
```

4. Создайте .env файл в корне проекта
*для django*:
- SECRET_KEY (сгенерировать)
- DEBUG (True или False)
- ALLOWED_HOSTS (разрешенные хосты)
- DATABASE_URL (url для подключения в бд)
если через django, то к базе как к localhost

```
// 5. выполните миграций
python3 manage.py migrate

// 6. создание суперпользователя
python3 manage.py createsuperuser

// 7. загрузка статики
python3 manage.py collectstatic --no-input

// 8. запустите сервера
python3 manage.py runserver 8000
```

## через Docker
```
// 1. клонирование репозитория
git clone https://github.com/V-inTim/foodgram-st
```

2. Создайте .env файл в корне проекта
*для django*:
- SECRET_KEY (сгенерировать)
- DEBUG (True или False)
- ALLOWED_HOSTS (разрешенные хосты)
- DATABASE_URL (url для подключения в бд)
если через django, то к базе как к db
*для postgres*
- POSTGRES_USER
- POSTGRES_PASSWORD
```
// 3. запуск проекта через docker-compose 
docker-compose up -d
```

## Эндпоинты
Приложение: http://localhost/
Документация: http://localhost/api/docs/
