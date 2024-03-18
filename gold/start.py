''' Первый и второй спринт.
Написание REST API в отдельном файле start.py, который вызывает из класса методы:
- по работе с данными;
-
'''
import psycopg2
from psycopg2.extras import Json
from flask import Flask, request, jsonify
import mountains

# Инициализация Flask приложения
app = Flask(__name__)
print(app)
# Метод POST submitData для REST API
# @app.route('/', methods=['POST'])
# def pas():
#     return print('3')

# def submitData():
#     data = request.get_json()
#     if not data:
#         return jsonify({"status": 400, "message": "Bad Request", "id": None})
#
#     try:
#         print('1')
#         inserted_id = db.insert_mountains(data)
#         return {"status": 200, "message": "Отправлено успешно", "id": inserted_id}
#
#     except Exception as e:
#         return jsonify({"status": 500, "message": str(e), "id": None})

if __name__ == '__main__':
    app.run(debug=True)