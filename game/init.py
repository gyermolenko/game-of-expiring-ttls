"""Run once per session to initialize map with players.
Map dimensions:    512x512
Number of players: 20,000 (20K) (distributed randomly)

Origin (0x0) is top left.
"""

import asyncio
import logging

import aioredis

from game.settings import NPLAYERS
from game.settings import REDIS_HOST, REDIS_PORT
from game.settings import PLAYERS
from game.utils import generate_players_coords


async def save_players(conn, coords):
    val = await conn.sadd(PLAYERS, *coords)
    logging.debug(f"save_players: {val}")
    return val


async def reset_players(conn):
    val = await conn.delete(PLAYERS)
    logging.debug(f"reset_players: {val}")
    return val


async def read_players(conn):
    val = await conn.smembers(PLAYERS)
    logging.debug(f"read_players: {val}")
    return val


async def main():
    conn = await aioredis.create_redis((
        REDIS_HOST,
        REDIS_PORT
    ))

    coords = generate_players_coords(NPLAYERS)
    player_tpl = '{}x{}'
    coords_as_str = [player_tpl.format(*tpl) for tpl in coords]

    val = await reset_players(conn)
    val = await read_players(conn)
    val = await save_players(conn, coords_as_str)
    val = await read_players(conn)


if __name__ == '__main__':
    asyncio.run(main())
