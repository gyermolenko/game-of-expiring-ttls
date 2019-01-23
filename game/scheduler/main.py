"""Run when players are present (so after init).
Otherwise it waits for players to be created.

For each player start generating new tasks following such rules:
 - each player has up to 4 tasks
 - each task is a timer between 10s and 10m
 - each of the players will start task(s) on the server with a random frequency
 - if the maximum number of tasks was reached - wait until all player's tasks are finished to start a new one
 """

import logging

import aioredis

from game import settings
from game.scheduler import db
from game.scheduler.init import main as initer

logging.basicConfig(level=settings.LOGGING_LEVEL)

SLEEP_FOR = 5

async def main():
    conn = await aioredis.create_redis((
        settings.REDIS_HOST,
        settings.REDIS_PORT
    ), encoding='utf-8')

    players = await db.read_players(conn)

    while True:
        futs = [db.create_task(conn, pid) for pid in players]
        await asyncio.gather(*futs)
        logging.info('-'*80)
        await asyncio.sleep(SLEEP_FOR)

if __name__ == '__main__':
    import asyncio
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(initer())
    asyncio.run(main())
