import libtcodpy as tcod
import random

width = 50
height = 50

tcod.console_set_color_control (tcod.COLCTRL_1, (255, 255, 255), (0, 0, 0))

class Cell (object):

    def __init__ (self, fg,  bg, char):
        self.fg = fg
        self.bg = bg
        self.char = char

chars = ['\'', '`', ',', '.', '.', '.']
raw_scene = [[Cell ((1, 255, 1), (1, 1, 1), random.choice (chars)) for x in range (width)] for y in range (height)]

def compile_scene (raw_scene):
    scene = []

    for y in range (height):
        scene.append ([])

        for x in range (width):
            cell = raw_scene[y][x]
            scene[y].append ('%c%c%c%c%c%c%c%c%c%c' % ((tcod.COLCTRL_FORE_RGB, ) + cell.fg + (tcod.COLCTRL_BACK_RGB, ) + cell.bg + (cell.char, tcod.COLCTRL_STOP)))
            # scene[y].append ('%c%c%c%c%c%c' % ((tcod.COLCTRL_1, ) + cell.fg + (cell.char, tcod.COLCTRL_STOP)))
        # print (scene[y])

    return scene

def draw (con, scene):
    scene_str = [''.join (scene[y]) for y in range (height)]

    # tcod.set_default_color(tcod.black)

    for y in range (height):
        tcod.console_print_ex (con, 0, y, tcod.BKGND_SET, tcod.LEFT, scene_str[y])
        # con.print_(0, y, scene_str[y], alignment=tcod.LEFT)
 
# Setup Font
font_filename = 'font.png'
tcod.console_set_custom_font(f"./assets/{font_filename}", tcod.FONT_TYPE_GREYSCALE | tcod.FONT_LAYOUT_TCOD)

# Initialize screen
title = 'SkyMocha'
con = tcod.console_init_root(width, height, title, False)

# Set FPS
s = compile_scene(raw_scene)
draw(con, s)
tcod.console_flush()

exit_game = False

while not tcod.console_is_window_closed() and not exit_game:
    
    for event in tcod.event.get():
        if event.type == "KEYDOWN":
            exit_game = True