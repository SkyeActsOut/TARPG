# https://www.redblobgames.com/maps/terrain-from-noise/
import numpy as np
from opensimplex import OpenSimplex
import random

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from enum import Enum

from tile import MapTile, Tile

from prefabs import house

seed = 125

generators = []
gen_i = 2
for x in range(0, gen_i):
    generators.append (OpenSimplex(seed=seed + x*2000))

HEIGHT = 325
WIDTH = 325
# Turns it into a tile array
tiles = np.empty((WIDTH, HEIGHT), dtype=Tile)
AREA = HEIGHT * WIDTH

total = HEIGHT + WIDTH

def noise(gen, nx, ny):
    return gen.noise2d(nx, ny) / 2.0 + 0.5

# THE MAIN WORLD-GEN ALGORITHM
values = np.empty((HEIGHT, WIDTH))
for y in range(HEIGHT):
    for x in range(WIDTH):
        nx = x/(WIDTH*0.1125) - 0.5
        ny = y/(HEIGHT*0.1125) - 0.5
        values[y][x] = noise(generators[0], nx, ny)
    print (f"{y * 100 / HEIGHT}% DONE!")


variants = []
for y in range(HEIGHT):
    carry = 0
    variants.append([0] * WIDTH)
    for x in range(WIDTH):
        variants[y][x] = random.randint(0, 100) + carry
        if (variants[y][x] > 95):
            carry += 3
        else:
            carry -= 2
        if (carry < 0):
            carry = 0

variants = np.array(variants)

def gen_town (tlx, tly, width, height):
    buildings = []
    # total_area = width * height
    buildings.append(house)
    buildings.append(house)

    for b in buildings:
        j = 0
        # Checks to see if the building would be out of bounds
        if (tlx + b.width >= WIDTH or
            tly + b.height >= HEIGHT):
                continue
        for tl in b.get_tiles():
            i = 0
            for t in tl:
                tiles[tlx + j][tly + i] = Tile(t, b.get_color(t))
                i+=1
            j+=1

        # Spaces out each building
        tlx += b.width + 5
        if (tlx > width):
            tly = b.height + 4
            if (tly > height):
                return

towns = []
for y in range(HEIGHT):
    towns.append([0] * WIDTH)
    for x in range(WIDTH):
        if (values[y][x] > 0.35 and values[y][x] < 0.55):
            if (random.randint(0, int(AREA/5)) == 0):
                gen_town (y, x, 65, 65) 


for y in range(HEIGHT):
    for x in range(WIDTH):
        if (not isinstance(tiles[y][x], Tile)):
            tiles[y][x] = MapTile(values[y][x], variants[y][x])
    print (f"{y * 100 / HEIGHT}% DONE!")

# Calculates the cost values for A* pathfinding
cost_values = []
for y in range(HEIGHT):
    cost_values.append([0] * WIDTH)
    for x in range(WIDTH):
        if (values[y][x] < 0.3125):
            cost_values[y][x] = False
        elif (values[y][x] < 0.75):
            cost_values[y][x] = True
        elif (values[y][x] < 1):
            cost_values[y][x] = False
        # else:
            # cost_values[y][x] = variants[y][x]*0.01 + values[y][x]*2
cost_values = np.array(cost_values, dtype=bool)

print (cost_values)

def gen_start ():
    start = (random.randrange(75, WIDTH-75), random.randrange(75, HEIGHT-75))

    for i in range (-1, 1):
        for j in range (-1, 1):
            if (cost_values[start[1] + i][start[0] + j]):
                return gen_start()
    return start

start = gen_start()