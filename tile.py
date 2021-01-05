import libtcodpy as tcod

class Tile():
    def __init__(self, t=' ', c=(255, 255, 255), rl_capable=False):
        self.rl_capable = rl_capable
        self.reload = False
        self.char = t
        self.color = c

        self.in_vision = True

class NullTile(Tile):
    def __init__(self):
        super().__init__('#', (1, 1, 1))

class BorderTile(Tile):
    def __init__(self):
        super().__init__('#', (55, 55, 55))

        self.reload = False
        self.rl_capable = True

class MapTile(Tile):
    def __init__(self, val, variant):
        super().__init__('#', (55, 55, 55))
        tmp = self.GetTile(val, variant)
        self.char = tmp[0]
        self.color = tmp[1]

    def GetTile (self, value, variant):

        tile = ' '
        color = (0, 0, 0)

        if (value == 0):
            return (' ', (0, 0, 0))
        # WATER
        elif (value < 0.3):
            # COLORS
            if (value < 0.15):
                color = (20, 20, 80)
            elif (value < 0.2):
                color = (20, 20, 100)
            elif (value < 0.235):
                color = (20, 20, 170)
            elif (value < 0.2625):
                color = (20, 20, 220)
            elif (value < 0.3):
                color = (20, 20, 255)
            # VARIANTS
            if (variant < 72):
                tile = '~'
            elif (variant < 90):
                tile = '-'
            elif (variant < 97):
                tile = '^'
            elif (variant < 101):
                tile = '='
            else:
                tile = '~'
        # BEACH
        elif (value < 0.325):
            # COLORS
            if (value < 0.3125):
                color = (178, 162, 100)
            elif (value < 0.3175):
                color = (184, 170, 112)
            elif (value < 0.325):
                color = (194, 178, 128)
            # VARIANTS
            if (variant < 80):
                tile = '#'
            elif (variant < 100):
                tile = '^'
            else:
                tile = '#'
        # GRASS
        elif (value < 0.75):
            g_val = int(255 * value * (10/7))
            if (g_val <= 50):
                g_val = 55
            elif (g_val <= 85):
                g_val = 85
            elif (g_val <= 135):
                g_val = 135
            elif (g_val <= 185):
                g_val = 185
            elif (g_val <= 215):
                g_val = 215
            elif (g_val <= 255):
                g_val = 225
            color = (20, g_val, 20)

            tile = '#'
            if (variant < 70):
                tile = '#'
            elif (variant < 95):
                color = (16, 59, 29)
                tile = '%'
            elif (variant < 101):
                color = (30, 80, 50)
                tile = '!'
        #VALLEY
        # elif (value < 0.7375):
        #     color = (20, 50, 20)
        #     tile = '#'
        # MOUNTAIN
        elif (value < 1):
            if (value < 0.75 and variant < 50):
                tile = '.'
            if (value < 0.7525):
                color = (133, 138, 133)
            elif (value < 0.775):
                color = (166, 172, 166)
            elif (value < 1):
                color = (220, 250, 215)
            tile = '^'
        # if (biome_tile == 0):
        #     return (tile, color)
        return (tile, color)