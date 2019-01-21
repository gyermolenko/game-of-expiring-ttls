import asyncio
import logging

import aioredis

from settings import NPLAYERS
from settings import REDIS_HOST, REDIS_PORT
from utils import generate_players_coords


PLAYERS = 'players'


async def save_players(conn, coords):
    val = await conn.sadd(PLAYERS, *coords)
    return val


async def reset_players(conn):
    val = await conn.delete(PLAYERS)
    return val


async def read_players(conn):
    val = await conn.smembers(PLAYERS)
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
    logging.debug(f"reset_players val: {val}")

    val = await read_players(conn)
    logging.debug(f"players before: {val}")

    val = await save_players(conn, coords_as_str)
    logging.debug(f"N new players' coords: {val}")

    val = await read_players(conn)
    logging.debug(f"players after: {val}")


if __name__ == '__main__':
    asyncio.run(main())
