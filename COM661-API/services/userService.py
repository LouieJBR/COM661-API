import datetime

import bcrypt
import jwt
from flask import request, jsonify, make_response
from pymongo import MongoClient

from app import app

BASE_URL = '/api/v1.0'

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Shop  # select the database
products = db.Products  # select the collection
users = db.Users
ingredients = db.Ingredients
blacklist = db.blacklist


def login():
    auth = request.authorization

    print(auth)

    if auth:

        user = users.find_one({'username': auth.username})

        if user is not None:

            if bcrypt.checkpw(bytes(auth.password, 'UTF-8'), user["password"]):

                token = jwt.encode({'user': auth.username, 'admin': user['admin'],

                                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},

                                   app.config['SECRET_KEY'])

                return make_response(jsonify({'token': token}), 200)

            else:

                return make_response(jsonify({'message': 'Incorrect Username or Password'}), 401)

        else:

            return make_response(jsonify({'message': 'Incorrect Username or Password'}), 401)

    return make_response(jsonify({'message': 'Authentication required'}), 401)


def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one({"token": token})
    return make_response(jsonify({'message': 'Logout successful'}), 200)
