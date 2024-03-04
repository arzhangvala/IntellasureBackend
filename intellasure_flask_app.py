from flask import Flask, request, jsonify

from dotenv import load_dotenv, dotenv_values
import psycopg2
import os
#Init app

app = Flask(__name__)
#Init DB
load_dotenv()

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_USER = os.getenv("DB_USER")

#class User(db.model)
user_hashmap = {
        "userid":[],
        "first_name":[],
        "last_name":[],
        "name": [],
        "email": [],
        "priviledges": [],
        "company": []
    }
def open_db():
    conn = psycopg2.connect(
        database = DB_NAME,
        user =DB_USER,
        password = DB_PASSWORD,
        host=DB_HOST
    )
    return conn

conn = open_db()
cursor = conn.cursor()
class User():

    def populate_user_hashmap(self):
        user_hashmap["userid"]

        cursor = conn.cursor()

        select_statement = "SELECT * FROM users"
        cursor.execute(select_statement)
        users = cursor.fetchall()

        for user in users:
            user_hashmap["userid"].append(user[0])
            user_hashmap["first_name"].append(user[1])
            user_hashmap["last_name"].append(user[2])
            user_hashmap["email"].append(user[3])
            user_hashmap["priviledges"].append(user[5])
            user_hashmap["company"].append(user[6])

def close_db(conn):
    conn.close()
app = Flask(__name__)
@app.route('/', methods=['GET'])
def check():

    return "API is working"
@app.route('/api/users/', methods=['GET'])
def api_user():

    return "Inside /api/users/"



@app.route('/api/users/<user_id>', methods=['GET','PUT'])
def update_user(user_id):
    method = request.json.get('method')
    data = request.json.get('data')
    if method == "PUT":

        if user_id is not user_hashmap:
            print(data)
            insert_query = '''INSERT INTO Users(UserID, First_Name, Last_Name, Name, Email, Priviledges, Company, Last_login, Creation_date)
            VALUES (%s, %s,%s, %s, %s, %s, %s, CAST(current_timestamp as timestamp), CAST(current_timestamp as timestamp) )'''
            data_to_insert = (data["user_id"],data["first_name"], data["last_name"], data["name"], data["email"], data["priviledges"], data["company"])
            cursor.execute(insert_query, data_to_insert)
            conn.commit()
            User.populate_user_hashmap()
            return jsonify({
                "Content-Type": "application/json",
                "status": "Success",
                "message": "User has been included in DB",

                "data":{
                    "first_name": data["first_name"],
                    "last_name": data["last_name"],
                    "name": data["name"],
                    "email": data["email"],
                    "priviledges": data["priviledges"],
                    "company": data["company"],
                    "user_id": data["user_id"]
                }
            })

        else:
            temp_response = {
                "Content-Type": "application/json",
                "status": "Error",
                "message": "User already exists, cannot create"
            }
            return jsonify(temp_response)
    if method == 'GET':
        response_body = request.json.get('data')
        select_query = '''SELECT * FROM Users WHERE UserID = %s'''
        cursor.execute("SELECT * FROM Users WHERE UserID = %s", (str(response_body["user_id"]),))
        user = cursor.fetchone()

        if user:
            last_login = user[7].strftime("%Y-%m-%d %H:%M:%S")
            creation_date = user[8].strftime("%Y-%m-%d %H:%M:%S")
            temp_repsonse ={
                "Content-Type":"application/json",
                "data":{
                "userid": user[0],
                "first_name": user[1],
                "last_name": user[2],
                "name": user[3],
                "email": user[4],
                "priviledges": user[5],
                "company": user[6],
                "last_login": last_login,
                "creation_date":creation_date
                }
            }

            return jsonify(temp_repsonse)
        else:
            temp_response = {
                "Content-Type": "application/json",
                "status": "Error",
                "message":"User not found"
            }
            return jsonify(temp_response)










if __name__ == '__main__':
    User = User()
    User.populate_user_hashmap()
    print(user_hashmap)
    app.debug = True
    app.run()