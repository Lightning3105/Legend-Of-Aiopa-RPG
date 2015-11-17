import entityClasses
import Variables as v
import pygame as py
import random



class beam(py.sprite.Sprite):
    
    def __init__(self, spellImage, castImage, master):
        super().__init__()
        self.spellSheet = entityClasses.SpriteSheet(spellImage, 4, 1)
        self.castSheet = entityClasses.SpriteSheet(castImage, 1, 9)
        self.aniCyclePos = 11
        self.sizeCyclePos = 0
        self.attCyclePos = 0
        self.direction = "Up"
        self.attacking = False
        self.master = master
        self.coolDownTime = master.attributes["Cooldown"]
        self.coolDown = self.coolDownTime
        self.firstTime = True
    
    def update(self):
        if self.attacking:
            v.playerStopped = True
            v.playerActing = True
            if self.firstTime:
                self.direction = v.playerDirection
                v.damagesNPCs.add(self)
                v.playerMana -= self.master.attributes["Mana"]
                self.firstTime = False
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
                self.firstTime = True
                self.coolDown = 0
                self.aniCyclePos = 11
                self.sizeCyclePos = 0
                self.attCyclePos = 0
                v.damagesNPCs.remove(self)
                self.image = py.Surface((0, 0))
                self.rect = py.Rect(0, 0, 0, 0)
            if self.aniCyclePos <= 3:
                if self.sizeCyclePos < 100:
                    self.sizeCyclePos += 5

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
                self.image = py.transform.scale(self.image, (int(self.sizeCyclePos * v.scale), int(self.image.get_rect().height / 2  * v.scale)))
                self.image = py.transform.rotate(self.image, rotate)
                self.rect = self.image.get_rect()
                self.rect.center = (v.screen.get_rect()[2]/2, v.screen.get_rect()[3]/2)
                if self.direction == "Up" or self.direction == "Down":
                    self.rect.centery = (self.rect.centery + (mod * (self.rect.height / 2))) 
                if self.direction == "Left" or self.direction == "Right":
                    self.rect.centerx = (self.rect.centerx + (mod * (self.rect.width / 2)))
            else:
                self.image = py.transform.scale(self.image, (int(self.image.get_rect().width * v.scale), int(self.image.get_rect().height * v.scale)))
                self.rect = self.image.get_rect()
                self.rect.center = (v.screen.get_rect()[2]/2, v.screen.get_rect()[3]/2)
            
            for thing in v.hitList:
                if self.rect.colliderect(thing.rect):
                    if not thing.ID == "playerHitbox":
                        self.sizeCyclePos -= 5
                        if self.sizeCyclePos < 0:
                            self.sizeCyclePos = 0
            """for thing in v.allNpc:
                if self.rect.colliderect(thing.rect):
                    self.sizeCyclePos -= 10
                    if self.sizeCyclePos < 0:
                        self.sizeCyclePos = 0"""
            
            self.rect.centery += int(5 * v.scale)
        else:
            self.image = py.Surface((0, 0))
            self.rect = py.Rect(0, 0, 0, 0)
            if self.coolDown < self.coolDownTime:
                for event in v.events:
                    if event.type == py.USEREVENT + 2:
                        self.coolDown += 1

class lightning(py.sprite.Sprite):
    
    def __init__(self, spellImage, castImage, master):
        super().__init__()
        self.spellSheet = entityClasses.SpriteSheet(spellImage, 1, 8)
        self.castSheet = entityClasses.SpriteSheet(castImage, 1, 9)
        self.aniCyclePos = 31
        self.sizeCyclePos = 0
        self.attCyclePos = 0
        self.direction = "Up"
        self.attacking = False
        self.master = master
        self.coolDownTime = master.attributes["Cooldown"]
        self.coolDown = self.coolDownTime
        self.firstTime = True
        self.rotcyc = 0
    
    def update(self):
        if self.attacking:
            v.playerStopped = True
            v.playerActing = True
            if self.firstTime:
                self.direction = v.playerDirection
                v.damagesNPCs.add(self)
                v.playerMana -= self.master.attributes["Mana"]
                self.firstTime = False
            if self.aniCyclePos <= 31 and self.aniCyclePos > 23:
                self.image = self.castSheet.images[28 - (self.aniCyclePos - 3)]
            if self.aniCyclePos <= 23:
                self.image = self.spellSheet.images[self.aniCyclePos % 8]
            if self.aniCyclePos > 0:
                for event in v.events:
                    if event.type == py.USEREVENT + 1:
                        self.aniCyclePos -= 1
            if self.aniCyclePos == 0:
                self.attCyclePos += 1
            if self.attCyclePos >= 30:
                self.attacking = False
                self.firstTime = True
                self.coolDown = 0
                self.aniCyclePos = 31
                self.attCyclePos = 0
                v.damagesNPCs.remove(self)
                self.image = py.Surface((0, 0))
                self.rect = py.Rect(0, 0, 0, 0)

            mod = 1
            if self.direction == "Up":
                rotate = -180
                mod = -1
            if self.direction == "Right":
                rotate = 90
                mod = 1
            if self.direction == "Down":
                rotate = 0
                mod = 1
            if self.direction == "Left":
                rotate = -90
                mod = -1
            
            if self.aniCyclePos <= 31 and self.aniCyclePos > 23:
                mod /= 2
            
            
            self.image = py.transform.rotate(self.image, rotate)
            self.image = py.transform.scale(self.image, (int(self.image.get_rect().width * v.scale/1.5), int(self.image.get_rect().height * v.scale/1.5)))
            if self.aniCyclePos <= 23:
                self.rotcyc += random.randint(0, 5)
                print("pre rot")
                print(self.rotcyc)
                self.image = py.transform.rotate(self.image, self.rotcyc)
                print("post rot")
            self.rect = self.image.get_rect()
            print("get rect")
            self.rect.center = (v.screen.get_rect()[2]/2, v.screen.get_rect()[3]/2)
            print("centre")
            """if self.direction == "Up" or self.direction == "Down":
                self.rect.centery = (self.rect.centery + (mod * (self.rect.height / 2)))
            if self.direction == "Left" or self.direction == "Right":
                self.rect.centerx = (self.rect.centerx + (mod * (self.rect.width / 2)))"""
            self.rect.centery += int(5 * v.scale)
            #py.draw.rect(v.screen, (255, 0, 0), self.rect, 2)
        else:
            self.image = py.Surface((0, 0))
            self.rect = py.Rect(0, 0, 0, 0)
            if self.coolDown < self.coolDownTime:
                for event in v.events:
                    if event.type == py.USEREVENT + 2:
                        self.coolDown += 1