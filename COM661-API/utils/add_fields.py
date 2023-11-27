from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Shop  # select the database
products = db.Products  # select the collection

for product in products.find():
    products.update_one(
        {"_id": product['_id']},
        {
            "$set": {
                "url": "http://localhost:5000/api/v1.0/products/" + str(product['_id'])
            }
        }
    )
