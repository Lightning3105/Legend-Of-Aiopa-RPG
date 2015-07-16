import pygame as py
from MenuItems import Button, Text, fill_gradient, fadeIn
import MenuItems
from pygame.color import Color as colour
import sys
def mainMenu():
    py.init()
    screen = py.display.set_mode((640, 480))
    MenuItems.screen = screen
    buttons = [Button("New Game", (160, 380), 80, colour("Light Green"), colour("Dark Green"), "Rescources\Fonts\MorrisRoman.ttf")]
    titletext1 = Text("The Legend", (90, 60), 80, colour("red"), "Rescources\Fonts\Runic.ttf")
    titletext2 = Text("Of Aiopa", (160, 140), 80, colour("red"), "Rescources\Fonts\Runic.ttf")
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
    while True:
        py.display.flip()