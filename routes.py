from auth.view import login, get_login_page


routes = [
    ('POST', '/login', login, 'login'),
    ('*', '/', get_login_page, 'login_page'),
]
