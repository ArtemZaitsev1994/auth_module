from aiohttp import web

from auth.utils import hash_password


async def create_user(request):
    data = await request.json()
    data['password'] = hash_password(data['password'])

    user = await request.app['models']['users'].create_user(data)

    if user.acknowledged:
        response = {'success': True}
    else:
        response = {
            'success': False,
            'mesage': 'Пользователь не был добавлен'
        }

    return web.json_response(response)


async def check_token(request):
    """Заглушка"""
    return web.json_response({'success': True})
