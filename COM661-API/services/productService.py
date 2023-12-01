from bson import ObjectId
from flask import request, jsonify, make_response

from utils import Utils

products = {}


def return_all_products():
    page_num, page_size, page_start = Utils.pagination()
    sort_field, sort_order = Utils.check_sort_params()

    pipeline = [
        {"$sort": {sort_field: sort_order}}
    ]

    data_to_return = []
    for product in products.aggregate(pipeline):
        product['_id'] = str(product['_id'])
        for review in product['reviews']:
            review['_id'] = str(review['_id'])
        data_to_return.append(product)

    data_to_return = data_to_return[page_start:page_start + page_size]

    return make_response(jsonify(data_to_return), 200)


def return_one_product(id):
    product = products.find_one({'_id': ObjectId(id)})
    if product is not None:
        product['_id'] = str(product['_id'])
        for review in product['reviews']:
            review['_id'] = str(review['_id'])
        print(product)
        return make_response(jsonify([product]), 200)
    else:
        return make_response(jsonify({"error": "Invalid product ID"}), 404)


def add_new_product():
    if "name" in request.form and request.form["name"] != "":
        if "price" in request.form and request.form["price"] is not None:
            if "type" in request.form and request.form["type"] != "":
                if "size" in request.form and request.form["size"] != "":
                    if "description" in request.form and request.form["description"] != "":
                        new_product = {"name": request.form["name"],
                                       "price": request.form["town"],
                                       "type": request.form["type"],
                                       "size": request.form["size"],
                                       "description": request.form["description"],
                                       "reviews": []
                                       }

                        new_product_id = products.insert_one(new_product)
                        new_product_link = "http://localhost:5000/api/v1.0/products/" \
                                           + str(new_product_id.inserted_id)
                        return make_response(jsonify(
                            {"url": new_product_link}), 201)
                    else:
                        return make_response(jsonify({"error": "Missing description data"}), 400)
                else:
                    return make_response(jsonify({"error": "Missing size data"}), 400)
            else:
                return make_response(jsonify({"error": "Missing type data"}), 400)
        else:
            return make_response(jsonify({"error": "Missing price data"}), 400)
    else:
        return make_response(jsonify({"error": "Missing name data"}), 400)


def edit_product(id):
    if "name" in request.form and request.form["name"] != "":
        if "price" in request.form and request.form["price"] is not None:
            if "type" in request.form and request.form["type"] != "":
                if "size" in request.form and request.form["size"] != "":
                    if "description" in request.form and request.form["description"] != "":
                        result = products.update_one({"_id": ObjectId(id)}, {
                            "$set": {"name": request.form["name"],
                                     "price": request.form["price"],
                                     "type": request.form["type"],
                                     "size": request.form["size"],
                                     "description": request.form["description"],
                                     }
                        })
                        if result.matched_count == 1:
                            edited_product_link = \
                                "http://localhost:5000/api/v1.0/products/" + id
                            return make_response(jsonify(
                                {"url": edited_product_link}), 200)
                    else:
                        return make_response(jsonify({"error": "Missing description data"}), 400)
                else:
                    return make_response(jsonify({"error": "Missing size data"}), 400)
            else:
                return make_response(jsonify({"error": "Missing type data"}), 400)
        else:
            return make_response(jsonify({"error": "Missing price data"}), 400)
    else:
        return make_response(jsonify({"error": "Missing name data"}), 400)


def delete_product(id):
    result = products.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 1:
        return make_response(jsonify({}), 204)
    else:
        return make_response(jsonify({"error": "Invalid product ID"}), 404)
