import pygame as py
from MenuItems import Button, Text, fill_gradient, fadeIn
from entityClasses import Player, Tile
import entityClasses
import MenuItems
from pygame.color import Color as colour
import sys
def mainMenu():
    py.init()
    screen = py.display.set_mode((640, 480))
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
            elif event.type == py.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.pressed(py.mouse.get_pos()):
                        return True
        fade.draw()
        fade.opacity -= 1
        py.display.flip()

def game():
    py.init()
    screen = py.display.set_mode((640, 480))
    screen.fill(colour("Green"))
    entityClasses.screen = screen
    screen.fill(colour("Red"))
    print(screen)
    print(entityClasses.screen)
    player = Player()
    player.sheetImage = "Resources/Images/Male_Basic.png"
    player.initSheet()
    clock = py.time.Clock()
    py.time.set_timer(py.USEREVENT, 200)
    tiles = py.sprite.Group()
    temp = entityClasses.SpriteSheet("Resources/Images/Tile_Land2.png", 12, 16)
    temp.getGrid()
    for i in range(10):
        tile = Tile((0, i), temp.images[0])
        tiles.add(tile)
    while True:
        screen.fill(colour("Dark Green"))
        py.event.pump()
        clock.tick(60)
        tiles.update()
        tiles.draw(screen)
        player.move()
        player.draw()
        py.display.flip()
        for event in py.event.get():
            if event.type == py.QUIT:
                sys.exit()