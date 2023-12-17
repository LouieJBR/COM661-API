from bson import ObjectId
from flask import request, jsonify, make_response, json
from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Shop  # select the database
users = db.Users  # select the collection
productsCollection = db.Products  # collection containing all products
wishlist_items = db.Wishlist

def add_product_to_wishlist(username, product_id):
    # Create a wishlist item document
    wishlist_item = {
        "username": username,
        "product_id": ObjectId(product_id)  # Assuming product_id is the ObjectId of the product
    }

    # Insert the wishlist item into the collection
    inserted_item = wishlist_items.insert_one(wishlist_item)

    if inserted_item.inserted_id:
        return make_response(jsonify({"message": "Product added to wishlist"}), 200)
    else:
        return make_response(jsonify({"error": "Failed to add product to wishlist"}), 400)

def remove_product_from_wishlist(username, product_id):
    if not username or not product_id:
        return make_response(jsonify({"error": "Username or product ID missing"}), 400)

    # Delete the wishlist item with the specified username and product ID
    delete_result = wishlist_items.delete_one({"username": username, "product_id": ObjectId(product_id)})

    if delete_result.deleted_count > 0:
        return make_response(jsonify({"message": "Product removed from wishlist"}), 200)
    else:
        return make_response(jsonify({"error": "Failed to remove product from wishlist"}), 400)



def get_all_products_from_wishlist(username):
    # Find wishlist items for the given username
    wishlist_items_cursor = wishlist_items.find({"username": username})

    # Retrieve product IDs from wishlist items
    product_ids = [item['product_id'] for item in wishlist_items_cursor]

    # Find products in the products collection based on product IDs
    wishlist_products_cursor = productsCollection.find({"_id": {"$in": product_ids}})

    # Convert ObjectId to string for each product in the wishlist
    wishlist = [{
        "_id": str(product['_id']),
        "name": product.get('name', ''),
        "price": product.get('price', 0.0),
        "type": product.get('type', ''),
        "description": product.get('description', '')
        # Add other fields as needed
    } for product in wishlist_products_cursor]

    return make_response(jsonify({"wishlist": wishlist}), 200)
