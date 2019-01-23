import asyncio
import logging
import time
from itertools import chain

from game import settings


async def find_players_in_view(conn, x=0, y=0):
    xe = x + settings.WINDOW_WIDTH
    ye = y + settings.WINDOW_WIDTH

    view = f"view:{x}-{xe}:{y}-{ye}"
    logging.debug(f"view: {view}")

    if not (await conn.exists(view)):
        logging.info(f"creating view: {view}")

        by_x = await conn.zrangebyscore(settings.PLAYERS_BY_X, x, xe)
        logging.debug(f"by_x: {by_x}")
        by_y = await conn.zrangebyscore(settings.PLAYERS_BY_Y, y, ye)
        logging.debug(f"by_y: {by_y}")

        intersection = sorted(set(by_x).intersection(by_y))
        logging.debug(f"intersection: {intersection}")
        if intersection:
            val = await conn.rpush(view, *intersection)
            logging.debug(f"stored in view: {val}")

    players = await conn.lrange(view, 0, -1)
    logging.debug(f"players: {players}")

    return players


async def find_tasks(conn, players):

    async def get_player_tasks(pid):
        # t0 = time.time()

        match = f"{pid}:t*"
        pid_tasks = [key async for key in conn.iscan(match=match, count=10_000)]
        logging.debug(f"pid_tasks: {pid} {pid_tasks}")

        # logging.info(f"--TIME-- get_player_tasks: {time.time() - t0}")
        return pid_tasks

    futs = [get_player_tasks(pid) for pid in players]
    lists_of_tasks = await asyncio.gather(*futs)

    tasks = list(chain(*lists_of_tasks))
    logging.debug(f"tasks: {tasks}")
    return tasks


async def append_ttls(conn, tasks):
    # todo: blocking loop
    pairs = []
    for t in tasks:
        ttl = await conn.ttl(t)
        pairs.append((t, ttl))
    return pairs

async def read_tasks_from_nearby_players(conn, x=0, y=0):
    # todo: x,y are not top-left but rather center where player with view is

    players = await find_players_in_view(conn, x=0, y=0)

    tasks = await find_tasks(conn, players)  # todo: too slow

    pairs = await append_ttls(conn, tasks)

    return pairs
