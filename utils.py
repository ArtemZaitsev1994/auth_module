import aioredis
from aiohttp.web import Application

from settings import REDIS_HOST, ADMIN_LOGIN, ADMIN_PASSWORD


async def make_redis_pool():
    redis_address = REDIS_HOST
    return await aioredis.create_pool(
        redis_address,
        create_connection_timeout=1,
    )


async def create_redis(app: Application):
    app['redis'] = await aioredis.create_redis(REDIS_HOST)
    app['redis'].decode_response = True


async def close_redis(app: Application):
    app['redis'].close()
    await app['redis'].wait_closed()


async def _check_admin(app: Application):
    if isinstance(ADMIN_LOGIN, str):
        if not await app['models']['admin'].get_admin(ADMIN_LOGIN):
            await app['models']['admin'].create_admin(ADMIN_LOGIN, ADMIN_PASSWORD)
