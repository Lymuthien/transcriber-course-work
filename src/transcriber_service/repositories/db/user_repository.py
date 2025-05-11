import os
from datetime import datetime
from typing import Optional
from pymongo import MongoClient
from dotenv import load_dotenv
from transcriber_service.domain.entities.user import User
from ...domain.interfaces import IUserRepository

load_dotenv()


class MongoUserRepository(IUserRepository):
    def __init__(self):
        self._client = MongoClient(os.getenv("MONGO_URI"))
        self._db = self._client[os.getenv("DB_NAME")]
        self._users = self._db.users

        self._users.create_index("email", unique=True)

    def get_by_email(self, email: str) -> Optional[User]:
        doc = self._users.find_one({"email": email})
        if doc:
            # Конвертируем MongoDB DateTime в Python datetime
            if doc.get("reset_token_expiry"):
                doc["reset_token_expiry"] = datetime.fromisoformat(
                    doc["reset_token_expiry"]
                )
            return User(**doc)
        return None

    def save(self, user: User) -> None:
        user_dict = user.__dict__
        # Конвертируем datetime в строку для MongoDB
        if user.reset_token_expiry:
            user_dict["reset_token_expiry"] = user.reset_token_expiry.isoformat()

        self._users.update_one({"email": user.email}, {"$set": user_dict}, upsert=True)
