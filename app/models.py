from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, user_doc):
        self.id = str(user_doc["_id"])
        self.username = user_doc["username"]
        self.email = user_doc["email"]
        self.password_hash = user_doc["password_hash"]
