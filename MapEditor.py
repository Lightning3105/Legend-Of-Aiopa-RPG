import pygame as py
import sys
from os import listdir
from entityClasses import SpriteSheet

class toggleButton(py.sprite.Sprite):
    
    def __init__(self, text, variable, pos):
        super().__init__()
        self.text = text
        self.variable = variable
        self.pos = pos
    
    def update(self):
        text = self.text + ":" + str(globals()[self.variable])
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
        label = font.render(text, 1, (255, 255, 255))
        rect = label.get_rect()
        rect.topleft = self.pos
        py.draw.rect(options, (0, 0, 255), rect)
        options.blit(label, self.pos)
        if rect.collidepoint((py.mouse.get_pos()[0], py.mouse.get_pos()[1] - 550)):
            for event in events:
                if event.type == py.MOUSEBUTTONDOWN:
                    globals()[self.variable] = not globals()[self.variable]
        



class tile(py.sprite.Sprite):
    
    def __init__(self, posx, posy, layer):
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.image = py.Surface((30, 30))
        self.image.fill((100, 0, 255))
        self.tileNumber = -1
        self.hitable = False
        self.waiting = False
        self.layer = layer
        self.hovered = False
        if self.layer == "base":
            self.sheetNum = 326
        else:
            self.sheetNum = "-"
        tiles.add(self)
        self.overP = False
        self.teleport = None
        self.npc = None
    
    def update(self):
        self.rect = py.Rect(0, 0, 30 * scale, 30 * scale)
        self.rect.centerx = map.get_rect()[2] / 2 + ((-scrollX + (30 * self.posx)) * scale)
        self.rect.centery = map.get_rect()[3] / 2 + ((scrollY + (30 * self.posy)) * scale)
        if self.rect.colliderect(map.get_rect()):
            if self.sheetNum == 0:
                self.image = py.Surface((30, 30))
                self.image.fill((100, 0, 255))
            else:
                if not self.sheetNum == "-":
                    self.image = tileImages[self.sheetNum]
                else:
                    self.image = py.Surface((0, 0))
            if not self.sheetNum == "-":
                self.image = py.transform.scale(self.image, (int(30 * scale), int(30 * scale)))
                if self.layer != eLayer:
                    self.image.fill((255, 255, 255, 200), special_flags=py.BLEND_RGBA_MULT)
                map.blit(self.image, self.rect)
            
            c = None
            if not scale < 0.5:
                if self.hitable:
                    c = (255, 0, 0)
                elif self.layer == "base":
                    c = (0, 0, 0)
                elif self.layer == "top" and self.overP:
                    c = (0, 255, 255)
                elif self.layer == "top" and self.teleport != None:
                    c = (0, 255, 0)
                elif self.layer == "top" and self.npc != None:
                    c = (255, 255, 0)
                    img = SpriteSheet(self.npc["Image"], 4, 3).images[1]
                    img.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
                    img = py.transform.scale(img, (int(30 * scale), int(30 * scale)))
                    map.blit(img, self.rect)
                    
                if c != None:
                    py.draw.rect(map, c, self.rect, 1)
            
            
        
            if self.rect.collidepoint((py.mouse.get_pos()[0], py.mouse.get_pos()[1])):
                if map.get_rect().collidepoint((py.mouse.get_pos()[0], py.mouse.get_pos()[1])):
                    if eLayer == self.layer:
                        self.hovered = True
                        h = py.Surface((int(30 * scale), int(30 * scale))).convert_alpha()
                        h.fill((255, 255, 255, 100))
                        map.blit(h, self.rect)
            else:
                self.hovered = False
            if self.hovered:
                global hoverPos
                hoverPos = (int(self.posx - (size[0] / 2)), int(self.posy - (size[1] / 2)))
                global hoverData
                hoverData = {"Teleport": self.teleport, "Skin": self.sheetNum, "Layer":self.layer, "Hitable":self.hitable}
                if py.mouse.get_pressed()[0]:
                    if not editHitable and not overPlayer and not makeTeleport and not makeNPC:
                        if eLayer == self.layer:
                            self.sheetNum = selected
                    elif not self.waiting:
                        if self.layer == "base" and editHitable:
                            self.hitable = not self.hitable
                            self.waiting = True
                        if self.layer == "top" and overPlayer:
                            self.overP = not self.overP
                            self.waiting = True
                        if self.layer == "top" and makeTeleport:
                            tpid = textInput((300, 275), 40, 3)
                            font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
                            label = font.render("Teleport ID:", 1, (0, 0, 0))
                            while not tpid.done:
                                screen.blit(label, (300, 200))
                                tpid.update()
                                py.display.flip()
                            self.teleport = outText
                            global makeTeleport
                            makeTeleport = False
                            self.waiting = True
                        if self.layer == "top" and makeNPC:
                            global selectedNpc
                            if selectedNpc != self.npc:
                                self.npc = selectedNpc.copy()
                                self.waiting = True
                            
                if py.mouse.get_pressed()[2]:
                    if eLayer == self.layer and self.layer == "top":
                        self.sheetNum = "-"
            if not py.mouse.get_pressed()[0]:
                self.waiting = False
        
        
class image(py.sprite.Sprite):
    
    def __init__(self, slotNum):
        super().__init__()
        self.image = py.transform.scale(tileImages[slotNum], (10, 10))
        self.posx = (slotNum % 32) * 10
        self.posy = int((slotNum / 32)) * 10
        self.slotNum = slotNum
        self.hovered = False
    
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posx, self.posy)
        global selected
        pallet.blit(self.image, self.rect)   
        if selected == self.slotNum:
            py.draw.rect(pallet, (255, 0, 0), self.rect, 1)
        if self.rect.collidepoint((py.mouse.get_pos()[0] - 600, py.mouse.get_pos()[1])):
            self.hovered = True
        else:
            self.hovered = False
        if self.hovered:
            for event in events:
                if event.type == py.MOUSEBUTTONDOWN:
                    if py.mouse.get_pressed()[0]:
                        selected = self.slotNum

class npcImage(py.sprite.Sprite):
    
    def __init__(self, num, image):
        super().__init__()
        self.image = py.transform.scale(SpriteSheet(image, 4, 3).images[1], (30, 30))
        self.posx = (num % 3) * 30
        self.posy = int((num / 3)) * 30
        self.num = num
        self.sheet = image
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posx, self.posy)
        pallet.blit(self.image, self.rect)
        if self.rect.collidepoint((py.mouse.get_pos()[0] - 600, py.mouse.get_pos()[1])):
            self.hovered = True
        else:
            self.hovered = False
        if selectedNpc["Image"] == self.sheet:
            py.draw.rect(pallet, (255, 0, 0), self.rect, 1)
        if self.hovered:
            for event in events:
                if event.type == py.MOUSEBUTTONDOWN:
                    if py.mouse.get_pressed()[0]:
                        selectedNpc["Image"] = self.sheet
                        createNPC()
                        
        
class textInput():
    
    def __init__(self, pos, fontSize, characters):
        self.font = py.font.Font("Resources/Fonts/RPGSystem.ttf", fontSize)
        self.rect = py.Rect(pos, self.font.size("W" * characters))
        self.rect.width += 20
        self.rect.height += 20
        self.string = []
        self.pos = pos
        self.characters = characters
        self.shift = False
        self.done = False
    
    def draw(self):
        py.draw.rect(screen, (255, 255, 255), self.rect)
        py.draw.rect(screen, (0, 0, 0), self.rect, 5)
        x = self.pos[0] + 10
        y = self.pos[1] + 10
        for letter in self.string:
            ren = self.font.render(letter, 1, (0, 0, 0))
            screen.blit(ren, (x, y))
            x += self.font.size(letter)[0] + 5
    
    def update(self):
        global textEdit
        textEdit = True
        events = py.event.get()
        for event in events:
            if event.type == py.KEYDOWN:
                if len(self.string) < self.characters:
                    if py.key.name(event.key) in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
                        if py.key.get_mods() == py.KMOD_LSHIFT:
                            let = py.key.name(event.key).upper()
                        else:
                            let = py.key.name(event.key)
                        self.string.append(let)
                    if event.key == py.K_SPACE:
                        self.string.append(" ")
                if event.key == py.K_BACKSPACE:
                    if len(self.string) > 0:
                        self.string.pop(-1)
        self.draw()
        
        label = self.font.render("GO", 1, (0, 0, 0))
        butRect = py.Rect(self.rect.topright, (self.rect.height, self.rect.height))
        butRect.centerx += 5
        py.draw.rect(screen, (255, 255, 255), butRect)
        py.draw.rect(screen, (0, 0, 0), butRect, 5)
        screen.blit(label, (butRect.centerx - self.font.size("GO")[0] / 2, butRect.centery - self.font.size("GO")[1] / 2))
        for event in events:
            if event.type == py.MOUSEBUTTONDOWN:
                if butRect.collidepoint(py.mouse.get_pos()):
                    global outText
                    outText = "".join(self.string)
                    self.done = True
                    py.time.wait(100)
        
        py.display.flip()





tileset = py.image.load("Resources/Images/Main_Tileset.png")

def getGrid(tileset):
    columns = 32
    rows = 63
    width = tileset.get_size()[0] / columns
    height = tileset.get_size()[1] / rows
    all = []
    for h in range(rows):
        for w in range(columns):
            image = py.Surface([width, height], py.SRCALPHA, 32).convert_alpha()
            image.blit(tileset, (0, 0), (w * width, h * height, width, height))
            all.append(image)
    return all

def save():
    outMap = []
    for y in range(size[1]):
        outMap.append([])
        for x in range(size[0]):
            outMap[y].append("")
    for tile in baseTiles:
        if tile.hitable:
            h = "#"
        else:
            h = ""
        outMap[tile.posy][tile.posx] = h + str(tile.sheetNum)
    
    print("[[")
    for i in outMap:
        print(str(i) + ",")
    print("], ")
    
    for tile in topTiles:
        if tile.overP:
            h = "+"
        elif tile.teleport != None:
            h = "&" + str(tile.teleport) + "|"
        elif tile.npc != None:
            h = "%" + str(tile.npc) + "|"
        else:
            h = ""
        outMap[tile.posy][tile.posx] = h + str(tile.sheetNum)
    
    print("[")
    for i in outMap:
        print(str(i) + ",")
    print("]]")

def toolTip():
    if not hoverPos == None:
        font = py.font.SysFont("Calibri", 20, True)
        label = font.render(str(hoverPos), 1, (255, 0, 0), (255, 255, 255, 100))
        screen.blit(label, py.mouse.get_pos())
        ymod = font.size(str(hoverPos))[1]
        for k, v in hoverData.items():
            if not v == None:
                label = font.render(str(k) + ": " + str(v), 1, (255, 0, 0), (255, 255, 255, 100))
                screen.blit(label, (py.mouse.get_pos()[0], py.mouse.get_pos()[1] + ymod))
                ymod += font.size(str(k) + ": " + str(v))[1]


def createNPC():
    font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
    label = font.render("NPC Name:", 1, (0, 0, 0))
    inp = textInput((300, 275), 20, 16)
    while not inp.done:
        screen.blit(label, (300, 200))
        inp.update()
        py.display.flip()
    selectedNpc["Name"] = outText
    screen.fill((255, 255, 255))
    
    label = font.render("NPC Attack:", 1, (0, 0, 0))
    inp = textInput((300, 275), 20, 2)
    while not inp.done:
        screen.blit(label, (300, 200))
        inp.update()
        py.display.flip()
    selectedNpc["Attack"] = outText
    screen.fill((255, 255, 255))
    
    label = font.render("NPC Health:", 1, (0, 0, 0))
    inp = textInput((300, 275), 20, 2)
    while not inp.done:
        screen.blit(label, (300, 200))
        inp.update()
        py.display.flip()
    selectedNpc["Health"] = outText
    screen.fill((255, 255, 255))
    
    label = font.render("NPC Speed:", 1, (0, 0, 0))
    inp = textInput((300, 275), 20, 2)
    while not inp.done:
        screen.blit(label, (300, 200))
        inp.update()
        py.display.flip()
    selectedNpc["Speed"] = outText
    screen.fill((255, 255, 255))

py.init()

screen = py.display.set_mode((920, 630), py.DOUBLEBUF)

map = py.Surface((600, 550))
pallet = py.Surface((400, 630))
options = py.Surface((1000, 80))

size = (10, 10)
scrollX = 0
scrollY = 0
scale = 2
selected = 0
selectedNpc = {"Image":None, "Name":None, "Health":None, "Attack":None, "Speed":None}
editHitable = False
eLayer = False
layerBool = False
overPlayer = False
hoverPos = None
hoverData = None
makeTeleport = False
makeNPC = False

baseTiles = py.sprite.Group()
topTiles = py.sprite.Group()
tiles = py.sprite.Group()
for x in range(size[0]):
    for y in range(size[1]):
        baseTiles.add(tile(x, y, "base"))
        topTiles.add(tile(x, y, "top"))

palletImages = py.sprite.Group()
tileImages = getGrid(tileset)
for i in range(0, len(tileImages)):
    palletImages.add(image(i))

npcImages = py.sprite.Group()
num = 0
for i in listdir("Resources\Images\EnemySkins"):
    npcImages.add(npcImage(num, "Resources/Images/EnemySkins/" + i))
    num += 1
    

clock = py.time.Clock()

py.time.set_timer(py.USEREVENT, 1000) #1 sec delay

buttons = py.sprite.Group()
buttons.add(toggleButton("Hitable", "editHitable", (10, 20)))
buttons.add(toggleButton("Edit Top Layer", "layerBool", (150, 20)))
buttons.add(toggleButton("Over Player", "overPlayer", (380, 20)))
buttons.add(toggleButton("Teleport", "makeTeleport", (10, 50)))
buttons.add(toggleButton("Make NPC", "makeNPC", (170, 50)))

textEdit = False
outText = ""

while True:
    py.event.pump()
    hoverPos = None
    events = []
    events = py.event.get()
    clock.tick(30)
    screen.fill((255, 255, 255))
    map.fill((0, 0, 255))
    pallet.fill((255, 255, 255))
    options.fill((0, 255, 255))
    baseTiles.update()
    topTiles.update()
    if not makeNPC:
        palletImages.update()
    if makeNPC:
        npcImages.update()
    buttons.update()
    
    if layerBool:
        eLayer = "top"
    else:
        eLayer = "base"

    keysPressed = py.key.get_pressed()
    speed = 20
    if keysPressed[py.K_d]:
        scrollX += speed
    if keysPressed[py.K_a]:
        scrollX -= speed
    if keysPressed[py.K_w]:
        scrollY += speed
    if keysPressed[py.K_s]:
        scrollY -= speed
    for event in events:
        if event.type == py.MOUSEBUTTONUP:
            if event.button == 4:
                scale += 0.1
            if event.button == 5:
                scale -= 0.1
            scale = round(scale, 1)
            if scale <= 0.1:
                scale = 0.1
        if event.type == py.KEYDOWN:
            if event.key == py.K_RETURN:
                outMap = save()
        if event.type == py.QUIT:
            save()
            sys.exit()
                
    screen.blit(map, (0, 0))
    screen.blit(options, (0, 550))
    screen.blit(pallet, (600, 0))
    toolTip()
    py.display.flip()