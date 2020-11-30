import libtcodpy as tcod
import numpy as np
from game_map import tiles, start, WIDTH, HEIGHT
from tile import Tile, NullTile, BorderTile, MapTile
from menu import LogsMenu, StaticInfo, StaticMenu
import random
from threading import Thread
from time import sleep
from entities import Player

# ######################################################################
# Global Game Settings
# ######################################################################
# Windows Controls
FULLSCREEN = False
SCREEN_WIDTH = 96  # characters wide
SCREEN_HEIGHT = 54  # characters tall
LIMIT_FPS = 60  # 20 frames-per-second maximum

exit_game = False

# Game Controls
map_pos = [start[0], start[1]]

chunk_size = 16

screen_values = []

chunk_ready = []

menues = [LogsMenu(), StaticInfo(), StaticMenu(1, SCREEN_HEIGHT-14, 13, 13)]

cooldown = 1/60

con = 0

p = Player()

def getAllPoints (radius):
    dia = radius*2
    cnt = 0
    # sq = dia * dia
    for i in range (dia):
        for j in range (dia):
            if (i**2 + j**2 > radius**2):
                cnt+=1
    return cnt
circle_r_five_points = getAllPoints(6)
print (circle_r_five_points)

def isHealthCircle(health_covered, x, y):
    circle_radius = 6
    circle_center_x = 7
    circle_center_y = SCREEN_HEIGHT - circle_radius - 2# Subtract more to move up/down
    
    if ((circle_center_x - x)**2 + (circle_center_y - y)**2 < circle_radius**2):
        num_of_points = circle_r_five_points
        health_ratio = p.getHealth() / p.getMaxHealth()
        # print (num_of_points - health_covered)
        # print (num_of_points * health_ratio)
        if (num_of_points - health_covered <= num_of_points * health_ratio):
            return 1
        else:
            return 0
    return -1

# Checks to see if the x,y coords are on any menu
def isOnMenu(x, y):
    for m in menues:
        if (y < m.height + m.y and 
            y >= m.y and
            x < m.width + m.x and
            x >= m.x):
                return True
    else:
        return False

# Checks to see if the x,y coords are on a specific menu
def isOnIMenu(x, y, i):
    for m in menues:
        if m == i:
            if (y <= m.height + m.y and 
                y >= m.y-1 and
                x <= m.width + m.x and
                x >= m.x-1):
                return True
    else:
        return False

def isOnBorder (x, y):
    for m in menues:
        if ( isOnIMenu (x, y, m) and 
            (y == m.y-1 or 
            y == m.height + m.y or
            x == m.width + m.x or
            x == m.x-1) and
            ( x != SCREEN_WIDTH or
            y-1 != SCREEN_HEIGHT)):
                return True
        # elif ( (y == m.y or 
        #     x == m.x) and
        #     ( x != 0 or
        #     y != 0)):
        #         return True
    else:
        return False

# Checks to see if there xis an existing tile with a character in that menu
def isTileInMenu (x, y):
    for m in menues:
        if (isOnIMenu(x, y, m)):
            t = m.get_char(x, y)
            if (t):
                return t
    else:
        return False

def setInfoPosition(x, y):
    px = "000"
    if (x < 10):
        px = f"00{x}"
    elif (x < 100):
        px = f"0{x}"
    else:
        px = x

    py = "000"
    if (y < 10):
        py = f"00{y}"
    elif (y < 100):
        py = f"0{y}"
    else:
        py = y

    ln = f"{px}x{py}"
    menues[1].add_line(1, 17, ln)

# Based on the game_map values, this gets a np array with the tiles ONLY around the player
def GetScreenValues():
    global screen_values
    screen_values = np.empty((SCREEN_WIDTH, SCREEN_HEIGHT), dtype=Tile)

    i = 0
    j = 0
    health_covered = 0
    for width in range(int(map_pos[0] - SCREEN_WIDTH/2), int(map_pos[0] + SCREEN_WIDTH/2)): # Loops through the values for what should be displayed on screen
        for height in range(int(map_pos[1] - SCREEN_HEIGHT/2), int(map_pos[1] + SCREEN_HEIGHT/2)): # loops through the height values for what should be displayed on screen

            # RENDER ORDER

            # THE HEALTH CIRCLE
            
            isHealth = isHealthCircle(health_covered, i, j)
            if (isHealth == 2):
                screen_values[i, j] = Tile('#', tcod.grey)
            elif (isHealth == 1):
                screen_values[i, j] = Tile('#', tcod.red)
                health_covered+=1
            elif (isHealth == 0):
                screen_values[i, j] = Tile('#', tcod.black)
                health_covered+=1

             # IS ON A MENU TILE
            elif (isOnMenu(i, j)):
                screen_values[i, j] = isTileInMenu(i, j)
            # IS ON THE BORDER OF A MNEU
            elif (isOnBorder(i, j)):
                screen_values[i, j] = BorderTile()

            elif (width < 0 or height < 0 or width >= WIDTH or height >= HEIGHT): # checks for stuff outside the map
                screen_values[i, j] = NullTile()
            elif (j < 0 or i < 0 or j >= SCREEN_WIDTH or i >= SCREEN_WIDTH): # checks for stuff outside the screen
                screen_values[i, j] = NullTile()
                
            # IS A NORMAL SCREEN TILE
            else:
                screen_values[i, j] = tiles[width][height]
            j+=1
        j=0
        i+=1

def DrawChunk (start_i, start_j):
    # while not tcod.console_is_window_closed() : 
        
        # if not AllChunksLoaded():

        # loops through all the tiles in screen_values and places them on screen
        for i in range(start_i, start_i + chunk_size):
            for j in range(start_j, start_j + chunk_size):
                if (i >= 96 or j >= 54):
                    continue
                if (i == player_x and j == player_y):
                    continue
                # (tile, color) = GetTile(screen_values[i, j], game_map.biomes[i, j], i, j)
                if (screen_values[i, j]):
                    set_tile (screen_values[i, j].char, screen_values[i, j].color, i, j)
                else:
                    set_tile ("#", tcod.black, i, j)

        # chunk_ready[chunk_i] = True

        # sleep(cooldown * 1.05)

        # else:
        #     for j in chunk_ready:
        #         chunk_ready[j] = False

# Checks to see if "all" chunks are loaded, meaning that if the majority of them are loaded, render them on screen
# def AllChunksLoaded():
#     i = 0
#     for chunk in chunk_ready:
#         if (chunk == True):
#             i += 1
#     print (i)
#     return i * 1.5 > len(chunk_ready)

def ThreadAllChunks ():
    while not tcod.console_is_window_closed() and not exit_game:
        # chunk_i = 0
        sleep(cooldown)
        for i in range (0, int(SCREEN_WIDTH/chunk_size)+1):
            for j in range (0, int(SCREEN_HEIGHT/chunk_size)+1):
                # chunk_ready.append(False)
                renderer = Thread(target=DrawChunk, args=(i*chunk_size, j*chunk_size))
                renderer.start()
                renderer.join()
                # chunk_i += 1

def SetScreenValues():
    screen_values = GetScreenValues()


def set_color (color, x, y):
    if (tcod.console_get_char_foreground (0, x, y) == tcod.Color(color[0], color[1], color[2])):
        return
    else:
        tcod.console_set_char_foreground(0, x, y, color)

def set_char (c, x, y):
    if (con.ch[y, x] == ord(c)):
        return
    else:
        con.ch[y, x] = ord(c)

def set_tile (c, color, x, y):
    # print ((c, color))
    con.ch[y, x] = ord (c)
    con.fg[y, x] = color

def set_bg (color, x, y):
    con.bg[y, x] = tcod.Color(color[0], color[1], color[2])


# ######################################################################
# User Input
# ######################################################################
 
 
def keyHandler(key):
    # if key.vk == tcod.KEY_ENTER and key.lalt:
    #     # Alt+Enter: toggle fullscreen
    #     tcod.console_set_fullscreen(not tcod.console_is_fullscreen())
 
     # movement keys
    if key == 119 : # W KEY
        map_pos[1] -= 1
 
    if key == 115 : # S KEY 
        map_pos[1] += 1
 
    if key == 97 : # A KEY
        map_pos[0] -= 1
 
    if key == 100 : # D KEY
        map_pos[0] += 1

    if (key == 119 or key == 115 or key == 97 or key == 100):
        # print (map_pos)
        setInfoPosition(map_pos[1], map_pos[0])
        GetScreenValues()
    
#############################################
# Main Game Loop
#############################################
 
 
def render_loop ():
    global player_x, player_y
    player_x = int (SCREEN_WIDTH / 2)
    player_y = int (SCREEN_HEIGHT / 2)

    ThreadAllChunks()

    # ValueLoop = Thread(target=GetScreenValues)
    # ValueLoop.start()

    # while not tcod.console_is_window_closed():
    #     sleep(cooldown * 1.1)
    #     con.ch [player_y, player_x] = ord ('@')
    #     con.fg [player_y, player_x] = tcod.white

def flusher_loop ():
    while not tcod.console_is_window_closed() and not exit_game:
        con.ch [player_y, player_x] = ord ('@')
        con.fg [player_y, player_x] = tcod.white

        sleep(cooldown)

        tcod.console_flush()

def main():
    global exit_game
    # Setup player
 
    # Setup Font
    font_filename = 'font.png'
    tcod.console_set_custom_font(f"./assets/{font_filename}", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
 
    # Initialize screen
    title = 'SkyMocha'
    global con
    con = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)
 
    # Set FPS
    tcod.sys_set_fps(LIMIT_FPS)
 
    SetScreenValues()
    # DrawFullMap(p_screen=-1)

    renderer = Thread(target=render_loop)
    renderer.start()

    flusher = Thread(target=flusher_loop)
    flusher.start()

    while not tcod.console_is_window_closed() and not exit_game:
        
        for event in tcod.event.get():
            if event.type == "KEYDOWN":
                exit_game = keyHandler(event.sym)
                sleep(cooldown)

main()