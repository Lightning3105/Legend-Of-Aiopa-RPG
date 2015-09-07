import pygame as py
import Variables as v
import entityClasses

class health:

    def __init__(self, number):
        sheet = entityClasses.SpriteSheet("Resources/Images/Hearts.png", 1, 4)
        sheet.getGrid()
        self.Q0 = py.Surface((0,0))
        self.Q4 = sheet.images[0]
        self.Q3 = sheet.images[1]
        self.Q2 = sheet.images[2]
        self.Q1 = sheet.images[3]
        self.image = self.Q4
        self.number = number

    def getPercent(self):
        if ((v.playerMaxHealth / 5) * self.number) <= v.playerHealth:
            self.image = self.Q4
        if (((v.playerMaxHealth / 5) * self.number) - ((v.playerMaxHealth / 20) * 1)) >= v.playerHealth:
            self.image = self.Q3
        if (((v.playerMaxHealth / 5) * self.number) - ((v.playerMaxHealth / 20) * 2)) >= v.playerHealth:
            self.image = self.Q2
        if (((v.playerMaxHealth / 5) * self.number) - ((v.playerMaxHealth / 20) * 3)) >= v.playerHealth:
            self.image = self.Q1
        if (((v.playerMaxHealth / 5) * self.number) - ((v.playerMaxHealth / 20) * 4)) >= v.playerHealth:
            self.image = self.Q0
    def draw(self):
        self.getPercent()
        rect = self.image.get_rect()
        image = py.transform.scale(self.image, (30, 30))
        pos = (10 + (31 * self.number), 450)
        rect.center = pos
        v.screen.blit(image, rect)

def update_health():
    for n in range(1, 6):
        health(n).draw()