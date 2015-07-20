import pygame as py
import entityClasses

def generateMap(map, sheet):
    mody = int(len(map) / 2)
    modx = int(len(map[0]) / 2)
    sheet.getGrid()
    outmap = py.sprite.Group()
    for row in range(len(map)):
        for tile in range(len(map[row])):
            if map[row][tile] == "0":
                image = sheet.images[0]
                wall = False
                terrain = 1
            if map[row][tile] == "#":
                image = sheet.images[2]
                wall = True
                terrain = 0
            outmap.add(entityClasses.Tile((tile - modx, row - mody), image, terrain, wall))
    return outmap
