import pygame as py
import entityClasses
import Variables as v

def generateMap(map, sheet):
    mody = int(len(map) / 2)
    modx = int(len(map[0]) / 2)
    sheet.getGrid()
    outmap = py.sprite.Group()
    for row in range(len(map)):
        for tile in range(len(map[row])):
            #print(list(map[row][tile]))
            if list(map[row][tile])[0] == "#":
                image = sheet.images[int(map[row][tile].replace('#', ""))]
                wall = True
                terrain = 0
            else:
                image = sheet.images[int(map[row][tile])]
                wall = False
                terrain = 1
            if not list(str(map[row][tile]))[0] == "-":
                image = image.convert_alpha()
                outmap.add(entityClasses.Tile((tile - modx, row - mody), image, terrain, wall))
    #v.screen.blit(sheet.images[325], (10, 10))
    #py.display.flip()
    return outmap

Map1G = [["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],]

Map1I = [["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],
            ["-","-","-","-","-","-","-","-","-","-"],]

Maps = [
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '70', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#665', '#665', '#665', '#665', '#665', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#697', '#697', '#697', '#697', '#697', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#50', '#50', '#50', '#50', '#50', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#81', '#81', '#81', '#50', '#50', '1954', '#50', '#50', '#81', '#81', '#81', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#81', '#81', '#81', '#50', '#50', '1986', '#50', '#50', '#81', '#81', '#81', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#81', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#81', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#81', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#81', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#81', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#81', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#81', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '#81', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '70', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
['326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326', '326'],
]