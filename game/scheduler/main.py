"""Run when players are present (so after init).
Otherwise it waits for players to be created.

For each player start generating new tasks following such rules:
 - each player has up to 4 tasks
 - each task is a timer between 10s and 10m
 - each of the players will start task(s) on the server with a random frequency
 - if the maximum number of tasks was reached - wait until all player's tasks are finished to start a new one
 """

import asyncio
import logging

import uvloop

from game import settings
from game.scheduler.init import main as initer
from game.scheduler.redis import Redis

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

logging.basicConfig(level=settings.LOGGING_LEVEL)


async def daemon():
    redis = await Redis.connect()

    task1 = redis.periodically_create_tasks()

    channel = await redis.subscribe_for_channel()
    task2 = redis.remove_expired_tasks(channel)

    await asyncio.gather(task1, task2)


def main():
    asyncio.run(initer())
    asyncio.run(daemon())


if __name__ == '__main__':
    main()
