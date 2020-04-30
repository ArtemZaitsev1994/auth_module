from aiohttp import web

from auth.utils import hash_password


async def create_user(request):
    response = {
        'success': False,
        'message': 'Пользователь не был добавлен'
    }
    data = await request.json()
    data['password'] = hash_password(data['password'])

    if await request.app['models']['users'].get_user(data['login']):
        response['message'] = 'Пользователь уже существует с таким логином'
        web.json_response(response)

    user = await request.app['models']['users'].create_user(data)

    if user.acknowledged:
        response = {'success': True}

    return web.json_response(response)


async def check_token(request):
    """Заглушка"""
    return web.json_response({'success': True})
