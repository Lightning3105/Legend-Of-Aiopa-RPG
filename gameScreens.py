import pygame as py
import Variables as v
from MenuItems import Button, Text, fill_gradient, fadeIn
from entityClasses import Player, Tile, Sword, HitBox, NPC

import Map
import entityClasses
import MenuItems
from pygame.color import Color as colour
import sys
def mainMenu():
    py.init()
    screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF|py.RESIZABLE)
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
                screen=py.display.set_mode(event.dict['size'],py.HWSURFACE|py.DOUBLEBUF|py.RESIZABLE)
            elif event.type == py.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.pressed(py.mouse.get_pos()):
                        return True
        fade.draw()
        fade.opacity -= 1
        py.display.flip()

def game():
    py.init()
    v.screen = py.display.set_mode((640, 480),py.HWSURFACE|py.DOUBLEBUF|py.RESIZABLE)
    v.screen.fill(colour("Green"))
    v.screen.fill(colour("Red"))
    print(v.screen)
    player = Player()
    player.sheetImage = "Resources/Images/Male_Basic.png"
    player.initSheet()
    player.draw()
    clock = py.time.Clock()
    py.time.set_timer(py.USEREVENT, 200)

    tileset = entityClasses.SpriteSheet("Resources/Images/Tile_Land2.png", 12, 16)
    v.hitList = py.sprite.Group()
    map1 = [["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","#","#","0","0","0","0"],
            ["0","0","0","0","#","#","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],
            ["0","0","0","0","0","0","0","0","0","0"],]
    v.allTiles = py.sprite.Group()
    tiles = Map.generateMap(map1, tileset)
    sword = Sword()
    sword.image = "Resources/Images/Sword_1.png"
    sword.get_rend()
    hits = py.sprite.Group()
    hits.add(HitBox(centre(v.screen)[0] + (5 * v.scale), centre(v.screen)[1] - (5 * v.scale), (2 * v.scale), (20 * v.scale), "Right"))
    hits.add(HitBox(centre(v.screen)[0] - (5 * v.scale), centre(v.screen)[1] - (5 * v.scale), (2 * v.scale), (20 * v.scale), "Left"))
    hits.add(HitBox(centre(v.screen)[0] - (3 * v.scale), centre(v.screen)[1] - (8 * v.scale), (8 * v.scale), (2 * v.scale), "Top"))
    hits.add(HitBox(centre(v.screen)[0] - (3 * v.scale), centre(v.screen)[1] + (16 * v.scale), (8 * v.scale), (2 * v.scale), "Bottom"))
    v.allNpc = py.sprite.Group()

    npc = NPC(100, 100)
    while True:
        v.ticks += 1
        #print("PX: " + str(v.playerPosX))
        #print("PY: " + str(v.playerPosY))
        v.screen.fill(colour("Dark Green"))
        py.event.pump()
        clock.tick(60)
        tiles.update()
        tiles.draw(v.screen)
        player.move()
        v.allNpc.update()
        hits.update()
        player.draw()
        sword.draw()
        #hits.draw(v.screen)

        v.allNpc.draw(v.screen)
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()
            elif event.type==py.VIDEORESIZE:
                v.screen = py.display.set_mode(event.dict['size'],py.HWSURFACE|py.DOUBLEBUF|py.RESIZABLE)

        keys_pressed = py.key.get_pressed()
        if keys_pressed[py.K_SPACE]:
            sword.attacking = True


def centre(screen):
    return screen.get_rect()[2] / 2, screen.get_rect()[3] / 2