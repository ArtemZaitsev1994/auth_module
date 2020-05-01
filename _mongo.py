import os
import json

from motor import motor_asyncio as ma
from aiohttp.web import Application
from aiofile import AIOFile

from settings import MONGO_DB_NAME, MONGO_HOST
from auth.models import User
from auth.utils import hash_password


async def _check_users(app: Application):
    if not os.path.isfile('users.json'):
        return

    async with AIOFile('users.json', 'r') as f:
        users = json.loads(await f.read())

    for user in users:
        if not await app['models']['users'].get_user(user['login']):
            user['password'] = hash_password(user['password'])
            await app['models']['users'].create_user(user)


def mongo_setup(app: Application):
    app.client = ma.AsyncIOMotorClient(MONGO_HOST)
    app.db = app.client[MONGO_DB_NAME]

    app['models'] = {
        'users': User(app.db)
    }

    app.on_startup.append(_check_users)
