import pygame as py
import Variables as v
from entityClasses import rot_center, arc, centre, SpriteSheet
import math



class Sword(py.sprite.Sprite):

    def __init__(self, image, weapon):
        super().__init__()
        self.image = image
        self.attacking = False
        self.attCyclePos = 0
        self.posX = 1280 / 2
        self.posY = 720 / 2
        v.damagesNPCs.add(self)
        self.rect = py.Rect(0, 0, 0, 0)
        self.master = weapon
        self.coolDown = 0
        
        self.attributes = {"Cooldown": 20, "AttSpeed": 16}
        self.attributes.update(self.master.attributes)
        
        self.maxcooldown = self.attributes["Cooldown"]
        self.attSpeed = self.attributes["AttSpeed"]

    def get_rend(self):
        self.rend = py.image.load(self.image).convert_alpha()
        self.rend = py.transform.scale(self.rend, (int(20 * v.scale), int(20 * v.scale)))

    def update(self):
        self.get_rend()
        if self.coolDown <= 0:
            if self.attacking:
                v.playerActing = True
                v.playerStopped = True
                if v.playerDirection == "Up":
                    angleMod = -90
                elif v.playerDirection == "Down":
                    angleMod = 90
                elif v.playerDirection == "Left":
                    angleMod = 0
                elif v.playerDirection == "Right":
                    angleMod = 180
                if self.attCyclePos == 0:
                    self.rect = self.rend.get_rect()
                    self.rect.center = (self.posX, self.posY)
                    self.rend = rot_center(self.rend, angleMod + 180)
                    self.rect.center = arc((centre()[0], centre()[1]), 20 * v.scale, angleMod)
                    self.attCyclePos += self.attSpeed
                else:
                    self.rend = rot_center(self.rend, angleMod + 180 - self.attCyclePos)
                    self.rect.center = arc((centre()[0], centre()[1]), 20 * v.scale, angleMod - self.attCyclePos)
                    self.attCyclePos += self.attSpeed
                    if self.attCyclePos > 180:
                        self.attacking = False
                        self.attCyclePos = 0
                        self.coolDown = self.maxcooldown
            else:
                self.rect = py.Rect(-110, -110, 0, 0)
        else:
            self.rect = py.Rect(-110, -110, 0, 0)
        
        if self.coolDown > 0:
            self.coolDown -= 1
        v.weaponCooldown = self.coolDown / self.maxcooldown

    def draw(self):
        #self.update()
        if self.attacking:
            v.screen.blit(self.rend, self.rect)


class manaOrb(py.sprite.Sprite):
    
    def __init__(self, image, weapon):
        super().__init__()
        self.attacking = False
        self.projectiles = py.sprite.Group()
        
        self.image = image
        self.master = weapon
        self.attributes = {"Cooldown": 20, "Orbs": 1}
        self.attributes.update(self.master.attributes)
        
        self.coolDown = 0
        self.maxcooldown = self.attributes["Cooldown"]
        self.orbs = self.attributes["Orbs"]
    
    def update(self):
        if self.attacking:
            if self.coolDown <= 0:
                if self.orbs == 1:
                    self.projectiles.add(self.projectile(self.image, self.master, self))
                if self.orbs == 2:
                    self.projectiles.add(self.projectile(self.image, self.master, self, 45))
                    self.projectiles.add(self.projectile(self.image, self.master, self, -45))
                if self.orbs == 3:
                    self.projectiles.add(self.projectile(self.image, self.master, self, 45))
                    self.projectiles.add(self.projectile(self.image, self.master, self, 0))
                    self.projectiles.add(self.projectile(self.image, self.master, self, -45))
                self.coolDown = self.maxcooldown #TODO: make this variable
            self.attacking = False
        if self.coolDown > 0:
            self.coolDown -= 1
        v.weaponCooldown = self.coolDown / self.maxcooldown
    
    def draw(self):
        for thing in self.projectiles:
            thing.update()
            thing.draw()
    
    class projectile(py.sprite.Sprite):
        def __init__(self, image, weapon, shooter, offset=0):
            super().__init__()
            self.attacking = True
            self.attSpeed = 3
            self.attCyclePos = 0
            self.aniCyclePos = 0
            self.posx = 0
            self.posy = -10 * v.scale
            self.sheet = SpriteSheet(image, 1, 10)
            self.image = self.sheet.images[0]
            self.direction = 90
            self.rect = py.Rect(0, 0, 0, 0)
            v.damagesNPCs.add(self)
            self.master = weapon
            self.shooter = shooter
            self.killDown = 5
            self.offset = offset

        def update(self):
            if self.attacking:
                try:
                    self.image = self.sheet.images[self.aniCyclePos]
                except:
                    self.attacking = False
                    return
                size = self.image.get_rect()
                self.image = py.transform.scale(self.image, (int(size.width * v.scale), int(size.height * v.scale)))
                if self.aniCyclePos < 9:
                    v.playerStopped = True
                    v.playerActing = True
                    self.posx = v.playerPosX
                    self.posy = v.playerPosY - 7
                    if self.shooter.attributes["Orbs"] != 1:
                        if v.playerDirection == "Up":
                            self.direction = 0
                        if v.playerDirection == "Right":
                            self.direction = 90
                        if v.playerDirection == "Down":
                            self.direction = 180
                        if v.playerDirection == "Left":
                            self.direction = 270
                        self.direction += self.offset
                        
                        self.posx = arc((self.posx, self.posy), 20, self.direction)[0]
                        self.posy = arc((self.posx, self.posy), 20, self.direction)[1]
                    for event in v.events:
                        if event.type == py.USEREVENT + 1:
                            self.aniCyclePos += 1
                if self.aniCyclePos == 9:
                    self.image = self.sheet.images[9]
                    self.image = py.transform.scale(self.image, (int(int(size.width / 2) * v.scale), int(int(size.height / 2) * v.scale)))
                    if self.attCyclePos == 0:
                        if v.playerDirection == "Up":
                            self.direction = 0
                        if v.playerDirection == "Right":
                            self.direction = 90
                        if v.playerDirection == "Down":
                            self.direction = 180
                        if v.playerDirection == "Left":
                            self.direction = 270
                        self.direction += self.offset
                    
                    self.posx += math.sin(math.radians(self.direction)) * self.attSpeed
                    self.posy += math.cos(math.radians(self.direction)) * self.attSpeed
                    
                    """if self.direction == 180:
                        self.posy -= self.attSpeed
                    if self.direction == 0:
                        self.posy += self.attSpeed
                    if self.direction == 270:
                        self.posx -= self.attSpeed
                    if self.direction == 90:
                        self.posx += self.attSpeed"""
                    
                    """if self.offset != 0:
                        if self.direction == "Down" or self.direction == "Up":
                            self.posx = math.tan(self.offset) * self.posy
                        if self.direction == "Left" or self.direction == "Right":
                            self.posy = math.tan(self.offset) * self.posx
                        if self.offset == 45:
                            print(self.posx, self.posy)"""
                    self.attCyclePos += 1
                if self.attCyclePos >= 10:
                    v.playerStopped = False
                if self.attCyclePos >= 30:
                    self.attacking = False
                    self.aniCyclePos = 0
                    self.attCyclePos = 0
                
            else:
                v.damagesNPCs.remove(self)
                self.shooter.projectiles.remove(self)
                        
            self.rect = self.image.get_rect()
            self.rect.centerx = 1280 / 2 + int(((-v.playerPosX + (1 * self.posx)) * v.scale))
            self.rect.centery = 720 / 2 - int(((-v.playerPosY + (1 * self.posy)) * v.scale))
            self.rend = self.image
            if self.aniCyclePos == 9:
                for thing in v.hitList:
                    if self.rect.colliderect(thing.rect):
                        self.killDown -= 1
                        if self.killDown <= 0:
                            self.attacking = False
                for thing in v.allNpc:
                    if self.rect.colliderect(thing.rect):
                        self.attacking = False
        
        def draw(self):
            if self.attacking:
                v.screen.blit(self.rend, self.rect)

class shooter(py.sprite.Sprite):
    
    def __init__(self, image, weapon):
        super().__init__()
        self.attacking = False
        self.projectiles = py.sprite.Group()
        
        self.image = image
        self.master = weapon
        self.attributes = {"Cooldown": 20, "Range": 20, "Rotate": False}
        self.attributes.update(self.master.attributes)
        
        self.coolDown = 0
        self.maxcooldown = self.attributes["Cooldown"]
        self.range = self.attributes["Range"]
        self.rotate = self.attributes["Rotate"]
    
    def update(self):
        if self.attacking:
            if self.coolDown <= 0:
                self.projectiles.add(self.projectile(self.image, self.master, self))
                self.coolDown = self.maxcooldown
            self.attacking = False
        if self.coolDown > 0:
            self.coolDown -= 1
        v.weaponCooldown = self.coolDown / self.maxcooldown
    
    def draw(self):
        for thing in self.projectiles:
            thing.update()
            thing.draw()

    class projectile(py.sprite.Sprite):
        
        def __init__(self, image, weapon, shooter):
            super().__init__()
            self.attacking = True
            self.attSpeed = 4
            self.attCyclePos = 0
            self.posx = v.playerPosX
            self.posy = v.playerPosY - int(1.5 * v.scale)
            if type(image) == str:
                self.skin = py.image.load(image).convert_alpha()
            elif type(image) == py.Surface:
                self.skin = image.convert_alpha()
            else:
                raise Exception("Incorrect projectile image type: " + str(type(image)))
            self.direction = "Down"
            self.rect = py.Rect(0, 0, 0, 0)
            v.damagesNPCs.add(self)
            self.master = weapon
            self.shooter = shooter
            self.range = self.shooter.attributes["Range"]
            self.rotate = self.shooter.attributes["Rotate"]
        
        def update(self):
            if self.attacking:
                v.playerActing = True
                size = self.skin.get_rect()
                self.image = py.transform.scale(self.skin, (int(size.width * v.scale / 2), int(size.height * v.scale / 2)))
                if self.rotate:
                    self.image = py.transform.rotate(self.image, self.attCyclePos * 20)
                if self.attCyclePos == 0:
                    self.direction = v.playerDirection
                if self.direction == "Down":
                    self.posy -= self.attSpeed
                    self.image = py.transform.rotate(self.image, 180)
                if self.direction == "Up":
                    self.posy += self.attSpeed
                if self.direction == "Left":
                    self.posx -= self.attSpeed
                    self.image = py.transform.rotate(self.image, 90)
                if self.direction == "Right":
                    self.posx += self.attSpeed
                    self.image = py.transform.rotate(self.image, 270)
                self.attCyclePos += 1
                if self.attCyclePos >= self.range:
                    self.attacking = False
                    self.attCyclePos = 0
                
            else:
                self.rect = py.Rect(0, 0, 0, 0)
                v.damagesNPCs.remove(self)
                self.shooter.projectiles.remove(self)
                        
            self.rect = self.image.get_rect()
            self.rect.centerx = 640 + int(((-v.playerPosX + (1 * self.posx)) * v.scale))
            self.rect.centery = 360 - int(((-v.playerPosY + (1 * self.posy)) * v.scale))
            self.rend = self.image
            for thing in v.hitList:
                if self.rect.colliderect(thing.rect):
                    self.attCyclePos = self.range
            for thing in v.allNpc:
                if self.rect.colliderect(thing.rect):
                    self.attCyclePos = self.range
                    
        def draw(self):
            if self.attacking:
                v.screen.blit(self.rend, self.rect)

def updateEquipped(key):
    if not v.equipped[key] == None:
        v.equipped[key].object.update()
    
def drawEquipped(key):
    if not v.equipped[key] == None:
        v.equipped[key].object.draw()

def weaponAttack():
    if not v.equipped["Weapon"] == None:
        v.equipped["Weapon"].object.attacking = True