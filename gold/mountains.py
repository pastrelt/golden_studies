''' Первый спринт, Второй спринт.
Создание базы данных (вынесено в класс -  Create_Databases_Tables файла classes).
Создание класса по работе с базой данных (файл classes).
Написание REST API, который вызывает методы из класса - Databases файла classes.
'''
import os
from flask import Flask, request, jsonify
import methods

# Проверка наличия/создание рабочей БД.
host_db = os.getenv('FSTR_DB_HOST')
port_db = os.getenv('FSTR_DB_PORT')
login_db = os.getenv('FSTR_DB_LOGIN')
password_db = os.getenv('FSTR_DB_PASS')

db = methods.Create_Databases_Tables(host_db, port_db, login_db, password_db)
db.create_db()
db.create_table()


# Инициализация Flask приложения.
app = Flask(__name__)
db = methods.Database(host_db, port_db)

@app.route('/submitData/<id>', methods=['PATCH'])
def submitData_id_patch(id):
    data = request.get_json()
    if not data:
        return jsonify({"status": 400, "message": "Bad Request", "id": None})

    try:
        inserted_id = db.edit_record_by_id(id, data)
        return jsonify({"status": 200, "message": "Отправлено успешно", "id": inserted_id})

    except Exception as e:
        return jsonify({"status": 500, "message": str(e), "id": None})

# Метод POST /submitData для REST API.
# Запись данных о горе'.
@app.route('/submitData', methods=['POST'])
def submitData():
    data = request.get_json()

    def method(db, data):
        return db.insert_mountains(data)

    result = methods.Check_And_Reply(data, method)
    return result.check_and_reply(db)

# Метод GET /submitData/<id> для REST API.
# Просматр конкретной записи по ее id.
@app.route('/submitData/', methods=['GET'])
def submitData_id():
    data_id = request.args.get('id')

    def method(db, data_id):
        return db.get_record_by_id(data_id)

    result = methods.Check_And_Reply(data_id, method)
    return result.check_and_reply(db)

# Метод GET /submitData/?user_email=<email> для REST API.
# Просматр списока записей всех объектов, которые внесены пользователем с почтой <email>.
@app.route('/submitData/<email>', methods=['GET'])
def submitData_email(email):

    def method(db, email):
        return db.get_records_by_user_email(email)

    result = methods.Check_And_Reply(email, method)
    return result.check_and_reply(db)

# Метод PATCH /submitData/<id> для REST API.
# Редактирование записи по id.
# @app.route('/submitData/<id>', methods=['PATCH'])
# def submitData_id_patch(id):
#     data = request.get_json()
#
#     def method(db, data):
#         return db.edit_record_by_id(id, data)
#
#     result = methods.Check_And_Reply(data, method)
#     return result.check_and_reply(db)




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




# {
#     "beauty_title": "Some Title",
#     "title": "Ну и ну",
#     "other_titles": "Other Titles",
#     "connect": "Some Connection",
#     "add_time": "2022-01-01",
#     "user": {
#         "email": "UUUUUU",
#         "fam": "XXXXXXX",
#         "name": "XXXXX",
#         "otc": "XXXXXX",
#         "phone": "VVVVVVVV"
#     },
#     "coords": {
#         "latitude": "888.888",
#         "longitude": "444.444",
#         "height": "5000"
#     },
#     "level": {
#         "winter": "High",
#         "summer": "Low",
#         "autumn": "Medium",
#         "spring": "Low"
#     },
#     "images": ["image1.jpg", "image2.jpg"]
# }



# UPDATE my_mountain SET beauty_title = %s, title = %s, other_titles = %s, connect = %s,
#                        add_time = %s, coords = %s, level = %s, images = %s
#                    WHERE id = 6
#                    ['Some Title', 'Ну и ну', 'Other Titles', 'Some Connection', '2022-01-01',
#                    {'latitude': '888.888', 'longitude': '444.444', 'height': '5000'},
#                    {'winter': 'High', 'summer': 'Low', 'autumn': 'Medium', 'spring': 'Low'},
#                    ['image1.jpg', 'image2.jpg']]
