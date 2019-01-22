import asyncio
import logging

import aioredis
import uvloop
from aiohttp import web

from game.settings import REDIS_HOST, REDIS_PORT
from game.webserver.routes import setup_routes


async def setup_redis(app):
    pool = await aioredis.create_redis_pool((
        REDIS_HOST,
        REDIS_PORT
    ), encoding='utf-8')

    async def close_redis(app):
        pool.close()
        await pool.wait_closed()

    app.on_cleanup.append(close_redis)
    app['redis_pool'] = pool
    return pool


async def init_app():
    app = web.Application()
    setup_routes(app)
    await setup_redis(app)
    return app


def main():
    logging.basicConfig(level=logging.DEBUG)
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    app = init_app()
    web.run_app(app)


if __name__ == '__main__':
    main()
