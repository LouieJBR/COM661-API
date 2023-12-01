from flask import jsonify, make_response
from pymongo import MongoClient

from utils import Utils

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Shop  # select the database
products = db.Products  # select the collection


def return_all_sprays():
    page_num, page_size, page_start = Utils.pagination()
    sort_field, sort_order = Utils.check_sort_params()

    pipeline = [
        {"$match": {"type": {'$in': ['Room Spray', 'Body Spray', 'Pillow Spray']}}},
        {"$sort": {sort_field: sort_order}}
    ]

    data_to_return = []
    for product in products.aggregate(pipeline):
        product['_id'] = str(product['_id'])
        data_to_return.append(product)

    # Apply skip and limit after aggregation
    data_to_return = data_to_return[page_start:page_start + page_size]

    return make_response(jsonify(data_to_return), 200)

