import pygame as py
import Variables as v
import entityClasses
import MenuItems
from time import sleep
from time import clock
from pygame.color import Color as colour 
import gameScreens

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
        image = py.transform.scale(self.image, (int(30 / 640 * v.screenX), int(30 / 640 * v.screenX)))
        pos = ((65 + (31 * self.number)) / 640 * v.screenX, 410 / 640 * v.screenX)
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
        if ((v.Attributes["Max Mana"] / 5) * self.number) <= v.playerMana:
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
        image = py.transform.scale(self.image, (int(30 / 640 * v.screenX), int(30 / 640 * v.screenX)))
        pos = ((65 + (31 * self.number)) / 640 * v.screenX, 450 / 640 * v.screenX)
        rect.center = pos
        v.screen.blit(image, rect)

def update_mana():
    for n in range(1, 6):
        mana(n).draw()
    for event in v.events:
        if event.type == py.USEREVENT + 1:
            if v.playerMana < v.Attributes["Max Mana"]:
                v.playerMana += ((v.Attributes["Max Mana"]/200) + (v.Attributes["Magical Strength"]/100)) / 4 #TODO: Turn into proper function
    if v.playerMana > v.Attributes["Max Mana"]:
        v.playerMana = v.Attributes["Max Mana"]
    v.playerMana = round(v.playerMana, 3)

class weaponSlot:

    def draw(self):
        image = "Resources/Images/Empty_Weapon_Slot.png"
        image = py.image.load(image)
        image = py.transform.scale(image, (int(80 / 640 * v.screenX), int(80 / 640 * v.screenX)))
        rect = image.get_rect()
        rect.center = (44, v.screen.get_rect().bottom - 45)
        v.screen.blit(image, rect)

class XP:
    
    def __init__(self):
        self.posx = 320 / 640 * v.screenX
        self.posy = 440 / 640 * v.screenX
        
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
                    segRect.center = entityClasses.arc((self.posx, self.posy), 30, -deg - 180) #30
                    v.screen.blit(rend, segRect)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(30 / 640 * v.screenX))
        label = font.render(str(v.experience["XPL"]), 1, (0, 255, 255))
        pos = (self.posx - font.size(str(v.experience["XPL"]))[0]/2, self.posy - font.size(str(v.experience["XPL"]))[1]/2)
        v.screen.blit(label, pos)
        
class ability(py.sprite.Sprite):
    
    def __init__(self, ability, image, num):
        super().__init__()
        self.ability = ability
        self.posx = (20 + (30 * num)) / 640 * v.screenX
        self.posy = 20 / 640 * v.screenX
        self.icon = py.image.load(image).convert_alpha()
        self.saveIcon = image
        self.saveNum = num
    
    def update(self):
        maxCooldown = self.ability.attributes["Cooldown"]
        cooldown = self.ability.object.coolDown
        self.image = py.transform.scale(self.icon, (int(32 / 640 * v.screenX), int(32 / 640 * v.screenX)))
        try:
            self.image.fill((255, 255, 255, int((cooldown / maxCooldown) * 255)), special_flags=py.BLEND_RGBA_MULT)
        except TypeError as detail:
            print("INVALID COLOUR:", (255, 255, 255, int((cooldown / maxCooldown) * 255)))
            print(detail)
        self.rect = self.image.get_rect()
        self.rect.center = (self.posx, self.posy)
        py.draw.rect(v.screen, (0, 0, 0), self.rect)
        v.screen.blit(self.image, self.rect)
        
        if self.ability.object.attacking:
            border = (255, 255, 0)
        else:
            border = (153, 76, 0)
        self.rect.width += 2
        self.rect.height += 2
        self.rect.center = (self.posx, self.posy)
        py.draw.rect(v.screen, border, self.rect, 2)
        
        keys_pressed = py.key.get_pressed()
        key = None
        if self.saveNum == 0:
            key = py.K_1
        if self.saveNum == 1:
            key = py.K_2
        if keys_pressed[key] and not v.playerActing:
            if cooldown == maxCooldown:
                if v.playerMana >= self.ability.attributes["Mana"]:
                    self.ability.object.attacking = True
    
    def save(self):
        save = {}
        save["icon"] = self.saveIcon
        save["num"] = self.saveNum
        save["ability"] = self.ability.save()
        return save
        

class pauseScreen:
    
    def __init__(self):
        self.pos = (v.screenX / 2, v.screenY / 2)
        self.bigRect = py.Rect(0, 0, v.screenX, v.screenY)
        self.text = py.sprite.Group()
        self.text.add(MenuItems.textLabel("Paused", (v.screenX / 2, 100), (255, 255, 255), "Resources\Fonts\RunicClear.ttf", 80, centred=True))
        self.buttons = py.sprite.Group()
        self.buttons.add(MenuItems.Button("Main Menu", (v.screenX / 2, 200), 40, colour("brown"), colour("white"), "Resources\Fonts\RunicSolid.ttf", "mainMenu", True))
        self.buttons.add(MenuItems.Button("Exit Game", (v.screenX / 2, 300), 40, colour("brown"), colour("white"), "Resources\Fonts\RunicSolid.ttf", "quit", True))
        
    def update(self):
        grey = py.Surface((v.screenX, v.screenY)).convert_alpha()
        grey.fill((20, 20, 20, 200))
        v.screen.blit(grey, self.bigRect)
        self.text.update()
        self.buttons.update()
        
        for event in v.events:
            if event.type == py.MOUSEBUTTONDOWN:
                for button in self.buttons:
                    if button.pressed():
                        id = button.ID
                        if id == "mainMenu":
                            gameScreens.mainMenu()
                            continue
                        if id == "quit":
                            import SaveLoad
                            SaveLoad.Save()
                            from sys import exit
                            exit()

class miniMap: #TODO make this work with baseMap
    
    def __init__(self):
        self.windowScale = 6
        self.tileScale = 4
        self.scale = 4
        self.hovered = False
        
    
    def update(self):
        self.scale = self.tileScale * (self.windowScale / 6)
        #self.scale = self.tileScale
        self.pos = (640 - (640/self.windowScale), 0)
        self.size = (640/self.windowScale, 480/self.windowScale)
        self.map = py.Surface(self.size)
        self.map.fill((100, 255, 100))
        baseMap = v.MAP.skin
        size = baseMap.get_rect().size
        baseMap = py.transform.scale(baseMap, (int(size[0]/self.scale), int(size[1]/self.scale)))
        rect = baseMap.get_rect()
        rect.center = ((-v.playerPosX/self.scale) + (rect.width/(self.scale * 10)), (v.playerPosY/self.scale) + (rect.height/(self.scale * 10)))
        self.map.blit(baseMap, rect)
        py.draw.rect(self.map, (255, 0, 0), (self.size[0]/2 - (22 / self.scale) / 2, self.size[1]/2 - (30 / self.scale) / 2, 15 / self.scale, 20 / self.scale))
        
        v.screen.blit(self.map, self.pos)
        rect = py.Rect(self.pos, self.size)
        py.draw.rect(v.screen, (153, 76, 0), rect, 2)
        
        if rect.collidepoint(py.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False
        
        if self.hovered:
            if self.windowScale > 4:
                self.windowScale -= 0.1
        else:
            if self.windowScale < 6:
                self.windowScale += 0.1
        
        for event in v.events:
            if event.type == py.MOUSEBUTTONUP:
                if event.button == 4:
                    pre = int(30 / self.tileScale)
                    while int(30 / self.tileScale) == pre and self.tileScale > 0.1:
                        self.tileScale -= 0.1
                if event.button == 5:
                    pre = int(30 / self.tileScale)
                    while int(30 / self.tileScale) == pre and self.tileScale < 7:
                        self.tileScale += 0.1
                self.tileScale = round(self.tileScale, 1)
                if self.tileScale <= 0.1:
                    self.tileScale = 0.1
                if self.tileScale >= 7:
                    self.tileScale = 7

def actionText():
    if not v.actionQueue == []:
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(20 / 640 * v.screenX))
        label = font.render(v.actionQueue[0], 1, (255, 255, 255))
        posy = 380 / 640 * v.screenX
        posx = ((v.screenX/2) - (font.size(v.actionQueue[0])[0] / 2)) / 640 * v.screenX
        v.screen.blit(label, (posx, posy))

def fps():
    pos = (v.screenX * 0.5, v.screenY * 0.021)
    font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(v.screenX * 0.03125))
    label = font.render(str(int(v.clock.get_fps())), 1, (255, 0, 0))
    v.screen.blit(label, pos)


class loadingScreen():
    
    def __init__(self):
        self.wizSheet = entityClasses.SpriteSheet("Resources/Images/LoadingWizard.png", 6, 7)
        self.aniPos = 7
        self.fade = MenuItems.fadeIn()
        self.fade.fadeIn = True
        self.font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(20/640 * v.screenX))
        self.label = self.font.render("Loading...", 1, (255, 255, 255))
        self.mod = self.font.size("Loading...")
        self.mod = (self.mod[0] / 2, self.mod[1] / 2)
        
    
    def update(self, stage=1):
        if stage == 0:
            for i in range(7, 14, 2):
                self.image = self.wizSheet.images[i]
                self.rect = (0, 0, v.screenX, v.screenY)
                py.draw.rect(v.screen, (0, 0, 0), self.rect)
                v.screen.blit(self.image, ((v.screenX / 2) - self.image.get_rect().width / 2, (v.screenY / 2)  - self.image.get_rect().height / 2))
                v.screen.blit(self.label, ((v.screenX / 2) - self.mod[0], (v.screenY / 2)  - self.mod[1] + 50/640 * v.screenX))
                self.fade.draw()
                self.fade.opacity -= 40
                py.display.flip()
                py.time.delay(100)
            self.time = clock()
        if stage == 1:
            self.image = self.wizSheet.images[14]
            self.rect = (0, 0, v.screenX, v.screenY)
            py.draw.rect(v.screen, (0, 0, 0), self.rect)
            v.screen.blit(self.image, ((v.screenX / 2) - self.image.get_rect().width / 2, (v.screenY / 2)  - self.image.get_rect().height / 2))
            v.screen.blit(self.label, ((v.screenX / 2) - self.mod[0], (v.screenY / 2)  - self.mod[1] + 50/640 * v.screenX))
        if stage == 2:
            t = self.font.render("Load Time: " + str(clock() - self.time), 1, (255, 255, 255))
            for i in range(28, 38, 2):
                py.time.delay(100)
                self.image = self.wizSheet.images[i]
                self.rect = (0, 0, v.screenX, v.screenY)
                py.draw.rect(v.screen, (0, 0, 0), self.rect)
                v.screen.blit(self.image, ((v.screenX / 2) - self.image.get_rect().width / 2, (v.screenY / 2)  - self.image.get_rect().height / 2))
                v.screen.blit(self.label, ((v.screenX / 2) - self.mod[0], (v.screenY / 2)  - self.mod[1] + 50/640 * v.screenX))
                v.screen.blit(t, (200/640 * v.screenX, 300/640 * v.screenX))
                self.fade.draw()
                self.fade.opacity += 40
                py.display.flip()

class locationTitle():
    
    def __init__(self):
        self.text = v.mapMeta[str(v.mapNum)]["Name"]
        self.font = py.font.Font("Resources/Fonts/Vecna.otf", int(60/640 * v.screenX))
        self.label = self.font.render(self.text, 1, (100, 100, 100))
        #self.label = py.Surface(self.font.size(self.text))
        #self.label.blit(ren, (0, 0))
        self.cycle = 1
        self.up = True
    
    def update(self):
        if self.up:
            self.cycle += 2
            if self.cycle >= 255:
                self.up = False
                self.cycle = 255
        if not self.up:
            self.cycle -= 1
            if self.cycle <= 0:
                return
        
        l = self.label.copy()
        l.fill((255, 255, 255, self.cycle), special_flags=py.BLEND_RGBA_MULT)
        #l.set_alpha(self.cycle)
        pos = ((v.screenX/2) - self.font.size(self.text)[0]/2, 50/640 * v.screenX)
        
        v.screen.blit(l, pos)
            
            