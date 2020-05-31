import jwt
import aiohttp_jinja2
from aiohttp import web

from auth.utils import verify_password
from auth.jwt_payload import BaseAuthPayload, BeerBlog
from settings import SERVICES


@aiohttp_jinja2.template('login.html')
async def get_login_page(request):
    return {}


@aiohttp_jinja2.template('create_user.html')
async def get_create_user_page(request):
    context = {
        'services': SERVICES
    }
    return context


async def login(request):
    response = {
        'success': False,
        'message': 'Пользователь не найден'
    }
    data = await request.json()
    services = request.app['services']
    service_name = data['service']
    if service_name is None:
        service_name = 'authorization'
    service = services.get(service_name)
    if service is None:
        response['message'] = 'Неверное имя сервиса'
        return web.json_response(response)

    user = await request.app['models']['users'].get_user(data['login'])

    if user is None \
            or service_name not in user['services'] \
            or not verify_password(user['password'], data['password']):
        return web.json_response(response)

    payload_class = {
        'beerblog': lambda service: BeerBlog(service),
        'admin': lambda service: BaseAuthPayload(service),
        'authorization': lambda service: BaseAuthPayload(service),
    }
    payload = payload_class[service_name](service)
    jwt_token = jwt.encode(
        payload.create_payload(user, **data),
        service['secret_key'],
        service['algorithm']
    ).decode('utf-8')

    del user['_id']

    response = {
        'success': True,
        'token': jwt_token,
        'auth_link': service['redirect_link'].format(jwt_token),
        'service': service_name,
        'user': user
    }
    return web.json_response(response)
