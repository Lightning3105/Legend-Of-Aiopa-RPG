import pygame as py
import Variables as v
import MenuItems 
import entityClasses 
import guiClasses 
from functools import reduce
from os import listdir

import Map
import spellClasses
import weaponClasses
import itemClasses
from pygame.color import Color as colour
import sys
import inventoryScreen
import time
from random import randint
import npcScripts
import setupScripts

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
                            game()
                            return
                        if id == "options":
                            options()
                            return
                        if id == "load":
                            print("Cannot load at the mo.")
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
    print(v.screenX, v.screenY)
    v.screenScale = round(v.screenX * 0.004, 1)
    """if v.screenX == 480:
        v.screenScale = 2
    if v.screenX == 800:
        v.screenScale = 2.5
    if v.screenX == 1024:
        v.screenScale = 4.3"""

def game():
    py.init()
    v.music.fadeout(2000)
    v.music = py.mixer.Sound("Resources/Music/Ambient 1.ogg")
    v.music.play(loops=-1)
    v.PAUSED = False
    
    """if v.fullScreen:
        v.screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF|py.FULLSCREEN)
    else:
        v.screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF)"""
    
    v.playerHealth = v.Attributes["Max Health"]
    v.playerMana = v.Attributes["Max Mana"]
    
    v.p_class = entityClasses.Player()
    v.clock = py.time.Clock()
    py.time.set_timer(py.USEREVENT, 200) # walking
    py.time.set_timer(py.USEREVENT + 1, 50) # Spell animation
    py.time.set_timer(py.USEREVENT + 2, 1000) #One second

    tileset = entityClasses.SpriteSheet("Resources/Images/Main_Tileset.png", 63, 32)
    
    Map.generateMap(Map.Maps, tileset)
    #py.time.wait(5000)
    #v.damagesNPCs = py.sprite.Group()
    
    v.hits = py.sprite.Group()
    v.hits.add(entityClasses.HitBox("Right"))
    v.hits.add(entityClasses.HitBox("Left"))
    v.hits.add(entityClasses.HitBox("Top"))
    v.hits.add(entityClasses.HitBox("Bottom"))
    
    weaponSlot = guiClasses.weaponSlot()

    entityClasses.Enemy(-100, -100, "Resources/Images/Generic Goblin.png", {"Name": "Groblin Lvl. 1", "Health":5, "Attack":5})
    
    cn = [{"Message": "Greetings. Why not press a button? Who knows, you might win a prize!", "B1": {"Text": "Button 1", "ID": 1}, "B2": {"Text": "Button 2", "ID": 2}, "B3": {"Text": "Button 3", "ID": 3}, "B4": {"Text": "Button 4", "ID": 4}, "ID":0}, {"Message": "You pressed Button 1", "Goto":5, "ID": 1}, {"Message": "You pressed Button 2", "Goto":5, "ID": 2}, {"Message": "You pressed Button 3", "Goto":5, "ID": 3}, {"Message": "You pressed Button 4", "Goto":5, "ID": 4}, {"Message": "Congratulations. You won.", "ID": 5, "End":True}]
    entityClasses.NPC((0, 30, "Down"), "Resources/Images/Male_Basic.png", {"Name":"Fred", "Conversation":cn})
    
    #v.Attributes.update(v.classAttributes["Paladin"]) # TODO: Remove when done
    
    xp = guiClasses.XP()
 
    fb = itemClasses.spell("Fire Beam", "beam", "Resources/Images/fireBeam.png", "Resources/Images/redCastCircle.png", {"Damage": 0.2, "Knockback": "S", "Cooldown": 5, "Mana": 10, "InvulnMod": 0})
       
    v.abilityButtons.add(guiClasses.ability(fb, "Resources/Images/Spell Icons/fireBeam.png", 0))  
       
    pause = guiClasses.pauseScreen()
    
    map = guiClasses.miniMap()
    
    v.inventory = inventoryScreen.inventory()
    v.inventory.add(itemClasses.item("Thing", py.image.load("Resources/Images/XPOrb.png")))
    v.inventory.add(itemClasses.weapon("Magic Orb", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[56], "manaOrb", "Resources/Images/castOrbPurple.png", {"Damage":2, "Knockback": 10}))
    v.inventory.add(itemClasses.weapon("Broken Sword", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[0], "swing", "Resources/Images/Sword_1.png", {"Damage":2, "Knockback": 10}))
    v.inventory.add(itemClasses.weapon("Short Bow", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[72], "shoot", "Resources/Images/Arrow.png", {"Damage":2, "Knockback": 10})) 
    
    entityClasses.droppedItem(itemClasses.item("Thing", py.image.load("Resources/Images/XPOrb.png")), (100, 100))
    while True:
        if not v.PAUSED:
            #print([i.name for i in v.inventory.contents ])
            v.ticks += 1
            v.screen.fill(colour("Dark Green"))
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
            guiClasses.update_health()
            guiClasses.update_mana()
            guiClasses.actionText()
            xp.update()
            weaponSlot.draw()
            v.abilityButtons.update()
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
    """if v.fullScreen:
        v.screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF|py.FULLSCREEN)
    else:
        v.screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF)"""
    
    

    classes = py.sprite.Group()
    classes.add(MenuItems.characterSelector("Resources/Images/PaladinClass.png", (v.screenX/2, v.screen.get_rect()[3]/2), "Paladin"))
    classes.add(MenuItems.characterSelector("Resources/Images/MageClass.png", (v.screenX/4, v.screen.get_rect()[3]/2), "Mage"))
    classes.add(MenuItems.characterSelector("Resources/Images/RangerClass.png", (v.screenX/1.3, v.screen.get_rect()[3]/2), "Ranger"))
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
                if v.custimizationStage == "Attributes" or v.custimizationStage == "Customisation":
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
                                game()
                        
            
        
        #v.characterHovered = False
        fade.draw()
        fade.opacity -= 1

        py.display.flip()

def centre(screen):
    return screen.get_rect()[2] / 2, screen.get_rect()[3] / 2
