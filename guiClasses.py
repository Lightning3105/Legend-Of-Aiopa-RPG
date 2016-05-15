import pygame as py
import Variables as v
import entityClasses
import MenuItems
from time import sleep
from time import clock
import gameScreens
import math

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
        image = py.transform.scale(self.image, (60, 60))
        pos = ((65 + (31 * self.number)) / 640 * 1280, 580)
        rect.center = pos
        background = self.Q4
        brect = background.get_rect()
        brect.center = pos
        background.fill((50, 50, 50, 200), special_flags=py.BLEND_RGB_MULT)
        background = py.transform.scale(background, (int(30 / 640 * 1280), int(30 / 640 * 1280)))
        v.screen.blit(background, brect)
        v.screen.blit(image, rect)

def update_health(): #TODO: Split label into separate class
    for n in range(1, 6):
        health(n).draw()
    
    #Mana text TODO: make text appear on hover
    font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
    size = font.size(str(int(v.playerHealth)) + "/" + str(v.Attributes["Max Health"]))
    r = py.Rect((340 - size[0]/2, 585), size)
    label = font.render(str(int(v.playerHealth)) + "/" + str(v.Attributes["Max Health"]), 1, (200, 200, 200))
    s = py.Surface(r.size)
    s.fill((255, 0, 0, 200))
    v.screen.blit(s, r)
    v.screen.blit(label, r)
    py.draw.rect(v.screen, (0, 0, 0), r, 2)
    
    if v.playerHealth <= 0:
        v.playerDead = True
        v.PAUSED = True
        v.pauseType = "Death"
    

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
        image = py.transform.scale(self.image, (int(60), int(60)))
        pos = ((65 + (31 * self.number)) / 640 * 1280, 650)
        rect.center = pos
        background = self.Q4
        brect = background.get_rect()
        brect.center = pos
        background.fill((50, 50, 50, 200), special_flags=py.BLEND_RGB_MULT)
        background = py.transform.scale(background, (int(60), int(60)))
        v.screen.blit(background, brect)
        v.screen.blit(image, rect)

def update_mana(): #TODO: Split label into separate class
    for n in range(1, 6):
        mana(n).draw()
    for event in v.events:
        if event.type == py.USEREVENT + 1:
            if v.playerMana < v.Attributes["Max Mana"]:
                v.playerMana += ((v.Attributes["Max Mana"]/200) + (v.Attributes["Magical Strength"]/100)) / 4 #TODO: Turn into proper function
    if v.playerMana > v.Attributes["Max Mana"]:
        v.playerMana = v.Attributes["Max Mana"]
    v.playerMana = round(v.playerMana, 3)
    
    #Mana text TODO: make text appear on hover
    font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
    size = font.size(str(int(v.playerMana)) + "/" + str(v.Attributes["Max Mana"]))
    r = py.Rect((340 - size[0]/2, 660), size)
    label = font.render(str(int(v.playerMana)) + "/" + str(v.Attributes["Max Mana"]), 1, (0, 0, 0))
    s = py.Surface(r.size)
    s.fill((0, 255, 255, 200))
    v.screen.blit(s, r)
    v.screen.blit(label, r)
    py.draw.rect(v.screen, (0, 0, 0), r, 2)
    
    

class weaponSlot:
    
    def __init__(self):
        self.image = "Resources/Images/Empty_Weapon_Slot.png"
        self.image = py.image.load(self.image).convert_alpha()
        self.image = py.transform.scale(self.image, (160, 160))
        self.rect = self.image.get_rect()
        self.rect.center = (80, 640)

    def draw(self):
        posy = self.rect.height - (self.rect.height * v.weaponCooldown)
        image = self.image.copy()
        image.fill((255, 0, 0, 200), rect=((0, posy), self.rect.size), special_flags=py.BLEND_RGB_MULT)
        
        v.screen.blit(image, self.rect)
        
        image = v.equipped["Weapon"].icon
        image = py.transform.scale(image, (int(image.get_rect().width * 4.8), int(image.get_rect().height * 4.8)))
        
        self.rect.center = (80, 640)
        v.screen.blit(image, self.rect)

class XP:
    
    def __init__(self):
        self.posx = 640
        self.posy = 640
        self.oldXP = 0
        
    def update(self):
        if v.experience["XP"] > self.oldXP:
            v.experience["Total"] += v.experience["XP"] - self.oldXP
            self.oldXP = v.experience["XP"]
        if v.experience["XP"] >= v.experience["XPtoL"]:
            v.experience["XP"] -= v.experience["XPtoL"]
            v.experience["XPL"] += 1
            v.experience["XPtoL"] *= v.xpMod
        self.draw()
    
    def draw(self):
        if not v.experience["XP"] == 0:
            xpSegment = 360 / v.experience["XPtoL"]
            seg = py.Surface((5, 10))
            seg.fill((0, 255, 255))
            deg = 0
            segRect = seg.get_rect()
            """seg = py.Surface((10, 10), py.SRCALPHA, 32)
            seg = seg.convert_alpha()
            py.draw.circle(seg, (0, 255, 255), (5, 5), 5)
            segRect = seg.get_rect()
            deg = 0"""
            
            for i in range(90): 
                deg += 8
                if deg <= xpSegment * v.experience["XP"]:
                    #rend = entityClasses.rot_center(seg, deg)
                    rend = py.transform.rotate(seg, deg)
                    segRect.center = entityClasses.arc((self.posx, self.posy), 60, -deg - 180) #30
                    v.screen.blit(rend, segRect)
                    
        
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 80)
        label = font.render(str(v.experience["XPL"]), 1, (0, 255, 255))
        pos = (self.posx - font.size(str(v.experience["XPL"]))[0]/2, self.posy - font.size(str(v.experience["XPL"]))[1]/2)
        v.screen.blit(label, pos)
        
class ability(py.sprite.Sprite):
    
    def __init__(self, num):
        super().__init__()
        self.posx = (20 + (40 * (num - 1))) / 640 * 1280
        self.posy = 20 / 640 * 1280
        self.num = num
    
    def update(self):
        try:
            self.ability = v.abilities[str(self.num)]
        except KeyError:
            self.ability = None
        if not self.ability == None:
            self.icon = py.image.load(self.ability.icon).convert_alpha()
            maxCooldown = self.ability.attributes["Cooldown"]
            cooldown = self.ability.object.coolDown
            self.image = py.transform.scale(self.icon, (int(32 / 640 * 1280), int(32 / 640 * 1280)))
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
            if self.num == 1:
                key = py.K_1
            if self.num == 2:
                key = py.K_2
            if self.num == 3:
                key = py.K_3
            if self.num == 4:
                key = py.K_4
            if self.num == 5:
                key = py.K_5
            if self.num == 6:
                key = py.K_6
            if keys_pressed[key] and not v.playerActing:
                if cooldown == maxCooldown:
                    if v.playerMana >= self.ability.attributes["Mana"]:
                        self.ability.object.attacking = True
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    if self.rect.collidepoint(v.mouse_pos):
                        if cooldown == maxCooldown:
                            if v.playerMana >= self.ability.attributes["Mana"]:
                                self.ability.object.attacking = True
        

class pauseScreen:
    
    def __init__(self):
        self.pos = (1280 / 2, 720 / 2)
        self.bigRect = py.Rect(0, 0, 1280, 720)
        self.text = py.sprite.Group()
        self.text.add(MenuItems.textLabel("Paused", (1280 / 2, 100), (255, 255, 255), "Resources\Fonts\RunicClear.ttf", 80, centred=True))
        self.buttons = py.sprite.Group()
        self.buttons.add(MenuItems.Button("Main Menu", (1280 / 2, 200), 40, (165,42,42), (255, 255, 255), "Resources\Fonts\RunicSolid.ttf", "mainMenu", True))
        self.buttons.add(MenuItems.Button("Exit Game", (1280 / 2, 300), 40, (165,42,42), (255, 255, 255), "Resources\Fonts\RunicSolid.ttf", "quit", True))
        
    def update(self):
        grey = py.Surface((1280, 720)).convert_alpha()
        grey.fill((20, 20, 20, 200))
        v.screen.blit(grey, self.bigRect)
        self.text.update()
        self.buttons.update()
        
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
        
        if rect.collidepoint(v.mouse_pos):
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

class actionText(py.sprite.Sprite):
    
    def __init__(self):
        self.font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
    
    def update(self):
        if not v.actionQueue == []:
            label = self.font.render(v.actionQueue[0], 1, (255, 255, 255))
            posy = 520
            posx = (640 - (self.font.size(v.actionQueue[0])[0] / 2))
            v.screen.blit(label, (posx, posy))

class fps(py.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.pos = (640, 20)
        self.font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(30))
    def update(self):
        self.label = self.font.render(str(int(v.clock.get_fps())), 1, (255, 0, 0))
        v.screen.blit(self.label, self.pos)


class loadingScreen():
    
    def __init__(self):
        self.wizSheet = entityClasses.SpriteSheet("Resources/Images/LoadingWizard.png", 6, 7)
        self.aniPos = 7
        self.fade = MenuItems.fadeIn()
        self.fade.fadeIn = True
        self.font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(40))
        self.label = self.font.render("Loading...", 1, (255, 255, 255))
        self.mod = self.font.size("Loading...")
        self.mod = (self.mod[0] / 2, self.mod[1] / 2)
        
    
    def update(self, stage=1):
        if stage == 0:
            for i in range(7, 14, 2):
                self.image = self.wizSheet.images[i]
                self.image = py.transform.scale(self.image, (self.image.get_rect().width * 2, self.image.get_rect().height * 2))
                self.rect = (0, 0, 1280, 720)
                py.draw.rect(v.screen, (0, 0, 0), self.rect)
                v.screen.blit(self.image, ((1280 / 2) - self.image.get_rect().width / 2, (720 / 2)  - self.image.get_rect().height / 2))
                v.screen.blit(self.label, ((1280 / 2) - self.mod[0], (720 / 2)  - self.mod[1] + 50/640 * 1280))
                self.fade.draw()
                self.fade.opacity -= 40
                MenuItems.screenFlip()
                py.time.delay(100)
            self.time = clock()
        if stage == 1:
            self.image = self.wizSheet.images[14]
            self.rect = (0, 0, 1280, 720)
            py.draw.rect(v.screen, (0, 0, 0), self.rect)
            v.screen.blit(self.image, ((1280 / 2) - self.image.get_rect().width / 2, (720 / 2)  - self.image.get_rect().height / 2))
            v.screen.blit(self.label, ((1280 / 2) - self.mod[0], (720 / 2)  - self.mod[1] + 50/640 * 1280))
        if stage == 2:
            t = self.font.render("Load Time: " + str(clock() - self.time), 1, (255, 255, 255))
            for i in range(28, 38, 2):
                py.time.delay(100)
                self.image = self.wizSheet.images[i]
                self.rect = (0, 0, 1280, 720)
                py.draw.rect(v.screen, (0, 0, 0), self.rect)
                v.screen.blit(self.image, ((1280 / 2) - self.image.get_rect().width / 2, (720 / 2)  - self.image.get_rect().height / 2))
                v.screen.blit(self.label, ((1280 / 2) - self.mod[0], (720 / 2)  - self.mod[1] + 50/640 * 1280))
                v.screen.blit(t, (200/640 * 1280, 300/640 * 1280))
                self.fade.draw()
                self.fade.opacity += 40
                MenuItems.screenFlip()

class locationTitle():
    
    def __init__(self):
        self.text = str(v.mapMeta["Name"])
        self.font = py.font.Font("Resources/Fonts/Vecna.otf", int(60/640 * 1280))
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
        pos = ((1280/2) - self.font.size(self.text)[0]/2, 50/640 * 1280)
        
        v.screen.blit(l, pos)
            

class deathScreen():
    
    def __init__(self):
        v.PAUSED = True
        v.pauseType = "Death"
        v.playerDead = True
        self.back = py.image.tostring(v.screen, "RGBA")
        self.back = py.image.fromstring(self.back, (1280, 720), "RGBA")
        self.cycle = 100
        self.red = py.Surface((1280, 720)).convert_alpha()
        self.ghost = entityClasses.playerGhost()
        v.p_class.direction = "Down"
        v.p_class.draw()
        self.pimg = v.p_class.image
        self.buttons = py.sprite.Group()
        self.buttons.add(MenuItems.Button("Respawn", (400, 375), 120, (200, 200, 200), (200, 0, 0),  "Resources/Fonts/Vecna.otf", "rs", True))
        self.buttons.add(MenuItems.Button("Load Save", (880, 375), 120, (200, 200, 200), (200, 0, 0), "Resources/Fonts/Vecna.otf", "ls", True))
        self.buttons.add(MenuItems.Button("Quit", (640, 480), 120, (200, 200, 200), (200, 0, 0), "Resources/Fonts/Vecna.otf", "qt", True))
        self.text = py.sprite.Group()
        self.text.add(MenuItems.textLabel("You Died!", (640, 255), (240, 240, 240), "Resources/Fonts/Vecna.otf", 180, centred=True))
        
        
    
    def update(self):
        if v.playerDead:
            ren = py.transform.scale(self.back, (int(1280 * (self.cycle / 100)), int(720 * (self.cycle / 100))))
            rect = py.Rect(1280/2 - (1280 * (self.cycle / 100))/2, 720/2 - (720 * (self.cycle / 100))/2, 1280 * (self.cycle / 100), 720 * (self.cycle / 100))
            v.screen.blit(ren, rect)
            self.red.fill((self.cycle - 100, 0, 0, self.cycle - 100))
            self.ghost.cycle = self.cycle
            self.ghost.update()
            v.screen.blit(self.red, (0, 0))
            if self.cycle > 250:
                self.buttons.update()
                self.text.update()
                for b in self.buttons:
                    if b.pressed():
                        if b.ID == "qt":
                            pass
                        if b.ID == "rs":
                            pass
                        if b.ID == "ls":
                            import setupScripts, SaveLoad
                            setupScripts.createGroups()
                            setupScripts.defaultVariables()
                            SaveLoad.Load()
                            v.newGame = False
                            gameScreens.game()
            if self.cycle < 355:
                self.cycle += 1
                