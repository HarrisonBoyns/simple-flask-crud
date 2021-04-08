from flask import Flask
from flask_jwt import JWT
from flask_restful import Api
from app.security import authenticate
from app.security import identity
from app.user import UserRegister
from app.items import Items, ItemList

app = Flask(__name__)
app.secret_key = "top_secret"
api = Api(app)
jwt = JWT(app, authentication_handler=authenticate, identity_handler=identity)

api.add_resource(Items, "/items/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/signup")