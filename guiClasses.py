import pygame as py
import Variables as v
import entityClasses
from time import sleep

class health:

    def __init__(self, number):
        sheet = entityClasses.SpriteSheet("Resources/Images/Hearts.png", 1, 4)
        sheet.getGrid()
        self.Q0 = py.Surface((1,1))
        self.Q0.convert_alpha()
        self.Q0.set_alpha(0)
        self.Q4 = sheet.images[0]
        self.Q3 = sheet.images[1]
        self.Q2 = sheet.images[2]
        self.Q1 = sheet.images[3]
        self.image = self.Q4
        self.number = number

    def getPercent(self):
        if ((v.Attributes["Max Health"] / 5) * self.number) <= v.playerHealth:
            self.image = self.Q4
        if (((v.Attributes["Max Health"] / 5) * self.number) - ((v.Attributes["Max Health"] / 20) * 1)) >= v.playerHealth:
            self.image = self.Q3
        if (((v.Attributes["Max Health"] / 5) * self.number) - ((v.Attributes["Max Health"] / 20) * 2)) >= v.playerHealth:
            self.image = self.Q2
        if (((v.Attributes["Max Health"] / 5) * self.number) - ((v.Attributes["Max Health"] / 20) * 3)) >= v.playerHealth:
            self.image = self.Q1
        if (((v.Attributes["Max Health"] / 5) * self.number) - ((v.Attributes["Max Health"] / 20) * 4)) >= v.playerHealth:
            self.image = self.Q0
    def draw(self):
        self.getPercent()
        rect = self.image.get_rect()
        image = py.transform.scale(self.image, (30, 30))
        pos = (65 + (31 * self.number), 410)
        rect.center = pos
        v.screen.blit(image, rect)

def update_health():
    for n in range(1, 6):
        health(n).draw()

class mana:

    def __init__(self, number):
        sheet = entityClasses.SpriteSheet("Resources/Images/Mana.png", 1, 4)
        sheet.getGrid()
        self.Q0 = py.Surface((1,1))
        self.Q0.convert_alpha()
        self.Q0.set_alpha(0)
        self.Q4 = sheet.images[0]
        self.Q3 = sheet.images[1]
        self.Q2 = sheet.images[2]
        self.Q1 = sheet.images[3]
        self.image = self.Q4
        self.number = number

    def getPercent(self):
        if ((v.Attributes["Max Mana"] / 5) * self.number) <= v.playerHealth:
            self.image = self.Q4
        if (((v.Attributes["Max Mana"] / 5) * self.number) - ((v.Attributes["Max Mana"] / 20) * 1)) >= v.playerMana:
            self.image = self.Q3
        if (((v.Attributes["Max Mana"] / 5) * self.number) - ((v.Attributes["Max Mana"] / 20) * 2)) >= v.playerMana:
            self.image = self.Q2
        if (((v.Attributes["Max Mana"] / 5) * self.number) - ((v.Attributes["Max Mana"] / 20) * 3)) >= v.playerMana:
            self.image = self.Q1
        if (((v.Attributes["Max Mana"] / 5) * self.number) - ((v.Attributes["Max Mana"] / 20) * 4)) >= v.playerMana:
            self.image = self.Q0
    def draw(self):
        self.getPercent()
        rect = self.image.get_rect()
        image = py.transform.scale(self.image, (30, 30))
        pos = (65 + (31 * self.number), 450)
        rect.center = pos
        v.screen.blit(image, rect)

def update_mana():
    for n in range(1, 6):
        mana(n).draw()

class weaponSlot:

    def draw(self):
        image = "Resources/Images/Empty_Weapon_Slot.png"
        image = py.image.load(image)
        image = py.transform.scale(image, (80, 80))
        rect = image.get_rect()
        rect.center = (44, 435)
        v.screen.blit(image, rect)

class XP:
    
    def __init__(self):
        self.posx = 320
        self.posy = 440
        
    def update(self):
        if v.experience["XP"] >= v.experience["XPtoL"]:
            v.experience["XP"] -= v.experience["XPtoL"]
            v.experience["XPL"] += 1
            v.experience["XPtoL"] *= v.xpMod
        self.draw()
    
    def draw(self):
        if not v.experience["XP"] == 0:
            xpSegment = 360 / v.experience["XPtoL"]
            seg = py.Surface((2, 5))
            seg.fill((0, 255, 255))
            segRect = seg.get_rect()
            deg = 0
            
            for i in range(90):
                deg += 8
                if deg <= xpSegment * v.experience["XP"]:
                    #rend = entityClasses.rot_center(seg, deg)
                    rend = py.transform.rotate(seg, deg)
                    segRect.center = entityClasses.arc((self.posx, self.posy), 30, -deg - 180)
                    v.screen.blit(rend, segRect)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
        label = font.render(str(v.experience["XPL"]), 1, (0, 255, 255))
        pos = (self.posx - font.size(str(v.experience["XPL"]))[0]/2, self.posy - font.size(str(v.experience["XPL"]))[1]/2)
        v.screen.blit(label, pos)
        
class ability(py.sprite.Sprite):
    
    def __init__(self, ability, num):
        self.ability = ability
        self.posx = 15 + (30 * num)
        self.posy = 15