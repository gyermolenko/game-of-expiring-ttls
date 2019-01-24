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


async def channel_for_expirations(conn):
    channels = await conn.psubscribe("__key*__:*")
    logging.info(f"channels {channels}")
    channel = channels[0]
    return channel


async def remove_expired_tasks(normal_conn):

    subs_conn = await aioredis.create_redis((
        settings.REDIS_HOST,
        settings.REDIS_PORT
    ), encoding='utf-8')
    await subs_conn.config_set("notify-keyspace-events", "Ex")
    logging.info(f"config_set `notify-keyspace-events`=`Ex`")

    channel = await channel_for_expirations(subs_conn)

    while await channel.wait_message():
        msg = await channel.get()
        expired_key = msg[1].decode()
        logging.debug(f"expired key: {expired_key}")

        player_id = expired_key.split(':')[0]
        # tasks_list_name = f"tasks:{player_id}"
        pid_tasks = settings.TASKS_LIST_TPL.format(player_id)
        await normal_conn.lrem(pid_tasks, 0, expired_key)
        logging.debug(f"lrem {expired_key} from {pid_tasks}")


async def create_one_task_for_each_player(conn, players):
    futs = [db.create_task(conn, pid) for pid in players]
    await asyncio.gather(*futs)


async def periodically_create_tasks(conn):
    players = await db.read_players(conn)
    while True:
        logging.info('-'*80)
        logging.info("Task creation round")
        logging.info('-'*80)
        await create_one_task_for_each_player(conn, players)
        await asyncio.sleep(settings.GENERATE_TASKS_EVERY_X_SECONDS)


async def main():
    normal_conn = await aioredis.create_redis((
        settings.REDIS_HOST,
        settings.REDIS_PORT
    ), encoding='utf-8')

    task1 = periodically_create_tasks(normal_conn)
    task2 = remove_expired_tasks(normal_conn)
    await asyncio.gather(task1, task2)


if __name__ == '__main__':
    import asyncio
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(initer())
    asyncio.run(main())
