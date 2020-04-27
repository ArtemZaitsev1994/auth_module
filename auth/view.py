from typing import Dict
import datetime

import jwt
import aiohttp_jinja2
from aiohttp import web

from auth.utils import verify_password


@aiohttp_jinja2.template('login.html')
async def get_login_page(request):
    return {}


async def login(request):
    data = await request.json()
    services = request.app['services']
    service_name = data['service']
    service = services[service_name]

    user = await request.app['models']['users'].get_user(data['login'])

    if user is None or not verify_password(user['password'], data['password']):
        return web.json_response({'success': False, 'message': 'Wrong credentials'})

    payload_class = {
        'beerblog': lambda x: BeerBlog(x),
        'admin': lambda x: Admin(x)
    }
    payload = payload_class[service_name](service)
    jwt_token = jwt.encode(
        payload.create_payload(user, **data),
        service['secret_key'],
        service['algorithm']
    ).decode('utf-8')

    response = {
        'success': True,
        'token': jwt_token,
        'auth_link': service['redirect_link'].format(jwt_token),
    }
    return web.json_response(response)


# TODO переписать эту байду
class BaseAuthPayload:

    def __init__(self, service):
        self.service = service

    def create_payload(self, user: Dict[str, str], **kw):

        payload = {
            'login': user['login'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=self.service['jwt_ttl_minutes']),
        }

        return payload


class Admin(BaseAuthPayload):

    def create_payload(self, user: Dict[str, str], **kw):

        payload = {
            'login': user['login'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=self.service['jwt_ttl_minutes']),
            'is_admin': True
        }

        return payload


class BeerBlog(BaseAuthPayload):

    def create_payload(self, user: Dict[str, str], **kw):

        payload = {
            'login': user['login'],
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=self.service['jwt_ttl_minutes']),
            'is_admin': True,
            'section': kw['section']
        }

        return payload
