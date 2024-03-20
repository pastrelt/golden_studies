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
        conn.close()


# Инициализация Flask приложения
app = Flask(__name__)

@app.route('/submitData/', methods=['GET'])
def get_record_by_id():
    data = request.get_json()
    print(data) #проверка
    if not data:
        return jsonify({"status": 400, "message": "Bad Request", "id": {}})

    try:
        db = Database()
        inserted_id = db.get_record_by_id(data)
        return jsonify({"status": 200, "message": "Запрос успешно завершен.", "id": inserted_id})

    except Exception as e:
        return jsonify({"status": 500, "message": str(e), "id": None})

if __name__ == '__main__':
    app.run(debug=True)