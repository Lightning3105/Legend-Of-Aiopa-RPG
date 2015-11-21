import pygame as py
import Variables as v
import MenuItems 
import entityClasses 
import guiClasses 
from functools import reduce
from os import listdir
from os import remove

import Map
import spellClasses

import itemClasses
from pygame.color import Color as colour
import sys
import inventoryScreen
import time
from random import randint
import npcScripts
import setupScripts
import SaveLoad

#TODO: Change projectiles so they work with lag
def mainMenu():
    py.init()
    windowUpdate()
    MenuItems.screen = v.screen
    buttons = py.sprite.Group()
    texts = []
    buttons.add(MenuItems.Button("New Game", (v.screenX * 0.25, v.screenY * 0.625), int(v.screenX * 0.125), colour("Light Green"), colour("Dark Green"), "Resources\Fonts\MorrisRoman.ttf", "play"))
    buttons.add(MenuItems.Button("Options", (v.screenX * 0.25, v.screenY * 0.79), int(v.screenX * 0.09375), colour("Light Green"), colour("Dark Green"), "Resources\Fonts\MorrisRoman.ttf", "options"))
    buttons.add(MenuItems.Button("Load", (v.screenX * 0.5625, v.screenY * 0.79), int(v.screenX * 0.09375), colour("Light Green"), colour("Dark Green"), "Resources\Fonts\MorrisRoman.ttf", "load"))
    texts.append(MenuItems.Text("The Legend", (v.screenX * 0.140625, v.screenY * 0.125), int(v.screenX * 0.125), colour("red"), "Resources\Fonts\RunicClear.ttf"))
    texts.append(MenuItems.Text("Of Aiopa", (v.screenX * 0.25, v.screenY * 0.29), int(v.screenX * 0.125), colour("red"), "Resources\Fonts\RunicClear.ttf"))
    texts.append(MenuItems.Text("Created By James", (v.screenX * 0.25, v.screenY * 0.5), int(v.screenX * 0.0625), colour("black"), "Resources\Fonts\Vecna.otf"))
    
    fade = MenuItems.fadeIn()
    fade.fadeIn = True
    
    setupScripts.initSound()
    f = open("log.txt", "w")
    f.write(str(listdir("Resources/Music")))
    f.close()
    v.music = py.mixer.Sound("Resources/Music/Title 1.ogg")
    v.music.play(loops=-1)
    while True:
        py.event.pump()
        
        MenuItems.fill_gradient(v.screen, colour("cyan"), colour("dark blue"))
        for text in texts:
            text.draw()
        buttons.update()
        v.events = []
        v.events = py.event.get()
        for event in v.events:
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.pressed():
                        id = button.ID
                        if id == "play":
                            setupScripts.createGroups()
                            classSelection()
                            setupScripts.defaultVariables()
                            #v.playerClass = "Mage"
                            setupScripts.setAttributes()
                            v.newGame = True
                            game()
                            return
                        if id == "options":
                            options()
                            return
                        if id == "load":
                            setupScripts.createGroups()
                            setupScripts.defaultVariables()
                            SaveLoad.Load()
                            v.newGame = False
                            game()
        fade.draw()
        fade.opacity -= 1
        py.display.flip()

def options():
    py.init()
    """if v.fullScreen:
        v.screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF|py.FULLSCREEN)
    else:
        v.screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF)"""
    buttons = py.sprite.Group()
    buttons.add(MenuItems.Button("Toggle Fullscreen", (v.screenX * 0.03125, v.screenY * 0.04), int(v.screenX * 0.09375), colour("beige"), colour("grey"), "Resources\Fonts\MorrisRoman.ttf", "fullscreen"))
    buttons.add(MenuItems.Button("Back", (v.screenX * 0.015625, v.screenY - v.screenY * 0.08), int(v.screenX * 0.046875), colour("red"), colour("brown"), "Resources\Fonts\RunicSolid.ttf", "back"))
    buttons.add(MenuItems.Button("Toggle Resolution", (v.screenX * 0.03125, v.screenY * 0.2), int(v.screenX * 0.09375), colour("beige"), colour("grey"), "Resources\Fonts\MorrisRoman.ttf", "resolution"))
    
    fade = MenuItems.fadeIn()
    fade.fadeIn = True
    while True:
        py.event.pump()
        MenuItems.fill_gradient(v.screen, colour("cyan"), colour("dark blue"))

        buttons.update()
        v.events = []
        v.events = py.event.get()
        for event in v.events:
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.pressed():
                        id = button.ID
                        if id == "fullscreen":
                            if v.fullScreen == False:
                                v.fullScreen = True
                            else:
                                v.fullScreen = False
                            
                        if id == "back":
                            mainMenu()
                            return
                        if id == "resolution":
                            if v.screenX == 640:
                                v.screenX = 800
                                v.screenY = 600
                            elif v.screenX == 800:
                                #v.screenX = 1024
                                #v.screenY = 768
                                v.screenX = 933
                                v.screenY = 700
                            elif v.screenX == 933:
                                v.screenX = 640
                                v.screenY = 480
                            elif v.screenX == 1024:
                                v.screenX = 640
                                v.screenY = 480
                        windowUpdate()
                        options()
                        return
        fade.draw()
        fade.opacity -= 1
        py.display.flip()


def windowUpdate():
    if v.fullScreen:
        v.screen = py.display.set_mode((v.screenX, v.screenY),py.HWSURFACE|py.DOUBLEBUF|py.FULLSCREEN)
    else:
        v.screen = py.display.set_mode((v.screenX, v.screenY),py.HWSURFACE|py.DOUBLEBUF)
    py.display.set_caption("The Legend Of Aiopa")
    icon = py.image.load("Resources/Images/Icon.ico")
    py.display.set_icon(icon)
    v.screenScale = round(v.screenX * 0.004, 1)
    """if v.screenX == 480:
        v.screenScale = 2
    if v.screenX == 800:
        v.screenScale = 2.5
    if v.screenX == 1024:
        v.screenScale = 4.3"""
        

    

def game():
    import weaponClasses
    load = guiClasses.loadingScreen()
    load.update(0)
    load.update(1)
    py.init()
    v.music.fadeout(2000)
    v.music = py.mixer.Sound("Resources/Music/Ambient 1.ogg")
    #v.music.play(loops=-1)
    v.PAUSED = False
    
    """if v.fullScreen:
        v.screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF|py.FULLSCREEN)
    else:
        v.screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF)"""

    v.p_class = entityClasses.Player()
    mask = entityClasses.mask()
    v.clock = py.time.Clock()
    py.time.set_timer(py.USEREVENT, 200) # walking
    py.time.set_timer(py.USEREVENT + 1, 50) # Spell animation
    py.time.set_timer(py.USEREVENT + 2, 1000) #One second

    
    
    
    v.allTiles = py.sprite.Group()
    v.topTiles = py.sprite.Group()
    v.allNpc = py.sprite.Group()
    v.droppedItems = py.sprite.Group()
    v.hitList = py.sprite.Group()
    Map.generateMap() #TODO: xp
    SaveLoad.loadMap(v.mapNum)
    #v.playerPosX = 0
    #v.playerPosY = 0
    
    v.hits = py.sprite.Group()
    v.hits.add(entityClasses.HitBox("Right"))
    v.hits.add(entityClasses.HitBox("Left"))
    v.hits.add(entityClasses.HitBox("Top"))
    v.hits.add(entityClasses.HitBox("Bottom"))
    
    weaponSlot = guiClasses.weaponSlot()
    
    xp = guiClasses.XP()
    loclab = guiClasses.locationTitle()
    

    pause = guiClasses.pauseScreen()
    
    #map = guiClasses.miniMap()

    if v.newGame:
        setupScripts.newGame()
        v.newGame = False
    load.update(2)
    while True:
        if not v.PAUSED:
            v.ticks += 1
            v.screen.fill((0, 0, 0))
            py.event.pump()
            v.actionsDone = []
            v.events = []
            v.events = py.event.get()
            v.clock.tick(60)
            try:
                v.fpsAdjuster = (v.fpsLock/v.clock.get_fps())
            except:
                v.fpsAdjuster = 1
            
            v.MAP.update()
            v.allTiles.update()
            #v.allTiles.draw(v.screen)
            v.droppedItems.update()
            v.droppedItems.draw(v.screen)
            v.p_class.draw()
            weaponClasses.updateEquipped("Weapon")
            v.equippedSpells.update()
            v.allNpc.update()
            v.allNpc.draw(v.screen)
            v.p_class.update()
            
            v.xpGroup.update()
            v.xpGroup.draw(v.screen)
            v.playerStopped = False
            v.playerActing = False
            weaponClasses.drawEquipped("Weapon")
            v.equippedSpells.draw(v.screen)
            v.particles.update()
            #v.hits.draw(v.screen)
            v.topTiles.draw(v.screen)
            mask.update()
            mask.draw()
            v.mask = False
            
            guiClasses.update_health()
            guiClasses.update_mana()
            guiClasses.actionText()
            xp.update()
            weaponSlot.draw()
            v.abilityButtons.update()
            loclab.update()
            #map.update()
            guiClasses.fps()
            
            py.display.flip()
            for event in v.events:
                if event.type == py.QUIT:
                    sys.exit()
                elif event.type==py.VIDEORESIZE:
                    v.screen = py.display.set_mode(event.dict['size'],py.HWSURFACE|py.DOUBLEBUF)
    
            keys_pressed = py.key.get_pressed()
            if keys_pressed[py.K_SPACE] and not v.playerActing:
                weaponClasses.weaponAttack()
            if keys_pressed[py.K_KP_PLUS]:
                v.scale += 0.1
                v.scale = round(v.scale, 1)
                print(v.scale)
            if keys_pressed[py.K_KP_MINUS]:
                v.scale -= 0.1
                v.scale = round(v.scale, 1)
                print(v.scale)
            for event in v.events:
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        v.PAUSED = True
                        v.justPaused = True
                        v.pauseType = "Pause"
                    if event.key == py.K_e:
                        v.PAUSED = True
                        v.justPaused = True
                        v.pauseType = "Inventory"
            if v.scale <= 0.1:
                v.scale = 0.1
        if v.PAUSED and v.pauseType == "Pause":
            if v.justPaused:
                background = py.image.tostring(v.screen, "RGBA")
                v.justPaused = False
            py.event.pump()
            v.clock.tick(30)
            v.events = []
            v.events = py.event.get()
            backgroundImage = py.image.fromstring(background, (v.screenX, v.screen.get_rect()[3]), "RGBA")
            v.screen.blit(backgroundImage, (0, 0))
            pause.update()
            py.display.flip()
            
            for event in v.events:
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        v.PAUSED = False
                if event.type == py.QUIT:
                    sys.exit()
        if v.PAUSED and v.pauseType == "Inventory":
            if v.justPaused:
                background = py.image.tostring(v.screen, "RGBA")
                v.justPaused = False
                invScreen = inventoryScreen.inventoryScreen()
            py.event.pump()
            v.clock.tick(30)
            v.events = []
            v.events = py.event.get()
            
            backgroundImage = py.image.fromstring(background, (v.screenX, v.screen.get_rect()[3]), "RGBA")
            v.screen.blit(backgroundImage, (0, 0))
            
            invScreen.update()
            
            py.display.flip()
            for event in v.events:
                if event.type == py.KEYDOWN:
                    if event.key == py.K_e:
                        v.PAUSED = False
                        invScreen.save()
                        #py.time.delay(100)
                if event.type == py.QUIT:
                    sys.exit()
        
        if v.PAUSED and v.pauseType == "Conversation":
            if v.justPaused:
                background = py.image.tostring(v.screen, "RGBA")
                v.justPaused = False
            py.event.pump()
            v.clock.tick(30)
            v.events = []
            v.events = py.event.get()
            backgroundImage = py.image.fromstring(background, (v.screenX, v.screen.get_rect()[3]), "RGBA")
            v.screen.blit(backgroundImage, (0, 0))
            grey = py.Surface((v.screenX, v.screen.get_rect()[3])).convert_alpha()
            grey.fill((20, 20, 20, 200))
            v.screen.blit(grey, (0, 0))
            v.conversationClass.update()
            py.display.flip()
            
            for event in v.events:
                if event.type == py.QUIT:
                    sys.exit()    
        

def classSelection():
    py.init()
    classes = py.sprite.Group()
    classes.add(MenuItems.characterSelector("Resources/Images/PaladinClass.png", (v.screenX / 8 * 1, v.screen.get_rect()[3]/1.5), "Paladin"))
    classes.add(MenuItems.characterSelector("Resources/Images/MageClass.png", (v.screenX / 8 * 2, v.screen.get_rect()[3]/3), "Mage"))
    classes.add(MenuItems.characterSelector("Resources/Images/RangerClass.png", (v.screenX / 8 * 3, v.screen.get_rect()[3]/1.5), "Ranger"))
    classes.add(MenuItems.characterSelector("Resources/Images/RogueClass.png", (v.screenX / 8 * 4, v.screen.get_rect()[3]/3), "Rogue"))
    classes.add(MenuItems.characterSelector("Resources/Images/BarbarianClass.png", (v.screenX / 8 * 5, v.screen.get_rect()[3]/1.5), "Barbarian"))
    classes.add(MenuItems.characterSelector("Resources/Images/NecromancerClass.png", (v.screenX / 8 * 6, v.screen.get_rect()[3]/3), "Necromancer"))
    classes.add(MenuItems.characterSelector("Resources/Images/VoyantClass.png", (v.screenX / 8 * 7, v.screen.get_rect()[3]/1.5), "Voyant"))
    py.time.set_timer(py.USEREVENT, 10) # moving and growing animation speed
    
    v.custimizationStage = "Class Selection"
    
    os = MenuItems.optionSlate()
    
    attOptions = py.sprite.Group()
    AoX = v.screenY * 0.21
    for attribute in v.Attributes:
        attOptions.add(MenuItems.optionAttribute(AoX, attribute))
        AoX += v.screenX * 0.046875
    #attOptions.add(MenuItems.optionAttribute(100, "Max Health"))
    #attOptions.add(MenuItems.optionAttribute(130, "Speed"))
    
    labels = py.sprite.Group()
    labels.add(MenuItems.textLabel("Define Character Attributes", (v.screenX * 0.390625, v.screenY * 0.08), colour("Black"), "Resources/Fonts/RPGSystem.ttf", int(v.screenX * 0.0546875)))
    labels.add(MenuItems.textLabel("Skill Points Remaining:", (v.screenX * 0.390625, v.screenY * 0.14), colour("grey"), "Resources/Fonts/RPGSystem.ttf", int(v.screenX * 0.046875)))
    labels.add(MenuItems.textLabel("skillPoints", (v.screenX * 0.78125, v.screenY * 0.14), colour("green"), "Resources/Fonts/RPGSystem.ttf", int(v.screenX * 0.046875), True))
    
    buttons = py.sprite.Group()
    buttons.add(MenuItems.Button("Back", (v.screenX * 0.015625, v.screenY * 0.9), int(v.screenX * 0.046875), colour("red"), colour("brown"), "Resources\Fonts\RunicSolid.ttf", "back"))
    buttons.add(MenuItems.Button("Continue", (v.screenX * 0.859375, v.screenY * 0.86875), int(v.screenX * 0.03125), colour("brown"), (153, 76, 0), "Resources\Fonts\RunicSolid.ttf", "continue"))

    background = MenuItems.shiftingGradient((50, 0, 0), (205, 0, 0))
    
    aps = py.sprite.Group()
    
    num = 1
    for i in listdir("Resources/Images/Character Customisation/Body"):
        aps.add(MenuItems.apearanceSelector("Resources/Images/Character Customisation/Body/" + i, "Body", num))
        num += 1
    
    num = 1
    for i in listdir("Resources/Images/Character Customisation/Face"):
        aps.add(MenuItems.apearanceSelector("Resources/Images/Character Customisation/Face/" + i, "Face", num))
        num += 1
    
    num = 1
    for i in listdir("Resources/Images/Character Customisation/Dress"):
        aps.add(MenuItems.apearanceSelector("Resources/Images/Character Customisation/Dress/" + i, "Dress", num))
        num += 1
    
    num = 1
    for i in listdir("Resources/Images/Character Customisation/Hair"):
        aps.add(MenuItems.apearanceSelector("Resources/Images/Character Customisation/Hair/" + i, "Hair", num))
        num += 1
    
    ap = MenuItems.appearancePreview()
    
    aTabs = MenuItems.appearanceTab()
    
    py.time.set_timer(py.USEREVENT + 1, 2000) #preview rotate speed
    fade = MenuItems.fadeIn()
    fade.fadeIn = True
    
    nti = MenuItems.textInput((260/640 * v.screenX, 240/640 * v.screenX), int(50/640 * v.screenX), 8, (255, 178, 102), None)
    nts = py.sprite.Group()
    nts.add(MenuItems.textLabel("Name Your Character:", (260/640 * v.screenX, 180/640 * v.screenX), colour("black"), "Resources/Fonts/RPGSystem.ttf", int(40/640 * v.screenX), False))
    nts.add(MenuItems.textLabel("(Max 8 Characters)", (260/640 * v.screenX, 220/640 * v.screenX), colour("grey"), "Resources/Fonts/RPGSystem.ttf", int(20/640 * v.screenX), False))
    
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        
        background.draw()
        
        classes.update()
        classes.draw(v.screen)
        
        os.update()
        attOptions.update()
        
        for button in buttons:
            if button.ID == "back":
                button.update()
            else:
                if v.custimizationStage == "Attributes" or v.custimizationStage == "Customisation" or v.custimizationStage == "Name":
                    button.update()
        
        if v.custimizationStage == "Attributes":
            labels.update()
        if v.custimizationStage == "Customisation":
            aps.update()
            aps.draw(v.screen)
            ap.draw()
            aTabs.draw()
            for key in v.testAppearance:
                v.testAppearance[key] = None
            for event in v.events:
                if event.type == py.USEREVENT + 1:
                    if v.appearancePrevNum == 7:
                        v.appearancePrevNum = 10
                    elif v.appearancePrevNum == 10:
                        v.appearancePrevNum = 1
                    elif v.appearancePrevNum == 1:
                        v.appearancePrevNum = 4
                    elif v.appearancePrevNum == 4:
                        v.appearancePrevNum = 7
                    else:
                        v.appearancePrevNum = 7
        if v.custimizationStage == "Name":
            nti.update()
            ap.draw()
            nts.update()
  
        for event in v.events:
            if event.type == py.QUIT:
                sys.exit()
            elif event.type == py.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.pressed():
                        id = button.ID
                        if id == "back":
                            mainMenu()
                            return
                        if id == "continue":
                            if v.custimizationStage == "Attributes":
                                v.custimizationStage = "Customisation"
                                v.appearanceTab = "Body"
                                for ao in attOptions:
                                    ao.save()
                            elif v.custimizationStage == "Customisation":
                                v.custimizationStage = "Name"
                            elif v.custimizationStage == "Name":
                                nti.outText
                                return
                        
            
        
        #v.characterHovered = False
        fade.draw()
        fade.opacity -= 1

        py.display.flip()


def story():
    py.init()
    windowUpdate()
    LS1 = py.transform.scale(py.image.load("Resources/Images/Story/LS1.png"), (v.screenX, v.screenY))
    _LS1 = py.transform.scale(py.image.load("Resources/Images/Story/LS1.png"), (v.screenX, v.screenY))
    LS2 = py.transform.scale(py.image.load("Resources/Images/Story/LS2.png"), (v.screenX, v.screenY))
    LS3 = py.transform.scale(py.image.load("Resources/Images/Story/LS3.png"), (v.screenX, v.screenY))
    LS4 = py.transform.scale(py.image.load("Resources/Images/Story/LS4.png"), (v.screenX, v.screenY))
    LS4Ani = entityClasses.SpriteSheet("Resources/Images/Story/LS4 Ani.png", 10, 1)
    LS3Ani = entityClasses.SpriteSheet("Resources/Images/Story/LS3 Ani.png", 2, 1)
    P1 = py.transform.scale(py.image.load("Resources/Images/Story/Ground Images/Person 1.png"), (int(22/640 * v.screenX), int(28/640 * v.screenX)))
    P2 = py.transform.scale(py.image.load("Resources/Images/Story/Ground Images/Person 2.png"), (int(22/640 * v.screenX), int(28/640 * v.screenX)))
    lsY = 1400
    zoom = 1
    v.clock = py.time.Clock()
    ani1 = py.Surface((0, 0))
    ani2 = py.Surface((0, 0))
    ani3 = py.Surface((0, 0))
    ani4 = py.Surface((0, 0))
    WB = py.Surface((v.screenX, v.screenY))
    WB.set_alpha(255)
    WB.fill((255, 255, 255))
    WBAlpha = 0
    STAGE = 2
    ST3 = 0
    
    Characters = []
    Characters.append(py.image.load("Resources/Images/PaladinClass.png"))
    Characters.append(py.image.load("Resources/Images/MageClass.png"))
    Characters.append(py.image.load("Resources/Images/RangerClass.png"))
    Characters.append(py.image.load("Resources/Images/RogueClass.png"))
    Characters.append(py.image.load("Resources/Images/BarbarianClass.png"))
    Characters.append(py.image.load("Resources/Images/NecromancerClass.png"))
    Characters.append(py.image.load("Resources/Images/VoyantClass.png"))
    IM1 = py.transform.scale(py.image.load("Resources/Images/Story/IB1.png"), (v.screenX, v.screenY))
    IMEvil = entityClasses.SpriteSheet("Resources/Images/Story/DarkLord.png", 4, 3)
    
    TM = py.transform.scale(py.image.load("Resources/Images/Story/Tall Mountain.png"), (v.screenX, v.screenY))
    TMZoom = 1
    
    while True:
        if STAGE == 1:
            v.clock.tick(60)
            v.screen.fill((0, 255, 255))
            if zoom > 1:
                LS1 = py.transform.scale(_LS1, (int(v.screenX * zoom), int(v.screenY * zoom)))
                v.screen.blit(LS1, ((v.screenX/2) - int(v.screenX * zoom)/2, ((v.screenY/4) - int(v.screenY * zoom)/4)))
            else:
                v.screen.blit(LS1, (0, v.screenY * -3 + lsY))
            v.screen.blit(LS2, (0, v.screenY * -2 + lsY))
            v.screen.blit(LS3, (0, v.screenY * -1 + lsY))
            v.screen.blit(LS4, (0, v.screenY * 0 + lsY))
            if lsY < 180:
                ani1 = py.transform.scale(LS4Ani.images[int(lsY/18)], (v.screenX, v.screenY))
            v.screen.blit(ani1, (0, v.screenY * 0 + lsY))
            
            ani2 = py.transform.scale(LS3Ani.images[lsY % 2], (v.screenX, v.screenY))
            v.screen.blit(ani2, (-v.screenX * 1.4 + lsY, v.screenY * -0.5 + lsY))
            
            ani2 = py.transform.scale(LS3Ani.images[(lsY + 1) % 2], (v.screenX, v.screenY))
            ani2 = py.transform.flip(ani2, True, False)
            v.screen.blit(ani2, (v.screenX * 1.6 - lsY, v.screenY * -1.1 + lsY))
            
            if lsY % 4 == 0:
                ani3 = py.transform.rotate(P1, randint(-5, 5))
                ani4 = py.transform.rotate(P2, randint(-5, 5))
            if zoom == 1:
                pos = (v.screenX * 2.6 - lsY, v.screenY * -2.55 + lsY * 1.1)
                v.screen.blit(ani3, pos)
                pos = (v.screenX * 2.65 - lsY, v.screenY * -2.55 + lsY * 1.1)
                v.screen.blit(ani4, pos)
            
            if lsY < 1440:
                lsY += 1
            elif zoom < 5:
                zoom *= 1.01
            if zoom >= 3:
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))
                WBAlpha += 5
            if WBAlpha >= 255:
                STAGE = 2
            py.display.flip()
        if STAGE == 2:
            v.clock.tick(60)
            v.screen.fill((0, 255, 255))
            
            tm = py.transform.scale(TM, (int(v.screenX * TMZoom), int(v.screenY * TMZoom)))
            v.screen.blit(tm, ((v.screenX/2) - int(v.screenX * TMZoom)/2, ((v.screenY/4) - int(v.screenY * TMZoom)/4)))
            
            if WBAlpha > 0:
                WBAlpha -= 3
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))
            if TMZoom < 5:
                TMZoom *= 1.01
            if TMZoom > 1.5:
                WB.set_alpha(WBAlpha)
                WB.fill((0, 0, 0))
                v.screen.blit(WB, (0, 0))
                WBAlpha += 5
            if WBAlpha >= 255:
                STAGE = 3
            py.display.flip()
        
        
        if STAGE == 3:
            v.clock.tick(60)
            v.screen.fill((0, 0, 0))
            v.screen.blit(IM1, (0, 0))
            
            ST3 += 1
            if WBAlpha > 0:
                WBAlpha -= 3
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))
            
            posx = 50
            posy = v.screenY * 0.55 #65
            for i in Characters:
                size = i.get_rect()
                size.width = ((size.width * 3) / 640) * v.screenX
                size.height = ((size.height * 3) / 480) * v.screenY
                ren = py.transform.scale(i, (size.width, size.height))
                pos = (posx, posy)
                posx += 80
                if posx < 320:
                    posy -= 15 #30
                else:
                    posy += 15
                
                v.screen.blit(ren, pos)
            
            size = IMEvil.images[1].get_rect().size
            ev = py.transform.scale(IMEvil.images[1], (int(size[0] * 4/640 * v.screenX), int(size[1] * 4/640 * v.screenX)))
            v.screen.blit(ev, (v.screenX * 0.4 - int(size[0] * 4/640 * v.screenX)/2, v.screenY * 0.7))
            
                
            py.display.flip()
            
            
        
        
