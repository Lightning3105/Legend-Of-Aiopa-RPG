import pygame as py
import Variables as v
import MenuItems 
import entityClasses 
import guiClasses 
from os import listdir

import Map

from pygame.color import Color as colour
import sys
import inventoryScreen
import time
from random import randint
import setupScripts
import SaveLoad
import random
import hashlib

#TODO: Change projectiles so they work with lag
def mainMenu():
    py.init()
    windowUpdate()
    MenuItems.screen = v.screen
    buttons = py.sprite.Group()
    texts = []
    buttons.add(MenuItems.Button("New Game", (v.screenX * 0.5, v.screenY * 0.5), int(v.screenX * 0.09), colour("Light Green"), colour("Dark Green"), "Resources\Fonts\MorrisRoman.ttf", "play", centred=True))
    buttons.add(MenuItems.Button("Options", (v.screenX * 0.5, v.screenY * 0.63), int(v.screenX * 0.09), colour("Light Green"), colour("Dark Green"), "Resources\Fonts\MorrisRoman.ttf", "options", centred=True))
    buttons.add(MenuItems.Button("Load", (v.screenX * 0.5, v.screenY * 0.76), int(v.screenX * 0.09), colour("Light Green"), colour("Dark Green"), "Resources\Fonts\MorrisRoman.ttf", "load", centred=True))
    buttons.add(MenuItems.Button("Aiopa Online", (v.screenX * 0.5, v.screenY * 0.89), int(v.screenX * 0.09), colour("Light Green"), colour("Dark Green"), "Resources\Fonts\MorrisRoman.ttf", "online", centred=True))
    
    texts.append(MenuItems.Text("The Legend", (v.screenX * 0.140625, v.screenY * 0.01), int(v.screenX * 0.125), colour("red"), "Resources\Fonts\RunicClear.ttf"))
    texts.append(MenuItems.Text("Of Aiopa", (v.screenX * 0.25, v.screenY * 0.15), int(v.screenX * 0.125), colour("red"), "Resources\Fonts\RunicClear.ttf"))
    texts.append(MenuItems.Text("Created By James", (v.screenX * 0.25, v.screenY * 0.32), int(v.screenX * 0.0625), colour("black"), "Resources\Fonts\Vecna.otf"))
    
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
                            setupScripts.defaultVariables()
                            classSelection()
                            #v.playerClass = "Mage"
                            setupScripts.setAttributes()
                            v.newGame = True
                            story()
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
                        if id == "online":
                            onlineLogin()
        fade.draw()
        fade.opacity -= 1
        py.display.flip()

def onlineLogin():
    py.init()
    texts = py.sprite.Group()
    tinps = py.sprite.Group()
    extraTexts = py.sprite.Group()
    buttons = py.sprite.Group()
    
    texts.add(MenuItems.textLabel("Username", (v.screenX * 0.2, v.screenX * 0.31), (220, 220, 220), "Resources\Fonts\MorrisRoman.ttf", 20, variable=False, centred=False))
    texts.add(MenuItems.textLabel("Password", (v.screenX * 0.2, v.screenX * 0.51), (220, 220, 220), "Resources\Fonts\MorrisRoman.ttf", 20, variable=False, centred=False))
    
    texts.add(MenuItems.textLabel("Login To", (v.screenX * 0.140625, v.screenY * 0.01), (255, 0, 255), "Resources\Fonts\RunicSolid.ttf", int(v.screenX * 0.1)))
    texts.add(MenuItems.textLabel("Aiopa Online", (v.screenX * 0.25, v.screenY * 0.15), (255, 0, 255), "Resources\Fonts\RunicSolid.ttf", int(v.screenX * 0.1)))
    
    v.textNum = 1
    tinps.add(MenuItems.textInput((v.screenX * 0.4, v.screenX * 0.3), 20, 16, num=1, button=None, default=['1'], type="str", fontfile="Resources/Fonts/RPGSystem.ttf", background=(255, 255, 255)))
    tinps.add(MenuItems.textInput((v.screenX * 0.4, v.screenX * 0.5), 20, 16, num=2, button=None, default=['1'], type="pass", fontfile="Resources/Fonts/RPGSystem.ttf", background=(255, 255, 255)))
    
    buttons.add(MenuItems.Button("Back", (v.screenX * 0.015625, v.screenY * 0.9), int(v.screenX * 0.046875), colour("red"), colour("brown"), "Resources\Fonts\RunicSolid.ttf", "back"))
    buttons.add(MenuItems.Button("Continue", (v.screenX * 0.77, v.screenY * 0.9), int(v.screenX * 0.046875), colour("red"), colour("brown"), "Resources\Fonts\RunicSolid.ttf", "continue"))
    
    logintext = MenuItems.textLabel("Logging In", (v.screenX * 0.5, v.screenY * 0.5), (255, 255, 255), "Resources/Fonts/RPGSystem.ttf", int(30/640 * v.screenX), variable=False, centred=True)
    background = MenuItems.shiftingGradient((0, 0, 'x'))
    fade = MenuItems.fadeIn()
    fade.fadeIn = True
    py.time.set_timer(py.USEREVENT, 500) #dot dot dot
    
    phase = 1
    loginTimer = 0
    
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        background.draw()
        if phase == 1:
            texts.update()
            extraTexts.update()
            tinps.update()
            buttons.update()
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.pressed():
                            if button.ID == "back":
                                mainMenu()
                                return
                            if button.ID == "continue":
                                phase = 2
                                loginTimer = 0
                                logintext.update()
                                for inp in tinps:
                                    if inp.num == 1:
                                        user = inp.outText
                                    if inp.num == 2:
                                        passw = inp.outText
        elif phase == 2:
            for event in v.events:
                if event.type == py.USEREVENT:
                    if logintext.text == "Logging In":
                        logintext.text = "Logging In."
                    elif logintext.text == "Logging In.":
                        logintext.text = "Logging In.."
                    elif logintext.text == "Logging In..":
                        logintext.text = "Logging In..."
                    elif logintext.text == "Logging In...":
                        logintext.text = "Logging In"
            logintext.update()
            loginTimer += 1
            if loginTimer >= 20:
                accOut = SaveLoad.getAccount(user, passw)
                if accOut == "USERNAME":
                    phase = 1
                    extraTexts = MenuItems.textLabel("Username does not exist", (v.screenX * 0.4, v.screenX * 0.26), (255, 0, 0), "Resources\Fonts\MorrisRoman.ttf", 20, variable=False, centred=False)
                elif accOut == "PASSWORD":
                    phase = 1
                    extraTexts = MenuItems.textLabel("Incorrect password", (v.screenX * 0.4, v.screenX * 0.46), (255, 0, 0), "Resources\Fonts\MorrisRoman.ttf", 20, variable=False, centred=False)
                else:
                    v.account = accOut
                    v.username = user
                    hash_object = hashlib.md5(passw.encode())
                    hash = hash_object.hexdigest()
                    v.password = hash
                    onlineMenu()
                    
                    return
        
        
        fade.draw()
        fade.opacity -= 1                    
        py.display.flip()
        
def onlineMenu():
    py.init()
    
    buttons = py.sprite.Group()
    
    buttons.add(MenuItems.Button("Upload Save", (v.screenX * 0.2, v.screenY * 0.5), 40, (100, 200, 200), (0, 255, 255), "Resources\Fonts\MorrisRoman.ttf", "upload", centred=True))
    buttons.add(MenuItems.Button("Download Save", (v.screenX * 0.8, v.screenY * 0.5), 40, (100, 200, 200), (0, 255, 255), "Resources\Fonts\MorrisRoman.ttf", "download", centred=True))
    buttons.add(MenuItems.Button("Back", (v.screenX * 0.015625, v.screenY * 0.9), int(v.screenX * 0.046875), colour("red"), colour("brown"), "Resources\Fonts\RunicSolid.ttf", "back"))

    
    background = MenuItems.shiftingGradient((0, 0, 'x'))
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        background.draw()
        buttons.update()
        for event in v.events:
            if event.type == py.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.pressed():
                        if button.ID == "upload":
                            SaveLoad.uploadSave()
                        if button.ID == "download":
                            SaveLoad.downloadSave()
                        if button.ID == "back":
                            mainMenu()
                            return
        
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
        MenuItems.fill_gradient(v.screen, colour("cyan"), colour("green"))

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
    v.NPCs = py.sprite.Group()
    v.droppedItems = py.sprite.Group()
    v.hitList = py.sprite.Group()
    SaveLoad.loadMap(v.mapNum)
    Map.generateMap() #TODO: xp
    
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
            
            v.quests.update()
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
            if keys_pressed[py.K_p]:
                v.playerHealth = 0
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
        
        if v.PAUSED and v.pauseType == "Death":
            if v.justPaused:
                background = py.image.tostring(v.screen, "RGBA")
                v.justPaused = False
                deathScreen = guiClasses.deathScreen()
            py.event.pump()
            v.clock.tick(30)
            v.events = []
            v.events = py.event.get()
            
            deathScreen.update()
            py.display.flip()
            
            for event in v.events:
                if event.type == py.KEYDOWN:
                    if event.key == py.K_ESCAPE:
                        v.PAUSED = False
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
    
    background = MenuItems.shiftingGradient(('x', 0, 0))
    
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
    
    nti = MenuItems.textInput((260/640 * v.screenX, 260/640 * v.screenX), int(40/640 * v.screenX), 8, 1, background=(255, 178, 102), button=None, default=[], type="str")
    nts = py.sprite.Group()
    nts.add(MenuItems.textLabel("Name Your Character:", (260/640 * v.screenX, 180/640 * v.screenX), colour("black"), "Resources/Fonts/RPGSystem.ttf", int(40/640 * v.screenX), False))
    nts.add(MenuItems.textLabel("(Max 8 Characters)", (260/640 * v.screenX, 220/640 * v.screenX), colour("grey"), "Resources/Fonts/RPGSystem.ttf", int(20/640 * v.screenX), False))
    
    bigcont = MenuItems.Button("Continue", (v.screenX * 0.77, v.screenY * 0.9), int(v.screenX * 0.046875), colour("red"), colour("brown"), "Resources\Fonts\RunicSolid.ttf", "continue")
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        
        background.draw()
        
        classes.update()
        classes.draw(v.screen)
        
        os.update()
        if v.custimizationStage == "Attributes":
            attOptions.update()
        
        for button in buttons:
            if button.ID == "back":
                button.update()
            else:
                if v.custimizationStage == "Attributes" or v.custimizationStage == "Customisation":
                    button.update()
                if v.custimizationStage == "Name":
                    bigcont.update()
        
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
                if v.custimizationStage == "Name" and bigcont.pressed():
                    nti.outText
                    return
                        
            
        
        #v.characterHovered = False
        fade.draw()
        fade.opacity -= 1

        py.display.flip()


def story():
    #2.05 minutes
    sTime = time.clock()
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
    lsY = -480
    zoom = 1
    v.clock = py.time.Clock()
    ani1 = py.transform.scale(LS4Ani.images[0], (v.screenX, v.screenY))
    ani2 = py.Surface((0, 0))
    ani3 = py.Surface((0, 0))
    ani4 = py.Surface((0, 0))
    WB = py.Surface((v.screenX, v.screenY))
    WB.set_alpha(255)
    WB.fill((255, 255, 255))
    WBAlpha = 0
    STAGE = 1
    ST3 = 0
    ST2 = 0
    ST4 = 0
    ST5 = 0
    ST6 = 0
    
    Characters = []
    Characters.append(py.image.load("Resources/Images/PaladinClass.png"))
    Characters.append(py.image.load("Resources/Images/MageClass.png"))
    Characters.append(py.image.load("Resources/Images/RangerClass.png"))
    Characters.append(py.image.load("Resources/Images/RogueClass.png"))
    Characters.append(py.image.load("Resources/Images/BarbarianClass.png"))
    Characters.append(py.image.load("Resources/Images/NecromancerClass.png"))
    Characters.append(py.image.load("Resources/Images/VoyantClass.png"))
    IM1 = py.transform.scale(py.image.load("Resources/Images/Story/IB1.png"), (v.screenX, v.screenY))
    IM2 = py.transform.scale(py.image.load("Resources/Images/Story/IB2.png"), (v.screenX, v.screenY))
    IMEvil = entityClasses.SpriteSheet("Resources/Images/Story/DarkLord.png", 4, 3)
    IMSpells = py.sprite.Group()
    NexusC = py.transform.scale(py.image.load("Resources/Images/Story/Nexus Beam C.png"), (int(145/640 * v.screenX), int(480/640 * v.screenX))).convert_alpha()
    NexusP = py.transform.scale(py.image.load("Resources/Images/Story/Nexus Beam P.png"), (int(145/640 * v.screenX), int(480/640 * v.screenX))).convert_alpha()
    NexusCP = py.transform.scale(py.image.load("Resources/Images/Story/Nexus Beam CP.png"), (int(145/640 * v.screenX), int(480/640 * v.screenX))).convert_alpha()
    NexusC.fill((255, 255, 255, 200), special_flags=py.BLEND_RGBA_MULT)
    NexusP.fill((255, 255, 255, 200), special_flags=py.BLEND_RGBA_MULT)
    NexusCP.fill((255, 255, 255, 200), special_flags=py.BLEND_RGBA_MULT)
    
    rock = py.transform.scale(py.image.load("Resources/Images/Story/Rock.png"), (int(200/640 * v.screenX), int(150/640 * v.screenX)))
    
    TM = py.transform.scale(py.image.load("Resources/Images/Story/Tall Mountain.png"), (v.screenX, v.screenY))
    TMZoom = 1
    
    FI1 = py.transform.scale(py.image.load("Resources/Images/Story/FI1.png"), (int(1280/640 * v.screenX), int(533/640 * v.screenX)))
    
    font = py.font.Font("Resources/Fonts/MorrisRoman.ttf", 40)
    font2 = py.font.Font("Resources/Fonts/MorrisRoman.ttf", 15)
    aiopaMain = entityClasses.SpriteSheet("Resources/Images/Story/Aiopa Title.png", 7, 3)
    
    MP = py.transform.scale(py.image.load("Resources/Images/Story/MP1.png"), (v.screenX, v.screenY))
    
    skp = 0
    
    #FONT OPACITY:
    #255 - abs(((VARIABLE + MIDPOINT) * (HALF OF RANGE/100))
    rot = []
    ran = []
    for i in range(0, 20):
        rot.append(randint(-45, 45))
    for i in range(0, 20):
        ran.append(randint(0, 200))
    
    fadeIn = False
    
    while True:
        py.event.pump()
        if STAGE == 1:
            v.clock.tick(60)
            v.screen.fill((0, 0, 0))
            if zoom > 1:
                LS1 = py.transform.scale(_LS1, (int(v.screenX * zoom), int(v.screenY * zoom)))
                v.screen.blit(LS1, ((v.screenX/2) - int(v.screenX * zoom)/2, ((v.screenY/4) - int(v.screenY * zoom)/4)))
            else:
                if lsY < 1440:
                    v.screen.blit(LS1, (0, v.screenY * -3 + lsY))
                else:
                    v.screen.blit(LS1, (0, 0))
                
            if lsY < 1440:    
                v.screen.blit(LS2, (0, v.screenY * -2 + lsY))
                v.screen.blit(LS3, (0, v.screenY * -1 + lsY))
                v.screen.blit(LS4, (0, v.screenY * 0 + lsY))
                if lsY < 200 and lsY > -300:
                    ani1 = py.transform.scale(LS4Ani.images[int((lsY + 300)/50)], (v.screenX, v.screenY))
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
            
            if lsY < 1700:
                lsY += 1
            elif zoom < 5:
                zoom *= 1.01
                
            if lsY > -480 and lsY < -200:
                label = font.render("Once Upon a time...", 1, (255, 255, 255))
                op = 255 - abs(((lsY + 340) * 1.8))
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.5, v.screenY * 0.75))
            
            if lsY > -280 and lsY < 0:
                label = font.render("There was a perfect land...", 1, (255, 255, 255))
                op = 255 - abs(((lsY + 140) * 1.8))
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (0, v.screenY * 0.25))
            if lsY > -80 and lsY < 200:
                label = font.render("A land of RICHES...", 1, (255, 255, 255))
                op = 255 - abs(((-1*lsY) + 60) * 1.8)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.4, v.screenY * 0.5))
            if lsY > 220 and lsY < 500:
                label = font.render("A land of NATURE...", 1, (255, 255, 255))
                op = 255 - abs((((-1*(lsY - 300)) + 60) * 1.8))
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.25, v.screenY * 0.2))
            if lsY > 420 and lsY < 700:
                label = font.render("A land of LIFE...", 1, (255, 255, 255))
                op = 255 - abs((((-1*(lsY - 500)) + 60) * 1.8))
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.6, v.screenY * 0.7))
            if lsY > 720 and lsY < 1000:
                label = font.render("A land of MAGIC...", 1, (255, 255, 255))
                op = 255 - abs((((-1*(lsY - 800)) + 60) * 1.8))
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.1, v.screenY * 0.5))
            if lsY > 920 and lsY < 1200:
                label = font.render("A land of PEACE...", 1, (255, 255, 255))
                op = 255 - abs((((-1*(lsY - 1000)) + 60) * 1.8))
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.4, v.screenY * 0.3))
            if lsY > 1120 and lsY < 1400:
                label = font.render("A land named...", 1, (255, 255, 255))
                op = 255 - abs((((-1*(lsY - 1200)) + 60) * 1.8))
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.3, v.screenY * 0.1))
            if lsY > 1300 and lsY < 1700:
                size = aiopaMain.images[lsY % 18].get_rect().size
                label = py.transform.scale(aiopaMain.images[lsY % 18], (int((size[0] * ((lsY - 1300)/100))/640 * v.screenX), int((size[1] * ((lsY - 1300)/100))/640 * v.screenX)))
                if lsY > 1550:
                    alph = 255 - ((lsY - 1550) * 1.7)
                    if alph > 0:
                        label.fill((255, 255, 255, alph), special_flags=py.BLEND_RGBA_MULT)
                
                v.screen.blit(label, (v.screenX * 0.5 - (label.get_rect().width/2), v.screenY * 0.5 - (label.get_rect().height/2)))
            
            
            if zoom >= 3:
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))
                WBAlpha += 5
                fadeIn = True
            if WBAlpha >= 255 and lsY > 1600:
                STAGE = 2

        if STAGE == 2:
            v.clock.tick(60)
            v.screen.fill((0, 255, 255))
            
            tm = py.transform.scale(TM, (int(v.screenX * TMZoom), int(v.screenY * TMZoom)))
            v.screen.blit(tm, ((v.screenX/2) - int(v.screenX * TMZoom)/2, ((v.screenY/4) - int(v.screenY * TMZoom)/4)))
            
            if WBAlpha > 0 and fadeIn:
                WBAlpha -= 3
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))
            if WBAlpha <= 0:
                fadeIn = False
            if TMZoom < 5:
                TMZoom *= 1.001
            if TMZoom > 2 and fadeIn == False:
                if WBAlpha <= 255:
                    WBAlpha += 4
                WB.set_alpha(WBAlpha)
                WB.fill((0, 0, 0))
                v.screen.blit(WB, (0, 0))
                
            
            if TMZoom > 1 and TMZoom < 2:
                label = font.render("The world was protected...", 1, (0, 0, 0))
                op = 255 - abs((TMZoom - 1.5) * 510)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.2, v.screenY * 0.4))
            if TMZoom > 1.3 and TMZoom < 2.3:
                label = font.render("...By the 7 most powerful", 1, (0, 0, 0))
                op = 255 - abs(((TMZoom - 0.3) - 1.5) * 510)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.0, v.screenY * 0.6))
            if TMZoom > 1.4 and TMZoom < 2.3:
                label = font.render("mages and fighters", 1, (0, 0, 0))
                op = 255 - abs(((TMZoom - 0.3) - 1.5) * 510)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.4, v.screenY * 0.7))
            if TMZoom > 1.5 and TMZoom < 2.3:
                label = font.render("in the land...", 1, (0, 0, 0))
                op = 255 - abs(((TMZoom - 0.3) - 1.5) * 510)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.7, v.screenY * 0.8))
            if WBAlpha >= 255:
                ST2 += 1
                if ST2 > 0 and ST2 < 200:
                    label = font.render("But one day...", 1, (255, 255, 255))
                    op = 255 - abs((ST2 - 100) * 2.55)
                    
                    label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                    v.screen.blit(label, (v.screenX * 0.25, v.screenY * 0.2))
                if ST2 > 150 and ST2 < 350:
                    label = font.render("when it mattered most...", 1, (255, 255, 255))
                    op = 255 - abs((ST2 - 250) * 2.55)
                    
                    label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                    v.screen.blit(label, (v.screenX * 0.4, v.screenY * 0.4))
                if ST2 > 300 and ST2 < 600:
                    label = font.render("THEY FAILED", 1, (255, 0, 0))
                    op = 255 - abs((ST2 - 450) * 1.7)
                    
                    label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                    v.screen.blit(label, (v.screenX * 0.3, v.screenY * 0.6))
                if ST2 > 600:
                    STAGE = 3
        
        if STAGE == 3:
            v.clock.tick(60)
            v.screen.fill((0, 0, 0))
            if ST3 < 825:
                v.screen.blit(IM1, (0, 0))
            else:
                v.screen.blit(IM2, (0, 0))
            
            ST3 += 1
            
            posx = 50
            posy = v.screenY * 0.55
            iNum = 0
            for i in Characters:
                size = i.get_rect()
                size.width = ((size.width * 3) / 640) * v.screenX
                size.height = ((size.height * 3) / 480) * v.screenY
                ren = py.transform.scale(i, (size.width, size.height))
                pos = (posx, posy)
                posx += 80
                if posx < 320:
                    posy -= 15
                else:
                    posy += 15
                
                if ST3 < 1000 + rot[iNum] * 2:
                    if ST3 > 475:
                        ren = py.transform.rotate(ren, rot[iNum])
                iNum += 1
                
                v.screen.blit(ren, pos)
                
                if ST3 < 300:
                    if randint(0, 100) == 1:
                        x, y = pos
                        pos = x, y
                        IMSpells.add(MenuItems.storySpells(pos))
            
            if ST3 < 825:
                v.screen.blit(NexusC, (v.screenX * 0.4, v.screenY * -0.08))
            if ST3 > 825:
                v.screen.blit(NexusP, (v.screenX * 0.4, v.screenY * -0.08))
                
            IMSpells.update()
            size = IMEvil.images[1].get_rect().size
            ev = py.transform.scale(IMEvil.images[1], (int(size[0] * 4/640 * v.screenX), int(size[1] * 4/640 * v.screenX)))
            if ST3 < 650:
                v.screen.blit(ev, (v.screenX * 0.4 - int(size[0] * 4/640 * v.screenX)/2, v.screenY * 0.7))
            else:
                if ST3 > 650 and ST3 < 750:
                    v.screen.blit(ev, ((v.screenX * 0.4 - int(size[0] * 4/640 * v.screenX)/2) + (ST3 - 650)/2, (v.screenY * 0.7) - (ST3 - 650)/2))
            
            if ST3 > 0 and ST3 < 200:
                label = font.render("Thanatos was the physical embodiment", 1, (255, 255, 0))
                op = 255 - abs((ST3 - 100) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.0, v.screenY * 0.2))
            if ST3 > 10 and ST3 < 200:
                label = font.render("of death and destruction...", 1, (255, 255, 0))
                op = 255 - abs((ST3 - 100) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.2, v.screenY * 0.3))
            if ST3 > 150 and ST3 < 400:
                label = font.render("He fought his way into the ", 1, (255, 255, 0))
                op = 255 - abs((ST3 - 275) * 2.04)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.1, v.screenY * 0.5))
            if ST3 > 160 and ST3 < 400:
                label = font.render("mountain of the nexus,", 1, (255, 255, 0))
                op = 255 - abs((ST3 - 275) * 2.04)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.3, v.screenY * 0.6))
            if ST3 > 170 and ST3 < 400:
                label = font.render("the core that holds the world together", 1, (255, 255, 0))
                op = 255 - abs((ST3 - 275) * 2.04)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.1, v.screenY * 0.7))
            if ST3 > 550 and ST3 < 750:
                label = font.render("AND DESTORYED IT", 1, (255, 0, 0))
                op = 255 - abs((ST3 - 650) * 2.04)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.2, v.screenY * 0.4))
            
            if ST3 > 850:
                for i in range(15):
                    r = py.transform.rotate(rock, rot[i] * 4)
                    v.screen.blit(r, (v.screenX * (i * 0.06), ((v.screenY/400) * ((ST3 - 850) - ran[i] * 3))))
            
            if ST3 > 1000:
                WBAlpha += 2
                WB.set_alpha(WBAlpha)
                WB.fill((0, 0, 0))
                v.screen.blit(WB, (0, 0))
                if WBAlpha >= 255:
                    STAGE = 4

            if ST3 > 450 and ST3 < 500:
                if randint(0, 2) == 1:
                    v.screen.fill((255, 0, 200))
            if ST3 > 800 and ST3 < 850:
                if randint(0, 2) == 1:
                    v.screen.fill((255, 0, 200))
            
            if WBAlpha > 0 and ST3 < 1000:
                WBAlpha -= 2
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))

        if STAGE == 4:
            v.clock.tick(60)
            ST4 += 1
            v.screen.fill((255, 255, 255))
            
            if ST4 < 310:
                _fi1 = py.transform.scale(FI1, (int(FI1.get_rect().width * (4 - (ST4/100))), int(FI1.get_rect().height * (4 - (ST4/100)))))
                pos = (v.screenX/2 - (FI1.get_rect().width * (4 - (ST4/100))/2), v.screenY/2 - (FI1.get_rect().height * (4 - (ST4/100))/2))
            if ST4 > 360:
                _fi1 = py.transform.scale(FI1, (int(FI1.get_rect().width * ((ST4/100) - 2.6)), int(FI1.get_rect().height * ((ST4/100) - 2.6))))
                pos = (v.screenX/2 - (FI1.get_rect().width * ((ST4/100) - 2.7)/(2 * ((ST4/100) - 2.7))), v.screenY/2 - (FI1.get_rect().height * ((ST4/100) - 2.7)/(2 * ((ST4/100) - 2.7))))
            v.screen.blit(_fi1, pos)
            
            if WBAlpha > 0 and ST4 < 200:
                WBAlpha -= 2
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))
            
            if ST4 > 360:
                WBAlpha += 2
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))
                if WBAlpha >= 255:
                    STAGE = 5
            
            if ST4 > 0 and ST4 < 200:
                label = font.render("The world was falling apart...", 1, (0, 0, 0))
                op = 255 - abs((ST4 - 100) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.2, v.screenY * 0.4))
            if ST4 > 150 and ST4 < 350:
                label = font.render("Entire continents collapsing", 1, (0, 0, 0))
                op = 255 - abs((ST4 - 250) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.3, v.screenY * 0.2))
            if ST4 > 150 and ST4 < 350:
                label = font.render("into the void...", 1, (0, 0, 0))
                op = 255 - abs((ST4 - 250) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.4, v.screenY * 0.3))
            
        if STAGE == 5:
            v.clock.tick(60)
            ST5 += 1
            v.screen.blit(IM2, (0, 0))
            
            posx = 50
            posy = v.screenY * 0.55
            iNum = 0
            for i in Characters:
                size = i.get_rect()
                size.width = ((size.width * 3) / 640) * v.screenX
                size.height = ((size.height * 3) / 480) * v.screenY
                ren = py.transform.scale(i, (size.width, size.height))
                pos = (posx, posy)
                posx += 80
                if posx < 320:
                    posy -= 15
                else:
                    posy += 15
                
                if ST5 > 200 + (560 - posx - 80):
                    xDiff = v.screenX/2 - pos[0]
                    yDiff = v.screenY/2 - pos[1]
                    pos = list(pos)
                    pos[0] += xDiff/100 * (ST5 - (200 + (560 - posx - 80)))
                    pos[1] -= yDiff/100 * (ST5 - (200 + (560 - posx - 80)))
                iNum += 1
                
                if ST5 < 300 + (560 - posx - 80):
                    v.screen.blit(ren, pos)
            
            if ST5 < 750:
                v.screen.blit(NexusP, (v.screenX * 0.4, v.screenY * -0.08))
            else:
                v.screen.blit(NexusCP, (v.screenX * 0.4, v.screenY * -0.08))
            
            
            if ST5 > 0 and ST5 < 200:
                label = font.render("There was only one thing that the", 1, (255, 255, 0))
                op = 255 - abs((ST5 - 100) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.1, v.screenY * 0.3))
            if ST5 > 0 and ST5 < 200:
                label = font.render("guardians could do...", 1, (255, 255, 0))
                op = 255 - abs((ST5 - 100) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.2, v.screenY * 0.4))
            if ST5 > 150 and ST5 < 350:
                label = font.render("One by one...", 1, (255, 255, 0))
                op = 255 - abs((ST5 - 250) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.4, v.screenY * 0.5))
            if ST5 > 300 and ST5 < 500:
                label = font.render("They cast themselves into the nexus...", 1, (255, 255, 0))
                op = 255 - abs((ST5 - 400) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.1, v.screenY * 0.6))
            if ST5 > 450 and ST5 < 750:
                label = font.render("It killed them, but the energy", 1, (255, 255, 0))
                op = 255 - abs((ST5 - 600) * 1.7)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.1, v.screenY * 0.3))
            if ST5 > 450 and ST5 < 750:
                label = font.render("they released offset that of Thanatos...", 1, (255, 255, 0))
                op = 255 - abs((ST5 - 600) * 1.7)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.0, v.screenY * 0.4))
            if ST5 > 700 and ST5 < 900:
                label = font.render("and halted the chaos.", 1, (255, 255, 0))
                op = 255 - abs((ST5 - 800) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.3, v.screenY * 0.5))
            
            if WBAlpha > 0 and ST5 < 200:
                WBAlpha -= 2
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))
            if ST5 > 800:
                WBAlpha += 2
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))
                if WBAlpha > 255:
                    STAGE = 6
            
        if STAGE == 6:
            v.clock.tick(60)
            v.screen.blit(MP, (0, 0))
            ST6 += 1
            
            if ST6 > 0 and ST6 < 200:
                label = font.render("The destruction had ceased...", 1, (255, 0, 0))
                op = 255 - abs((ST6 - 100) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.1, v.screenY * 0.2))
            
            if ST6 > 150 and ST6 < 350:
                label = font.render("But the effects of it remained...", 1, (255, 0, 0))
                op = 255 - abs((ST6 - 250) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.2, v.screenY * 0.3))
            
            if ST6 > 300 and ST6 < 500:
                label = font.render("7 major islands,", 1, (255, 0, 0))
                op = 255 - abs((ST6 - 400) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.3, v.screenY * 0.4))
            if ST6 > 300 and ST6 < 500:
                label = font.render("floating above the endless void...", 1, (255, 0, 0))
                op = 255 - abs((ST6 - 400) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.1, v.screenY * 0.5))
            
            if ST6 > 450 and ST6 < 650:
                label = font.render("The only way between them were", 1, (255, 0, 0))
                op = 255 - abs((ST6 - 550) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.2, v.screenY * 0.6))
            if ST6 > 450 and ST6 < 650:
                label = font.render("teleport pads scattered across the world...", 1, (255, 0, 0))
                op = 255 - abs((ST6 - 550) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.0, v.screenY * 0.7))
   
            
            if WBAlpha > 0 and ST6 < 200:
                WBAlpha -= 2
                WB.set_alpha(WBAlpha)
                v.screen.blit(WB, (0, 0))
            
            if ST6 > 700:
                WBAlpha += 2
                WB.set_alpha(WBAlpha)
                WB.fill((0, 0, 0))
                v.screen.blit(WB, (0, 0))
            
            if ST6 > 750 and ST6 < 950:
                label = font.render("But that was 200 years ago...", 1, (255, 255, 255))
                op = 255 - abs((ST6 - 850) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.1, v.screenY * 0.4))
            
            if ST6 > 900 and ST6 < 1100:
                label = font.render("And now, a new story has begun...", 1, (255, 255, 255))
                op = 255 - abs((ST6 - 1000) * 2.55)
                
                label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (v.screenX * 0.1, v.screenY * 0.5))
            if ST6 > 1100:
                print("STORY TIME")
                print(time.clock() - sTime)
                return
            
        label = font2.render("(space to skip)", 1, (255, 255, 255))
        op = 255 - abs((((skp % 400) - 200) * 1.275))
        label.fill((255, 255, 255, op), special_flags=py.BLEND_RGBA_MULT)
        v.screen.blit(label, (v.screenX * 0.45, v.screenY * 0.95))
        skp += 1
        v.events = []
        v.events = py.event.get()
        for event in v.events:
            if event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    return
            if event.type == py.QUIT:
                sys.exit()
        py.display.flip()
