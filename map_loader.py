import xml.etree.ElementTree as ET
from math import sqrt
import tile

def load_map (name):
    tree = ET.parse(f'./Maps/{name}.xml')
    root = tree.getroot()
    info = root.find("info")
    raw_map = root.find("map").text.split ('/')
    length = int(sqrt(len(raw_map)))

    for x in raw_map:
        if x.index('\n') != -1:
            raw_map.remove(x)

    tiles = []

    for l in raw_map:
        ln = []
        for i in l.split(' '):
            ln.append(tile.Tile(i, c=(122,122,122)))
            print(i)
        tiles.append(ln)
    
    print (len(tiles))

    # print (tiles)
    return tiles, len(tiles)-1, len(tiles[0])-1

# load_map('commons')