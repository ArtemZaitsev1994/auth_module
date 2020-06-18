import jwt
from aiohttp.web import middleware, json_response


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
    
    payload = None
    for service in request.app['services']:
        try:
            payload = jwt.decode(token, service['secret_key'], algorithms=[service['algorithm']])
        except (jwt.DecodeError, jwt.ExpiredSignatureError):
            # токен невалидный или истек
            continue
    if payload is None:
        return json_response(response)
     
    request['login'] = payload['login']
    return await handler(request)    
