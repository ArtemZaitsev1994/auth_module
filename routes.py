from auth.view import login, get_login_page, get_create_user_page, change_password
from auth.api import create_user, check_token


routes = [
    ('GET', '/', get_login_page, 'login_page'),
    ('POST', '/login', login, 'login'),

    ('GET', '/create_user', get_create_user_page, 'create_user_page'),

    ('POST', '/api/create_user', create_user, 'create_user'),
    ('POST', '/api/check_token', check_token, 'check_token'),
    ('POST', '/api/change_password', change_password, 'change_password'),
]
