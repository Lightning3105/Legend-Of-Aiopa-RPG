import urllib.request
import pickle
import sys
import Variables as v

import pygame as py
from MenuItems import Button, textLabel
py.init()
v.screen = py.display.set_mode((640, 480))
v.screen.fill((20, 20, 20))
textLabel("Checking For Updates...", (320, 240), (255, 255, 255), "Resources/Fonts/Vecna.otf", 50, False, True).update()
py.display.flip()

def reporthook(count, blockSize, totalSize):
    #Shows percentage of download
    py.event.pump()
    percent = int(count*blockSize*100/totalSize)
    rect = py.Rect(100, 240, percent*4.4, 30)
    v.screen.fill((20, 20, 20))
    py.draw.rect(v.screen, (255, 0, 0), rect)
    py.draw.rect(v.screen, (0, 0, 0), rect, 2)
    py.draw.rect(v.screen, (0, 0, 0), (100, 240, 440, 30), 2)
    #font = py.font.Font("Resources/Fonts/Vecna.otf", 25)
    #title = font.render("Downloading...", 1, (255, 255, 255))
    #progress = font.render(str(percent) + "%", 1, (255, 255, 255))
    #v.screen.blit(title, (200, 200))
    #v.screen.blit(progress, (200, 250))
    textLabel("Downloading...", (320, 150), (255, 255, 255), "Resources/Fonts/Vecna.otf", 50, False, True).update()
    textLabel(str(percent) + "%", (320, 255), (255, 255, 255), "Resources/Fonts/Vecna.otf", 20, False, True).update()
    py.display.flip()
    
    
    #sys.stdout.write("\r" + "...%d%%" % percent)
    #sys.stdout.flush()


def updateCheck():
    global latest
    page = urllib.request.urlopen('https://github.com/Lightning3105/Legend-Of-Aiopa-RPG/commits/master')
    page = str(page.read())
    ind = page.find('class="sha btn btn-outline"')
    latest = page[ind + 38:ind + 45]
    print(latest)
    
    #CHECK IF LATEST IS PROPER
    
    try:
        f = open("Saves/current.version", "rb")
        current = pickle.load(f)
        f.close()
    except:
        print("create new file")
        f = open("Saves/current.version", "wb")
        current = 0000
        pickle.dump(current, f)
        f.close()
    current = 0 #TEMP TEST
    print(current, "vs", latest)
    if current != latest:
        print("downloading latest")
        buttons = py.sprite.Group()
        buttons.add(Button("Update", (220, 240), 60, (100, 100, 100), (255, 255, 255), "Resources/Fonts/Vecna.otf", "Y", centred=True))
        buttons.add(Button("Ignore", (420, 240), 60, (100, 100, 100), (255, 255, 255), "Resources/Fonts/Vecna.otf", "N", centred=True))
        labels = py.sprite.Group()
        labels.add(textLabel("An Update Is Available:", (320, 150), (255, 255, 255), "Resources/Fonts/Vecna.otf", 50, False, True))
        labels.add(textLabel(str(str(current) + " ==> " + str(latest)), (320, 180), (255, 255, 255), "Resources/Fonts/Vecna.otf", 20, False, True))
        
        while True:
            py.event.pump()
            v.screen.fill((20, 20, 20))
            buttons.update()
            labels.update()
            for event in py.event.get():
                if event.type == py.QUIT:
                    sys.exit()
                elif event.type == py.MOUSEBUTTONDOWN:
                    for button in buttons:
                        if button.pressed():
                            id = button.ID
                            if id == "Y":
                                download()
                                return
                            if id == "N":
                                return 
            py.display.flip()
        
def download():        
    urllib.request.urlretrieve("https://github.com/Lightning3105/Legend-Of-Aiopa-RPG/archive/master.zip", "Update/download.zip", reporthook)
    f = open("Saves/current.version", "wb")
    current = latest
    pickle.dump(current, f)
    f.close()
    unzip()

def unzip():
    v.screen.fill((20, 20, 20))
    textLabel("Extracting Data...", (320, 240), (255, 255, 255), "Resources/Fonts/Vecna.otf", 50, False, True).update()
    py.display.flip()
    import zipfile
    with zipfile.ZipFile('Update/download.zip', "r") as z:
        z.extractall("Update/")
    
    v.screen.fill((20, 20, 20))
    textLabel("Updating Files...", (320, 240), (255, 255, 255), "Resources/Fonts/Vecna.otf", 50, False, True).update()
    py.display.flip()
    
    #from shutil import copytree
    from os import getcwd
    from distutils.dir_util import copy_tree
    copy_tree("Update/Legend-Of-Aiopa-RPG-master", getcwd())

unzip()   