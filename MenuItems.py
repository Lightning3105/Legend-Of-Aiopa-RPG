import pygame as py
import entityClasses
import Variables as v
from _operator import pos
from msilib.schema import Font
from os import listdir
import itemClasses
import setupScripts

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
        self.font = py.font.Font(font, size)
        self.centred = centred
        self.size = bsize
        self.set_rect()
    
    def update(self):
        self.set_rend()
        py.draw.rect(v.screen, self.get_color(), self.rect)
        v.screen.blit(self.rend, self.rect)
        if self.rect.collidepoint(py.mouse.get_pos()):
                self.hovered = True
        else:
            self.hovered = False

    def set_rend(self):
        self.rend = self.font.render(self.text, True, (0,0,0))

    def get_color(self):
        if self.hovered:
            return self.hcolour
        else:
            return self.ncolour

    def set_rect(self):
        self.set_rend()
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
        mouse = py.mouse.get_pos()
        if mouse[0] > self.rect.topleft[0]:
            if mouse[1] > self.rect.topleft[1]:
                if mouse[0] < self.rect.bottomright[0]:
                    if mouse[1] < self.rect.bottomright[1]:
                        return True
                    else: return False
                else: return False
            else: return False
        else: return False


class Text:

    def __init__(self, text, pos, size, colour, font):
        self.text = text
        self.pos = pos
        self.size = size
        self.colour = colour
        self.font = font
        self.font = py.font.Font(font, size)
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        v.screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.font.render(self.text, True, self.colour)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

def centre():
    return (v.screen.get_rect()[2] / 2, v.screen.get_rect()[3] / 2)

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

    def draw(self):
        black = py.Surface((v.screen.get_rect()[2], v.screen.get_rect()[3]))
        black.fill((0, 0, 0))
        black.set_alpha(self.opacity)
        v.screen.blit(black, (0, 0))

class characterSelector(py.sprite.Sprite):

    def __init__(self, image, pos, name):
        super().__init__()
        self.pos = pos
        self.name = name
        self.skin = py.image.load(image)
        self.hovered = False
        self.hoveredCycle = 0
        self.greyedCycle = 0
        self.movingCycle = 200
        self.movDistance = abs(self.pos[0] - 130)
        self.opacity = 255
        

    def update(self):
        if v.custimizationStage == "Class Selection":
            sMod = (self.hoveredCycle / 10) + 3
            cMod = self.greyedCycle * 4
            cMod = 255 - cMod
            size = self.skin.get_rect()
            size.width = (size.width / 640) * v.screenX
            size.height = (size.height / 480) * v.screenY
            self.image = py.transform.scale(self.skin, (int(size.width * sMod), int(size.height * sMod)))
            
            self.image.fill((cMod, cMod, cMod), special_flags=py.BLEND_RGBA_MULT)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos
            if self.rect.collidepoint(py.mouse.get_pos()):
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
        elif v.custimizationStage == "To Attributes":
            if self.name == v.playerClass:
                for event in v.events:
                    if event.type == py.USEREVENT:
                        sMod = 6 + ((200 - self.movingCycle) / 40)
                        size = self.skin.get_rect()
                        size.width = (size.width / 640) * v.screenX
                        size.height = (size.height / 480) * v.screenY
                        self.image = py.transform.scale(self.skin, (int(size.width * sMod), int(size.height * sMod)))
                        self.rect = self.image.get_rect()
                        newpos = list(self.pos)
                        newpos[0] = self.pos[0] - (self.movDistance - (self.movingCycle * (self.movDistance / 200)))  # TODO: Make this work
                        newpos[1] = self.pos[1] - (40 - (self.movingCycle * (40 / 200)))
                        if self.movingCycle > 0:
                            self.movingCycle -= 1
                        self.rect.center = newpos
                        
            else:
                size = self.skin.get_rect()
                size.width = (size.width / 640) * v.screenX
                size.height = (size.height / 480) * v.screenY
                self.image = py.transform.scale(self.skin, (int(size.width * 3), int(size.height * 3)))
                self.image.fill((135, 135, 135, self.opacity), special_flags=py.BLEND_RGBA_MULT)
                self.opacity -= 1
                if self.opacity < 0:
                    self.opacity = 0
        if v.custimizationStage == "Customisation":
            self.image.fill((255, 255, 255, 0))
                
class optionSlate():
    
    def __init__(self):
        self.width = v.screenX * 0.625
        self.height = v.screenX * 0.625
        self.posx = v.screenX * 1.5
        self.posy = v.screenY * 0.5
        
    
    def update(self):
        if v.custimizationStage == "To Attributes":
            self.innerRect = py.Rect(0, 0, self.width, self.height)
            self.innerRect.center = self.posx, self.posy
            self.outerRect = py.Rect(0, 0, self.width + 20, self.height + 20)
            self.outerRect.center = self.posx, self.posy
            py.draw.rect(v.screen, py.Color(153, 76, 0), self.outerRect)
            py.draw.rect(v.screen, py.Color(255, 178, 102), self.innerRect)
            if self.posx != v.screenX * 0.6875:
                self.posx -= v.screenX * 0.003125
            else:
                v.custimizationStage = "Attributes"
        if v.custimizationStage == "Attributes" or v.custimizationStage == "Customisation":
            self.posx = v.screenX * 0.6875
            self.posy = v.screenY * 0.5
            self.innerRect = py.Rect(0, 0, self.width, self.height)
            self.innerRect.center = self.posx, self.posy
            self.outerRect = py.Rect(0, 0, self.width + 20, self.height + 20)
            self.outerRect.center = self.posx, self.posy
            py.draw.rect(v.screen, py.Color(153, 76, 0), self.outerRect)
            py.draw.rect(v.screen, py.Color(255, 178, 102), self.innerRect)

class optionAttribute(py.sprite.Sprite):
    
    def __init__(self, posy, attribute):
        super().__init__()
        self.posx = v.screenX * 0.375
        self.posy = posy
        self.attribute = attribute
        self.baseValue = v.Attributes[attribute]
        self.addedValue = 0
    
    def save(self):
        v.Attributes[self.attribute] += self.addedValue
        self.addedValue = 0
    
    def update(self):
        if v.custimizationStage == "Attributes":
            self.baseValue = v.Attributes[self.attribute]
            arrow = py.image.load("Resources/Images/AttributeArrow.png")
            arrow = py.transform.scale(arrow, (int(arrow.get_rect().width * v.screenX * 0.00234375), int(arrow.get_rect().height * v.screenX * 0.00234375)))
            
            arrowL = py.transform.rotate(arrow, 180)
            v.screen.blit(arrowL, (self.posx, self.posy))
            self.minusRect = py.Rect(self.posx, self.posy, arrow.get_rect().width, arrow.get_rect().height)
            
            font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(v.screenX * 0.046875))
            
            label = font.render(str(self.attribute) + ":", 1, (255,255,255))
            lx = v.screenX * 0.40625
            v.screen.blit(label, (lx, self.posy - 6))
            
            textLength = font.size(str(self.attribute) + ":")[0] + 5
            
            label = font.render(str(self.baseValue), 1, (255,255,255))
            lx = (v.screenX * 0.40625) + textLength
            v.screen.blit(label, (lx, self.posy - 6))
            
            textLength += font.size(str(self.baseValue))[0] + 5
            
            label = font.render("+" + str(self.addedValue), 1, (0,255,0))
            lx = (v.screenX * 0.40625) + textLength
            v.screen.blit(label, (lx, self.posy - 6))
            
            textLength += font.size("+" + str(self.addedValue))[0] + 25
            
            
            v.screen.blit(arrow, (self.posx + textLength, self.posy))
            self.plusRect = py.Rect(self.posx + textLength, self.posy, arrow.get_rect().width, arrow.get_rect().height)
            

            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    if self.minusRect.collidepoint(py.mouse.get_pos()):
                        if self.addedValue > 0:
                            self.addedValue -= 1
                            v.skillPoints += 1
                    if self.plusRect.collidepoint(py.mouse.get_pos()):
                        if v.skillPoints > 0:
                            self.addedValue += 1
                            v.skillPoints -= 1

class textLabel(py.sprite.Sprite):
    
    def __init__(self, text, pos, colour, font, size, variable = False, centred = False):
        super().__init__()
        self.text = text
        self.pos = pos
        self.colour = colour
        self.font = font
        self.size = size
        self.variable = variable
        self.centred = centred
        
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
    
        v.screen.blit(label, pos)
        
class shiftingGradient():
    
    def __init__(self, colour1, colour2):
        self.colourMod = 255
        self.colour1 = colour1
        self.colour2 = colour2
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
        colour1 = (255 - self.colourMod, 0, 0)
        colour2 = (0 + self.colourMod, 0, 0)
        fill_gradient(v.screen, colour1, colour2, vertical=self.colourDirection, forward=self.colourForward)

class apearanceSelector(py.sprite.Sprite):
    
    def __init__(self, sheet, part, number):
        super().__init__()
        self.skin = sheet
        self.sheet = entityClasses.SpriteSheet(self.skin, 4, 3)
        self.part = part
        self.num = number
        if number % 3 == 1:
            self.posx = 300
        if number % 3 == 2:
            self.posx = 400
        if number % 3 == 0:
            self.posx = 500
        
        self.posy = (int((number / 3)  - 0.1) * 100) + 100
    
    def update(self):
        if v.appearanceTab == self.part:
            self.image = self.sheet.images[7]
            size = self.image.get_rect()
            self.image = py.transform.scale(self.image, (size.width * 3, size.height * 3))
            size = self.image.get_rect()
            self.rect = py.Rect(self.posx, self.posy, size.width, size.height)
            if self.rect.collidepoint(py.mouse.get_pos()):
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
    
    def __init__(self):
        self.pos = (0, 0)
        self.sMod = 11
    
    def draw(self):
        if v.testAppearance["Body"] == None:
            self.sheet = entityClasses.SpriteSheet(v.appearance["Body"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        else:
            self.sheet = entityClasses.SpriteSheet(v.testAppearance["Body"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        
        v.screen.blit(self.image, self.pos)
        
        if v.testAppearance["Face"] == None and v.appearance["Face"] != None:
            self.sheet = entityClasses.SpriteSheet(v.appearance["Face"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        elif v.testAppearance["Face"] != None:
            self.sheet = entityClasses.SpriteSheet(v.testAppearance["Face"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        else:
            self.image = py.Surface((0, 0))
        v.screen.blit(self.image, self.pos)
        
        if v.testAppearance["Dress"] == None and v.appearance["Dress"] != None:
            self.sheet = entityClasses.SpriteSheet(v.appearance["Dress"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        elif v.testAppearance["Dress"] != None:
            self.sheet = entityClasses.SpriteSheet(v.testAppearance["Dress"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        else:
            self.image = py.Surface((0, 0))
        v.screen.blit(self.image, self.pos)
        
        if v.testAppearance["Hair"] == None and v.appearance["Hair"] != None:
            self.sheet = entityClasses.SpriteSheet(v.appearance["Hair"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        elif v.testAppearance["Hair"] != None:
            self.sheet = entityClasses.SpriteSheet(v.testAppearance["Hair"], 4, 3)
            self.image = self.sheet.images[v.appearancePrevNum]
            size = self.image.get_rect()
            self.image = py.transform.scale(self.image, (size.width * self.sMod, size.height * self.sMod))
        else:
            self.image = py.Surface((0, 0))
        v.screen.blit(self.image, self.pos)

class appearanceTab(py.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        self.startx = 250
        self.posy = 40
    
    def draw(self):
        image = py.image.load("Resources/Images/Character Customisation/Tabs/Body.png")
        size = image.get_rect()
        image = py.transform.scale(image, (int(size.width * 1.5), int(size.height * 1.5)))
        rect = py.Rect(self.startx, self.posy + 2, 20, 20)
        v.screen.blit(image, rect)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 20)
        label = font.render("Body", 1, (255, 255, 255))
        v.screen.blit(label, (280, 50))
        rect = py.Rect(241, 41, 80, 38)
        if rect.collidepoint(py.mouse.get_pos()):
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
        image = py.transform.scale(image, (int(size.width * 2), int(size.height * 2)))
        rect = py.Rect(self.startx + 80, self.posy + 7, 20, 20)
        v.screen.blit(image, rect)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 20)
        label = font.render("Face", 1, (255, 255, 255))
        v.screen.blit(label, (280 + 83, 50))
        rect = py.Rect(241 + 83, 41, 80, 38)
        if rect.collidepoint(py.mouse.get_pos()):
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
        image = py.transform.scale(image, (int(size.width * 2), int(size.height * 2)))
        rect = py.Rect(self.startx + 160, self.posy + 7, 20, 20)
        v.screen.blit(image, rect)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 20)
        label = font.render("Dress", 1, (255, 255, 255))
        v.screen.blit(label, (280 + 166, 50))
        rect = py.Rect(241 + 166, 41, 85, 38)
        if rect.collidepoint(py.mouse.get_pos()):
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
        image = py.transform.scale(image, (int(size.width * 2), int(size.height * 2)))
        rect = py.Rect(self.startx + 250, self.posy + 10, 20, 20)
        v.screen.blit(image, rect)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 20)
        label = font.render("Hair", 1, (255, 255, 255))
        v.screen.blit(label, (280 + 254, 50))
        rect = py.Rect(241 + 254, 41, 85, 38)
        if rect.collidepoint(py.mouse.get_pos()):
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    v.appearanceTab = "Hair"
            py.draw.rect(v.screen, (255, 255, 0), rect, 4)
        elif v.appearanceTab == "Hair":
            py.draw.rect(v.screen, (0, 0, 255), rect, 4)
        else:
            py.draw.rect(v.screen, (153, 76, 0), rect, 4)
