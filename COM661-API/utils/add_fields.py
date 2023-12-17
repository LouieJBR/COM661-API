from pymongo import MongoClient

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.Shop  # select the database
users = db.Users  # select the collection

users.update_many(
    {},
    {
        "$set": {
            "wishlist": []  # Set 'wishlist' as an empty array for each document
        }
    }
)
