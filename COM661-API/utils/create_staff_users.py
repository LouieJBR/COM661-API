from pymongo import MongoClient
import bcrypt

client = MongoClient("mongodb://127.0.0.1:27017")
db = client.bizDB      # select the database
staff = db.staff        # select the collection name

staff_list = [
    {
        "name" : "Homer Simpson",
        "username" : "homer",
        "password" : b"homer_s",
        "email" : "homer@springfield.net",
        "admin" : False
    },
    {
        "name" : "Marge Simpson",
        "username" : "marge",
        "password" : b"marge_s",
        "email" : "marge@springfield.net",
        "admin" : False
    },
    {
        "name" : "Bart Simpson",
        "username" : "bart",
        "password" : b"bart_s",
        "email" : "bart@springfield.net",
        "admin" : False
    },
    {
        "name" : "Lisa Simpson",
        "username" : "lisa",
        "password" : b"lisa_s",
        "email" : "lisa@springfield.net",
        "admin" : True
    },
    {
        "name" : "Maggie Simpson",
        "username" : "maggie",
        "password" : b"maggie_s",
        "email" : "maggie@springfield.net",
        "admin" : False
    }
]

for new_staff_user in staff_list:
    new_staff_user["password"] = bcrypt.hashpw(new_staff_user["password"], bcrypt.gensalt())
    staff.insert_one(new_staff_user)
