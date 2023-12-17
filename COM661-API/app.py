from bson import ObjectId
from bson.json_util import default
from flask import Flask, json
from pymongo import MongoClient
from flask_cors import CORS

from services import productService, sprayService, reviewService, userService, tokenService, wishlistService
from services.tokenService import jwt_required, admin_required


app = Flask(__name__)
CORS(app)

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Shop  # select the database
products = db.Products  # select the collection
users = db.Users
ingredients = db.Ingredients
blacklist = db.blacklist

app.config['SECRET_KEY'] = 'mysecret'

BASE_URL = '/api/v1.0'


@app.route(BASE_URL + '/login', methods=['POST'])
def login():
    return userService.login()


@app.route(BASE_URL + '/signup', methods=['POST'])
def signup():
    return userService.signup()


@app.route(BASE_URL + '/logout', methods=["GET"])
@jwt_required
def logout():
    return userService.logout()


@app.route(BASE_URL + "/products", methods=["GET"])
def return_all_products():
    return productService.return_all_products()


@app.route(BASE_URL + "/wishlist/<string:username>/add/<string:product_id>", methods=["POST"])
def add_product_to_wishlist(username, product_id):
    return wishlistService.add_product_to_wishlist(username, product_id)


@app.route(BASE_URL + "/wishlist/<string:username>/remove/<string:product_id>", methods=["DELETE"])
def remove_product_from_wishlist(username, product_id):
    return wishlistService.remove_product_from_wishlist(username, product_id)


@app.route(BASE_URL + "/wishlist/<string:username>", methods=["GET"])
def get_all_products_from_wishlist(username):
    return wishlistService.get_all_products_from_wishlist(username)


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


@app.route(BASE_URL + "/products/type/<string:productType>", methods=["GET"])
def return_type_of_product(productType):
    return productService.return_type_of_product(productType)


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


@app.route(BASE_URL + "/users/<string:username>", methods=["GET"])
def get_user_id(username):
    print(userService.get_user_id(username))
    return userService.get_user_id(username)


if __name__ == "__main__":
    tokenService.appKey = app.config['SECRET_KEY']
    productService.products = products
    reviewService.products = products

    app.run(debug=True)
