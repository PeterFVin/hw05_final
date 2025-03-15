# yatube_project

Социальная сеть блогеров. Пользователи могут писать посты, оставлять комментарии кчужим постам,а также подписываться на любимых авторов. Есть система авторизации.

### **Стек**
![python version](https://img.shields.io/badge/Python-3.10.5-blue)
![django version](https://img.shields.io/badge/Django-2.2.16-blue)
![pillow version](https://img.shields.io/badge/Pillow-8.3.1-blue)
![pytest version](https://img.shields.io/badge/pytest-5.3.5-blue)
![requests version](https://img.shields.io/badge/requests-2.22.0-blue)

### Автор проекта:

[Петр Виноградов](https://github.com/PeterFVin)

### Как запустить проект

Клонируйте репозиторий:
```
git clone git@github.com:PeterFVin/hw05_final.git
```

Установите и активируйте виртуальное окружение:
- Linux/MacOS
```
python3 -m venv venv
source venv/bin/activate
```
- Windows
```
python -m venv venv
source venv/Scripts/activate
```
Установите зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```
Примените миграции:
```
python manage.py migrate
```
Запустить проект:
```
В папке yatube (с файлом manage.py) выполните команду:
python manage.py runserver
```
