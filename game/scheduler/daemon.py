"""Run when players are present (so after init).
Otherwise it waits for players to be created.

For each player start generating new tasks following such rules:
 - each player has up to 4 tasks
 - each task is a timer between 10s and 10m
 - each of the players will start task(s) on the server with a random frequency
 - if the maximum number of tasks was reached - wait until all player's tasks are finished to start a new one
 """

import logging
import random

import aioredis

from game import settings
from game.scheduler import db
from game.scheduler.init import main as initer

logging.basicConfig(level=logging.DEBUG)

SLEEP_FOR = 60

async def main():
    conn = await aioredis.create_redis((
        settings.REDIS_HOST,
        settings.REDIS_PORT
    ), encoding='utf-8')

    players = await db.read_players(conn)

    # while True:
    for p in players:
        ttl = random.randrange(10, 10*60)
        await db.create_task(conn, p, ttl)
        # logging.debug('-'*80)
        # await asyncio.sleep(SLEEP_FOR)

if __name__ == '__main__':
    import asyncio
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    asyncio.run(initer())
    asyncio.run(main())
