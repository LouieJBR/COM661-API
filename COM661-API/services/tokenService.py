from functools import wraps

import jwt
from flask import request, jsonify, make_response
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Shop  # select the database
products = db.Products  # select the collection
users = db.Users
ingredients = db.Ingredients
blacklist = db.blacklist

appKey = any


def jwt_required(func):
    @wraps(func)
    def jwt_required_wrapper(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify(
                {'message': 'Token is missing'}), 401
        try:
            data = jwt.decode(token, appKey)
        except:
            return jsonify(
                {'message': 'Token is invalid'}), 401

        bl_token = blacklist.find_one({"token": token})
        if bl_token is not None:
            return make_response(jsonify(
                {'message':
                     'Token has been cancelled. This session was ended.'}), 401)
        return func(*args, **kwargs)

    return jwt_required_wrapper


def admin_required(func):
    @wraps(func)
    def admin_required_wrapper(*args, **kwargs):
        token = request.headers['x-access-token']
        data = jwt.decode(token, appKey)
        if data['admin']:
            return func(*args, **kwargs)
        else:
            return make_response(jsonify({'message': 'Administrator access is required for this operation'}), 401)

    return admin_required_wrapper
