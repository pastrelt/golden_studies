''' Первый спринт, Второй спринт.
Классы
Методы открытие/создание БД PostgreSQL, REST API.
'''
import psycopg2
from psycopg2.extras import Json


class Create_Databases_Tables:
    def __init__(self, host_db, port_db, login_db, password_db):
        self.host_db = host_db
        self.port_db = port_db
        self.login_db = login_db
        self.password_db = password_db

    def create_db(self):
        conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="6J46rc2(eg",
            host=self.host_db,
            port=self.port_db
        )
        conn.autocommit = True

        cursor = conn.cursor()

        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'mountains';")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("CREATE DATABASE mountains;")
            conn.commit()

        conn.close()

    def create_table(self):
        conn = psycopg2.connect(
            database="mountains",
            user="postgres",
            password="6J46rc2(eg",
            host=self.host_db,
            port=self.port_db
        )
        cursor = conn.cursor()

        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'my_mountain');")
        table_exists = cursor.fetchone()[0]

        if not table_exists:
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
            conn.commit()

        conn.close()

class Database:
    # Класс для работы с базой данных

    def __init__(self, host_db, port_db):
        self.conn = psycopg2.connect(
            database="mountains",
            user="postgres",
            password="6J46rc2(eg",
            host=host_db,
            port=port_db
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

    def get_record_by_id(self, id):
        self.cur.execute("SELECT * FROM my_mountain WHERE id = %s", (id,))
        record = self.cur.fetchone()
        if record:
            return {
                "id": record[0],
                "beauty_title": record[1],
                "title": record[2],
                "other_titles": record[3],
                "connect": record[4],
                "add_time": record[5],
                "email": record[6],
                "phone": record[7],
                "fam": record[8],
                "name": record[9],
                "otc": record[10],
                "latitude": record[11],
                "longitude": record[12],
                "height": record[13],
                "winter": record[14],
                "summer": record[15],
                "autumn": record[16],
                "spring": record[17],
                "images": record[18],
                "status": record[19]
            }
        else:
            return None

    def get_records_by_user_email(self, email):
        self.cur.execute("SELECT * FROM my_mountain WHERE email = %s", (email,))
        records = []
        for record in self.cur.fetchall():
            records.append({
                "id": record[0],
                "beauty_title": record[1],
                "title": record[2],
                "other_titles": record[3],
                "connect": record[4],
                "add_time": record[5],
                "email": record[6],
                "phone": record[7],
                "fam": record[8],
                "name": record[9],
                "otc": record[10],
                "latitude": record[11],
                "longitude": record[12],
                "height": record[13],
                "winter": record[14],
                "summer": record[15],
                "autumn": record[16],
                "spring": record[17],
                "images": record[18],
                "status": record[19]
            })
        return records

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