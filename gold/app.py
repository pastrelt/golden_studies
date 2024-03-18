# import psycopg2
# from psycopg2.extras import Json
# from flask import Flask, request, jsonify
#app = Flask(__name__)

# @app.route('/')
# def submit():
#   return 'Hello, World!'
#
# @app.route('/about')
# def about():
#   return 'This is the about page'
#
# @app.route('/submitData')
# def submitData():
#   data = request.get_json()
#   return data
#
# # Маршрут для добавления новой записи
# @app.route('/submitData', methods=['POST'])
# def submit_data():
#     data = request.json
#     inserted_id = db.insert_pereval(data)
#     return jsonify({"status": 200, "message": "Отправлено успешно", "id": inserted_id})
#
# # Маршрут для обновления статуса записи
# @app.route('/updateStatus/<int:pereval_id>', methods=['PUT'])
# def update_status(pereval_id):
#     data = request.json
#     new_status = data.get('status')
#     update_result = db.update_status(pereval_id, new_status)
#     return jsonify(update_result)



# # GET запрос
# @app.route('/greet/pas')
# def greet(name):
#   return f'Hello, {name}!'

# if __name__ == '__main__':
#   app.run(debug=True)
