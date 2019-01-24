import random
from itertools import chain

from game import settings
import logging


async def flush(conn):
    val = await conn.flushdb()
    logging.debug(f"flush: {val}")
    return val

async def read_players(conn):
    val = await conn.zrange(settings.PLAYERS_BY_X)
    logging.debug(f"read_players: qty {len(val)} {val}")
    return val


async def save_players(conn, coords):
    xscore_member = [(tpl[0], f"{tpl[0]}x{tpl[1]}") for tpl in coords]
    yscore_member = [(tpl[1], f"{tpl[0]}x{tpl[1]}") for tpl in coords]
    val = await conn.zadd(settings.PLAYERS_BY_X, *chain(*xscore_member))
    logging.info(f"PLAYERS_BY_X: {val}")
    val = await conn.zadd(settings.PLAYERS_BY_Y, *chain(*yscore_member))
    logging.info(f"PLAYERS_BY_Y: {val}")


async def create_task(conn, player_id):
    # todo: remove expired tasks from task_list

    ttl = random.randrange(10, 10 * 60)

    # tasks_list = f"tasks:{player_id}"
    tasks_list = settings.TASKS_LIST_TPL.format(player_id)
    ln = await conn.llen(tasks_list)
    if 0 <= ln < 4:
        idx = ln + 1
        task_name = f"{player_id}:t{idx}"

        await conn.psetex(task_name, ttl * 1000, "_")
        # logging.debug(f"create_task: `{task_name}`, ttl: {ttl}s")

        await conn.rpush(tasks_list, task_name)
        # logging.debug(f"append task `{task_name}` to `{tasks_list}`")

        return

    logging.debug(f"skip task creation. `{tasks_list}` is full")
