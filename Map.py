import pygame as py
import entityClasses
import Variables as v
from ast import literal_eval

def generateMap(map, sheet):
    #import Variables as v
    print(map)
    map = map[str(v.mapNum)]
    allMap = map
    map = allMap[0]
    mody = int(len(map) / 2)
    modx = int(len(map[0]) / 2)
    sheet.getGrid()
    outmap = py.sprite.Group()
    size = [0, 0]
    size[0] = len(map[0]) * 30
    size[1] = len(map[1]) * 30
    baseMap = py.Surface(size)
    for row in range(len(map)):
        for tile in range(len(map[row])):
            if list(map[row][tile])[0] == "#":
                image = sheet.images[int(map[row][tile].replace('#', ""))]
                posx = (tile * 30)# - (modx * 30)
                posy = (row * 30)# - (mody * 30)
                baseMap.blit(image, (posx, posy))
                outmap.add(entityClasses.Tile((tile - modx, row - mody), 0, True))
            else:
                image = sheet.images[int(map[row][tile])]
                posx = (tile * 30)# - (modx * 30)
                posy = (row * 30)# - (mody * 30)
                baseMap.blit(image, (posx, posy))
    
    
    map = allMap[1]
    mody = int(len(map) / 2)
    modx = int(len(map[0]) / 2)
    outmap = py.sprite.Group()
    size = [0, 0]
    size[0] = len(map[0]) * 30
    size[1] = len(map[1]) * 30
    for row in range(len(map)):
        for tile in range(len(map[row])):
            if map[row][tile] != "-":
                teleport = None
                over = False
                draw = True
                create = True
                if list(map[row][tile])[0] == "+":
                    over = True
                if list(map[row][tile])[0] == "&":
                    teleport = (int(map[row][tile].replace('&', "").split("|")[0]))
                    map[row][tile] = map[row][tile].replace('&', "").split("|")[1]
                if list(map[row][tile])[0] == "%":
                    npc = literal_eval(map[row][tile].replace('%', "").split("|")[0])
                    for k, va in npc.items():
                        try:
                            npc[k] = int(va)
                        except:
                            pass
                    entityClasses.Enemy((tile - modx) * 30, (row - mody) * 30, v.mapNum, npc["Image"], npc)
                    draw = False
                else:
                    over = False
                    create = False
                if draw:
                    image = sheet.images[int(map[row][tile].replace('+', ""))]
                    posx = (tile * 30)# - (modx * 30)
                    posy = (row * 30)# - (mody * 30)
                    baseMap.blit(image, (posx, posy))
                if create:
                    entityClasses.Tile((tile - modx, row - mody), 0, False, over, image, teleport) 
    
    v.MAP = BaseMap(baseMap)    

class BaseMap():
    
    def __init__(self, image):
        self.posx = 0
        self.posy = 0
        self.skin = image.convert()
        v.MAP = self
        self.oldScale = None
        self.oldPos = None
        self.reRender = False
    
    def update(self):
        if self.oldScale != v.scale:
            size = self.skin.get_rect().size
            self.image = py.transform.scale(self.skin, (int(size[0] * v.scale), int(size[1] * v.scale)))
            self.oldScale = v.scale
            self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = v.screenX / 2 + ((-v.playerPosX + (1 * self.posx) - 15) * v.scale)
        self.rect.centery = v.screenY / 2 + ((v.playerPosY + (1 * self.posy) - 15) * v.scale)
        self.draw()
        
    def draw(self):
        v.screen.blit(self.image, self.rect)

Maps = {"1":[[
['326', '326', '77', '326', '326'],
['326', '326', '326', '326', '326'],
['77', '326', '186', '326', '77'],
['326', '326', '326', '326', '326'],
['326', '326', '77', '326', '326'],
], 
[
['-', '-', "%{'Health': '10', 'Speed': '2', 'Name': 'Stanly', 'Attack': '4', 'Image': 'Resources/Images/EnemySkins/GuardSheet.png'}|-", '-', '-'],
['-', '-', '-', '-', '-'],
["%{'Health': '10', 'Speed': '2', 'Name': 'Stanly', 'Attack': '4', 'Image': 'Resources/Images/EnemySkins/GuardSheet.png'}|-", '-', '-', '-', "%{'Health': '10', 'Speed': '2', 'Name': 'Stanly', 'Attack': '4', 'Image': 'Resources/Images/EnemySkins/GuardSheet.png'}|-"],
['-', '-', '-', '-', '-'],
['-', '-', "%{'Health': '10', 'Speed': '2', 'Name': 'Stanly', 'Attack': '4', 'Image': 'Resources/Images/EnemySkins/GuardSheet.png'}|-", '-', '-'],
]]}