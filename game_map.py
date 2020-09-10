# https://www.redblobgames.com/maps/terrain-from-noise/
import numpy as np
from opensimplex import OpenSimplex
import random

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


seed = 125

generators = []
gen_i = 2
for x in range(0, gen_i):
    generators.append (OpenSimplex(seed=seed))

vals = []
for x in range(0, gen_i):
    generators.append (OpenSimplex())

height = 1000
width = 1000

total = height + width

def noise(gen, nx, ny):
    return gen.noise2d(nx, ny) / 2.0 + 0.5

# values_list = []
# for v in range(0, gen_i):
#     values = []
#     for y in range(height):
#         values.append([0] * width)
#         for x in range(width):
#             nx = x/325 - 0.625
#             ny = y/325 - 0.625
#             values[y][x] = noise(generators[v], nx, ny)
#     values_list.append (values)

# values = []
# for y in range(height):
#     values.append([0] * width)
#     for x in range(width):
#         for v in range(0, gen_i):
#             values[y][x] += values_list[v][y][x]
#         values[y][x] /= gen_i * 0.95

values = []
for y in range(height):
    values.append([0] * width)
    for x in range(width):
        nx = x/(width*0.1125) - 0.5
        ny = y/(height*0.1125) - 0.5
        values[y][x] = noise(generators[0], nx, ny)
    print (f"{y * 100 / height}% DONE!")

values = np.array(values)

plt.imshow(values)
plt.show()

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