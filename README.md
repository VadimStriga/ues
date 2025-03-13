# ues

"Программа для учета потребления электрической энергии потребителями"


Программа предназначена для внесения показаний приборов учета, получения файлов расчета потребления и актов приёма-передачи.

# Технологии
[![Python 3.11](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![Django 4.2.11](https://img.shields.io/badge/-Django-464646?style=flat&logo=Django&logoColor=ffffff&color=043A6B)](https://www.djangoproject.com/)

# Запуск проекта в dev-режиме
- Клонируйте репозиторий и перейжите в него в командной строке
- Установите и активируйте виртуальное окружение
- В корневой папке создайте файл .env со следующим наполнением:
```
'SECRET_KEY' = 'very-secret-key'
'ENGINE' = 'django.db.backends.sqlite3'
'NAME' = 'db.sqlite3'
```
- Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
``` 
- Выполните миграции:
```
python3 manage.py migrate
```
- В папке с файлом manage.py выполните команду:
```
python3 manage.py runserver
```