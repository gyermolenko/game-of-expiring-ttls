import random
import logging
from game import settings


def generate_one_coords_pair(width, height):
    x = random.randrange(width)
    y = random.randrange(height)
    # logging.debug(f'pair: {(x, y)}')
    return x, y

def generate_players_coords(n):
    coords = []
    while len(coords) < n:
        pair = generate_one_coords_pair(settings.WIDTH, settings.HEIGHT)
        if pair not in coords:
            coords.append(pair)

    logging.debug(f'coords: {coords}')
    return coords


if __name__ == '__main__':
    coords = generate_players_coords(settings.NPLAYERS)
