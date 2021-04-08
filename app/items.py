from flask_restful import Resource, reqparse
import sqlite3


# Move to sql statements into class methods
# warp these classmethods in a try except to catch any errors

class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, required=True, help="include name field")
    parser.add_argument('price', type=float, required=True, help="include price field")

    @classmethod
    def get_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE item=?"
        item = cursor.execute(query, (name,))
        return item.fetchone()

    @classmethod
    def insert_into(cls, data):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "INSERT INTO items VALUES (Null, ?, ?)"
        cursor.execute(query, (data.get('name'), data.get('price')))
        connection.commit()
        connection.close()

    @classmethod
    def update(cls, data):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "UPDATE items SET price=?"
        cursor.execute(query, (data.get("price"),))
        connection.commit()
        connection.close()

    # @jwt_required()
    def get(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items WHERE item=?"
        item = cursor.execute(query, (name,))
        json_item = item.fetchone()
        connection.close()
        return {"item": json_item}, 200 if json_item else 404

    # @jwt_required()
    def post(self, name):

        json_item = self.get_by_name(name)

        if json_item is not None:
            return {"message": "item with this name already exists"}, 404
        data = Items.parser.parse_args()
        try:
            self.insert_into(data)
        except IOError:
            return {"message": "Error inserting into database"}, 500

        return {"message": "successfully added"}, 201

    def delete(self, name):
        json_item = self.get_by_name(name)

        if json_item is None:
            return {"message": "item not found"}, 400

        try:
            connection = sqlite3.connect('data.db')
            cursor = connection.cursor()
            query = "DELETE FROM items WHERE item=?"
            cursor.execute(query, (name,))
            connection.commit()
            connection.close()
        except:
            return {"message": "server error"}, 500
        
        return {"message": "deleted"}, 201

    def put(self, name):
        json_item = self.get_by_name(name)

        data = Items.parser.parse_args()
        try:
            if json_item is None:
                self.insert_into(data)
            else:
                self.update(data)
        except:
            return {"message": "error inserting data into the database"}, 500

        return {"item": data}, 200


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "SELECT * FROM items"
        item = cursor.execute(query)
        json_item = item.fetchall()
        connection.commit()
        connection.close()
        return {"items": json_item}, 200 if json_item else 404

    def delete(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = "DELETE FROM items"
        cursor.execute(query)
        connection.commit()
        connection.close()
        return {"message": "success"}, 200
