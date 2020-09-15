# https://www.redblobgames.com/maps/terrain-from-noise/
import numpy as np
from opensimplex import OpenSimplex
import random

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

from enum import Enum

seed = 125

generators = []
gen_i = 2
for x in range(0, gen_i):
    generators.append (OpenSimplex(seed=seed + x*2000))

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

# plt.imshow(values)
# plt.show()

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

biomes = []

# class Biome (Enum):
#     desert = 1

def biome_gen_two ():
    for y in range(height):
        biomes.append([0] * width)
        for x in range(width):
            nx = x/(width*0.1125) - 0.375
            ny = y/(height*0.1125) - 0.375
            biomes[y][x] = noise(generators[1], nx, ny)
            # Check to see if the base value is a plains biome
            if (not values[y][x] > 0.3 and not values[y][x] < 0.7):
                biomes[y][x] = 0
            # Check to see if the base value is in the plains biome
            if (not values[y][x] > 0.35 and not values[y][x] < 0.75):
                biomes[y][x] = 0
        print (f"{y * 100 / height}% DONE!")

def biome_gen_one():
    chunk_size = 9
    desert = [1, False]
    desert_cap = int(width*height / 3) # THE NUMBER DETERMINES APPROX HOW MANY DESERTS PER MAP

    for i in range(height):   
        biomes.append([0] * width)

    for j in range(int(height/chunk_size)):
        
        for i in range(int(width/chunk_size)):

            for k in range(0, chunk_size):

                for l in range(0, chunk_size):

                    y = j * k
                    x = i * l

                    # print ((y, x))

                    # GENERATES DESERTS
                    if (values[y][x] > 0.325 and (values[y][x] < 0.7)):
                        rng = random.randint(0, desert_cap)
                        if (rng <= desert[0] and not desert[1]): # Checks to place the initial desert tile
                            desert[0] = desert_cap*1.125
                            desert[1] = True
                            biomes[y][x] = 1
                        elif (rng <= desert[0] and desert[1]): # Over-time decreases the value of desert[0] until it randomly stops the generation of the biome
                            desert[0] -= 5
                            biomes[y][x] = 1
                        else: # Checks to see if the desert generation should be stopped
                            desert[0] = 1
                            desert[1] = False


biome_gen_two()
biomes = np.array(biomes)
        
print (biomes)

plt.imshow(biomes)
plt.show()
            

        # biomes[y][x] = random.randint(0, 100)


start = (random.randrange(75, width-75), random.randrange(75, height-75))