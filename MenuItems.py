import pygame as py
import entityClasses
import Variables as v
from _operator import pos
from msilib.schema import Font

class Button(py.sprite.Sprite):

    def __init__(self, text, pos, size, hovercolour, normalcolour, font, ID):
        super().__init__()
        self.ID = ID
        self.hovered = False
        self.text = text
        self.pos = pos
        self.size = size
        self.hcolour = hovercolour
        self.ncolour = normalcolour
        self.font = font
        self.font = py.font.Font(font, size)
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
        self.rect.topleft = self.pos

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
                if event.type == py.USEREVENT + 1: 
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
            
            
                
            font = py.font.SysFont("Resources/Fonts/RPGSystem.ttf", int(10 * sMod)) #TODO: Scale
            label = font.render(self.name, 1, (cMod, cMod, cMod))
            v.screen.blit(label, (self.rect.centerx - (font.size(self.name)[0] / 2), self.rect.bottom  + (2 * sMod)))
        if v.custimizationStage == "To Attributes":
            if self.name == v.playerClass:
                for event in v.events:
                    if event.type == py.USEREVENT + 1:
                        sMod = 6 + ((200 - self.movingCycle) / 40)
                        size = self.skin.get_rect()
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
                self.image = py.transform.scale(self.skin, (int(size.width * 3), int(size.height * 3)))
                self.image.fill((135, 135, 135, self.opacity), special_flags=py.BLEND_RGBA_MULT)
                self.opacity -= 1
                if self.opacity < 0:
                    self.opacity = 0
                
class optionSlate():
    
    def __init__(self):
        self.posx = 960
        self.posy = 240
        self.width = 400
        self.height = 400
    
    def update(self):
        if v.custimizationStage == "To Attributes":
            self.innerRect = py.Rect(0, 0, self.width, self.height)
            self.innerRect.center = self.posx, self.posy
            self.outerRect = py.Rect(0, 0, self.width + 20, self.height + 20)
            self.outerRect.center = self.posx, self.posy
            py.draw.rect(v.screen, py.Color(153, 76, 0), self.outerRect)
            py.draw.rect(v.screen, py.Color(255, 178, 102), self.innerRect)
            if self.posx != 440:
                self.posx -= 1
            else:
                v.custimizationStage = "Attributes"
        if v.custimizationStage == "Attributes":
            self.posx = 440
            self.posy = 240
            self.innerRect = py.Rect(0, 0, self.width, self.height)
            self.innerRect.center = self.posx, self.posy
            self.outerRect = py.Rect(0, 0, self.width + 20, self.height + 20)
            self.outerRect.center = self.posx, self.posy
            py.draw.rect(v.screen, py.Color(153, 76, 0), self.outerRect)
            py.draw.rect(v.screen, py.Color(255, 178, 102), self.innerRect)

class optionAttribute(py.sprite.Sprite):
    
    def __init__(self, posy, attribute):
        super().__init__()
        self.posx = 240
        self.posy = posy
        self.attribute = attribute
        self.baseValue = v.Attributes[attribute]
        self.addedValue = 0
    
    def update(self):
        if v.custimizationStage == "Attributes":
            arrow = py.image.load("Resources/Images/AttributeArrow.png")
            arrow = py.transform.scale(arrow, (int(arrow.get_rect().width * 1.5), int(arrow.get_rect().height * 1.5)))
            
            arrowL = py.transform.rotate(arrow, 180)
            v.screen.blit(arrowL, (self.posx, self.posy))
            self.minusRect = py.Rect(self.posx, self.posy, arrow.get_rect().width, arrow.get_rect().height)
            
            font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
            
            label = font.render(str(self.attribute) + ":", 1, (255,255,255))
            lx = 260
            v.screen.blit(label, (lx, self.posy - 6))
            
            textLength = font.size(str(self.attribute) + ":")[0] + 5
            
            label = font.render(str(self.baseValue), 1, (255,255,255))
            lx = 260 + textLength
            v.screen.blit(label, (lx, self.posy - 6))
            
            textLength += font.size(str(self.baseValue))[0] + 5
            
            label = font.render("+" + str(self.addedValue), 1, (0,255,0))
            lx = 260 + textLength
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
    
    def __init__(self, text, pos, colour, font, size, variable = False):
        super().__init__()
        self.text = text
        self.pos = pos
        self.colour = colour
        self.font = font
        self.size = size
        self.variable = variable
        
    def update(self):
        font = py.font.Font(self.font, self.size)
        if not self.variable:
            label = font.render(self.text, 1, self.colour)
        if self.variable:
            label = font.render(str(getattr(v, self.text)), 1, self.colour)
    
        v.screen.blit(label, self.pos)