import os

import envparse
import trafaret as T
from trafaret_config import read_and_validate
from os.path import isfile
from envparse import env
from aiohttp.web import Application

ADMIN_COLLECTION = 'admin'

if isfile('.env'):
    env.read_envfile('.env')
else:
    raise SystemExit('Create an env-file please.!')

MONGO_HOST = os.getenv('MONGO_HOST')
MONGO_DB_NAME = env.str('MONGO_DB_NAME')

REDIS_HOST = env.tuple('REDIS_HOST')

PORT = env.int('PORT')

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
