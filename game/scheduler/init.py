"""Run once per session to initialize map with players.
Map dimensions:    512x512
Number of players: 20,000 (20K) (distributed randomly)

Origin (0x0) is top left.
"""

import aioredis

from game import settings
from game.scheduler import db
from game.scheduler.utils import generate_players_coords


# def zfill_with_zeros(coords):
#     player_tpl = "{}x{}"
#     coords_as_str = []
#     for tpl in coords:
#         x = str(tpl[0]).zfill(3)
#         y = str(tpl[1]).zfill(3)
#         coords_as_str.append(player_tpl.format(x, y))
#     return coords_as_str

async def main():
    conn = await aioredis.create_redis((
        settings.REDIS_HOST,
        settings.REDIS_PORT
    ), encoding='utf-8')

    coords = generate_players_coords(settings.NPLAYERS)
    # coords_as_str = zfill_with_zeros(coords)

    val = await db.flush(conn)
    val = await db.save_players(conn, coords)


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
