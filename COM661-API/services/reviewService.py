from bson import ObjectId
from flask import request, jsonify, make_response

products: {}


def fetch_all_reviews(id):
    data_to_return = []
    product = products.find_one(
        {"_id": ObjectId(id)},
        {"reviews": 1, "_id": 0})
    if product is not None:
        for review in product["reviews"]:
            review["_id"] = str(review["_id"])
            data_to_return.append(review)
        if data_to_return:
            return make_response(jsonify(data_to_return), 200)
        else:
            return make_response(jsonify({"error": "There are no reviews associated wth this product."}), 404)
    else:
        return make_response(jsonify({"error": "Invalid product ID"}), 404)


def add_new_review(p_id):
    if "username" in request.form and request.form["username"] != "":
        if "comment" in request.form and request.form["comment"] != "":
            if "stars" in request.form and request.form["stars"] != "":
                new_review = {
                    "_id": ObjectId(),
                    "username": request.form["username"],
                    "comment": request.form["comment"],
                    "stars": request.form["stars"]
                }
                products.update_one({"_id": ObjectId(p_id)}, {"$push": {"reviews": new_review}})
                new_review_link = "http://localhost:5000/api/v1.0/products/" \
                                  + p_id + "/reviews/" + str(new_review['_id'])
                return make_response(jsonify({"url": new_review_link}), 201)
            else:
                return make_response(jsonify({"error": "Missing stars data"}), 400)
        else:
            return make_response(jsonify({"error": "Missing comment data"}), 400)
    else:
        return make_response(jsonify({"error": "Missing username data"}), 400)


def fetch_one_review(p_id, r_id):
    product = products.find_one({'_id': ObjectId(p_id)})
    if product is not None:
        productReview = products.find_one(
            {"reviews._id": ObjectId(r_id)},
            {"_id": 0, "reviews.$": 1})
        if productReview is not None:
            productReview['reviews'][0]['_id'] = str(productReview['reviews'][0]['_id'])
            return make_response(jsonify(productReview['reviews'][0]), 200)
        else:
            return make_response(jsonify({"error": "Invalid review ID"}), 404)
    else:
        return make_response(jsonify({"error": "Invalid product ID"}), 404)


def edit_review(p_id, r_id):
    if "username" in request.form and request.form["username"] != "":
        if "comment" in request.form and request.form["comment"] != "":
            if "stars" in request.form and request.form["stars"] != "":
                product = products.find_one({'_id': ObjectId(p_id)})
                if product is not None:
                    edited_review = {
                        "reviews.$.username": request.form["username"],
                        "reviews.$.comment": request.form["comment"],
                        "reviews.$.stars": request.form['stars']
                    }
                    updatedReview = products.update_one({"reviews._id": ObjectId(r_id)}, {"$set": edited_review})
                    if updatedReview.matched_count == 1:
                        edit_review_url = \
                            "http://localhost:5000/api/v1.0/products/" + \
                            p_id + "/reviews/" + r_id
                        return make_response(jsonify({"url": edit_review_url}), 200)
                    else:
                        return make_response(jsonify({"error": "Invalid review ID"}), 404)
                else:
                    return make_response(jsonify({"error": "Invalid product ID"}), 404)
            else:
                return make_response(jsonify({"error": "Missing stars data"}), 400)
        else:
            return make_response(jsonify({"error": "Missing comment data"}), 400)
    else:
        return make_response(jsonify({"error": "Missing username data"}), 400)


def delete_review(p_id, r_id):
    product = products.find_one({'_id': ObjectId(p_id)})
    if product is not None:
        productReview = products.find_one(
            {"reviews._id": ObjectId(r_id)},
            {"_id": 0, "reviews.$": 1})
        if productReview is not None:
            products.update_one( \
                {"_id": ObjectId(p_id)}, \
                {"$pull": {"reviews": \
                               {"_id": ObjectId(r_id)}}})
            return make_response(jsonify({}), 204)
        else:
            return make_response(jsonify({"error": "Invalid review ID"}), 404)
    else:
        return make_response(jsonify({"error": "Invalid product ID"}), 404)
