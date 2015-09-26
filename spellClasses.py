import entityClasses
import Variables as v
import pygame as py



class manaBeam(py.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.sheet = entityClasses.SpriteSheet("Resources/Images/manaBeam.png", 4, 1)
        self.aniCyclePos = 3
        self.sizeCyclePos = 0
        self.attCyclePos = 0
        self.direction = "Up"
        self.attacking = True
    
    def update(self):
        if self.attacking:
            if self.aniCyclePos == 3:
                self.direction = v.playerDirection
                v.damagesNPCs.add(self)
            if self.aniCyclePos > 0:
                for event in v.events:
                    if event.type == py.USEREVENT + 1:
                        self.aniCyclePos -= 1
            if self.aniCyclePos == 0:
                self.attCyclePos += 1
            if self.attCyclePos >= 30:
                self.attacking = False
                v.currentSpells.remove(self)
                v.damagesNPCs.remove(self)
            if self.sizeCyclePos < 200:
                self.sizeCyclePos += 25
            
            self.image = self.sheet.images[self.aniCyclePos]
            mod = 1
            if self.direction == "Up":
                rotate = -90
                mod = -1
            if self.direction == "Right":
                rotate = 180
                mod = 1
            if self.direction == "Down":
                rotate = 90
                mod = 1
            if self.direction == "Left":
                rotate = 0
                mod = -1
            self.image = py.transform.scale(self.image, (self.sizeCyclePos, self.image.get_rect().height))
            self.image = py.transform.rotate(self.image, rotate)
            self.rect = self.image.get_rect()
            self.rect.center = (v.screen.get_rect()[2]/2, v.screen.get_rect()[3]/2)
            
            if self.direction == "Up" or self.direction == "Down":
                self.rect.centery = self.rect.centery + (mod * (self.rect.height / 2))
                print(mod * (self.rect.width / 2))
            if self.direction == "Left" or self.direction == "Right":
                self.rect.centerx = self.rect.centerx + (mod * (self.rect.width / 2))
                