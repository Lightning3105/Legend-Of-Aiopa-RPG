import Variables as v
import pygame as py
import entityClasses

class inventory():
    
    def __init__(self):
        self.size = 3
        self.contents = []
    
    def update(self):
        self.grey()
        self.background()
        self.player()
        self.equipedSlots("Weapon")
        
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
        item = v.equipped[slot]
        size = (30, 30)
        if slot == "Weapon":
            pos = (70, 100)
            image = py.image.load("Resources/Images/Inventory Icons/Weapon.png").convert_alpha()
            image = py.transform.scale(image, size)
        
        
        rect = py.Rect(pos, size)
        py.draw.rect(v.screen, (255, 255, 255), rect, 2)
        if rect.collidepoint(py.mouse.get_pos()):
            pass
        else:
            image.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
        v.screen.blit(image, pos)
        
        if not item == None:
            icon = py.transform.scale(item.icon, (28, 28))
            v.screen.blit(icon, pos)
        