import entityClasses
import Variables as v
import pygame as py



class beam(py.sprite.Sprite):
    
    def __init__(self, spellImage, castImage, master):
        super().__init__()
        self.spellSheet = entityClasses.SpriteSheet(spellImage, 4, 1)
        self.castSheet = entityClasses.SpriteSheet(castImage, 1, 9)
        self.aniCyclePos = 11
        self.sizeCyclePos = 0
        self.attCyclePos = 0
        self.direction = "Up"
        self.attacking = True
        self.master = master
    
    def update(self):
        if self.attacking:
            v.playerStopped = True
            if self.aniCyclePos == 11:
                self.direction = v.playerDirection
                v.damagesNPCs.add(self)
            if self.aniCyclePos <= 11 and self.aniCyclePos > 3:
                self.image = self.castSheet.images[8 - (self.aniCyclePos - 3)]
            if self.aniCyclePos <= 3:
                self.image = self.spellSheet.images[self.aniCyclePos]
            if self.aniCyclePos > 0:
                for event in v.events:
                    if event.type == py.USEREVENT + 1:
                        self.aniCyclePos -= 1
            if self.aniCyclePos == 0:
                self.attCyclePos += 1
            if self.attCyclePos >= 30:
                self.attacking = False
                self.aniCyclePos = 11
                self.sizeCyclePos = 0
                self.attCyclePos = 0
                v.currentSpells.remove(self)
                v.damagesNPCs.remove(self)
            if self.aniCyclePos <= 3:
                if self.sizeCyclePos < 200:
                    self.sizeCyclePos += 10

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
            
            if self.aniCyclePos <= 3:
                self.image = py.transform.scale(self.image, (self.sizeCyclePos, self.image.get_rect().height))
                self.image = py.transform.rotate(self.image, rotate)
                self.rect = self.image.get_rect()
                self.rect.center = (v.screen.get_rect()[2]/2, v.screen.get_rect()[3]/2)
                if self.direction == "Up" or self.direction == "Down":
                    self.rect.centery = (self.rect.centery + (mod * (self.rect.height / 2))) 
                if self.direction == "Left" or self.direction == "Right":
                    self.rect.centerx = (self.rect.centerx + (mod * (self.rect.width / 2)))
            else:
                self.image = py.transform.scale(self.image, (self.image.get_rect().width * v.scale, self.image.get_rect().height * v.scale))
                self.rect = self.image.get_rect()
                self.rect.center = (v.screen.get_rect()[2]/2, v.screen.get_rect()[3]/2)
            
            for thing in v.hitList:
                if self.rect.colliderect(thing.rect):
                    if not thing.ID == "playerHitbox":
                        self.sizeCyclePos -= 10
                        if self.sizeCyclePos < 0:
                            self.sizeCyclePos = 0
            for thing in v.allNpc:
                if self.rect.colliderect(thing.rect):
                    self.sizeCyclePos -= 10
                    if self.sizeCyclePos < 0:
                        self.sizeCyclePos = 0
            
            self.rect.centery += (5 * v.scale)
                