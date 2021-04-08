import sqlite3
from flask_restful import Resource, reqparse

# Have to insert null in as id is autoincrementing
class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="password field cannot be blank")
    parser.add_argument('password', type=str, required=True, help="username field cannot be blank")

    def post(self):
        data = UserRegister.parser.parse_args()
        item = User.find_by_username(data["username"])
        if item:
            return {"message": "username already exists"}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data["username"], data["password"]))
        connection.commit()
        connection.close()
        return {"message": "user created successfully"}

class User:
    def __init__(self, _id, username, password):
        self.id = _id
        self.username = username
        self.password = password

    @classmethod
    def find_by_username(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_user_by_name = "SELECT * FROM users where username=?"
        result = cursor.execute(select_user_by_name, (name,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        select_user_by_name = "SELECT * FROM users where id=?"
        result = cursor.execute(select_user_by_name, (_id,))
        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None
        connection.close()
        return user
