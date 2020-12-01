# http://cheesesun.blogspot.com/2009/10/fast-rendering-with-libtcod-in-python.html
import random

class Cell (object):
    __slots__ = '_fg', '_bg', 'char'

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

    return scene

def draw (con, scene):
    scene_str = [''.join (scene[y]) for y in range (height)]

    for y in range (height):
        tcod.console_print_left (con, 0, y, tcod.BKGND_SET, scene_str[y])

def draw (con, scene, left, top):
    scene_str = [''.join (scene[y][left:left + scr_width]) for y in range (top, top + scr_height)]

    for y in range (scr_height):
        tcod.console_print_left (con, 0, y, tcod.BKGND_SET, scene_str[y])