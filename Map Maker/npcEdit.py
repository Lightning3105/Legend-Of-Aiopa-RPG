import mapMakerVariables as v
import mapMenuItems
import pygame as py


class npcImage(py.sprite.Sprite):
    
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
        if v.selectedNpc["Image"] == self.sheet:
            py.draw.rect(v.pallet, (255, 0, 0), self.rect, 1)
        if self.hovered:
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    if py.mouse.get_pressed()[0]:
                        v.selectedNpc["Image"] = self.sheet
                        createNPC()


def createNPC():
    font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
    label = font.render("NPC Name:", 1, (0, 0, 0))
    inp = textInput((300, 275), 20, 16)
    while not inp.done:
        v.screen.blit(label, (300, 200))
        inp.update()
        py.display.flip()
    v.selectedNpc["Name"] = outText
    v.screen.fill((255, 255, 255))
    
    label = font.render("NPC Attack:", 1, (0, 0, 0))
    inp = textInput((300, 275), 20, 2)
    while not inp.done:
        v.screen.blit(label, (300, 200))
        inp.update()
        py.display.flip()
    v.selectedNpc["Attack"] = outText
    v.screen.fill((255, 255, 255))
    
    label = font.render("NPC Health:", 1, (0, 0, 0))
    inp = textInput((300, 275), 20, 2)
    while not inp.done:
        v.screen.blit(label, (300, 200))
        inp.update()
        py.display.flip()
    v.selectedNpc["Health"] = outText
    v.screen.fill((255, 255, 255))
    
    label = font.render("NPC Speed:", 1, (0, 0, 0))
    inp = textInput((300, 275), 20, 2)
    while not inp.done:
        v.screen.blit(label, (300, 200))
        inp.update()
        py.display.flip()
    v.selectedNpc["Speed"] = outText
    v.screen.fill((255, 255, 255))