import base64
import datetime

import bcrypt
import jwt as jwt
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
    auth_header = request.headers.get('Authorization')
    print('auth headers: ', auth_header)

    if not auth_header or 'Basic ' not in auth_header:
        return make_response(jsonify({'message': 'Authentication required'}), 401)

    encoded_credentials = auth_header.split(' ')[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    username, password = decoded_credentials.split(':')

    print(username, password)

    user = users.find_one({'username': username})

    if user is not None and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        token = jwt.encode({'user': username, 'admin': user['admin'],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY'])
        return make_response(jsonify({'token': token}), 200)
    else:
        return make_response(jsonify({'message': 'Incorrect Username or Password'}), 401)
# def login():
#     auth = request.authorization
#
#     print(request.authorization)
#
#     if auth:
#
#         user = users.find_one({'username': auth.username})
#
#         if user is not None:
#
#             if bcrypt.checkpw(bytes(auth.password, 'UTF-8'), user["password"]):
#
#                 token = jwt.encode({'user': auth.username, 'admin': user['admin'],
#
#                                     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
#
#                                    app.config['SECRET_KEY'])
#
#                 return make_response(jsonify({'token': token}), 200)
#
#             else:
#
#                 return make_response(jsonify({'message': 'Incorrect Username or Password'}), 401)
#
#         else:
#
#             return make_response(jsonify({'message': 'Incorrect Username or Password'}), 401)
#
#     return make_response(jsonify({'message': 'Authentication required'}), 401)


def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one({"token": token})
    return make_response(jsonify({'message': 'Logout successful'}), 200)
