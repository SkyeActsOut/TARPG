# https://www.redblobgames.com/maps/terrain-from-noise/
import numpy as np
from opensimplex import OpenSimplex
import random

seed = 200

gen = OpenSimplex()

height = 500
width = 500

def noise(nx, ny):
    return gen.noise2d(nx, ny) / 2.0 + 0.5

values = []
for y in range(height):
    values.append([0] * width)
    for x in range(width):
        nx = x/width - 0.5
        ny = y/height - 0.5
        values[y][x] = noise(nx, ny)

values = np.array(values)

variants = []
for y in range(height):
    carry = 0
    variants.append([0] * width)
    for x in range(width):
        variants[y][x] = random.randint(0, 100) + carry
        if (variants[y][x] > 95):
            carry += 3
        else:
            carry -= 2
        if (carry < 0):
            carry = 0

variants = np.array(variants)

start = (random.randrange(0, width), random.randrange(0, height))