import Variables as v
import pygame as py

class inventory():
    
    def __init__(self):
        self.size = 3
        self.contents = []
    
    def update(self):
        self.grey()
        self.background()
        
    def grey(self):
        grey = py.Surface((v.screen.get_rect()[2], v.screen.get_rect()[3])).convert_alpha()
        grey.fill((20, 20, 20, 200))
        v.screen.blit(grey, (0, 0))
    
    def background(self):
        size = v.screen.get_rect().size
        size = (size[0] - 100, size[1] - 100)
        innerRect = py.Rect(50, 50, size[0], size[1])
        outerRect = py.Rect(40, 40, size[0] + 20, size[1] + 20)
        py.draw.rect(v.screen, py.Color(153, 76, 0), outerRect)
        py.draw.rect(v.screen, py.Color(255, 178, 102), innerRect)