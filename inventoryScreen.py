import Variables as v
import pygame as py
import entityClasses
from random import randint


class inventory():
    
    def __init__(self):
        self.size = 10
        self.contents = []
    
    def add(self, item):
        if not item == None:
            if not item in self.contents:
                self.contents.append(item)
                return True
        return False
    
    def remove(self, item):
        if item in self.contents:
            self.contents.remove(item)


class inventoryScreen(): #TODO: Split into inventory and inventoryScreen
    
    def __init__(self):
        self.grabbed = None
        self.grabbedOrigin = None
        self.hovering = None
        self.inventorySlots = py.sprite.Group()
        for i in range(0, 24):
            self.inventorySlots.add(self.inventorySlot(i, self))
        self.inventorySlots.add(self.discardSlot(self))
        self.equippedSlots = py.sprite.Group()
        self.equippedSlots.add(self.equippedSlot("Weapon", self))
    
    def update(self):
        self.hovering = None
        self.grey()
        self.background()
        self.player()
        self.inventorySlots.update()
        self.equippedSlots.update()
        self.drag()
    
    def save(self):
            for thing in self.inventorySlots:
                thing.save()
            for thing in self.equippedSlots:
                thing.save()
        
        
    def grey(self):
        grey = py.Surface((v.screen.get_rect()[2], v.screen.get_rect()[3])).convert_alpha()
        grey.fill((20, 20, 20, 200))
        v.screen.blit(grey, (0, 0))
    
    def background(self):
        size = v.screen.get_rect().size
        size = (size[0] - 100, size[1] - 100)
        innerRect = py.Rect(50, 50, size[0], size[1])
        outerRect = py.Rect(40, 40, size[0] + 20, size[1] + 20)
        py.draw.rect(v.screen, py.Color(153, 76, 0), outerRect)
        py.draw.rect(v.screen, py.Color(255, 178, 102), innerRect)
    
    def player(self):
        pos = (100, 100)
        sheetImage = py.image.load(v.appearance["Body"])
        sheetImage.blit(py.image.load(v.appearance["Face"]), (0, 0))
        sheetImage.blit(py.image.load(v.appearance["Dress"]), (0, 0))
        sheetImage.blit(py.image.load(v.appearance["Hair"]), (0, 0))
        sheet = entityClasses.SpriteSheet(sheetImage, 4, 3)
        image = sheet.images[7]
        image = py.transform.scale(image, (image.get_rect().width * 5, image.get_rect().height * 5))
        v.screen.blit(image, pos)
    
    class equippedSlot(py.sprite.Sprite):
        
        def __init__(self, slot, master):
            super().__init__()
            self.hovered = False
            self.item = v.equipped[slot]
            self.size = (50, 50)
            self.master = master
            self.slot = slot
            self.equipType = slot
        
        def save(self):
            v.equipped[self.slot] = self.item
            v.inventory.remove(self.item)
            
        
        def update(self):
            if self.slot == "Weapon":
                self.pos = (70, 100)
                self.image = py.image.load("Resources/Images/Inventory Icons/Weapon.png").convert_alpha()
            image = py.transform.scale(self.image, self.size)
            rect = py.Rect(self.pos, self.size)
            py.draw.rect(v.screen, (255, 255, 255), rect, 2)
            if rect.collidepoint(py.mouse.get_pos()):
                self.hovered = True
                self.master.hovering = self
            else:
                self.hovered = False
                image.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
            v.screen.blit(image, self.pos)
            
            if not self.item == None:
                icon = py.transform.scale(self.item.icon, (self.size[0] - 2, self.size[1] - 2))
                if self.master.grabbed == self.item:
                    icon.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(icon, self.pos)
                if self.hovered:
                    for event in v.events:
                        if event.type == py.MOUSEBUTTONDOWN:
                            self.master.grabbed = self.item
                            self.master.grabbedOrigin = self
        
        
        
    
    class inventorySlot(py.sprite.Sprite):
        
        def __init__(self, slotNum, master):
            super().__init__()
            self.size = (50, 50)
            self.hovered = False
            self.slotNum = slotNum
            self.master = master
            try:
                self.item = v.inventory.contents[self.slotNum]
            except:
                self.item = None
            self.equipType = "Item"
        
        def save(self):
            v.inventory.add(self.item)
        
        def update(self):
            if self.item == None:
                image = py.image.load("Resources/Images/Inventory Icons/Empty.png").convert_alpha()
            else:
                image = py.Surface(self.size).convert_alpha()
                image.fill((255, 255, 255))
            posx = 280 + (self.slotNum % 6) * 50
            posy = (int(self.slotNum / 6) * 50) + 200
            
            pos = (posx, posy)
            
            image = py.transform.scale(image, self.size)
            
            
            rect = py.Rect(pos, self.size)
            py.draw.rect(v.screen, (255, 255, 255), rect, 2)
            
            if rect.collidepoint(py.mouse.get_pos()):
                self.hovered = True
                self.master.hovering = self
            else:
                self.hovered = False
                image.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
            v.screen.blit(image, pos)
            
            try:
                icon = py.transform.scale(self.item.icon, (self.size[0] - 4, self.size[1] - 4))
                icon.convert_alpha()
                if self.master.grabbed == self.item:
                    icon.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(icon, pos)
                if self.hovered:
                    for event in v.events:
                        if event.type == py.MOUSEBUTTONDOWN:
                            self.master.grabbed = self.item
                            self.master.grabbedOrigin = self
            except:
                pass
            
    class discardSlot(py.sprite.Sprite):
        
        def __init__(self, master):
            super().__init__()
            self.size = (50, 50)
            self.hovered = False
            self.master = master
            self.equipType = "Item"
            self.item = None
        
        def save(self):
            pass
        
        def update(self):
            image = py.image.load("Resources/Images/Inventory Icons/Discard.png").convert_alpha()
            
            posx = 229
            posy = 350
            
            pos = (posx, posy)
            image = py.transform.scale(image, self.size)
            
            rect = py.Rect(pos, self.size)
            py.draw.rect(v.screen, (255, 0, 0), rect, 2)
            
            if rect.collidepoint(py.mouse.get_pos()):
                self.hovered = True
                self.master.hovering = self
                image.fill((200, 0, 0), special_flags=py.BLEND_RGBA_MULT)
            else:
                self.hovered = False
                image.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
            v.screen.blit(image, pos)
            if not self.item == None:
                v.inventory.remove(self.item)
                entityClasses.droppedItem(self.item, (v.playerPosX + randint(-5, 5), v.playerPosY + randint(-5, 5)))
                self.item = None
        
    def drag(self):
        if not self.grabbed == None:
            size = (50, 50)
            image = self.grabbed.icon
            image = py.transform.scale(image, size)
            pos = py.mouse.get_pos()
            v.screen.blit(image, pos)
            rect = py.Rect(pos, size)
            py.draw.rect(v.screen, (200, 200, 200), rect, 2)
            for event in v.events:
                if event.type == py.MOUSEBUTTONUP:
                    if not self.hovering == None:
                        if self.grabbed.equipType == self.hovering.equipType or self.hovering.equipType == "Item":
                            old = self.grabbed
                            self.grabbedOrigin.item = self.hovering.item
                            self.hovering.item = old
                            self.grabbed = None
            if not py.mouse.get_pressed()[0]:
                self.grabbed = None
                self.grabbedOrigin = None
                                       
        