#RESOURCES
#http://cheesesun.blogspot.com/2009/10/fast-rendering-with-libtcod-in-python.html

import libtcodpy as tcod
import numpy as np
from game_map import tiles, start, WIDTH, HEIGHT
from tile import Tile, NullTile, BorderTile, MapTile
from menu import LogsMenu, StaticInfo, StaticMenu, CircleBar
import random
from threading import Thread
from time import sleep
from entities import Player
import abilities

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

menues = [LogsMenu(), StaticInfo(), StaticMenu(1, SCREEN_HEIGHT-14, 13, 13), StaticMenu(SCREEN_WIDTH - 14, SCREEN_HEIGHT-14, 13, 13)]
bars = [CircleBar(6, 7, SCREEN_HEIGHT - 8, (175, 22, 22), (55, 22, 22)), 
        CircleBar(6, SCREEN_WIDTH - 8, SCREEN_HEIGHT - 8, (22, 22, 200), (22, 22, 55))]

game_mem_save = False

cooldown = 1/60

con = 0

player_x = int (SCREEN_WIDTH / 2)
player_y = int (SCREEN_HEIGHT / 2)

p = Player()

keys_held = []

class Cell (object):
    def __init__ (self, fg,  bg, char):
        self.fg = fg
        self.bg = (1, 1, 1)
        self.char = char

def compile_scene (raw_scene):
    scene = []

    for y in range (SCREEN_HEIGHT):
        scene.append ([])

        for x in range (SCREEN_WIDTH):
            cell = raw_scene[x][y]
            scene[y].append ('%c%c%c%c%c%c%c%c%c%c' % ((tcod.COLCTRL_FORE_RGB, ) + cell.color + (tcod.COLCTRL_BACK_RGB, ) + (1, 1, 1) + (cell.char, tcod.COLCTRL_STOP)))

    return scene

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

def MoveStaticObjects(x_move, y_move):
    for ability in p.active_abilities:
        for proj in ability.projectiles:
            proj.translate(x_move, y_move)

# Based on the game_map values, this gets a np array with the tiles ONLY around the player
def GetScreenValues():
    global screen_values
    screen_values = np.empty((SCREEN_WIDTH, SCREEN_HEIGHT), dtype=Tile)

    i = 0
    j = 0
    health_covered = 0
    mana_coverd = 0
    for width in range(int(map_pos[0] - SCREEN_WIDTH/2), int(map_pos[0] + SCREEN_WIDTH/2)): # Loops through the values for what should be displayed on screen
        for height in range(int(map_pos[1] - SCREEN_HEIGHT/2), int(map_pos[1] + SCREEN_HEIGHT/2)): # loops through the height values for what should be displayed on screen

            # RENDER ORDER
            stop = False

            if (i == player_x and j == player_y):
                screen_values[i, j] = Tile('#', (255, 20, 255))
                j+=1
                continue

            # THE HEALTH CIRCLE
            isBar = bars[0].isInCircle(p, health_covered, i, j, True)
            if (isBar == 1):
                screen_values[i, j] = Tile('#', bars[0].color)
                health_covered+=1
                j+=1
                continue
            elif (isBar == 0):
                screen_values[i, j] = Tile('#', bars[0].bg_color)
                health_covered+=1
                j+=1
                continue

            # MANA CIRCLE
            isBar = bars[1].isInCircle(p, mana_coverd, i, j, False)
            if (isBar == 1):
                screen_values[i, j] = Tile('#', bars[1].color)
                mana_coverd+=1
                j+=1
                continue
            elif (isBar == 0):
                screen_values[i, j] = Tile('#', bars[1].bg_color)
                mana_coverd+=1
                j+=1
                continue

            # IS ON A MENU TILE
            elif (isOnMenu(i, j)):
                t = isTileInMenu(i, j)
                if (screen_values[i, j] == t):
                    screen_values[i, j].reload = True
                else: 
                    screen_values[i, j] = t
                j+=1
                continue
            # IS ON THE BORDER OF A MNEU
            elif (isOnBorder(i, j)):
                screen_values[i, j] = BorderTile()
                j+=1
                continue

            # CHECKS FOR PROJECTILES & SPELLS
            for ability in p.active_abilities:
                for proj in ability.projectiles:
                    if (i == proj.curr_x and j == proj.curr_y):
                        screen_values[i, j] = Tile('-')
                        stop=True
                        break
            if (stop):
                j+=1
                continue

            if (width < 0 or height < 0 or width >= WIDTH or height >= HEIGHT): # checks for stuff outside the map
                screen_values[i, j] = NullTile()
                j+=1
                continue
            elif (j < 0 or i < 0 or j >= SCREEN_WIDTH or i >= SCREEN_WIDTH): # checks for stuff outside the screen
                screen_values[i, j] = NullTile()
                j+=1
                continue
                
            # IS A NORMAL SCREEN TILE
            else:
                t = tiles[width][height]
                # The tile already has been drawn that exact same way; skip
                if (t == screen_values[i, j]):
                    screen_values[i, j].reload = True
                    j+=1
                    continue
                # There is a new tile, it must be redrawn
                else:
                    screen_values[i, j] = t
                    j+=1
                    continue
        j=0
        i+=1

    pre_compiled_scene = compile_scene(screen_values)
    ThreadLines (pre_compiled_scene)
    
    # LineRenderScreen(pre_compiled_scene, 0, SCREEN_HEIGHT)
    # LineRenderFullScreen(pre_compiled_scene)

def ThreadLines(s):
    chunk_cnt = 2
    chunk_size = int(SCREEN_HEIGHT / chunk_cnt)
    for i in range (chunk_cnt):
        # chunk_ready.append(False)
        renderer = Thread(target=LineRenderScreen, args=(s, i*chunk_size, i*chunk_size+chunk_size))
        renderer.start()
        renderer.join()

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

                c = screen_values[i, j]
                if (c):
                    if (c.reload):
                        continue
                    else:
                        if (c.rl_capable):
                            c.reload = True
                        set_tile (c.char, c.color, i, j)
                else:
                    set_tile ("#", (0, 0, 0), i, j)

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

def LineRenderScreen(pre_compiled_scene, y_start, y_end):
    # print (pre_compiled_scene)
    scene_str = [''.join (pre_compiled_scene[y]) for y in range (y_start, y_end)]

    for y in range (y_end-y_start):
        con.print_(0, y_start+y, scene_str[y], alignment=tcod.LEFT)
        # tcod.console_print_ex (con, 0, y, tcod.BKGND_SET, tcod.LEFT, scene_str[y])

def LineRenderFullScreen(pre_compiled_scene):
    # print (pre_compiled_scene)
    scene_str = [''.join (pre_compiled_scene[y]) for y in range (SCREEN_HEIGHT)]
    q = ''
    for y in scene_str:
        q += y + '\n'
    con.print_(0, 0, q, alignment=tcod.LEFT)

def SetScreenValues():
    screen_values = GetScreenValues()


# def set_tile (c, color, x, y):
#     # print ((c, color))
#     con.ch[y, x] = ord (c)
#     con.fg[y, x] = color

# def set_bg (color, x, y):
#     con.bg[y, x] = tcod.Color(color[0], color[1], color[2])


# ######################################################################
# User Input
# ######################################################################
 
 
def keyUpHandler(key):
    if (key == 119 or key == 115 or key == 97 or key == 100):
        if key in keys_held:
            keys_held.remove (key)

def keyDownHandler(key):
    if (key == 119 or key == 115 or key == 97 or key == 100):
        if key not in keys_held:
            keys_held.append (key)

def keyHandler():

    if (p.move_cooldown()):
        for key in keys_held:
            x_move = 0
            y_move = 0

            # movement keys
            if key == 119 : # W KEY
                if (map_pos[1] > 0):
                    y_move = 1
        
            if key == 115 : # S KEY 
                if (map_pos[1] < HEIGHT-1):
                    y_move = -1
        
            if key == 97 : # A KEY
                if (map_pos[0] > 0):
                    x_move = 1
        
            if key == 100 : # D KEY
                if (map_pos[0] < WIDTH-1):
                    x_move = -1

            if (key == 119 or key == 115 or key == 97 or key == 100):
                # print (map_pos)
                map_pos[1] -= y_move
                map_pos[0] -= x_move
                setInfoPosition(map_pos[1], map_pos[0])
                MoveStaticObjects(x_move, y_move)
                # GetScreenValues()

def MouseHandler (event):
    if (p.global_cooldown()):
        px = int(SCREEN_WIDTH/2)
        py = int(SCREEN_HEIGHT/2)
        button = event.button
        tile = event.tile
        
        dir_x = 0
        dir_y = 0

        tolerance = 5

        if (tile.x < px-tolerance):
            dir_x = -1
        elif (tile.x > px+tolerance):
            dir_x = 1

        if (tile.y < py-tolerance):
            dir_y = -1
        elif (tile.y > py+tolerance):
            dir_y = 1

        p.add_active_ability(
            abilities.KnifeThrow
                (int(SCREEN_WIDTH/2), int(SCREEN_HEIGHT/2),
                tile.x, tile.y, 
                dir_x, dir_y)
        )

def update():
    for ability in p.active_abilities:
        for proj in ability.projectiles:
            destroy = proj.update()
            if (destroy):
                ability.projectiles.remove(proj)

    
#############################################
# Main Game Loop
#############################################
 
 
def render_loop ():
    while not tcod.console_is_window_closed() and not exit_game:
        GetScreenValues()

    # SetScreenValues()

    # ThreadAllChunks()

    # LineRenderScreen()

    # ValueLoop = Thread(target=GetScreenValues)
    # ValueLoop.start()

    # while not tcod.console_is_window_closed():
    #     sleep(cooldown * 1.1)
    #     con.ch [player_y, player_x] = ord ('@')
    #     con.fg [player_y, player_x] = tcod.white

def flusher_loop ():
    while not tcod.console_is_window_closed() and not exit_game:
        # con.ch [player_y, player_x] = ord ('@')
        # con.fg [player_y, player_x] = (255, 255, 255)

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
                keyDownHandler(event.sym)
                # sleep(cooldown)
            if event.type == "KEYUP":
                keyUpHandler(event.sym)
            elif event.type == "MOUSEBUTTONDOWN":
                MouseHandler(event)
                # sleep(cooldown)
            elif event.type == "QUIT":
                exit_game = True
                raise SystemExit()
        keyHandler()
        update()


main()