from typing import Dict, Any

from motor.motor_asyncio import AsyncIOMotorDatabase
from bson.objectid import ObjectId

from settings import COLLECTION_NAME
from auth.utils import hash_password


class User:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = self.db[COLLECTION_NAME]

    async def create_admin(self, login, password):
        data = {
            'login': login,
            'password': hash_password(password)
        }
        await self.collection.insert_one(data)

    async def create_user(self, data: Dict[str, Any]):
        return await self.collection.insert_one(data)

    async def check_admin(self, login: str) -> Dict[str, str]:
        return await self.collection.find_one({'login': login})

    async def del_admin(self):
        pass

    async def get_user(self, login: str) -> Dict[str, str]:
        return await self.collection.find_one({'login': login})

    async def get_user_by_service(self, login: str, service: str) -> Dict[str, str]:
        return await self.collection.find_one({'login': login, 'services': service})

    async def change_password(self, _id: str, psw: str):
        return await self.collection.update_one({'_id': ObjectId(_id)}, {'$set': {'password': psw}})
