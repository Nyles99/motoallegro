# motoallegro
Парсинг сайта запчастей для работодателя(Польша)

# bamper-reppart
Парсинг сайта запчастей для работодателя

Скачать приложение через SSH Зайти в папку и установить виртуальное окружение:

1. python -m venv venv
Активировать его:
2. source venv/scripts/activate

Обновить виртуальное окружение:
3. python -m pip install --upgrade pip

Установить зависимости из файла requirements.txt:
4. pip install -r requirements.txt

Выполнить миграции:
5. python manage.py migrate

Запустить проект:
6. python manage.py runserver