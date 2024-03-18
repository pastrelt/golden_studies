''' Первый спринт
Создание базы данных.
Создание класса по работе с данными, с помощью которого добавляяю новые значения в таблицу.
Написание REST API в отдельном файле start.py, который вызывает метод из класса по работе с данными.
'''
import os
import psycopg2
from psycopg2.extras import Json


host = os.getenv('FSTR_DB_HOST')
port = os.getenv('FSTR_DB_PORT')
login = os.getenv('FSTR_DB_LOGIN')
password = os.getenv('FSTR_DB_PASS')

# Establishing the connection
# Устанавливаем соединение с базой данных PostgreSQL,
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

# # Closing the connection
# conn.close()

# Класс для работы с базой данных
class Database:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="mountains",
            user="postgres",
            password="6J46rc2(eg",
            host=host,
            port=port
        )
        self.cur = self.conn.cursor()

    def insert_mountains(self, my_data):
        # Метод insert_pereval принимает словарь pereval_data с информацией о перевале
        # и вставляет его в базу данных.
        # Статус модерации устанавливается в "new" при добавлении новой записи.
        query = '''
            INSERT INTO my_mountain (beauty_title, title, other_titles, connect, add_time,
                                     email, fam, name, otc, phone, latitude, longitude, height,
                                     winter, summer, autumn, spring, images, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        '''
        self.cur.execute(query, (my_data['beauty_title'], my_data['title'], my_data['other_titles'],
                                 my_data['connect'], my_data['add_time'], my_data['user']['email'],
                                 my_data['user']['fam'], my_data['user']['name'], my_data['user']['otc'],
                                 my_data['user']['phone'], my_data['coords']['latitude'],
                                 my_data['coords']['longitude'], my_data['coords']['height'],
                                 my_data['level']['winter'], my_data['level']['summer'],
                                 my_data['level']['autumn'], my_data['level']['spring'],
                                 Json(my_data['images']), 'new' # начальный статус модерации
                                 ))
        inserted_id = self.cur.fetchone()[0]
        self.conn.commit()
        return inserted_id

    def update_status(self, pereval_id, new_status):
        # Mетод update_status принимает идентификатор перевала pereval_id и
        # новый статус new_status. Перед выполнением обновления проверяется,
        # что новый статус является одним из допустимых значений.
        # Затем выполняется SQL-запрос для обновления статуса записи в базе данных.
        valid_statuses = ['new', 'pending', 'accepted', 'rejected']
        if new_status not in valid_statuses:
            return {"status": 400, "message": "Недопустимое значение для статуса", "id": None}

        sql = """
        UPDATE my_mountain
        SET status = %s
        WHERE id = %s;
        """
        values = (new_status, pereval_id)

        try:
            self.cur.execute(sql, values)
            self.conn.commit()
            return {"status": 200, "message": "Статус успешно обновлен", "id": pereval_id}
        except psycopg2.Error as e:
            return {"status": 500, "message": str(e), "id": None}

# Оставил данный код, он подтверждает работоспособность класса.
# Создаем экземпляр класса Database
db = Database()

# Пример - проверка для метода insert_pereval
my_data = {
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
}

# Вызываем метод insert_pereval
inserted_id = db.insert_mountains(my_data)
print("Inserted ID:", inserted_id)

# Вызываем метод update_status для проверки работоспособности
update_result = db.update_status(inserted_id, 'pending')
print(update_result)



# # Инициализация Flask приложения
# Mountains = Flask(__name__)
#
# # Метод POST submitData для REST API
# @Mountains.route('/submitData', methods=['POST'])
# def submitData():
#     data = request.get_json()
#     if not data:
#         return jsonify({"status": 400, "message": "Bad Request", "id": None})
#
#     try:
#         inserted_id = db.insert_mountains(data)
#         return jsonify({"status": 200, "message": "Отправлено успешно", "id": inserted_id})
#
#     except Exception as e:
#         return jsonify({"status": 500, "message": str(e), "id": None})
#
# if __name__ == '__main__':
#     Mountains.run(debug=True)
