import mapMakerVariables as v
import mapMenuItems
import pygame as py


class enemyImage(py.sprite.Sprite):
    
    def __init__(self, num, image):
        super().__init__()
        self.image = py.transform.scale(mapMenuItems.SpriteSheet(image, 4, 3).images[1], (30, 30))
        self.posx = (num % 3) * 30
        self.posy = int((num / 3)) * 30
        self.num = num
        self.sheet = image
    def update(self):
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posx, self.posy)
        v.pallet.blit(self.image, self.rect)
        if self.rect.collidepoint((py.mouse.get_pos()[0] - 600, py.mouse.get_pos()[1])):
            self.hovered = True
        else:
            self.hovered = False
        if v.selectedEnemy["Image"] == self.sheet:
            py.draw.rect(v.pallet, (255, 0, 0), self.rect, 1)
        if self.hovered:
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    if py.mouse.get_pressed()[0]:
                        v.selectedEnemy["Image"] = self.sheet
                        createEnemy()


def createEnemy():
    tinps = py.sprite.Group()
    texts = py.sprite.Group()
    v.textNum = 1
    
    tinps.add(mapMenuItems.textInput((400, 100), 40, 16, 1, button=None, default=[], type="str"))
    texts.add(mapMenuItems.textLabel("Enemy Name:", (150, 110), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    tinps.add(mapMenuItems.textInput((400, 200), 40, 2, 2, button=None, default=[], type="int"))
    texts.add(mapMenuItems.textLabel("Attack:", (150, 210), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    tinps.add(mapMenuItems.textInput((400, 300), 40, 3, 3, button=None, default=[], type="int"))
    texts.add(mapMenuItems.textLabel("Health:", (150, 310), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    tinps.add(mapMenuItems.textInput((400, 400), 40, 2, 4, button=None, default=[], type="int"))
    texts.add(mapMenuItems.textLabel("Speed:", (150, 410), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    button = mapMenuItems.button("Done", (500, 500), 60, (200, 0, 0), (255, 0, 0), "../Resources/Fonts/RPGSystem.ttf", "GO")
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        v.screen.fill((200, 200, 200))
        tinps.update()
        texts.update()
        button.update()
        for event in v.events:
            if event.type == py.MOUSEBUTTONDOWN:
                if button.pressed():
                    for t in tinps:
                        if t.num == 1:
                            v.selectedEnemy["Name"] = t.outText
                        if t.num == 2:
                            v.selectedEnemy["Attack"] = t.outText
                        if t.num == 3:
                            v.selectedEnemy["Health"] = t.outText
                        if t.num == 4:
                            v.selectedEnemy["Speed"] = t.outText
                    py.time.delay(200)
                    return
        py.display.flip()
        
        
class npcImageButton(py.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        from os import listdir
        self.images = []
        for i in listdir("../Resources/Images/NpcSkins/Spritesheets"):
            self.images.append("../Resources/Images/NpcSkins/Spritesheets/" + i)
        
        self.x = 460
        self.y = 100
        self.selected = self.images[0]
        
    def update(self):
        image = mapMenuItems.SpriteSheet(self.selected, 4, 3).images[7]
        image = py.transform.scale(image, (96, 128))
        rect = image.get_rect()
        rect.center = (self.x, self.y)
        py.draw.rect(v.screen, (255, 255, 255), rect)
        py.draw.rect(v.screen, (200, 100, 100), rect, 2)
        v.screen.blit(image, rect)
    


def createNPC():
    imageButton = npcImageButton()
    bar = mapMenuItems.scrollBar(910, 10, 610)
    
    tinps = py.sprite.Group()
    texts = py.sprite.Group()
    
    tinps.add(mapMenuItems.textInput((350, 200), 30, 16, 1, button=None, default=[], type="str"))
    texts.add(mapMenuItems.textLabel("NPC Name:", (150, 210), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    tinps.add(mapMenuItems.textInput((450, 300), 30, 2, 2, button=None, default=[], type="int"))
    texts.add(mapMenuItems.textLabel("Base Friendliness:", (150, 310), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    rb1 = mapMenuItems.radioButtons(350, 410, ["Good", "Evil"])
    texts.add(mapMenuItems.textLabel("Alignment:", (150, 410), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    button = mapMenuItems.button("Done", (500, 500), 60, (200, 0, 0), (255, 0, 0), "../Resources/Fonts/RPGSystem.ttf", "GO")
    
    while True:
        v.screen.fill((220, 220, 220))
        v.events = []
        v.events = py.event.get()
        imageButton.update()
        bar.update()
        tinps.update()
        texts.update()
        rb1.update()
        
        py.display.flip()