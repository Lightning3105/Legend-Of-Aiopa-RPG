import mapMakerVariables as v
import pygame as py

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
        v.tiles.add(self)
        self.overP = False
        self.teleport = None
        self.npc = None
    
    def update(self):
        self.rect = py.Rect(0, 0, 30 * v.scale, 30 * v.scale)
        self.rect.centerx = v.map.get_rect()[2] / 2 + ((-v.scrollX + (30 * self.posx)) * v.scale)
        self.rect.centery = v.map.get_rect()[3] / 2 + ((v.scrollY + (30 * self.posy)) * v.scale)
        if self.rect.colliderect(v.map.get_rect()):
            if self.sheetNum == 0:
                self.image = py.Surface((30, 30))
                self.image.fill((100, 0, 255))
            else:
                if not self.sheetNum == "-":
                    self.image = v.tileImages[self.sheetNum]
                else:
                    self.image = py.Surface((0, 0))
            if not self.sheetNum == "-":
                self.image = py.transform.scale(self.image, (int(30 * v.scale), int(30 * v.scale)))
                if self.layer != v.eLayer:
                    self.image.fill((255, 255, 255, 200), special_flags=py.BLEND_RGBA_MULT)
                v.map.blit(self.image, self.rect)
            
            c = None
            if not v.scale < 0.5:
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
                    img = py.transform.v.scale(img, (int(30 * v.scale), int(30 * v.scale)))
                    v.map.blit(img, self.rect)
                    
                if c != None:
                    py.draw.rect(v.map, c, self.rect, 1)
            
            
        
            if self.rect.collidepoint((py.mouse.get_pos()[0], py.mouse.get_pos()[1])):
                if v.map.get_rect().collidepoint((py.mouse.get_pos()[0], py.mouse.get_pos()[1])):
                    if v.eLayer == self.layer:
                        self.hovered = True
                        h = py.Surface((int(30 * v.scale), int(30 * v.scale))).convert_alpha()
                        h.fill((255, 255, 255, 100))
                        v.map.blit(h, self.rect)
            else:
                self.hovered = False
            if self.hovered:
                v.hoverPos = (int(self.posx - (v.size[0] / 2)), int(self.posy - (v.size[1] / 2)))
                v.hoverData = {"Teleport": self.teleport, "Skin": self.sheetNum, "Layer":self.layer, "Hitable":self.hitable}
                if py.mouse.get_pressed()[0]:
                    if not v.editHitable and not v.overPlayer and not v.makeTeleport and not v.makeNPC:
                        if v.eLayer == self.layer:
                            self.sheetNum = v.selected
                    elif not self.waiting:
                        if self.layer == "base" and v.editHitable:
                            self.hitable = not self.hitable
                            self.waiting = True
                        if self.layer == "top" and v.overPlayer:
                            self.overP = not self.overP
                            self.waiting = True
                        if self.layer == "top" and v.makeTeleport:
                            tpid = textInput((300, 275), 40, 3)
                            font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
                            label = font.render("Teleport ID:", 1, (0, 0, 0))
                            while not tpid.done:
                                v.screen.blit(label, (300, 200))
                                tpid.update()
                                py.display.flip()
                            self.teleport = outText
                            v.makeTeleport = False
                            self.waiting = True
                        if self.layer == "top" and v.makeNPC:
                            if v.selectedNpc != self.npc:
                                self.npc = v.selectedNpc.copy()
                                self.waiting = True
                            
                if py.mouse.get_pressed()[2]:
                    if v.eLayer == self.layer and self.layer == "top":
                        self.sheetNum = "-"
            if not py.mouse.get_pressed()[0]:
                self.waiting = False
        
        
class image(py.sprite.Sprite):
    
    def __init__(self, slotNum):
        super().__init__()
        self.image = py.transform.scale(v.tileImages[slotNum], (10, 10))
        self.posx = (slotNum % 32) * 10
        self.posy = int((slotNum / 32)) * 10
        self.slotNum = slotNum
        self.hovered = False
    
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posx, self.posy)
        v.pallet.blit(self.image, self.rect)   
        if v.selected == self.slotNum:
            py.draw.rect(v.pallet, (255, 0, 0), self.rect, 1)
        if self.rect.collidepoint((py.mouse.get_pos()[0] - 600, py.mouse.get_pos()[1])):
            self.hovered = True
        else:
            self.hovered = False
        if self.hovered:
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    if py.mouse.get_pressed()[0]:
                        v.selected = self.slotNum


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