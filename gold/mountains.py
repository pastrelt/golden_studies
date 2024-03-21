''' Первый спринт
Создание базы данных.
Создание класса по работе с данными, с помощью которого добавляю новые значения в таблицу.
Написание REST API, который вызывает метод из класса по работе с данными.
'''
import os
import psycopg2
from psycopg2.extras import Json
from flask import Flask, request, jsonify
import methods


host = os.getenv('FSTR_DB_HOST')
port = os.getenv('FSTR_DB_PORT')
login = os.getenv('FSTR_DB_LOGIN')
password = os.getenv('FSTR_DB_PASS')

# Establishing the connection
# Устанавливаем соединение с PostgreSQL через базу данных по умолчанию postgres,
# используя указанные параметры, через модуль psycopg2.
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="6J46rc2(eg",
    host=host,
    port=port
)
conn.autocommit = True

# Creating a cursor object using the cursor() method
# Создание объекта курсора с помощью метода cursor()
cursor = conn.cursor()

# Проверяем существование базы данных
cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'mountains';")
exists = cursor.fetchone()

if not exists:
    # Создание базы данных в PostgreSQL
    cursor.execute("CREATE DATABASE mountains;")

    # Фиксируем транзакцию, чтобы изменения были сохранены.
    conn.commit()

# Closing the connection
conn.close()

conn = psycopg2.connect(
    database="mountains",
    user="postgres",
    password="6J46rc2(eg",
    host=host,
    port=port
)
cursor = conn.cursor()

# Проверяем существование таблицы
cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'my_mountain');")
table_exists = cursor.fetchone()[0]
if not table_exists:
    # Выполняется SQL-запрос для создания таблицы mountains.
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS my_mountain (
            id SERIAL PRIMARY KEY,
    
            beauty_title VARCHAR(100),
            title VARCHAR(100) NOT NULL,
            other_titles VARCHAR(100),
            connect TEXT,
            add_time TIMESTAMP,
    
            email VARCHAR(100),
            phone VARCHAR(20),
            fam VARCHAR(100),
            name VARCHAR(100),
            otc VARCHAR(100),
    
            latitude VARCHAR(20),
            longitude VARCHAR(20),
            height VARCHAR(20),
    
            winter VARCHAR(10),
            summer VARCHAR(10),
            autumn VARCHAR(10),
            spring VARCHAR(10),
    
            images JSON,
            
            status VARCHAR(10)
        );
    ''')
    # Фиксируем транзакцию, чтобы изменения были сохранены в базе данных.
    conn.commit()

# Closing the connection
conn.close()

# Инициализация Flask приложения
app = Flask(__name__)

# Метод POST /submitData для REST API
@app.route('/submitData', methods=['POST'])
def submitData():
    data = request.get_json()
    if not data:
        return jsonify({"status": 400, "message": "Bad Request", "id": None})

    try:
        db = methods.Database(host, port)
        inserted_id = db.insert_mountains(data)
        return jsonify({"status": 200, "message": "Отправлено успешно", "id": inserted_id})

    except Exception as e:
        return jsonify({"status": 500, "message": str(e), "id": None})

# Метод GET /submitData/<id> для REST API
@app.route('/submitData/', methods=['GET'])
def submitData_id():
    data_id = request.args.get('id')
    if not data_id:
        return jsonify({"status": 400, "message": "Bad Request", "id": {}})

    try:
        db = methods.Database(host, port)
        inserted_id = db.get_record_by_id(data_id)
        return jsonify({"status": 200, "message": "Запрос успешно завершен.", "id": inserted_id})

    except Exception as e:
        return jsonify({"status": 500, "message": str(e), "id": None})


# Метод GET /submitData/?user_email=<email> для REST API
@app.route('/submitData/<email>', methods=['GET'])
def submitData_email(email):
    print(email)  # для проверки
    if not email:
        return jsonify({"status": 400, "message": "Bad Request", "id": {}})

    try:
        db = methods.Database(host, port)
        inserted_id = db.get_records_by_user_email(email)
        return jsonify({"status": 200, "message": "Запрос успешно завершен.", "id": inserted_id})

    except Exception as e:
        return jsonify({"status": 500, "message": str(e), "id": None})

if __name__ == '__main__':
    app.run(debug=True)



# # Оставил данный код для себя, он подтверждает работоспособность класса и является POST запросом.
# # Создаем экземпляр класса Database
# db = Database()
#
# # Пример - проверка для метода insert_pereval
# my_data = {
#     "beauty_title": "Some Title",
#     "title": "Title",
#     "other_titles": "Other Titles",
#     "connect": "Some Connection",
#     "add_time": "2022-01-01",
#     "user": {
#         "email": "user@example.com",
#         "fam": "User Fam",
#         "name": "User Name",
#         "otc": "User Otc",
#         "phone": "1234567890"
#     },
#     "coords": {
#         "latitude": "123.456",
#         "longitude": "456.789",
#         "height": "1000"
#     },
#     "level": {
#         "winter": "High",
#         "summer": "Low",
#         "autumn": "Medium",
#         "spring": "Low"
#     },
#     "images": ["image1.jpg", "image2.jpg"]
# }
#
# # Вызываем метод insert_pereval
# inserted_id = db.insert_mountains(my_data)
# print("Inserted ID:", inserted_id)
#
# # Вызываем метод update_status для проверки работоспособности
# update_result = db.update_status(inserted_id, 'pending')
# print(update_result)
