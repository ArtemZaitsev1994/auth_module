import jwt
import aiohttp_jinja2
from aiohttp import web

from auth.utils import verify_password
from auth.jwt_payload import Admin, BeerBlog


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
        'beerblog': lambda service: BeerBlog(service),
        'admin': lambda service: Admin(service)
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
