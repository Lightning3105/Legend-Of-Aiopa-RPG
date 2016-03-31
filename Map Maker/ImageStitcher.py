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


width = max(i.get_rect().width for i in images)
height = sum(i.get_rect().height for i in images)
print("Width:", width)
print("Height:", height)

out = py.Surface((width, height), flags=py.SRCALPHA|py.HWSURFACE)
out2 = py.Surface((width, height), flags=py.SRCALPHA|py.HWSURFACE)
pos = 0

for i in images:
    if not i.get_rect().height > 44000:
        r = out.blit(i, (0, pos))
        #r = py.draw.rect(out, (255, 0, 0), ((0, pos), i.get_rect().size), 2)
        print(pos, r, i)
        screen.fill((50, 50, 50))
        outBlit = i
        screen.blit(outBlit, (0, 0))
        py.display.flip()
        py.time.delay(200)
        pos += i.get_rect().height
for i in images:
    if i.get_rect().height > 44000:
        r = out.blit(i, (0, pos))
        print(pos, r, i)
        screen.fill((50, 50, 50))
        outBlit = i
        screen.blit(outBlit, (0, 0))
        py.display.flip()
        py.time.delay(200)
        pos += i.get_rect().height

print("Saving...")    
py.image.save(out, "../Resources/Images/Main_Tileset.png")