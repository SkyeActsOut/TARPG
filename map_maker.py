import libtcodpy as tcod
from tile import Tile, NullTile, BorderTile, MapTile
import numpy as np
from menu import MapEditMenu
from menu import *
from threading import Thread
from time import sleep

FULLSCREEN = False
SCREEN_WIDTH = 96  # characters wide
SCREEN_HEIGHT = 54  # characters tall
LIMIT_FPS = 60  # 20 frames-per-second maximum

con = 0

exit_game = False

menues = [MapEditMenu()]

cooldown = 1/60

raw_map = np.empty((100, 100), dtype=Tile)
map_pos = [0, 0]
for x in range(raw_map.shape[0]):
    for y in range(raw_map.shape[1]):
        raw_map[x, y] = Tile('#', (22, 22, 22))

raw_cover = 0
def define_raw ():
    global raw_cover
    raw_cover = np.empty((100, 100), dtype=Tile)
    for x in range(raw_map.shape[0]):
        for y in range(raw_map.shape[1]):
            raw_cover[x, y] = NullTile()
def redraw_cover():
    for x in range(raw_map.shape[0]):
        for y in range(raw_map.shape[1]):
            raw_cover[x, y] = None
            
define_raw()

def keyHandler(ev):
    pass

rclick = False
lclick = False
r_start = 0

def MouseHandler (ev):
    print (ev.type)
    if (ev.type == "MOUSEBUTTONDOWN"):
        t = ev.tile
        if t.y > menues[0].height:
            if (ev.button == 1): # LEFT CLCIK TURNS ON
                global lclick
                lclick = True
            else: # ANY OTHER BUTTON PLACE SQUARE
                global rclick
                global r_start
                rclick = True
                r_start = ev.tile

    if (ev.type == "MOUSEBUTTONUP"):
        rclick = False
        lclick = False
        print (ev.button)
        if (ev.button == 3):
            # PUTS ALL CHANCES MADE TO RAW MAP ON REAL MAP
            for x in range(raw_map.shape[0]):
                for y in range(raw_map.shape[1]):
                    if (raw_cover[x, y] != None):
                        raw_map[x, y] = raw_cover[x, y]
            redraw_cover()

def MouseMove (ev):
    # ON MOUSE MOVEMENT WHEN RIGHT CLICK IS HELD DOWN, DRAW SQUARE
    if (lclick and ev.type == "MOUSEMOTION"): # LEFT CLICK PLACE ONE TILE AT A TIME
        t = ev.tile
        raw_map[map_pos[0] + t.x, map_pos[1] + t.y] = Tile('#')   
    if (rclick and ev.type == "MOUSEMOTION"):
        redraw_cover()
        x_dif = r_start.x - ev.tile.x # difference between the first held down point and the current square
        y_dif = r_start.y - ev.tile.y
        if (x_dif > 0):
            for x in range (x_dif):
                if (y_dif > 0):
                    for y in range (y_dif):
                        raw_cover[map_pos[0] - x + r_start.x, map_pos[1] - y + r_start.y] = Tile('#')
                else:
                    for y in range (y_dif, 0):
                        raw_cover[map_pos[0] - x + r_start.x, map_pos[1] - y + r_start.y] = Tile('#')
        else:
            for x in range (x_dif, 0):
                if (y_dif > 0):
                    for y in range (y_dif):
                        raw_cover[map_pos[0] - x + r_start.x, map_pos[1] - y + r_start.y] = Tile('#')
                else:
                    for y in range (y_dif, 0):
                        raw_cover[map_pos[0] - x + r_start.x, map_pos[1] - y + r_start.y] = Tile('#')

def keyDownHandler (ev):
    pass

def keyUpHandler (ev):
    # SHIFT KEY
    if (ev == 1073742049):
        return

    menues[0] = MapEditMenu() # Refreshes the map menu (might need to find a better way)

    key = ""
    # Sets the key and available colors
    if (ev == 51):
        key = '#'
        colors = [
            (80, 80, 80),
            (40, 40, 150),
            (40, 150, 70)
        ]
    elif (ev == 49):
        key = '!'
        colors = [
            (40, 200, 70)
        ]

    # Displays the available options
    menues[0].add_line(2, 1, f"CURRENT KEY: {key*3}")
    if (key != ""):
        menues[0].add_line(3, 1, f"COLORS:")
        for j in range (3):
            i = 0
            for c in colors:
                menues[0].add_line(5 + j, i*4+2, f"{key*3}", c)
                i+=1
    else:
        menues[0].add_line(2, 1, f"CURRENT KEY: NOT SUPPORTED")
            
def update ():
    screen_values = setScreenValues()
    # print (screen_values)
    s = compile_scene(screen_values)
    LineRenderFullScreen(s)
    sleep(cooldown/2)

def flusher_loop ():
    while not tcod.console_is_window_closed() and not exit_game:
        # con.ch [player_y, player_x] = ord ('@')
        # con.fg [player_y, player_x] = (255, 255, 255)

        sleep(cooldown*2)

        tcod.console_flush()

def main():
    global exit_game
    
    # Setup Font
    font_filename = 'font.png'
    tcod.console_set_custom_font(f"./assets/{font_filename}", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)
 
    # Initialize screen
    title = 'SkyMocha'
    global con
    con = tcod.console_init_root(SCREEN_WIDTH, SCREEN_HEIGHT, title, FULLSCREEN)
    
    # Set FPS
    tcod.sys_set_fps(LIMIT_FPS)

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
            elif event.type == "MOUSEBUTTONUP":
                MouseHandler(event)
            if ("MOUSEMOTION"):
                MouseMove(event)
            elif event.type == "QUIT":
                exit_game = True
                raise SystemExit()
            keyHandler(event)
        update()

def setScreenValues():
    screen_values = np.empty((SCREEN_WIDTH, SCREEN_HEIGHT), dtype=Tile)

    # SETS THE BACKGROUND NULL COLOR
    # for x in range (SCREEN_WIDTH):
    #     for y in range (SCREEN_HEIGHT):
    #         screen_values[x, y] = NullTile()
    
    for x in range (SCREEN_WIDTH):
        for y in range (SCREEN_HEIGHT):
            screen_values[x, y] = raw_map[map_pos[0] + x, map_pos[1] + y]

    for x in range (SCREEN_WIDTH):
        for y in range (SCREEN_HEIGHT):
            if (not isinstance(raw_cover[map_pos[0] + x, map_pos[1] + y], NullTile) and 
                raw_cover[map_pos[0] + x, map_pos[1] + y] != None):
                screen_values[x, y] = raw_cover[map_pos[0] + x, map_pos[1] + y]

    # SETS THE MENU
    for x in range (SCREEN_WIDTH):
        for y in range (menues[0].height):
            screen_values[x, y] = isTileInMenu(x, y, menues)

    return screen_values

def LineRenderFullScreen(pre_compiled_scene):
    scene_str = [''.join (pre_compiled_scene[y]) for y in range (SCREEN_HEIGHT)]
    q = ''
    for y in scene_str:
        q += y + '\n'
    con.print(0, 0, q, alignment=tcod.LEFT)

def compile_scene (raw_scene):
    scene = []

    for y in range (SCREEN_HEIGHT):
        scene.append ([])

        for x in range (SCREEN_WIDTH):
            cell = raw_scene[x][y]
            if not cell:
                return
            scene[y].append ('%c%c%c%c%c%c%c%c%c%c' % ((tcod.COLCTRL_FORE_RGB, ) + cell.color + (tcod.COLCTRL_BACK_RGB, ) + (1, 1, 1) + (cell.char, tcod.COLCTRL_STOP)))

    return scene

main()