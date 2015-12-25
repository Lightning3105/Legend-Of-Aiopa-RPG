import pygame as py
import sys
from os import listdir
import mapMenuItems, npcEdit, tileEdit
import mapMakerVariables as v
from ast import literal_eval

class vars:
    def __init__(self):
        pass

#v = vars()

"""class toggleButton(py.sprite.Sprite):
    
    def __init__(self, text, variable, pos):
        super().__init__()
        self.text = text
        self.variable = variable
        self.pos = pos
    
    def update(self):
        text = self.text + ":" + str(globals()[self.variable])
        font = py.font.Font("../Resources/Fonts/RPGSystem.ttf", 30)
        label = font.render(text, 1, (255, 255, 255))
        rect = label.get_rect()
        rect.topleft = self.pos
        py.draw.rect(v.options, (0, 0, 255), rect)
        v.options.blit(label, self.pos)
        if rect.collidepoint((py.mouse.get_pos()[0], py.mouse.get_pos()[1] - 550)):
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    globals()[self.variable] = not globals()[self.variable]"""
                


tileset = py.image.load("../Resources/Images/Main_Tileset.png")

def save():
    outMap1 = []
    for y in range(v.size[1]):
        outMap1.append([])
        for x in range(v.size[0]):
            outMap1[y].append("")
    for tile in v.baseTiles:
        if tile.hitable:
            h = "#"
        else:
            h = ""
        outMap1[tile.posy][tile.posx] = h + str(tile.sheetNum)
    
    """print("[[")
    for i in outMap1:
        print(str(i) + ",")
    print("], ")"""
    
    outMap2 = []
    for y in range(v.size[1]):
        outMap2.append([])
        for x in range(v.size[0]):
            outMap2[y].append("")
    
    for tile in v.topTiles:
        if tile.overP:
            h = "+"
        elif tile.teleport != None:
            h = "&" + str(tile.teleport) + "|"
        elif tile.npc != None:
            h = "%" + str(tile.npc) + "|"
        else:
            h = ""
        outMap2[tile.posy][tile.posx] = h + str(tile.sheetNum)
    
    """print("[")
    for i in outMap2:
        print(str(i) + ",")
    print("]]")"""
    
    outTotal = [outMap1, outMap2]
    outTotal = ({"Biome": v.currentBiome, "Name": v.currentName}, outTotal)
    v.totalMap[str(v.currentID)] = outTotal
    print("{")
    for k, va in v.totalMap.items():
        print('"' + str(k) + '"' +  ":(")
        print(str(outTotal[0]) + ", [")
        for i in va[1]:
            print("[")
            for j in i:
                print(str(j) + ",")
            print("], ")
        print("])")
    print("}")
    

def load():
    print("LOAD")
    themap = v.totalMap[str(v.currentID)][1][1]
    v.topTiles = py.sprite.Group()
    v.baseTiles = py.sprite.Group()
    v.tiles = py.sprite.Group()
    for x in range(len(themap[0])):
        for y in range(len(themap[1])):
            #print(themap[y][x])
            tp = None
            ep = False
            nc = None
            if "+" in themap[y][x]:
                ep = True
            if "&" in themap[y][x]:
                tp = literal_eval(themap[y][x].replace('&', "").split("|")[0])
            if "%" in themap[y][x]:
                nc = literal_eval(themap[y][x].replace('%', "").split("|")[0])
            
            if "|" in themap[y][x]:
                img = themap[y][x].split("|")[1]
            else:
                img = themap[y][x]
            v.topTiles.add(tileEdit.tile(x, y, "top", img, ep, tp, nc))
    
    themap = v.totalMap[str(v.currentID)][1][0]
    for x in range(len(themap[0])):
        for y in range(len(themap[1])):
            if "#" in themap[y][x]:
                hb = True
            else:
                hb = False
            if "|" in themap[y][x]:
                img = themap[y][x].split("|")[1]
            else:
                img = themap[y][x]
            img = img.strip("#")
            v.baseTiles.add(tileEdit.tile(x, y, "base", img, ep, tp, nc, hb))
    
    mapEditor()

def mapEditor():
    v.map = py.Surface((600, 550))
    v.pallet = py.Surface((400, 630))
    v.options = py.Surface((1000, 80))
    
    v.scrollX = 0
    v.scrollY = 0
    v.scale = 2
    v.selected = 0
    v.selectedNpc = {"Image":None, "Name":None, "Health":None, "Attack":None, "Speed":None}
    v.editHitable = False
    v.eLayer = "base"
    v.overPlayer = False
    v.hoverPos = None
    v.hoverData = None
    v.makeTeleport = False
    v.makeNPC = False
    
    v.palletImages = py.sprite.Group()
    v.tileImages = tileEdit.getGrid(tileset)
    for i in range(0, len(v.tileImages)):
        v.palletImages.add(tileEdit.image(i))
    
    v.npcImages = py.sprite.Group()
    num = 0
    for i in listdir("..\Resources\Images\EnemySkins"):
        v.npcImages.add(npcEdit.npcImage(num, "../Resources/Images/EnemySkins/" + i))
        num += 1
        
    v.clock = py.time.Clock()
    
    py.time.set_timer(py.USEREVENT, 1000) #1 sec delay
    
    buttons = py.sprite.Group()
    #buttons.add(toggleButton("Make NPC", "v.makeNPC", (170, 50)))
    buttons.add(mapMenuItems.toggleButton("layer", 0))
    buttons.add(mapMenuItems.toggleButton("hitbox", 1))
    buttons.add(mapMenuItems.toggleButton("over", 2))
    buttons.add(mapMenuItems.toggleButton("teleport", 3))
    
    while True:
        py.event.pump()
        v.hoverPos = None
        v.events = []
        v.events = py.event.get()
        v.clock.tick(30)
        v.screen.fill((255, 255, 255))
        v.map.fill((0, 255, 255))
        v.pallet.fill((255, 255, 255))
        v.options.fill((0, 0, 255))
        v.baseTiles.update()
        v.topTiles.update()
        if not v.makeNPC:
            v.palletImages.update()
        if v.makeNPC:
            v.npcImages.update()
        buttons.update()
        
        if not v.pauseEdit:
            keysPressed = py.key.get_pressed()
            speed = 20
            if keysPressed[py.K_d]:
                v.scrollX += speed
            if keysPressed[py.K_a]:
                v.scrollX -= speed
            if keysPressed[py.K_w]:
                v.scrollY += speed
            if keysPressed[py.K_s]:
                v.scrollY -= speed
        for event in v.events:
            if event.type == py.MOUSEBUTTONUP:
                if event.button == 4:
                    v.scale += 0.1
                if event.button == 5:
                    v.scale -= 0.1
                v.scale = round(v.scale, 1)
                if v.scale <= 0.1:
                    v.scale = 0.1
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    outMap = save()
            if event.type == py.QUIT:
                save()
                sys.exit()
        
        
        v.screen.blit(v.map, (0, 0))
        v.screen.blit(v.options, (0, 550))
        v.screen.blit(v.pallet, (600, 0))
        if not v.editTeleport == None:
            v.editTeleport.update()
            v.pauseEdit = True
        else:
            v.pauseEdit = False
        mapMenuItems.toolTip()
        py.display.flip()

def startMenu():
    py.init()
    v.screen = py.display.set_mode((920, 630), py.DOUBLEBUF)
    buttons = py.sprite.Group()
    buttons.add(mapMenuItems.button("New Map", (460, 270), 50, (255, 255, 0), (0, 0, 255), "../Resources/Fonts/RunicSolid.ttf", "NM", True, (220, 50)))
    buttons.add(mapMenuItems.button("Load Map", (460, 360), 50, (255, 255, 0), (0, 0, 255), "../Resources/Fonts/RunicSolid.ttf", "LM", True, (220, 50)))
    
    texts = py.sprite.Group()
    texts.add(mapMenuItems.textLabel("Legend Of Aiopa RPG", (460, 150), (255, 0, 255), "../Resources/Fonts/RunicSolid.ttf", 50, variable = False, centred = True))
    texts.add(mapMenuItems.textLabel("Map Editor", (460, 200), (200, 0, 200), "../Resources/Fonts/RunicSolid.ttf", 40, variable = False, centred = True))
    
    v.textNum = 1
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        v.screen.fill((0, 255, 255))
        texts.update()
        buttons.update()
        py.display.flip()
        
        for event in v.events:
            if event.type == py.MOUSEBUTTONDOWN:
                for b in buttons:
                    if b.pressed():
                        if b.ID == "NM":
                            setup()
                        if b.ID == "LM":
                            from Resources import mapFile  # @UnresolvedImport
                            v.totalMap = mapFile.map
                            load()

def setup():
    tinps = py.sprite.Group()
    texts = py.sprite.Group()
    tinps.add(mapMenuItems.textInput((500, 100), 60, 2, 1, button=None, default=['1', '0'], type="int"))
    texts.add(mapMenuItems.textLabel("Map Width:", (240, 110), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 60))
    
    tinps.add(mapMenuItems.textInput((500, 180), 60, 2, 2, button=None, default=['1', '0'], type="int"))
    texts.add(mapMenuItems.textLabel("Map Height:", (240, 190), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 60))
    
    if v.tempId == None:
        df = ['1']
    else:
        df = list(str(v.tempId))
    tinps.add(mapMenuItems.textInput((500, 260), 60, 2, 3, button=None, default=df, type="int"))
    texts.add(mapMenuItems.textLabel("Map ID:", (240, 270), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 60))
    
    tinps.add(mapMenuItems.textInput((400, 350), 30, 24, 4, button=None, default=['P', 'l', 'a', 'c', 'e'], type="str"))
    texts.add(mapMenuItems.textLabel("Location Name:", (40, 350), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 60))
    
    tinps.add(mapMenuItems.textInput((500, 430), 40, 10, 5, button=None, default=['P', 'l', 'a', 'i', 'n', 's'], type="str"))
    texts.add(mapMenuItems.textLabel("Biome:", (240, 440), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 60))
    
    buttons = py.sprite.Group()
    buttons.add(mapMenuItems.button("Back", (10, 550),80, (255, 255, 255), (255, 0, 0), "../Resources/Fonts/RPGSystem.ttf", "B"))
    buttons.add(mapMenuItems.button("Continue", (690, 550), 70, (255, 255, 255), (255, 0, 0), "../Resources/Fonts/RPGSystem.ttf", "C"))
    
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        v.screen.fill((0, 255, 0))
        tinps.update()
        texts.update()
        buttons.update()
        py.display.flip()
        
        for b in buttons:
            if b.pressed():
                if py.mouse.get_pressed()[0]:
                    if b.ID == "B":
                        startMenu()
                        return
                    if b.ID == "C":
                        for i in tinps:
                            if i.num == 1:
                                x = int(i.outText)
                            if i.num == 2:
                                y = int(i.outText)
                            if i.num == 3:
                                v.currentID = int(i.outText)
                            if i.num == 4:
                                v.currentName = str(i.outText)
                            if i.num == 5:
                                v.currentBiome = str(i.outText)
                        v.size = (x, y)
                        v.baseTiles = py.sprite.Group()
                        v.topTiles = py.sprite.Group()
                        v.tiles = py.sprite.Group()
                        for x in range(v.size[0]):
                            for y in range(v.size[1]):
                                v.baseTiles.add(tileEdit.tile(x, y, "base"))
                                v.topTiles.add(tileEdit.tile(x, y, "top"))
                        mapEditor()
                        return
if __name__ == "__main__":
    startMenu()
    