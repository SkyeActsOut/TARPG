SCREEN_HEIGHT = 54
from tile import Tile

from numpy import empty

class Menu:
    def __init__(self):
        self.height = 0
        self.width = 0

        self.x = 0
        self.y = 0

        self.menu_text = []
    
    # Gets the character in the menu or a blank tile if there is none
    def get_char (self, x, y):

        # the relative x? y? coordinates in the menu
        rel_x = x - self.x 
        rel_y = y - self.y

        if (self.menu_text[rel_y][rel_x] != '|'):
            return Tile(self.menu_text[rel_y][rel_x])
        else:
            return Tile('#', (22, 22, 22))
    
    def init_lines (self):
        self.menu_text = empty((self.height, self.width), dtype=str)

        for i in range (self.height):
            for j in range (self.width):
                self.menu_text[i, j] = '|' # | is a stop string, meaning do not do anything to that tile

    # Adds a line to the menu text
    def add_line(self, y, x, text):
        for i in range(len(text)):
            self.menu_text[y][i+x] = text[i]
            if (i > self.width + x):
                pass
                # WRAP AROUND

    def replace_chr (self, x, y, c):
        self.menu_text[y][x] = c
        
# Logs menu
class LogsMenu (Menu):
    def __init__(self):
        super().__init__()
        
        self.height = 11
        self.width = 50

        self.x = 15
        self.y = SCREEN_HEIGHT - self.height - 1

        self.logs = ""

        self.init_lines()

        self.add_line(0, 1, "UWU!")
        self.add_line(1, 1, "S-senpai~!")
        self.add_line(2, 1, "P-pwease notice me!!!!")
        self.add_line(3, 1, "S.. senpai...")

# The top left info menu for static info
class StaticInfo (Menu):
    def __init__(self):
        super().__init__()

        self.height = 8
        self.width = 25

        self.x = 0
        self.y = 0

        self.init_lines()

        self.add_line(0, 0, "PLAYER")
        self.add_line(1, 1, "POS:")
        self.add_line(1, 17, "000x000")
    
class StaticMenu (Menu):
    def __init__(self, x, y, w, h):
        super().__init__()
        self.height = w
        self.width = h

        self.x = x
        self.y = y

        self.init_lines()