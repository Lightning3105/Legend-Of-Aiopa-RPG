import pygame as py
import entityClasses
import Variables as v

screen = None

class Button:

    hovered = False

    def __init__(self, text, pos, size, hovercolour, normalcolour, font):
        self.text = text
        self.pos = pos
        self.size = size
        self.hcolour = hovercolour
        self.ncolour = normalcolour
        self.font = font
        self.font = py.font.Font(font, size)
        self.set_rect()
        self.draw()

    def draw(self):
        self.set_rend()
        py.draw.rect(screen, self.get_color(), self.rect)
        screen.blit(self.rend, self.rect)

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

    def pressed(self, mouse):
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
        screen.blit(self.rend, self.rect)

    def set_rend(self):
        self.rend = self.font.render(self.text, True, self.colour)

    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos

def centre():
    return (screen.get_rect()[2] / 2, screen.get_rect()[3] / 2)

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
        black = py.Surface((screen.get_rect()[2], screen.get_rect()[3]))
        black.fill((0, 0, 0))
        black.set_alpha(self.opacity)
        screen.blit(black, (0, 0))

class characterSelector(py.sprite.Sprite):

    def __init__(self, image, pos, name):
        super().__init__()
        self.pos = pos
        self.sheet = entityClasses.SpriteSheet(image, 1, 5)
        self.sheet.getGrid()
        self.animationPosition = 0
        self.image = self.sheet.images[self.animationPosition]

    def update(self):
        for event in v.events:
            if event.type == py.USEREVENT + 1:
                if not self.animationPosition > len(self.sheet.images) - 1:
                    self.image = self.sheet.images[self.animationPosition]
                    self.animationPosition += 1
                else:
                    self.image = self.sheet.images[0]
                    self.animationPosition += 1
                    if self.animationPosition >= len(self.sheet.images) * 2:
                        self.animationPosition = 0

        print(self.animationPosition)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = self.pos
