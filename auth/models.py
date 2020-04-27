from typing import Dict

from motor.motor_asyncio import AsyncIOMotorDatabase

from settings import ADMIN_COLLECTION
from auth.utils import hash_password


class User:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db[ADMIN_COLLECTION]

    async def create_admin(self, login, password):
        data = {
            'login': login,
            'password': hash_password(password)
        }
        await self.collection.insert_one(data)

    async def check_admin(self, login: str) -> Dict[str, str]:
        return await self.collection.find_one({'login': login})

    async def del_admin(self):
        pass

    async def get_user(self, login: str) -> Dict[str, str]:
        return await self.collection.find_one({'login': login})
