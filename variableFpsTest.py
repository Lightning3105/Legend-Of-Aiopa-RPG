import pygame as py

class blob(py.sprite.Sprite):
    
    def __init__(self, posy):
        super().__init__()
        self.posx = 0
        self.posy = posy
        self.direction = False
        self.start = py.time.get_ticks()
    
    def update(self):
        self.image = py.Surface((20, 20))
        self.image.fill((255, 0, 0))
        self.rect = py.Rect(self.posx, self.posy, 20, 20)
        if self.posx > 200:
            self.direction = True
            print("############")
            print(py.time.get_ticks() - self.start)
            #py.time.wait(1000)
            self.start = py.time.get_ticks()
        if self.rect.right < 0:
            self.direction = False
            print("############")
            print(py.time.get_ticks() - self.start)
            #py.time.wait(1000)
            self.start = py.time.get_ticks()
        
        try:
            adjuster = (speed/clock.get_fps())
        except:
            adjuster = 1
        
        if self.direction:
            self.posx -= 1 * adjuster
        else:
            self.posx += 1 * adjuster


screen = py.display.set_mode((200, 100))

blobs = py.sprite.Group()
blobs.add(blob(50))
clock = py.time.Clock()
speed = 60

while True:
    clock.tick(30)
    #print(clock.get_fps())
    screen.fill((0, 255, 255))
    blobs.update()
    blobs.draw(screen)
    py.display.flip()