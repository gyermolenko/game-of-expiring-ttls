"""Run once per session to initialize map with players.
Map dimensions:    512x512
Number of players: 20,000 (20K) (distributed randomly)

Origin (0x0) is top left.
"""

import aioredis

from game import db
from game import settings
from game.utils import generate_players_coords


async def main():
    conn = await aioredis.create_redis((
        settings.REDIS_HOST,
        settings.REDIS_PORT
    ), encoding='utf-8')

    coords = generate_players_coords(settings.NPLAYERS)
    player_tpl = '{}x{}'
    coords_as_str = [player_tpl.format(*tpl) for tpl in coords]

    val = await db.reset_players(conn)
    val = await db.read_players(conn)
    val = await db.save_players(conn, coords_as_str)
    val = await db.read_players(conn)


if __name__ == '__main__':
    import asyncio
    import uvloop
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    asyncio.run(main())
