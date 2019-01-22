import logging

from game import settings


async def save_players(conn, coords):
    val = await conn.sadd(settings.PLAYERS, *coords)
    logging.debug(f"save_players: {val}")
    return val


async def reset_players(conn):
    val = await conn.delete(settings.PLAYERS)
    logging.debug(f"reset_players: {val}")
    return val


async def read_players(conn):
    val = await conn.smembers(settings.PLAYERS)
    logging.debug(f"read_players: {val}")
    return val


async def create_task(conn, player_id, ttl):
    key = f"{player_id}:t2"
    val = await conn.psetex(key, ttl*1000, "_")
    logging.debug(f"create_task with key `{key}` ttl `{ttl}`s: {val}")
    return val


async def read_tasks_by_mask(conn, x, y):
    match = f"[0-{x}]x[0-{y}]:t2"
    tasks = [key async for key in conn.iscan(match=match)]
    # logging.debug(f"read_tasks_by_mask: {tasks}")

    pairs = []
    for t in tasks:
        ttl = await conn.pttl(t)
        pairs.append((t, ttl))

    return pairs
