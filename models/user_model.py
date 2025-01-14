from werkzeug.security import generate_password_hash
from flask_pymongo import PyMongo

class UserModel:
    def __init__(self, db):
        self.collection = db.signup

    def is_mobile_registered(self, mobile):
        """Check if the mobile number is already registered."""
        return self.collection.find_one({"mobile": mobile})

    def create_user(self, name, mobile, password):
        """Insert a new user into the database."""
        hashed_password = generate_password_hash(password)
        user_data = {
            "name": name,
            "mobile": mobile,
            "password": hashed_password
        }
        self.collection.insert_one(user_data)
        return True
