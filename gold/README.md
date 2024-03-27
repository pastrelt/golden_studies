Всем привет!

Название проекта - "Горы".

Смысл в том, что каждый, находясь в милом для сердца
месте, хочет оставить себе воспоминание об этом
месте, сохранить важные детали данного события,
будь это время события или фотография места. Горы -
одно из таких мест.

Проект, как раз об этом, он позволяет фиксировать 
информацию, смотреть ее, сортировать, дополнять и 
делиться ею с единомышленниками.

Работа проекта организована на основе:
Стек первый уровень: Python, PostgreSQL; 
Стек второй уровень: Flask, Swagger;
Стек тестирования: Postmen.

Состоит проект из трех файлов:
1. mountains.py - основная программа, 
он же файл запуска;
2. class_mount.py - файл рабочих методов, 
объединенных в классы;
3. README.md - описание проекта.

Запуск проекта:
1. установите приложения стека первого уровня
2. создайте необходимую папку для работы
3. перейдите в терминале в данную папку
4. клонируйте из репозитория содержимое папки gold
5. выполните команды:
pip install Flask;   
pip install flask psycopg2;
pip install flask-swagger.
6. выполните старт файла mountains.py

Работа проекта:
После запуска Вы увидите приглашение сервера,
после чего,  можете выполнять свои запросы.

Для выполнения запросов можете воспользоваться 
примерами, приложенными ниже, либо перейти по ссылке:
http://127.0.0.1:5000/spec, чтобы воспользоваться
Swagger документацией.

Пример 1:
curl --location 'http://127.0.0.1:5000/submitData' \
--header 'Content-Type: application/json' \
--data-raw '{
    "beauty_title": "Some Title",
    "title": "Title",
    "other_titles": "Other Titles",
    "connect": "Some Connection",
    "add_time": "2022-01-01",
    "user": {
        "email": "user@example.com",
        "fam": "User Fam",
        "name": "User Name",
        "otc": "User Otc",
        "phone": "1234567890"
    },
    "coords": {
        "latitude": "123.456",
        "longitude": "456.789",
        "height": "1000"
    },
    "level": {
        "winter": "High",
        "summer": "Low",
        "autumn": "Medium",
        "spring": "Low"
    },
    "images": ["image1.jpg", "image2.jpg"]
}'

Пример 2:
curl --location 'http://127.0.0.1:5000/submitData/user@example.com' \
--header 'Content-Type: application/json'

Пример 3:
curl --location 'http://127.0.0.1:5000/submitData/?id=8' \
--header 'Content-Type: application/json'

Пример 4:
curl --location --request PATCH 'http://127.0.0.1:5000/submitData/12' \
--header 'Content-Type: application/json' \
--data '{
    "beauty_title": "Some Title",
    "title": "Ну и ну",
    "other_titles": "Other Titles",
    "connect": "Some Connection",
    "add_time": "2022-01-01",
    "coords": {
        "latitude": "888.888",
        "longitude": "444.444",
        "height": "5000"
    },
    "level": {
        "winter": "High",
        "summer": "Low",
        "autumn": "Medium",
        "spring": "Low"
    },
    "images": ["image1.jpg", "image2.jpg"]
}'