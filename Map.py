import pygame as py
import entityClasses
import Variables as v
from ast import literal_eval
import npcScripts
from Saves import mapFile
def generateMap():
    #import Variables as v
    amap = dict(mapFile.map)
    sheet = entityClasses.SpriteSheet("Resources/Images/Main_Tileset.png", 63, 32)
    
    map = amap[str(v.mapNum)]
    allMap = map
    v.mapMeta = allMap[0]
    print(v.mapMeta)
    map = allMap[1][0]
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
            mrt = map[row][tile]
            if list(mrt)[0] == "#":
                image = sheet.images[int(mrt.replace('#', ""))]
                posx = (tile * 30)# - (modx * 30)
                posy = (row * 30)# - (mody * 30)
                baseMap.blit(image, (posx, posy))
                outmap.add(entityClasses.Tile((tile - modx, row - mody), 0, True))
            else:
                image = sheet.images[int(mrt)]
                posx = (tile * 30)# - (modx * 30)
                posy = (row * 30)# - (mody * 30)
                baseMap.blit(image, (posx, posy))
    
    
    map = allMap[1][1]
    mody = int(len(map) / 2)
    modx = int(len(map[0]) / 2)
    outmap = py.sprite.Group()
    size = [0, 0]
    size[0] = len(map[0]) * 30
    size[1] = len(map[1]) * 30
    for row in range(len(map)):
        for tile in range(len(map[row])):
            mrt = map[row][tile]
            if mrt != "-":
                teleport = None
                over = False
                draw = True
                create = True
                if list(mrt)[0] == "+":
                    over = True
                elif list(mrt)[0] == "&":
                    teleport = literal_eval(mrt.replace('&', "").split("|")[0])
                    mrt = mrt.replace('&', "").split("|")[1]
                elif list(mrt)[0] == "$":
                    exists = False
                    npc = literal_eval(mrt.replace('$', "").split("|")[0])
                    npc = NPCs[npc]
                    for k, va in npc.items():
                        try:
                            npc[k] = int(va)
                        except:
                            pass
                    for thing in v.allNpc:
                        if thing.name == npc["Name"]:
                            exists = True
                    if not exists:        
                        entityClasses.NPC(((tile - modx) * 30, 30, (row - mody) * 30, npc["Direction"]), npc["Image"], {"Name":npc["Name"], "Conversation":npc["Conversation"]})
                    draw = False
                elif list(mrt)[0] == "%":
                    npc = literal_eval(mrt.replace('%', "").split("|")[0])
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
                    image = sheet.images[int(mrt.replace('+', ""))]
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

NPCs = [{'Image': 'Resources/Images/NpcSkins/Spritesheets/Male_Basic.png', 'Name': 'Fred', "Direction": "Down", 
            "Conversation": [{"Message": "Greetings child. Could you spare the time to run an errand for me?", "B1":{"Text": "Yes", "ID": 1}, "B2":{"Text": "No", "ID": 2}, "ID":0},
                             {"Message": "Why, that is wonderful!", "Goto":3, "ID": 1},
                             {"Message": "Fine. Suit yourself.", "Goto":0, "End": True, "ID": 2},
                             {"Message": "Groblins have been a real nuisance lately. Could you go and a few for me?", "Quest":("Hunting Groblins", "Kill", {"Name": "Groblin", "Amount": 3}), "Goto": 4, "End":True, "ID":3},
                             {"Message": "Go kill those Groblins!", "ID":4, "End": True}
                             ]},
        ]




#NPC Conversations:
#{"Message":****, "B1":{"Text":****, "ID":**}, "Goto":**, "ID":**}
#Add "End" key to signify the end of a conversation
#