from flask import Flask
from pymongo import MongoClient

from services import productService, sprayService, reviewService, userService, tokenService
from services.tokenService import jwt_required, admin_required

app = Flask(__name__)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Shop  # select the database
products = db.Products  # select the collection
users = db.Users
ingredients = db.Ingredients
blacklist = db.blacklist

app.config['SECRET_KEY'] = 'mysecret'

BASE_URL = '/api/v1.0'


@app.route(BASE_URL + '/login', methods=['GET'])
def login():
    return userService.login()


@app.route(BASE_URL + '/logout', methods=["GET"])
@jwt_required
def logout():
    return userService.logout()


@app.route(BASE_URL + "/products", methods=["GET"])
def return_all_products():
    return productService.return_all_products()


@app.route(BASE_URL + "/products/sprays", methods=["GET"])
def return_all_sprays():
    return sprayService.return_all_sprays()


@app.route(BASE_URL + "/products/<string:id>", methods=["GET"])
def return_one_product(id):
    return productService.return_one_product(id)


@app.route(BASE_URL + "/products", methods=["POST"])
@jwt_required
def add_new_product():
    return productService.add_new_product()


@app.route(BASE_URL + "/products/<string:id>", methods=["PUT"])
@jwt_required
def edit_product(id):
    return productService.edit_product(id)


@app.route(BASE_URL + "/products/<string:id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_product(id):
    return productService.delete_product(id)


@app.route(BASE_URL + "/products/<string:id>/reviews", methods=["GET"])
def fetch_all_reviews(id):
    return reviewService.fetch_all_reviews(id)


@app.route(BASE_URL + "/products/<string:p_id>/reviews", methods=["POST"])
def add_new_review(p_id):
    return reviewService.add_new_review(p_id)


@app.route(BASE_URL + "/products/<string:p_id>/reviews/<string:r_id>", methods=["GET"])
def fetch_one_review(p_id, r_id):
    return reviewService.fetch_one_review(p_id, r_id)


@app.route(BASE_URL + "/products/<string:p_id>/reviews/<string:r_id>", methods=["PUT"])
@jwt_required
def edit_review(p_id, r_id):
    return reviewService.edit_review(p_id, r_id)


@app.route(BASE_URL + "/products/<string:p_id>/reviews/<string:r_id>", methods=["DELETE"])
@jwt_required
@admin_required
def delete_review(p_id, r_id):
    return reviewService.delete_review(p_id, r_id)


if __name__ == "__main__":
    tokenService.appKey = app.config['SECRET_KEY']
    productService.products = products
    reviewService.products = products

    app.run(debug=True)
