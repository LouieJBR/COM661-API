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

def signup():
    data = request.get_json()

    # Check if all required fields are present
    if not all(key in data for key in ('name', 'username', 'password', 'email')):
        return make_response(jsonify({'message': 'Missing required fields'}), 400)

    # Check if username or email already exists in the database
    existing_user = users.find_one({'$or': [{'username': data['username']}, {'email': data['email']}]})
    if existing_user:
        return make_response(jsonify({'message': 'Username or Email already exists'}), 400)

    # Hash the password before storing it
    hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

    # Create a new user document
    new_user = {
        'name': data['name'],
        'username': data['username'],
        'password': hashed_password,
        'email': data['email'],
        'admin': False  # You can set admin status here if needed
    }

    # Insert the new user into the database
    users.insert_one(new_user)

    # Prepare the response
    response_data = {
        'message': 'User registered successfully',
    }

    return make_response(jsonify(response_data), 201)



def login():
    auth_header = request.headers.get('Authorization')

    if not auth_header or 'Basic ' not in auth_header:
        return make_response(jsonify({'message': 'Authentication required'}), 401)

    encoded_credentials = auth_header.split(' ')[1]
    decoded_credentials = base64.b64decode(encoded_credentials).decode('utf-8')
    username, password = decoded_credentials.split(':')

    user = users.find_one({'username': username})

    if user is not None and bcrypt.checkpw(password.encode('utf-8'), user["password"]):
        token = jwt.encode({'user': username, 'admin': user['admin'],
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                           app.config['SECRET_KEY']).decode('utf-8')

        response = jsonify({'token': token})
        # Set the token as a header in the response
        response.headers['x-access-token'] = token

        return make_response(response, 200)
    else:
        return make_response(jsonify({'message': 'Incorrect Username or Password'}), 401)


def logout():
    token = request.headers['x-access-token']
    blacklist.insert_one({"token": token})
    return make_response(jsonify({'message': 'Logout successful'}), 200)
