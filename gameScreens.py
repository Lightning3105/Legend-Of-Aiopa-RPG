import pygame as py
import Variables as v
from MenuItems import Button, Text, fill_gradient, fadeIn
from entityClasses import Player, Tile, Sword, HitBox, NPC
from guiClasses import update_health
from functools import reduce

import Map
import entityClasses
import MenuItems
import guiClasses
from pygame.color import Color as colour
import sys
def mainMenu():
    py.init()
    screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF)
    MenuItems.screen = screen
    buttons = [Button("New Game", (160, 380), 80, colour("Light Green"), colour("Dark Green"), "Resources\Fonts\MorrisRoman.ttf")]
    titletext1 = Text("The Legend", (90, 60), 80, colour("red"), "Resources\Fonts\Runic.ttf")
    titletext2 = Text("Of Aiopa", (160, 140), 80, colour("red"), "Resources\Fonts\Runic.ttf")
    fade = fadeIn()
    fade.fadeIn = True
    while True:
        py.event.pump()
        fill_gradient(screen, colour("cyan"), colour("dark blue"))
        titletext1.draw()
        titletext2.draw()

        for button in buttons:
            if button.rect.collidepoint(py.mouse.get_pos()):
                button.hovered = True
            else:
                button.hovered = False
            button.draw()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type==py.VIDEORESIZE:
                screen=py.display.set_mode(event.dict['size'],py.HWSURFACE|py.DOUBLEBUF)
            elif event.type == py.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.pressed(py.mouse.get_pos()):
                        return True
        fade.draw()
        fade.opacity -= 1
        py.display.flip()

def game():
    py.init()
    v.screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF)
    v.screen.fill(colour("Green"))
    v.screen.fill(colour("Red"))
    v.p_class = Player()
    v.p_class.sheetImage = "Resources/Images/Male_Basic.png"
    v.p_class.initSheet()
    v.clock = py.time.Clock()
    py.time.set_timer(py.USEREVENT, 200)

    tileset = entityClasses.SpriteSheet("Resources/Images/Tile_Land2.png", 12, 16)
    v.hitList = py.sprite.Group()
    v.map1 = [["0","0","0","0","0","0","0","0","0","0"],
            ["#","0","0","0","#","#","0","0","0","0"],
            ["#","#","0","#","#","#","#","#","0","0"],
            ["#","#","#","#","0","0","0","#","0","0"],
            ["#","#","#","#","0","0","0","0","0","0"],
            ["#","#","#","#","0","0","0","0","0","0"],
            ["#","#","#","#","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],]
    v.allTiles = py.sprite.Group()
    tiles = Map.generateMap(v.map1, tileset)
    v.cur_weapon = Sword()
    v.cur_weapon.image = "Resources/Images/Sword_1.png"
    v.cur_weapon.get_rend()
    v.hits = py.sprite.Group()
    v.hits.add(HitBox(centre(v.screen)[0] + (5 * v.scale), centre(v.screen)[1] - (5 * v.scale), (2 * v.scale), (20 * v.scale), "Right"))
    v.hits.add(HitBox(centre(v.screen)[0] - (5 * v.scale), centre(v.screen)[1] - (5 * v.scale), (2 * v.scale), (20 * v.scale), "Left"))
    v.hits.add(HitBox(centre(v.screen)[0] - (3 * v.scale), centre(v.screen)[1] - (8 * v.scale), (8 * v.scale), (2 * v.scale), "Top"))
    v.hits.add(HitBox(centre(v.screen)[0] - (3 * v.scale), centre(v.screen)[1] + (16 * v.scale), (8 * v.scale), (2 * v.scale), "Bottom"))
    v.allNpc = py.sprite.Group()
    weaponSlot = guiClasses.weaponSlot()

    v.particles = py.sprite.Group()

    npc = NPC("Groblin Lvl. 1", 100, 100, 5)
    while True:
        v.ticks += 1
        #print(v.clock.get_fps())
        v.screen.fill(colour("Dark Green"))
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        v.clock.tick(30)
        tiles.update()
        tiles.draw(v.screen)
        v.p_class.draw()
        v.cur_weapon.update()
        v.allNpc.update()
        v.allNpc.draw(v.screen)
        v.p_class.update()
        v.playerStopped = False

        v.cur_weapon.draw()
        v.particles.update()
        #v.hits.draw(v.screen)
        update_health()
        weaponSlot.draw()


        py.display.flip()
        for event in v.events:
            if event.type == py.QUIT:
                sys.exit()
            elif event.type==py.VIDEORESIZE:
                v.screen = py.display.set_mode(event.dict['size'],py.HWSURFACE|py.DOUBLEBUF)

        keys_pressed = py.key.get_pressed()
        if keys_pressed[py.K_SPACE]:
            v.cur_weapon.attacking = True

def classSelection():
    py.init()
    screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF)
    colourMod = 255
    colour1 = colour(50, 0, 0)
    colour2 = colour(205, 0, 0)
    colourDirection = True
    colourModIncreasing = False
    colourForward = True


    while True:
        py.event.pump()
        print(colourMod)
        if colourModIncreasing == False:
            colourMod -= 0.1
        if colourModIncreasing == True:
            colourMod += 0.1
        colourMod = round(colourMod, 6)
        if colourMod <= 50:
            colourModIncreasing = True
        if colourMod >= 205:
            colourModIncreasing = False
        if colourMod == 127:
            colourDirection = not colourDirection
            if colourModIncreasing == False:
                colourForward = not colourForward

        colour1 = (255 - colourMod, 0, 0)
        colour2 = (0 + colourMod, 0, 0)

        fill_gradient(screen, colour1, colour2, vertical=colourDirection, forward=colourForward)
        py.display.flip()

def centre(screen):
    return screen.get_rect()[2] / 2, screen.get_rect()[3] / 2