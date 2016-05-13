import pygame as py
import entityClasses
import Variables as v
from _operator import pos
from msilib.schema import Font
from os import listdir
import itemClasses
import setupScripts
import sys
import time

class Button(py.sprite.Sprite):

    def __init__(self, text, pos, size, hovercolour, normalcolour, font, ID, centred = False, bsize=(0,0)):
        super().__init__()
        self.ID = ID
        self.hovered = False
        self.text = text
        self.pos = pos
        self.hcolour = hovercolour
        self.ncolour = normalcolour
        self.font = font
        self.font = py.font.Font(font, int(size))
        self.centred = centred
        self.size = bsize
        self.rend = self.font.render(self.text, True, (0,0,0))
        self.set_rect()
    
    def update(self):
        if self.hovered:
            colour = self.hcolour
        else:
            colour = self.ncolour
        py.draw.rect(v.screen, colour, self.rect)
        v.screen.blit(self.rend, self.rect)
        if self.rect.collidepoint(v.mouse_pos):
            self.hovered = True
        else:
            self.hovered = False

    def set_rect(self):
        self.rect = self.rend.get_rect()
        if not self.centred:
            self.rect.topleft = self.pos
        if self.centred:
            self.rect.center = self.pos
        
        if not self.size[0] == 0:
            self.rect.width = self.size[0]
        if not self.size[1] == 0:
            self.rect.height = self.size[1]

    def pressed(self):
        for event in v.events:
            if self.hovered:
                if event.type == py.MOUSEBUTTONDOWN:
                    return True
            if event.type == py.KEYDOWN:
                if event.key == py.K_RETURN:
                    if self.ID == "continue":
                        return True
        return False

class radioButton(py.sprite.Sprite):
    
    def __init__(self, text, position, size, colour, font, ID, right=True, selected=False):
        font = py.font.Font(font, size)
        self.rend = font.render(text, 1, colour)
        self.position = position
        self.ID = ID
        self.right = right
        if self.right:
            self.buttonRect = py.Rect(self.position, (self.rend.get_rect()[3], self.rend.get_rect()[3]))
        else:
            self.buttonRect = py.Rect((self.position[0] + self.rend.get_rect()[0] + 5, self.position[1]), (self.rend.get_rect()[3], self.rend.get_rect()[3]))
    
        self.hovered = False
        self.selected = selected
    
    def update(self):
        if self.right:
            v.screen.blit(self.rend, (self.buttonRect[0] + self.buttonRect[2] + 5, self.buttonRect[1]))
        else:
            v.screen.blit(self.rend, (self.buttonRect[0] - self.rend.get_rect()[2] - 5, self.buttonRect[1]))

        if self.buttonRect.collidepoint(v.mouse_pos):
            self.hovered = True
        else:
            self.hovered = False
        
        if self.hovered:
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    self.selected = not self.selected
        
        if self.hovered and self.selected:
            colour = (255, 100, 100)
        elif self.hovered:
            colour = (200, 100, 100)
        elif self.selected:
            colour = (255, 0, 0)
        else:
            colour = (255, 255, 255)
        
        py.draw.rect(v.screen, colour, self.buttonRect)
        py.draw.rect(v.screen, (0, 0, 0), self.buttonRect, 2)
        

def fill_gradient(surface, color, gradient, rect=None, vertical=True, forward=True):
    """fill a surface with a gradient pattern
    Parameters:
    color -> starting color
    gradient -> final color
    rect -> area to fill; default is surface's rect
    vertical -> True=vertical; False=horizontal
    forward -> True=forward; False=reverse

    Pygame recipe: http://www.pygame.org/wiki/GradientCode
    """
    if rect is None: rect = surface.get_rect()
    x1,x2 = rect.left, rect.right
    y1,y2 = rect.top, rect.bottom
    if vertical: h = y2-y1
    else:        h = x2-x1
    if forward: a, b = color, gradient
    else:       b, a = color, gradient
    rate = (
        float(b[0]-a[0])/h,
        float(b[1]-a[1])/h,
        float(b[2]-a[2])/h
    )
    fn_line = py.draw.line
    if vertical:
        for line in range(y1,y2):
            color = (
                min(max(a[0]+(rate[0]*(line-y1)),0),255),
                min(max(a[1]+(rate[1]*(line-y1)),0),255),
                min(max(a[2]+(rate[2]*(line-y1)),0),255)
            )
            fn_line(surface, color, (x1,line), (x2,line))
    else:
        for col in range(x1,x2):
            color = (
                min(max(a[0]+(rate[0]*(col-x1)),0),255),
                min(max(a[1]+(rate[1]*(col-x1)),0),255),
                min(max(a[2]+(rate[2]*(col-x1)),0),255)
            )
            fn_line(surface, color, (col,y1), (col,y2))

class fadeIn:
    def __init__(self):
        self.opacity = 255
        self.speed = 3
        self.black = py.Surface((1280, 720))
        self.black.fill((0, 0, 0))

    def draw(self):
        self.black.set_alpha(self.opacity)
        v.screen.blit(self.black, (0, 0))
        if self.opacity <= 0:
            self.opacity = 0
        if self.opacity >= 255:
            self.opacity = 255

class characterSelector(py.sprite.Sprite):

    def __init__(self, image, pos, name):
        super().__init__()
        self.pos = pos
        self.name = name
        self.skin = py.image.load(image)
        self.hovered = False
        self.hoveredCycle = 0
        self.greyedCycle = 0
        self.movingCycle = 100
        self.movDistanceX = abs(self.pos[0] - 200)
        self.movDistanceY = 300 - self.pos[1]
        self.opacity = 255
        

    def update(self):
        if v.custimizationStage == "Class Selection":
            sMod = (self.hoveredCycle / 10) + 3
            cMod = self.greyedCycle * 4
            cMod = 255 - cMod
            size = self.skin.get_rect()
            size.width = size.width * 1.8
            size.height = size.height * 1.8
            self.image = py.transform.scale(self.skin, (int(size.width * sMod), int(size.height * sMod)))
            
            self.image.fill((cMod, cMod, cMod), special_flags=py.BLEND_RGBA_MULT)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            if self.rect.collidepoint(v.mouse_pos):
                self.hovered = True
                v.characterHovered = True
            else:
                self.hovered = False
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN and self.hovered:
                    v.playerClass = self.name
                    v.custimizationStage = "To Attributes"
                    setupScripts.setAttributes()
                if event.type == py.USEREVENT: 
                    if self.hovered and self.hoveredCycle < 30:
                        self.hoveredCycle += 1
                        self.greyedCycle -= 1
                    if not self.hovered and self.hoveredCycle > 0:
                        self.hoveredCycle -= 1
                    
                    if v.characterHovered == True:
                        if self.hovered == False:
                            self.greyedCycle += 1
                        
                    if v.characterHovered == False:
                        self.greyedCycle -= 1
            
            if self.hoveredCycle >= 30:
                self.hoveredCycle = 30
            if self.hoveredCycle <= 0:
                self.hoveredCycle = 0
            
            if self.greyedCycle >= 30:
                self.greyedCycle = 30
            if self.greyedCycle <= 0:
                self.greyedCycle = 0
            
            
                
            font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(10 * sMod)) #TODO: Scale
            label = font.render(self.name, 1, (cMod, cMod, cMod))
            v.screen.blit(label, (self.rect.centerx - (font.size(self.name)[0] / 2), self.rect.bottom  + (2 * sMod)))
        elif v.custimizationStage == "To Attributes" or v.custimizationStage == "Attributes":
            if self.name == v.playerClass:
                for event in v.events:
                    if event.type == py.USEREVENT:
                        sMod = 6 + ((100 - self.movingCycle) / 40)
                        size = self.skin.get_rect()
                        size.width = size.width * 1.8
                        size.height = size.height * 1.8
                        self.image = py.transform.scale(self.skin, (int(size.width * sMod), int(size.height * sMod)))
                        self.rect = self.image.get_rect()
                        
                        
                        newpos = list(self.pos)
                        newpos[0] = self.pos[0] - (self.movDistanceX - (self.movDistanceX/100)*self.movingCycle)  # TODO: Make this work
                        newpos[1] = self.pos[1] + (self.movDistanceY - (self.movDistanceY/100)*self.movingCycle)  # TODO: Make this work
                        
                        if self.movingCycle > 0:
                            self.movingCycle -= 1
                        self.rect.center = newpos
                        
            else:
                size = self.skin.get_rect()
                size.width = size.width * 1.8
                size.height = size.height * 1.8
                self.image = py.transform.scale(self.skin, (int(size.width * 3), int(size.height * 3)))
                self.image.fill((135, 135, 135, self.opacity), special_flags=py.BLEND_RGBA_MULT)
                self.opacity -= 1
                if self.opacity < 0:
                    self.opacity = 0
        if v.custimizationStage == "Customisation":
            self.image.fill((255, 255, 255, 0))
                
class optionSlate():
    
    def __init__(self):
        self.width = 800
        self.height = 600
        self.posx = 1620
        self.posy = 360
        
    
    def update(self):
        if v.custimizationStage == "To Attributes":
            self.innerRect = py.Rect(0, 0, self.width, self.height)
            self.innerRect.center = self.posx, self.posy
            self.outerRect = py.Rect(0, 0, self.width + 20, self.height + 20)
            self.outerRect.center = self.posx, self.posy
            py.draw.rect(v.screen, (153, 76, 0), self.outerRect)
            py.draw.rect(v.screen, (255, 178, 102), self.innerRect)
            if self.posx >= 880:
                self.posx -= 20
            if self.posx < 880:
                v.custimizationStage = "Attributes"
        if v.custimizationStage == "Attributes" or v.custimizationStage == "Customisation":
            self.posx = 880
            self.posy = 360
            self.innerRect = py.Rect(0, 0, self.width, self.height)
            self.innerRect.center = self.posx, self.posy
            self.outerRect = py.Rect(0, 0, self.width + 20, self.height + 20)
            self.outerRect.center = self.posx, self.posy
            py.draw.rect(v.screen, (153, 76, 0), self.outerRect)
            py.draw.rect(v.screen, (255, 178, 102), self.innerRect)
        
        if v.custimizationStage == "Name":
            self.innerRect = py.Rect(0, 0, self.width, self.height)
            self.innerRect.center = self.posx, self.posy
            self.outerRect = py.Rect(0, 0, self.width + 20, self.height + 20)
            self.outerRect.center = self.posx, self.posy
            py.draw.rect(v.screen, (153, 76, 0), self.outerRect)
            py.draw.rect(v.screen, (255, 178, 102), self.innerRect)
            if self.posx <= 1920: # TODO
                self.posx += 10

class optionAttribute(py.sprite.Sprite):
    
    def __init__(self, posy, attribute, posx=480):
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.attribute = attribute
        self.baseValue = v.Attributes[attribute]
        self.addedValue = 0
    
    def save(self):
        v.Attributes[self.attribute] += self.addedValue
        self.addedValue = 0
    
    def update(self):
        self.baseValue = v.Attributes[self.attribute]
        arrow = py.image.load("Resources/Images/AttributeArrow.png")
        arrow = py.transform.scale(arrow, (int(arrow.get_rect().width * 1280 * 0.00234375), int(arrow.get_rect().height * 1280 * 0.00234375)))
        
        arrowL = py.transform.rotate(arrow, 180)
        v.screen.blit(arrowL, (self.posx, self.posy))
        self.minusRect = py.Rect(self.posx, self.posy, arrow.get_rect().width, arrow.get_rect().height)
        
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(1280 * 0.046875))
        
        label = font.render(str(self.attribute) + ":", 1, (255,255,255))
        lx = self.posx + (20/640 * 1280)
        v.screen.blit(label, (lx, self.posy - 6))
        
        textLength = font.size(str(self.attribute) + ":")[0] + 5
        
        label = font.render(str(self.baseValue), 1, (255,255,255))
        lx = ((self.posx + (20/640 * 1280))) + textLength
        v.screen.blit(label, (lx, self.posy - 6))
        
        textLength += font.size(str(self.baseValue))[0] + 5
        
        label = font.render("+" + str(self.addedValue), 1, (0,255,0))
        lx = ((self.posx + (20/640 * 1280))) + textLength
        v.screen.blit(label, (lx, self.posy - 6))
        
        textLength += font.size("+" + str(self.addedValue))[0] + 40
        
        
        v.screen.blit(arrow, (self.posx + textLength, self.posy))
        self.plusRect = py.Rect(self.posx + textLength, self.posy, arrow.get_rect().width, arrow.get_rect().height)
        

        for event in v.events:
            if event.type == py.MOUSEBUTTONDOWN:
                if self.minusRect.collidepoint(v.mouse_pos):
                    if self.addedValue > 0:
                        self.addedValue -= 1
                        v.skillPoints += 1
                if self.plusRect.collidepoint(v.mouse_pos):
                    if v.skillPoints > 0:
                        self.addedValue += 1
                        v.skillPoints -= 1

class textLabel(py.sprite.Sprite):
    
    def __init__(self, text, pos, colour, font, size, variable = False, centred = False, screen=None):
        super().__init__()
        self.text = text
        self.pos = pos
        self.colour = colour
        self.font = font
        self.size = size
        self.variable = variable
        self.centred = centred
        self.screen = screen
        
    def update(self):
        pos = self.pos
        font = py.font.Font(self.font, self.size)
        if not self.variable:
            label = font.render(self.text, 1, self.colour)
        if self.variable:
            label = font.render(str(getattr(v, self.text)), 1, self.colour)
        if self.centred:
            pos = list(self.pos)
            pos[0] -= font.size(self.text)[0] / 2
            pos[1] -= font.size(self.text)[1] / 2
            pos = tuple(pos)
        if self.screen == None:
            v.screen.blit(label, pos)
        else:
            self.screen.blit(label, pos)
        
class shiftingGradient():
    
    def __init__(self, colour):
        self.colourMod = 255
        self.colour = colour
        self.colourDirection = True
        self.colourModIncreasing = False
        self.colourForward = True
    
    def draw(self):
        if self.colourModIncreasing == False:
            self.colourMod -= 0.1
        if self.colourModIncreasing == True:
            self.colourMod += 0.1
        self.colourMod = round(self.colourMod, 6)
        if self.colourMod <= 50:
            self.colourModIncreasing = True
        if self.colourMod >= 205:
            self.colourModIncreasing = False
        if self.colourMod == 127:
            self.colourDirection = not self.colourDirection
            if self.colourModIncreasing == False:
                self.colourForward = not self.colourForward
        
        if self.colour == ('x', 0, 0):
            colour1 = (255 - self.colourMod, 0, 0)
            colour2 = (0 + self.colourMod, 0, 0)
        if self.colour == (0, 0, 'x'):
            colour1 = (0, 0, 255 - self.colourMod)
            colour2 = (0, 0, 0 + self.colourMod)
        if self.colour == (0, 'x', 0):
            colour1 = (0, 255 - self.colourMod, 0)
            colour2 = (0, 0 + self.colourMod, 0)
        fill_gradient(v.screen, colour1, colour2, vertical=self.colourDirection, forward=self.colourForward)

class apearanceSelector(py.sprite.Sprite):
    
    def __init__(self, sheet, part, number):
        super().__init__()
        self.skin = sheet
        self.sheet = entityClasses.SpriteSheet(self.skin, 4, 3)
        self.part = part
        self.num = number
        if number % 3 == 1:
            self.posx = 1280 * 0.46875
        if number % 3 == 2:
            self.posx = 1280 * 0.625
        if number % 3 == 0:
            self.posx = 1280 * 0.78125
        
        self.posy = (int((number / 3)  - 0.1) * 720 * 0.21) + 720 * 0.21
    
    def update(self):
        if v.appearanceTab == self.part:
            self.image = self.sheet.images[7]
            size = self.image.get_rect()
            size.width = (size.width / 640) * 1280
            size.height = (size.height / 480) * 720
            self.image = py.transform.scale(self.image, (size.width * 3, size.height * 3))
            size = self.image.get_rect()
            self.rect = py.Rect(self.posx, self.posy, size.width, size.height)
            if self.rect.collidepoint(v.mouse_pos):
                py.draw.rect(v.screen, (255, 255, 0), self.rect, 4)
                v.testAppearance[self.part] = self.skin
                for event in v.events:
                    if event.type == py.MOUSEBUTTONDOWN:
                        v.appearance[self.part] = self.skin
            elif v.appearance[self.part] == self.skin:
                py.draw.rect(v.screen, (0, 0, 255), self.rect, 4)
            else:
                py.draw.rect(v.screen, (255, 165, 0), self.rect, 4)
        else:
            self.image = py.Surface((0, 0))
            self.rect = py.Rect(0,0,0,0)
            self.image.fill((255, 255, 255, 0))

class appearancePreview():
    
    def __init__(self, pos=(-40, -70), sizem=11):
        self.pos = pos
        self.sMod = sizem
    
    def draw(self):
        if v.testAppearance["Body"] == None:
            self.sheet = entityClasses.SpriteSheet(v.appearance["Body"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            size.width = size.width * 2
            size.height = size.height * 2
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        else:
            self.sheet = entityClasses.SpriteSheet(v.testAppearance["Body"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            size.width = size.width * 2
            size.height = size.height * 2
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        
        v.screen.blit(self.image, self.pos)
        
        if v.testAppearance["Face"] == None and v.appearance["Face"] != None:
            self.sheet = entityClasses.SpriteSheet(v.appearance["Face"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            size.width = size.width * 2
            size.height = size.height * 2
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        elif v.testAppearance["Face"] != None:
            self.sheet = entityClasses.SpriteSheet(v.testAppearance["Face"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            size.width = size.width * 2
            size.height = size.height * 2
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        else:
            self.image = py.Surface((0, 0))
        v.screen.blit(self.image, self.pos)
        
        if v.testAppearance["Dress"] == None and v.appearance["Dress"] != None:
            self.sheet = entityClasses.SpriteSheet(v.appearance["Dress"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            size.width = size.width * 2
            size.height = size.height * 2
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        elif v.testAppearance["Dress"] != None:
            self.sheet = entityClasses.SpriteSheet(v.testAppearance["Dress"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            size.width = size.width * 2
            size.height = size.height * 2
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        else:
            self.image = py.Surface((0, 0))
        v.screen.blit(self.image, self.pos)
        
        if v.testAppearance["Hair"] == None and v.appearance["Hair"] != None:
            self.sheet = entityClasses.SpriteSheet(v.appearance["Hair"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            size.width = size.width * 2
            size.height = size.height * 2
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        elif v.testAppearance["Hair"] != None:
            self.sheet = entityClasses.SpriteSheet(v.testAppearance["Hair"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            size.width = size.width * 2
            size.height = size.height * 2
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        else:
            self.image = py.Surface((0, 0))
        v.screen.blit(self.image, self.pos)

class appearanceTab(py.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.startx = 490
        self.posy = 60
    
    def draw(self): #TODO: Fix with screen size
        image = py.image.load("Resources/Images/Character Customisation/Tabs/Body.png")
        size = image.get_rect()
        size.width = size.width * 2
        size.height = size.height * 2
        image = py.transform.scale(image, (int(size.width * 1.5), int(size.height * 1.5)))
        rect = py.Rect(self.startx, self.posy + 4, 40, 40)
        v.screen.blit(image, rect)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 40)
        label = font.render("Body", 1, (255, 255, 255))
        v.screen.blit(label, (560, 80))
        rect = py.Rect(481, 61, 190, 76)
        if rect.collidepoint(v.mouse_pos):
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    v.appearanceTab = "Body"
            py.draw.rect(v.screen, (255, 255, 0), rect, 4)
        elif v.appearanceTab == "Body":
            py.draw.rect(v.screen, (0, 0, 255), rect, 4)
        else:
            py.draw.rect(v.screen, (153, 76, 0), rect, 4)
            
        
        image = py.image.load("Resources/Images/Character Customisation/Tabs/Face.png")
        size = image.get_rect()
        size.width = size.width * 2
        size.height = size.height * 2
        image = py.transform.scale(image, (int(size.width * 2), int(size.height * 2)))
        rect = py.Rect(self.startx + 190, self.posy + 14, 40, 40)
        v.screen.blit(image, rect)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 40)
        label = font.render("Face", 1, (255, 255, 255))
        v.screen.blit(label, (750, 80))
        rect = py.Rect(673, 61, 190, 76)
        if rect.collidepoint(v.mouse_pos):
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    v.appearanceTab = "Face"
            py.draw.rect(v.screen, (255, 255, 0), rect, 4)
        elif v.appearanceTab == "Face":
            py.draw.rect(v.screen, (0, 0, 255), rect, 4)
        else:
            py.draw.rect(v.screen, (153, 76, 0), rect, 4)
        
        
        
        image = py.image.load("Resources/Images/Character Customisation/Tabs/Dress.png")
        size = image.get_rect()
        size.width = size.width * 2
        size.height = size.height * 2
        image = py.transform.scale(image, (int(size.width * 2), int(size.height * 2)))
        rect = py.Rect(self.startx + 380, self.posy + 14, 40, 40)
        v.screen.blit(image, rect)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 40)
        label = font.render("Dress", 1, (255, 255, 255))
        v.screen.blit(label, (960, 80))
        rect = py.Rect(865, 61, 190, 76)
        if rect.collidepoint(v.mouse_pos):
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    v.appearanceTab = "Dress"
            py.draw.rect(v.screen, (255, 255, 0), rect, 4)
        elif v.appearanceTab == "Dress":
            py.draw.rect(v.screen, (0, 0, 255), rect, 4)
        else:
            py.draw.rect(v.screen, (153, 76, 0), rect, 4)
        
        image = py.image.load("Resources/Images/Character Customisation/Tabs/Hair.png")
        size = image.get_rect()
        size.width = size.width * 2
        size.height = size.height * 2
        image = py.transform.scale(image, (int(size.width * 2), int(size.height * 2)))
        rect = py.Rect(self.startx + 580, self.posy + 20, 40, 40)
        v.screen.blit(image, rect)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 40)
        label = font.render("Hair", 1, (255, 255, 255))
        v.screen.blit(label, (1150, 80))
        rect = py.Rect(1057, 61, 190, 76)
        if rect.collidepoint(v.mouse_pos):
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    v.appearanceTab = "Hair"
            py.draw.rect(v.screen, (255, 255, 0), rect, 4)
        elif v.appearanceTab == "Hair":
            py.draw.rect(v.screen, (0, 0, 255), rect, 4)
        else:
            py.draw.rect(v.screen, (153, 76, 0), rect, 4)

class textInput(py.sprite.Sprite):
    
    def __init__(self, pos, fontSize, characters, num, button="GO", default=[], type="str", fontfile="Resources/Fonts/RPGSystem.ttf", background=(255, 255, 255)):
        super().__init__()
        self.font = py.font.Font(fontfile, fontSize)
        self.thickness = 2 #int(fontSize / 4)
        biggest = "W "
        if type =="pass":
            biggest = "* "
        self.rect = py.Rect(pos, self.font.size(biggest * characters))
        self.rect.width += fontSize / 1.5
        self.rect.height += fontSize / 1.5
        self.fontSize = fontSize
        self.string = default
        self.pos = pos
        self.characters = characters
        self.shift = False
        self.done = False
        self.button = button
        self.num = num
        self.type = type
        self.outText = ""
        self.background = background
    
    def draw(self):
        if self.num == v.textNum:
            c = (255, 0, 0)
        else:
            c = (0, 0, 0,)
        py.draw.rect(v.screen, self.background, self.rect)
        py.draw.rect(v.screen, c, self.rect, self.thickness)
        x = self.pos[0] + self.fontSize / 3
        y = self.pos[1] + self.fontSize / 3
        for letter in self.string:
            char = letter
            if self.type == "pass":
                char = "*"
            ren = self.font.render(char, 1, (0, 0, 0))
            v.screen.blit(ren, (x, y))
            x += self.font.size(char)[0] + self.fontSize / 6
    
    def update(self):
        
        global textEdit
        textEdit = True
        self.outText = "".join(self.string)
        if self.num == v.textNum:
            
            for event in v.events:
                if event.type == py.KEYDOWN:
                    if len(self.string) < self.characters:
                        if py.key.name(event.key) in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', ',', '.', "'", '/', '#', ';', '-']:
                            if py.key.get_mods() == py.KMOD_LSHIFT:
                                let = py.key.name(event.key).upper()
                                if py.key.name(event.key) == '1':
                                    let = '!'
                                if py.key.name(event.key) == '2':
                                    let = '"'
                                if py.key.name(event.key) == '3':
                                    let = '£'
                                if py.key.name(event.key) == '4':
                                    let = '$'
                                if py.key.name(event.key) == '5':
                                    let = '%'
                                if py.key.name(event.key) == '9':
                                    let = '('
                                if py.key.name(event.key) == '0':
                                    let = ')'
                                if py.key.name(event.key) == '/':
                                    let = '?'
                                if py.key.name(event.key) == ';':
                                    let = ':'
        
                            else:
                                let = py.key.name(event.key)
                            allow = True
                            if self.type == "int":
                                try:
                                    int(let)
                                    allow = True
                                except:
                                    allow = False
                            if allow:        
                                self.string.append(let)
                        if event.key == py.K_SPACE:
                            self.string.append(" ")
                        if event.key == py.K_TAB:
                            v.events.remove(event)
                            print("PRESS TAB")
                            v.textNum += 1
                    if event.key == py.K_BACKSPACE:
                        if len(self.string) > 0:
                            self.string.pop(-1)
        self.draw()
        
        if not self.button == None:
            label = self.font.render(self.button, 1, (0, 0, 0))
            butRect = py.Rect(self.rect.topright, (self.rect.height, self.rect.height))
            butRect.centerx += 5
            py.draw.rect(v.screen, (255, 255, 255), butRect)
            py.draw.rect(v.screen, (0, 0, 0), butRect, 5)
            v.screen.blit(label, (butRect.centerx - self.font.size(self.button)[0] / 2, butRect.centery - self.font.size(self.button)[1] / 2))
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    if butRect.collidepoint(v.mouse_pos):
                        global outText
                        outText = "".join(self.string)
                        self.done = True
                        py.time.wait(100)
        if self.rect.collidepoint(v.mouse_pos):
            if py.mouse.get_pressed()[0]:
                v.textNum = self.num
        

def notImplimented():
    font = py.font.SysFont("Comic Sans", 60, True)
    for k, colour in py.color.THECOLORS.items():
        label = font.render("NOT YET IMPLEMENTED!", 1, colour, (255, 255, 255))
        size = font.size("NOT YET IMPLEMENTED!")
        v.screen.blit(label, (1280/2 - size[0]/2, 720/2 - size[1]/2))
        py.time.delay(1)
        py.display.flip()

class storySpells(py.sprite.Sprite):
    
    def __init__(self, start):
        super().__init__()
        self.active = True
        self.image = entityClasses.SpriteSheet("Resources/Images/castOrbPurple.png", 1, 10).images[9]
        self.image.fill((0, 255, 255), special_flags=py.BLEND_MULT)
        self.shield = py.transform.scale(py.image.load("Resources/Images/Story/Shield.png"), (int((30 * 4.5)/640 * 1280), int((40 * 4.5)/640 * 1280)))
        self.end = (1280 * 0.4, 720 * 0.9)
        self.start = (start[0] + ((24 * 3)/640 * 1280)/2, start[1] + ((32 * 3)/640 * 1280)/2)
        self.posx = self.start[0]
        self.posy = self.start[1]
        xDiff = self.end[0] - self.start[0]
        yDiff = self.end[1] - self.start[1]
        self.xStep = xDiff / 100
        self.yStep = yDiff / 100
        self.cycle = 0
        from math import sqrt
        self.cycleStep = sqrt((xDiff ** 2) + (yDiff ** 2)) / 100
    
    def update(self):
        img = py.transform.scale(self.image, (int(30/640 * 1280), int(30/640 * 1280)))
        v.screen.blit(img, (self.posx, self.posy))
        self.posx += self.xStep
        self.posy += self.yStep
        self.cycle += self.cycleStep
        if self.cycle >= 80:
            pos = (1280 * 0.3, 720 * 0.7)
            v.screen.blit(self.shield, pos)
        if self.cycle >= 90:
            self.kill()

def screenFlip():
    for event in v.events:
        if event.type == py.VIDEORESIZE:
            if not v.fullScreen:
                v.screenDisplay = py.display.set_mode(event.size, py.HWSURFACE|py.DOUBLEBUF|py.RESIZABLE)
                v.screenX, v.screenY = event.size
        if event.type == py.KEYDOWN:
            if event.key == py.K_r:
                curFunc = sys._getframe(1).f_code.co_name
                print(curFunc)
                v.events.remove(event)
                raise Exception("Reload:" + curFunc)
    
    screen_rect = v.screenDisplay.get_rect()
    image = py.Surface(v.screenStart).convert()
    image_rect = image.get_rect()
    image.fill((0, 0, 0))
    image.blit(v.screen, (0, 0))
    if (v.screenX, v.screenY) == (1280, 720):
        v.screenDisplay.blit(image, (0, 0))
    elif screen_rect.size != v.screenStart:
        fit_to_rect = image_rect.fit(screen_rect)
        fit_to_rect.center = screen_rect.center
        scaled = py.transform.smoothscale(image, fit_to_rect.size)
        v.screenDisplay.blit(scaled, fit_to_rect)
    else:
        v.screenDisplay.blit(image, (0,0))
        fit_to_rect = image_rect
    
    if (v.screenX, v.screenY) != (1280, 720):
        scale = (v.screenStart[0]/fit_to_rect[2], v.screenStart[1]/fit_to_rect[3])
        x,y = py.mouse.get_pos()
        v.mouse_pos = (int((x - fit_to_rect[0])*scale[0]), int((y - fit_to_rect[1])*scale[1]))
    else:
        v.mouse_pos = py.mouse.get_pos()
    
    py.display.flip()