import asyncio
import logging

import aioredis
from game import settings
from game.scheduler import db


class Redis:

    @classmethod
    async def connect(cls):
        self = cls()

        self.conn = await aioredis.create_redis_pool((
            settings.REDIS_HOST,
            settings.REDIS_PORT
        ), encoding='utf-8')

        self.subs_conn = await aioredis.create_redis((
            settings.REDIS_HOST,
            settings.REDIS_PORT
        ), encoding='utf-8')

        return self


    async def periodically_create_tasks(self):
        players = await db.read_players(self.conn)
        while True:
            logging.info('-' * 80)
            logging.info("Task creation round")
            logging.info('-' * 80)
            await self.create_one_task_for_each_player(players)
            await asyncio.sleep(settings.GENERATE_TASKS_EVERY_X_SECONDS)

    async def create_one_task_for_each_player(self, players):
        futs = [db.create_task(self.conn, pid) for pid in players]
        await asyncio.gather(*futs)


    async def remove_expired_tasks(self, channel):

        while await channel.wait_message():
            msg = await channel.get()
            expired_key = msg[1].decode()
            logging.debug(f"expired key: {expired_key}")

            player_id = expired_key.split(':')[0]
            pid_tasks = settings.TASKS_LIST_TPL.format(player_id)
            await self.conn.lrem(pid_tasks, 0, expired_key)
            logging.debug(f"lrem {expired_key} from {pid_tasks}")


    async def channel_for_expirations(self):
        channels = await self.subs_conn.psubscribe("__key*__:*")
        logging.info(f"channels {channels}")
        channel = channels[0]
        return channel


    async def subscribe_for_channel(self):

        await self.subs_conn.config_set("notify-keyspace-events", "Ex")
        logging.info(f"config_set `notify-keyspace-events`=`Ex`")

        channel = await self.channel_for_expirations()
        return channel
