import libtcodpy as tcod
import numpy as np
import game_map
import random
from threading import Thread
from time import sleep

# ######################################################################
# Global Game Settings
# ######################################################################
# Windows Controls
FULLSCREEN = False
SCREEN_WIDTH = 96  # characters wide
SCREEN_HEIGHT = 54  # characters tall
LIMIT_FPS = 60  # 20 frames-per-second maximum
# Game Controls
TURN_BASED = False  # turn-based game

map_pos = [game_map.start[0], game_map.start[1]]

chunk_size = 16

screen_values = []

chunk_ready = []

cooldown = 0.001

con = 0

# Based on the game_map values, this gets a np array with the tiles ONLY around the player
def GetScreenValues():
    global screen_values
    screen_values = np.zeros((SCREEN_WIDTH, SCREEN_HEIGHT, 2))

    i = 0
    j = 0
    for width in range(int(map_pos[0] - SCREEN_WIDTH/2), int(map_pos[0] + SCREEN_WIDTH/2)): # Loops through the values for what should be displayed on screen
        for height in range(int(map_pos[1] - SCREEN_HEIGHT/2), int(map_pos[1] + SCREEN_HEIGHT/2)): # loops through the height values for what should be displayed on screen
            if (width < 0 or height < 0 or width > game_map.width-1 or height > game_map.height-1): # checks for stuff outside the map
                continue
            screen_values[i, j, 0] = game_map.values[width][height]
            screen_values[i, j, 1] = game_map.variants[width][height]
            j+=1
        j=0
        i+=1
    
# Draws the full map unless the tile to be drawn is already on screen
def DrawFullMap ():
    global screen_values

    # Checks to see if the p_screen has not been defined yet
    x = 0
    y = 0
    # Loops through the screen_values as well as the p_screen
    for i in range(screen_values.shape[0]):
        for j in range(screen_values.shape[1]):
            tile = GetTile(screen_values[i, j], i, j)
            set_char(tile, x, y)
            y+=1
        y=0
        x+=1

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
                (tile, color) = GetTile(screen_values[i, j], game_map.biomes[i, j], i, j)
                set_tile (tile, color, i, j)

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
    while (1):
        # chunk_i = 0
        for i in range (0, int(SCREEN_WIDTH/chunk_size)+1):
            for j in range (0, int(SCREEN_HEIGHT/chunk_size)+1):
                # chunk_ready.append(False)
                renderer = Thread(target=DrawChunk, args=(i*chunk_size, j*chunk_size))
                renderer.start()
                # chunk_i += 1

def SetScreenValues():
    screen_values = GetScreenValues()

def GetTile (tile, biome_tile, i, j):
    value = tile[0]
    variant = tile[1]

    tile = ' '
    color = tcod.black

    if (value == 0):
        return (' ', tcod.Color (0, 0, 0))
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
        color = (20, int(255 * value * (10/7)), 20)
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
    # DESERT
    elif (biome_tile < 0.3):
        # COLORS
        if (value < 0.1):
            color = (178, 162, 100)
        elif (value < 0.2):
            color = (184, 170, 112)
        elif (value < 0.3):
            color = (194, 178, 128)
        # VARIANTS
        if (variant < 60):
            tile = '#'
        elif (variant < 85):
            tile = '~'
        elif (variant < 100):
            tile = '^'
        else:
            tile = '#'
    # FOREST
    elif (biome_tile < 0.55):
        # COLORS
        if (variant < 42):
            color = (20, 80, 30)
            tile = '#'
        elif (variant < 80):
            color = (10, 50, 20)
            tile = '!'
        elif (variant < 101):
            color = (25, 70, 42)
            tile = '%'
        color = (20, 80, 30)
        tile = '#'
    return (tile, color)

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
    con.fg[y, x] = tcod.Color(color[0], color[1], color[2])

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
    while not tcod.console_is_window_closed():
        con.ch [player_y, player_x] = ord ('@')
        con.fg [player_y, player_x] = tcod.white

        sleep(cooldown * 1.125)

        tcod.console_flush()

def main():
    # Setup player
 
    # Setup Font
    font_filename = 'arial16x16.png'
    tcod.console_set_custom_font(f"./assets/{font_filename}", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
 
    # Initialize screen
    title = 'SkyMocha'
    global con
    con = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)
 
    # Set FPS
    tcod.sys_set_fps(LIMIT_FPS)
 
    SetScreenValues()
    # DrawFullMap(p_screen=-1)

    exit_game = False

    renderer = Thread(target=render_loop)
    renderer.start()

    flusher = Thread(target=flusher_loop)
    flusher.start()

    while not tcod.console_is_window_closed() and not exit_game:
    
        for event in tcod.event.get():
            if event.type == "KEYDOWN":
                exit_game = keyHandler(event.sym)
                sleep(cooldown * 0.95)

main()