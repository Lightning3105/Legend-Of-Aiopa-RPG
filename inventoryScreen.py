import Variables as v
import pygame as py
import entityClasses

class inventory(): #TODO: Split into inventory and inventoryScreen
    
    def __init__(self):
        self.size = 3
        self.contents = []
        self.grabbed = None
        self.hovering = None
    
    def update(self):
        self.hovering = None
        self.grey()
        self.background()
        self.player()
        self.equipedSlots("Weapon")
        for i in range(0, 24):
            self.inventorySlots(i)
        self.drag()
        
        
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
        sheet = entityClasses.SpriteSheet(sheetImage, 4, 3)
        image = sheet.images[7]
        image = py.transform.scale(image, (image.get_rect().width * 5, image.get_rect().height * 5))
        v.screen.blit(image, pos)
    
    def equipedSlots(self, slot):
        hovered = False
        item = v.equipped[slot]
        size = (50, 50)
        if slot == "Weapon":
            pos = (70, 100)
            image = py.image.load("Resources/Images/Inventory Icons/Weapon.png").convert_alpha()
        
        image = py.transform.scale(image, size)
        rect = py.Rect(pos, size)
        py.draw.rect(v.screen, (255, 255, 255), rect, 2)
        if rect.collidepoint(py.mouse.get_pos()):
            hovered = True
            self.hovering = ("Equiped", slot)
        else:
            image.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
        v.screen.blit(image, pos)
        
        if not item == None:
            icon = py.transform.scale(item.icon, (size[0] - 2, size[1] - 2))
            v.screen.blit(icon, pos)
            if hovered:
                for event in v.events:
                    if event.type == py.MOUSEBUTTONDOWN:
                        self.grabbed = item
        
        
    
    def inventorySlots(self, slotNum):
        size = (50, 50)
        hovered = False
        if slotNum >= len(self.contents):
            image = py.image.load("Resources/Images/Inventory Icons/Empty.png").convert_alpha()
        else:
            image = py.Surface(size).convert_alpha()
            image.fill((255, 255, 255))
        posx = 280 + (slotNum % 6) * 50
        posy = (int(slotNum / 6) * 50) + 200
        
        pos = (posx, posy)
        
        image = py.transform.scale(image, size)
        
        
        rect = py.Rect(pos, size)
        py.draw.rect(v.screen, (255, 255, 255), rect, 2)
        
        if rect.collidepoint(py.mouse.get_pos()):
            hovered = True
            self.hovering = ("Inventory", slotNum)
        else:
            image.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
        v.screen.blit(image, pos)
        
        try:
            icon = py.transform.scale(self.contents[slotNum].icon, (size[0] - 4, size[1] - 4))
            icon.convert_alpha()
            v.screen.blit(icon, pos)
            if hovered:
                for event in v.events:
                    if event.type == py.MOUSEBUTTONDOWN:
                        self.grabbed = self.contents[slotNum]
        except:
            pass
        
        
    def drag(self):
        if not self.grabbed == None:
            size = (50, 50)
            image = self.grabbed.icon
            image = py.transform.scale(image, size)
            pos = py.mouse.get_pos()
            v.screen.blit(image, pos)
            rect = py.Rect(pos, size)
            py.draw.rect(v.screen, (200, 200, 200), rect, 2)
            if not py.mouse.get_pressed()[0]:
                self.grabbed = None
                                       
        