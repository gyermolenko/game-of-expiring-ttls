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
    logging.debug(f"PLAYERS_BY_X: {val}")
    val = await conn.zadd(settings.PLAYERS_BY_Y, *chain(*yscore_member))
    logging.debug(f"PLAYERS_BY_Y: {val}")


async def create_task(conn, player_id, ttl):
    # todo: t1 only
    key = f"{player_id}:t1"
    val = await conn.psetex(key, ttl*1000, "_")
    logging.debug(f"create_task: `{key}`, ttl: {ttl}s")
    return val
