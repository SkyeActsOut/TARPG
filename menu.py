SCREEN_HEIGHT = 54
from tile import Tile
import libtcodpy as tcod
from numpy import empty

# Checks to see if the x,y coords are on a specific menu
def isOnIMenu(x, y, i, menues):
    for m in menues:
        if m == i:
            if (y <= m.height + m.y and 
                y >= m.y-1 and
                x <= m.width + m.x and
                x >= m.x-1):
                return True
    else:
        return False

# Checks to see if the x,y coords are on any menu
def isOnMenu(x, y, menues):
    for m in menues:
        if (y < m.height + m.y and 
            y >= m.y and
            x < m.width + m.x and
            x >= m.x):
                return True
    else:
        return False

# Checks to see if there xis an existing tile with a character in that menu
def isTileInMenu (x, y, menues):
    for m in menues:
        if (isOnIMenu(x, y, m, menues)):
            t = m.get_char(x, y)
            if (t):
                return t
    else:
        return False

class Menu:
    def __init__(self):
        self.height = 0
        self.width = 0

        self.x = 0
        self.y = 0

        self.menu_text = []
        self.menu_accents = []

        self.bg_color = (33, 33, 33)
    
    # Gets the character in the menu or a blank tile if there is none
    def get_char (self, x, y):

        # the relative x? y? coordinates in the menu
        rel_x = x - self.x 
        rel_y = y - self.y

        if (self.menu_text[rel_y][rel_x] != '|'):
            return Tile(self.menu_text[rel_y][rel_x], (self.menu_accents[rel_y, rel_x]))
        else:
            # if (isinstance(self, StaticMenu)):
            return Tile('#', self.bg_color)
            # else:
                # return Tile('#', (22, 22, 22))
    
    def add_char (self, x, y, char):
        rel_x = x - self.x 
        rel_y = y - self.y

        self.menu_text[rel_y][rel_x] = char
    
    def init_lines (self):
        self.menu_text = empty((self.height, self.width), dtype=str)
        self.menu_accents = empty((self.height, self.width), dtype=tuple)

        for i in range (self.height):
            for j in range (self.width):
                self.menu_text[i, j] = '|' # | is a stop string, meaning do not do anything to that tile

        for i in range (self.height):
            for j in range (self.width):
                self.menu_accents[i, j] = (255, 255, 255) # | is a stop string, meaning do not do anything to that tile
    
    def set_accent (self, x, y, col):
        self.menu_accents[y, x] = col

    # Adds a line to the menu text
    def add_line(self, y, x, text, col=(255, 255, 255)):
        for i in range(len(text)):
            self.menu_text[y][i+x] = text[i]
            self.menu_accents[y][i+x] = col
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
        self.width = 66

        self.x = 15
        self.y = SCREEN_HEIGHT - self.height - 1

        self.logs = ""

        self.init_lines()

        self.add_line(1, 1, "Hello!")
        self.add_line(2, 1, "This is the first log!")
        self.add_line(3, 1, "It's added manually and entirely for testing")
        # self.add_line(1, 1, "S-senpai~!")
        # self.add_line(2, 1, "P-pwease notice me!!!!")
        # self.add_line(3, 1, "S.. senpai...")

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

class CircleBar ():
    def __init__ (self, radius, x, y, color, bg_color):
            
        self.radius = radius
        self.center_x = x
        self.center_y = y
        self.pnt_count = self.getAllPoints(radius)
        self.color = color
        self.bg_color = bg_color

    def isInCircle(self, player, covered, x, y, health_mana):    

        if ((self.center_x - x)**2 + (self.center_y - y)**2 < self.radius**2):
            ratio = 0
            if (health_mana):
                ratio = player.getHealth() / player.getMaxHealth()
            else:
                ratio = player.getMana() / player.getMaxMana()
            if (self.pnt_count - covered <= self.pnt_count  * ratio):
                return 1
            else:
                return 0
        return -1

    def getAllPoints (self, radius):
        dia = radius*2
        cnt = 0
        # sq = dia * dia
        for i in range (dia):
            for j in range (dia):
                if (i**2 + j**2 > radius**2):
                    cnt+=1
        return cnt

class MapEditMenu (Menu):
    def __init__(self):
        super().__init__()

        self.height = 10
        self.width = 96

        self.x = 0
        self.y = 0

        self.bg_color = (58, 58, 58)

        self.init_lines()

        text = "MAP CREATOR"
        self.add_line(1, int(self.width/2 - len(text)/2), text)
        text = "CURR KEYS AVAIL"
        self.add_line(1, self.width - len(text) - 1, text)
        text = "# !"
        self.add_line(3, self.width - len(text) - 1, text)