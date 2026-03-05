from flask_login import UserMixin
from bson.objectid import ObjectId

class User(UserMixin):
    def __init__(self, doc):
        self.id = str(doc["_id"])
        self.email = doc["email"]
        self.plan = doc.get("plan", "free")

    def get_id(self):
        return self.id

    @staticmethod
    def from_id(db, user_id: str):
        try:
            doc = db.users.find_one({"_id": ObjectId(user_id)})
        except Exception:
            return None
        return User(doc) if doc else None
