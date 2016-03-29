import pygame as py
import os

screen = py.display.set_mode((200, 400))

folder = "../Resources/Images/Tile Set/"

width = 0
height = 0

images = []
for i in os.listdir(folder):
    print(folder + i)
    #images.insert(0, py.image.load(folder + i))
    images.append(py.image.load(folder + i))

for i in images:
    if i.get_rect().size[0] > width:
        width = i.get_rect().size[0]
        print("New Width:", width)
    height += i.get_rect().size[1]
    
out = py.Surface((width, height), flags=py.SRCALPHA)

pos = 0

for i in images:
    r = out.blit(i, (0, pos))
    print(pos, r)
    screen.fill((50, 50, 50))
    outBlit = i
    screen.blit(outBlit, (0, 0))
    py.display.flip()
    py.time.delay(200)
    pos += i.get_rect().size[1]

print("Saving...")    
py.image.save(out, "../Resources/Images/Main_Tileset.png")