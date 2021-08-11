# HEIs Employers
##### Все приложения:
- Python3.9 (Django, Gunicorn)
- PostgreSQL
- NGINX

*Внутри одного Django проекта 2 сайта:*
- Один на localhost:8001 (work4practice.com)
- Другой на localhost:8003 (admin.work4practice.com)

##### Подготовка проекта
```
# Установка виртуального окружения
python3.9 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# Добавление всех миграций и начальных данных (список языков, стран)
cd src
python manage.py migrate
python manage.py init_fill_db

# Сбор статических файлов
# Для work4practice.com
python manage.py collectstatic --settings=config.settings.main.local
# Для admin.work4practice.com
python manage.py collectstatic --settings=config.settings.admin.local
```

##### Workers для Crontab

```
# Проверяем каждый час, нужно ли менять статус для Стажировки
0 * * * * cd /home/admin/Project/heisemployers/src && /home/admin/Project/heisemployers/venv/bin/python manage.py check_internships > /tmp/cronlog.txt 2>&1
```

##### Запуск gunicorn (Добавить в supervisor)
```
# Для work4practice.com
bin/start_gunicorn_main.sh
# Для admin.work4practice.com
bin/start_gunicorn_admin.sh
```