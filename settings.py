import os

import envparse
import trafaret as T
from trafaret_config import read_and_validate
from os.path import isfile
from envparse import env
from aiohttp.web import Application


if isfile('.env'):
    env.read_envfile('.env')
else:
    raise SystemExit('Create an env-file please.!')

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_DB_NAME = env.str('MONGO_DB_NAME')
COLLECTION_NAME = env.str('COLLECTION_NAME')

JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')
JWT_ALGORITHM = env.str('JWT_ALGORITHM')

PORT = env.int('PORT')

SERVICES = env.list('SERVICES')

try:
    ADMIN_LOGIN = env.str('ADMIN_LOGIN')
    ADMIN_PASSWORD = env.str('ADMIN_PASSWORD')
except envparse.ConfigurationError:
    ADMIN_PASSWORD, ADMIN_LOGIN = None, None


def setup_app(app: Application):

    if isfile('config.yaml'):
        TRAFARET = T.Dict({
            T.Key('services'): T.List(
                T.Dict({
                    'name': T.String(),
                    'jwt_ttl_minutes': T.Int(),
                    'redirect_link': T.String(),
                    'algorithm': T.String(),
                    'secret_key': T.String()
                })
            )
        })

        config = read_and_validate('config.yaml', TRAFARET)
        app['services'] = {x['name']: x for x in config['services']}
