import jwt
from aiohttp.web import middleware, json_response
from settings import JWT_ALGORITHM, JWT_SECRET_KEY


@middleware
async def check_token(request, handler):
    protected_paths = ('/api')
    if not request.path.startswith(protected_paths):
        return await handler(request)

    response = {
        'auth_link': '/',
        'success': False,
        'invalid_token': True
    }

    token = request.headers.get('Authorization')
    if not token:
        # нет токена в заголовке
        return json_response(response)

    try:
        jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except (jwt.DecodeError, jwt.ExpiredSignatureError):
        # токен невалидный или истек
        return json_response(response)

    return await handler(request)
