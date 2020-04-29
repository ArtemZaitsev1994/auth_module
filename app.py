import aiohttp_jinja2
import jinja2
from aiohttp import web

from routes import routes
from settings import PORT, setup_app
from _mongo import mongo_setup
from auth.middlewares import check_token


app = web.Application(middlewares=[check_token])

# add some urls
for route in routes:
    app.router.add_route(*route[:3], name=route[3])
aiohttp_jinja2.setup(app, loader=jinja2.FileSystemLoader('templates'))

app.router.add_static('/static', 'static', name='static')
app['static_root_url'] = '/static'

# инициализация redis, также сессии хранятся в редис
mongo_setup(app)

# установка конфигов
setup_app(app)

# запуск приложения
if __name__ == '__main__':
    web.run_app(app, port=PORT)
