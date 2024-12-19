from werkzeug.security import check_password_hash
from flask_pymongo import PyMongo

class SignInModel:
    def __init__(self, db):
        self.collection = db.signup  # Collection name is 'signup'

    def validate_user(self, mobile, password):
        """
        Validate user credentials.
        1. Check if the mobile exists.
        2. Verify the password using bcrypt.
        """
        user = self.collection.find_one({"mobile": mobile})
        if user and check_password_hash(user["password"], password):
            return user
        return None

