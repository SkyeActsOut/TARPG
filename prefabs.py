class Prefab():
    def __init__(self, tiles, colors):
        
        # Turns the text prefab into a matrix
        self.tiles = []
        self.height = 0
        self.width = 0
        for line in tiles:
            split_line = line.split(' ')
            self.tiles.append ([0]*len(split_line))
            self.width = 0
            for t in split_line:
                self.tiles[self.height][self.width] = t
                self.width+=1
            self.height+=1

        # Turns the color tuples into a dictionary
        self.colors = {}
        for c in colors:
            self.colors[c[0]] = c[1]

        self.area = self.height * self.width

    def get_tiles(self):
        return self.tiles

    def get_color (self, t):
        return self.colors[t]

house = Prefab( (
    "* - - - - - - - *",
    "| # # # # # | o |",
    "| # # h # # * - |",
    "| # h T # # # # |",
    "| # # # # # # # |",
    "| # # # # # # # |",
    "* - - # # - - - *"
), 
(
    ('#', (193,154,107)),
    ('-', (230,150,100)),
    ('|', (230,150,100)),
    ('*', (220,140,90)),
    ('h', (250,140,90)),
    ('T', (240,140,90)),
    ('o', (180,140,90)),
))