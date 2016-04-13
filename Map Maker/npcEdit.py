import mapMakerVariables as v
import mapMenuItems
import pygame as py
from _ast import Num
import math

class enemyImage(py.sprite.Sprite):
    
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
        if v.selectedEnemy["Image"] == self.sheet:
            py.draw.rect(v.pallet, (255, 0, 0), self.rect, 1)
        if self.hovered:
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    if py.mouse.get_pressed()[0]:
                        v.selectedEnemy["Image"] = self.sheet
                        createEnemy()


def createEnemy():
    tinps = py.sprite.Group()
    texts = py.sprite.Group()
    v.textNum = 1
    
    tinps.add(mapMenuItems.textInput((400, 100), 40, 16, 1, button=None, default=[], type="str"))
    texts.add(mapMenuItems.textLabel("Enemy Name:", (150, 110), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    tinps.add(mapMenuItems.textInput((400, 200), 40, 2, 2, button=None, default=[], type="int"))
    texts.add(mapMenuItems.textLabel("Attack:", (150, 210), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    tinps.add(mapMenuItems.textInput((400, 300), 40, 3, 3, button=None, default=[], type="int"))
    texts.add(mapMenuItems.textLabel("Health:", (150, 310), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    tinps.add(mapMenuItems.textInput((400, 400), 40, 2, 4, button=None, default=[], type="int"))
    texts.add(mapMenuItems.textLabel("Speed:", (150, 410), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    button = mapMenuItems.button("Done", (500, 500), 60, (200, 0, 0), (255, 0, 0), "../Resources/Fonts/RPGSystem.ttf", "GO")
    while True:
        py.event.pump()
        v.events = []
        v.events = py.event.get()
        v.screen.fill((200, 200, 200))
        tinps.update()
        texts.update()
        button.update()
        for event in v.events:
            if event.type == py.MOUSEBUTTONDOWN:
                if button.pressed():
                    for t in tinps:
                        if t.num == 1:
                            v.selectedEnemy["Name"] = t.outText
                        if t.num == 2:
                            v.selectedEnemy["Attack"] = t.outText
                        if t.num == 3:
                            v.selectedEnemy["Health"] = t.outText
                        if t.num == 4:
                            v.selectedEnemy["Speed"] = t.outText
                    py.time.delay(200)
                    return
        py.display.flip()
        
        
class npcImageButton(py.sprite.Sprite):
    
    def __init__(self, drb):
        super().__init__()
        from os import listdir
        self.images = []
        for i in listdir("../Resources/Images/NpcSkins/Spritesheets"):
            self.images.append("../Resources/Images/NpcSkins/Spritesheets/" + i)
        
        self.x = 400
        self.y = 100
        self.selected = self.images[0]
        self.drb = drb
        
    def update(self):
        direction = 7
        if self.drb.outText == "Down":
            direction = 7
        if self.drb.outText == "Up":
            direction = 1
        if self.drb.outText == "Left":
            direction = 10
        if self.drb.outText == "Right":
            direction = 4
        image = mapMenuItems.SpriteSheet(self.selected, 4, 3).images[direction]
        image = py.transform.scale(image, (96, 128))
        rect = image.get_rect()
        rect.center = (self.x, self.y)
        if rect.collidepoint(py.mouse.get_pos()):
            py.draw.rect(v.screen, (255, 255, 0), rect)
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    self.selected = changeNpcImage()
        else:
            py.draw.rect(v.screen, (255, 255, 255), rect)
        py.draw.rect(v.screen, (200, 100, 100), rect, 2)
        v.screen.blit(image, rect)
    
class npcFaceButton(py.sprite.Sprite):
    
    def __init__(self):
        super().__init__()
        from os import listdir
        self.images = []
        for i in listdir("../Resources/Images/NpcSkins/Faces"):
            self.images.append("../Resources/Images/NpcSkins/Faces/" + i)
        
        self.x = 520
        self.y = 100
        self.selected = self.images[0]
        
    def update(self):
        image = py.image.load(self.selected)
        image = py.transform.scale(image, (96, 96))
        rect = image.get_rect()
        rect.center = (self.x, self.y)
        if rect.collidepoint(py.mouse.get_pos()):
            py.draw.rect(v.screen, (255, 255, 0), rect)
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    self.selected = changeNpcFace()
        else:
            py.draw.rect(v.screen, (255, 255, 255), rect)
        py.draw.rect(v.screen, (200, 100, 100), rect, 2)
        v.screen.blit(image, rect)

def createNPC():
    
    bar = mapMenuItems.scrollBar(910, 10, 610, 10)
    
    texts = py.sprite.Group()
    
    ni = mapMenuItems.textInput((350, 200), 30, 16, 1, button=None, default=[], type="str")
    texts.add(mapMenuItems.textLabel("NPC Name:", (150, 210), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    fi = mapMenuItems.textInput((450, 260), 30, 2, 2, button=None, default=[], type="int")
    texts.add(mapMenuItems.textLabel("Base Friendliness:", (150, 270), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    arb = mapMenuItems.radioButtons(350, 330, ["Good", "Evil"])
    texts.add(mapMenuItems.textLabel("Alignment:", (150, 330), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    drb = mapMenuItems.radioButtons(350, 390, ["Up", "Down", "Left", "Right"])
    texts.add(mapMenuItems.textLabel("Direction:", (150, 390), (0, 0, 0), "../Resources/Fonts/RPGSystem.ttf", 40, variable=False, centred=False))
    
    buttons = py.sprite.Group()
    buttons.add(mapMenuItems.button("Done", (800, 550), 60, (200, 0, 200), (255, 50, 255), "../Resources/Fonts/RPGSystem.ttf", "done"))
    buttons.add(mapMenuItems.button("Add Conversation", (460, 500), 60, (200, 200, 100), (100, 200, 200), "../Resources/Fonts/RPGSystem.ttf", "convo", centred=True))
    
    imageButton = npcImageButton(drb)
    faceButton = npcFaceButton()
    while True:
        v.screen.fill((220, 220, 220))
        v.events = []
        v.events = py.event.get()
        imageButton.update()
        faceButton.update()
        bar.update()
        texts.update()
        arb.update()
        drb.update()
        ni.update()
        fi.update()
        buttons.update()
        for event in v.events:
            if event.type == py.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.pressed():
                        if button.ID == "done":
                            v.selectedNPC = {"Image": imageButton.selected, "Name": ni.outText, "Alignment": arb.outText, "Base Like": fi.outText, "Direction": drb.outText}
                            print(v.selectedNPC)
                            return  
                        if button.ID == "convo":
                            chatEdit()
        
        py.display.flip()

class npcImage(py.sprite.Sprite):
    
    def __init__(self, image, num, face=False):
        print(num)
        super().__init__()
        self.image = image
        self.num = num
        self.face = face
        
        if num % 5 == 1:
            self.posx = 200
        if num % 5 == 2:
            self.posx = 300
        if num % 5 == 3:
            self.posx = 400
        if num % 5 == 4:
            self.posx = 500
        if num % 5 == 0:
            self.posx = 600
        
        self.posy = (int((num / 5)  - 0.1) * 70) + 50
    
    def update(self):
        if self.face:
            image = py.image.load(self.image)
            image = py.transform.scale(image, (96, 96))
        else:
            image = mapMenuItems.SpriteSheet(self.image, 4, 3).images[7]
            image = py.transform.scale(image, (48, 64))
        rect = image.get_rect()
        rect.topleft = (self.posx, self.posy)
        py.draw.rect(v.screen, (150, 150, 200), rect)
        v.screen.blit(image, (self.posx, self.posy))
        if rect.collidepoint(py.mouse.get_pos()):
            py.draw.rect(v.screen, (255, 255, 0), rect, 3)
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    return self.image
        else:
            py.draw.rect(v.screen, (255, 165, 0), rect, 3)

def changeNpcImage():
    from os import listdir
    images = py.sprite.Group()
    num = 1
    for i in listdir("../Resources/Images/NpcSkins/Spritesheets"):
        images.add(npcImage("../Resources/Images/NpcSkins/Spritesheets/" + i, num))
        num += 1
    
    while True:
        v.screen.fill((220, 220, 220))
        v.events = []
        v.events = py.event.get()
        for i in images:
            r = i.update()
            if r != None:
                return r
        py.display.flip()

def changeNpcFace():
    from os import listdir
    images = py.sprite.Group()
    num = 1
    for i in listdir("../Resources/Images/NpcSkins/Faces"):
        images.add(npcImage("../Resources/Images/NpcSkins/Faces/" + i, num, face=True))
        num += 1
    
    while True:
        v.screen.fill((220, 220, 220))
        v.events = []
        v.events = py.event.get()
        for i in images:
            r = i.update()
            if r != None:
                return r
        py.display.flip()

class editChunk(py.sprite.Sprite):
    
    def __init__(self, c_message="", c_goto = "", c_id = "", c_charisma = "", c_buttons = [], c_changelike = "", c_end = ""):
        super().__init__()
        
        self.created = False
        
        self.c_message = c_message
        self.c_goto = c_goto
        self.c_id = c_id
        self.c_charisma = c_charisma
        self.c_buttons = c_buttons
        self.c_changelike = c_changelike
        self.c_end = c_end
        
        self.posx = 210
        self.posy = 50
        self.rect = py.Rect(self.posx, self.posy, 500, 150)
    
        self.tinps = py.sprite.Group()
        self.texts = py.sprite.Group()
        
        self.texts.add(mapMenuItems.textLabel("ID:", (self.posx + 20, self.posy + 20), (0, 0, 0), None, 25))
        self.tinps.add(mapMenuItems.textInput((self.posx + 10, self.posy + 40), 25, 2, 1, button=None, default=list(self.c_id), type="int", fontfile=None))
        
        self.texts.add(mapMenuItems.textLabel("Message: (Lines are conjoined with no space)", (self.posx + 20, self.posy + 80), (0, 0, 0), None, 25))
        self.tinps.add(mapMenuItems.textInput((self.posx + 10, self.posy + 100), 15, 50, 2, button=None, default=list(self.c_message[:len(self.c_message)//2]), type="str", fontfile=None))
        self.tinps.add(mapMenuItems.textInput((self.posx + 10, self.posy + 120), 15, 50, 3, button=None, default=list(self.c_message[len(self.c_message)//2:]), type="str", fontfile=None))
        
        self.texts.add(mapMenuItems.textLabel("Goto:", (self.posx + 80, self.posy + 20), (0, 0, 0), None, 25))
        self.tinps.add(mapMenuItems.textInput((self.posx + 80, self.posy + 40), 25, 2, 4, button=None, default=list(self.c_goto), type="int", fontfile=None))
        
        self.texts.add(mapMenuItems.textLabel("Charisma", (self.posx + 160, self.posy + 5), (0, 0, 0), None, 20))
        self.texts.add(mapMenuItems.textLabel("Needed:", (self.posx + 160, self.posy + 20), (0, 0, 0), None, 20))
        self.tinps.add(mapMenuItems.textInput((self.posx + 160, self.posy + 40), 25, 2, 5, button=None, default=list(self.c_charisma), type="int", fontfile=None))
        
        self.texts.add(mapMenuItems.textLabel("Change", (self.posx + 240, self.posy + 5), (0, 0, 0), None, 20))
        self.texts.add(mapMenuItems.textLabel("Friendliness:", (self.posx + 240, self.posy + 20), (0, 0, 0), None, 20))
        self.tinps.add(mapMenuItems.textInput((self.posx + 240, self.posy + 40), 25, 2, 6, button=None, default=list(self.c_changelike), type="int", fontfile=None))
    
        self.texts.add(mapMenuItems.textLabel("End:", (self.posx + 330, self.posy + 20), (0, 0, 0), None, 25))
        self.tinps.add(mapMenuItems.textInput((self.posx + 330, self.posy + 40), 25, 2, 7, button=None, default=list(self.c_end), type="int", fontfile=None))
    
        self.Btexts = py.sprite.Group()
        self.Btinps = py.sprite.Group()
    
        self.Bselect = py.sprite.Group()
        if len(self.c_buttons) == 0:
            self.c_buttons.append({})
        for i in range(len(self.c_buttons)):
            self.Bselect.add(self.button(i, self))
        
        self.editButton = None
        
        self.buttonGo = mapMenuItems.button("Save", (570, 60), 80, (100, 100, 100), (150, 150, 150), None, "save", centred=False, bsize=(130, 80), centretext=True)
    
    
    def update(self):
        self.rect = py.Rect(self.posx, self.posy, 500, 150)
        
        py.draw.rect(v.screen, (200, 200, 200), self.rect)
        
        py.draw.rect(v.screen, (200, 200, 200), (self.rect[0] - 160, self.rect[1], 150, 150))
        if self.editButton == None:
            self.tinps.update()
            self.texts.update()
        else:
            self.Btexts.update()
            self.Btinps.update()
            self.buttonGo.update()
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    if self.buttonGo.pressed():
                        for inp in self.Btinps:
                            if inp.num == 1:
                                self.c_buttons[self.editButton]["ID"] = inp.outText
                            if inp.num == 2:
                                self.c_buttons[self.editButton]["Text"] = inp.outText
                        if self.editButton + 1 == len(self.c_buttons) and len(self.c_buttons) < 4:
                            self.c_buttons.append({})
                            self.Bselect.add(self.button(len(self.c_buttons) - 1, self))
                        self.editButton = None
        self.Bselect.update()
        
        done = 0
        for inp in self.tinps:
            if inp.num == 1:
                if inp.outText != "":
                    done += 1
            if inp.num == 2:
                if inp.outText != "":
                    done += 1
            if inp.num == 4:
                for inp2 in self.tinps:
                    if inp2.num == 1:
                        if inp.outText != inp2.outText:
                            done += 1
        if done >= 3:
            self.created = True
    
    def save(self):
        self.created = True
        firstmsgnum = None
        for inp in self.tinps:
            if inp.num == 1:
                self.c_id = inp.outText
            if inp.num == 2:
                if firstmsgnum == None:
                    self.c_message = inp.outText
                    firstmsgnum = 2
                elif firstmsgnum == 3:
                    self.c_message = inp.outText + self.c_message
            if inp.num == 3:
                if firstmsgnum == None:
                    self.c_message = inp.outText
                    firstmsgnum = 3
                elif firstmsgnum == 2:
                    self.c_message = self.c_message + inp.outText
            if inp.num == 4:
                self.c_goto = inp.outText
            if inp.num == 5:
                self.c_charisma = inp.outText
            if inp.num == 6:
                self.c_changelike = inp.outText
            if inp.num == 7:
                self.c_end = inp.outText
    
    class button(py.sprite.Sprite):
        
        def __init__(self, num, master):
            super().__init__()
            self.num = num
            self.master = master
            self.rect = py.Rect(self.master.rect[0] - 150, self.master.rect[1] + 10 + num * 33.75, 130, 28.75)
            self.hovered = False
            font = py.font.Font(None, 30)
            self.text = font.render("Button " + str(num + 1), 1, (0, 0, 0))
            
        
        def update(self):
            if not self.hovered:
                py.draw.rect(v.screen, (150, 150, 150), self.rect)
            else:
                py.draw.rect(v.screen, (100, 100, 100), self.rect)
            
            if self.rect.collidepoint(py.mouse.get_pos()):
                self.hovered = True
            else:
                self.hovered = False
            
            v.screen.blit(self.text, (self.rect[0] + 20, self.rect[1] + 5))
            
            if self.hovered:
                for event in v.events:
                    if event.type == py.MOUSEBUTTONDOWN:
                        self.master.editButton = self.num
                        
                        if "Text" in self.master.c_buttons[self.num].keys():
                            print(self.master.c_buttons[self.num])
                            self.b_message = self.master.c_buttons[self.num]["Text"]
                            self.b_id = self.master.c_buttons[self.num]["ID"]
                        else:
                            self.b_id = ""
                            self.b_message = ""
                                                
                        self.master.Btexts = py.sprite.Group()
                        self.master.Btinps = py.sprite.Group()
                        
                        self.master.Btexts.add(mapMenuItems.textLabel("Goto:", (self.master.posx + 20, self.master.posy + 20), (0, 0, 0), None, 25))
                        self.master.Btinps.add(mapMenuItems.textInput((self.master.posx + 10, self.master.posy + 40), 25, 2, 1, button=None, default=list(self.b_id), type="int", fontfile=None))
                    
                        self.master.Btexts.add(mapMenuItems.textLabel("Text:", (self.master.posx + 20, self.master.posy + 80), (0, 0, 0), None, 25))
                        self.master.Btinps.add(mapMenuItems.textInput((self.master.posx + 10, self.master.posy + 100), 15, 50, 2, button=None, default=list(self.b_message), type="str", fontfile=None))
            

class chatChunk(py.sprite.Sprite):
    
    def __init__(self, c_message, c_id, c_goto = None, c_charisma = None, c_buttons = None, c_changelike = None, c_end = None):
        super().__init__()
        
        self.c_message = c_message
        self.c_goto = c_goto
        self.c_id = c_id
        self.c_charisma = c_charisma
        self.c_buttons = c_buttons
        self.c_changelike = c_changelike
        self.c_end = c_end
        
        v.chunkIDs[str(self.c_id)].append(self)
        
        self.posx = 20 + int(self.c_id) * 300
        self.posy = 300 + v.chunkIDs[str(self.c_id)].index(self) * 60
        
        
        self.texts = py.sprite.Group()
        
        self.texts.add(mapMenuItems.textLabel("Goto", (self.posx + 15, self.posy + 2), (10, 10, 10), None, 20))
        self.texts.add(mapMenuItems.textLabel(self.c_goto, (self.posx + 10, self.posy + 13), (10, 10, 10), None, 60))
        if self.c_goto == "":
            self.texts.add(mapMenuItems.textLabel("---", (self.posx + 20, self.posy + 25), (10, 10, 10), None, 30))

        
        self.texts.add(mapMenuItems.textLabel("Charisma", (self.posx + 65, self.posy + 2), (10, 10, 10), None, 20))
        self.texts.add(mapMenuItems.textLabel("Needed", (self.posx + 65, self.posy + 15), (10, 10, 10), None, 15))
        self.texts.add(mapMenuItems.textLabel("Added", (self.posx + 105, self.posy + 15), (10, 10, 10), None, 15))
        
        if not self.c_charisma == "":
            self.texts.add(mapMenuItems.textLabel(">" + str(self.c_charisma), (self.posx + 60, self.posy + 25), (10, 10, 10), None, 40))
        else:
            self.texts.add(mapMenuItems.textLabel("---", (self.posx + 70, self.posy + 25), (10, 10, 10), None, 30))
        if not self.c_changelike == "":
            plusminus = lambda i: ("+" if int(i) > 0 else "") + str(i) if type(i) == int else str(i)
            self.texts.add(mapMenuItems.textLabel(plusminus(self.c_charisma), (self.posx + 100, self.posy + 25), (10, 10, 10), None, 40))
        else:
            self.texts.add(mapMenuItems.textLabel("---", (self.posx + 110, self.posy + 25), (10, 10, 10), None, 30))
        
        self.texts.add(mapMenuItems.textLabel("End", (self.posx + 150, self.posy + 2), (10, 10, 10), None, 20))
        
        if not self.c_end == "":
            self.texts.add(mapMenuItems.textLabel(self.c_end, (self.posx + 155, self.posy + 13), (10, 10, 10), None, 60))
        else:
            self.texts.add(mapMenuItems.textLabel("---", (self.posx + 155, self.posy + 25), (10, 10, 10), None, 30))
        
        self.buttons = py.sprite.Group()
        for i in range(len(self.c_buttons)):
            self.buttons.add(self.cButton(i, self.c_buttons[i], self.rect.topleft))
        
        self.hovered = False
        
    def update(self):
        self.posx = 20 + int(self.c_id) * 300
        self.posy = 300 + v.chunkIDs[str(self.c_id)].index(self) * 60
        self.rect = py.Rect(self.posx, self.posy, 200, 50)
        if self.hovered:
            self.rect.height += 50
        if self.rect.collidepoint(py.mouse.get_pos()):
            self.hovered = True
        else:
            self.hovered = False

        if self.c_goto != "":
            if int(self.c_goto) > int(self.c_id):
                line = 0
                endmod = 0
            if int(self.c_goto) < int(self.c_id):
                line = 200
                endmod = 0
            if int(self.c_goto) == int(self.c_id):
                line = 0
                
            end = int(self.c_goto) * 300 + line + endmod + 20
            
            
            for chunk in v.chunks:
                if chunk.c_id == self.c_goto:
                    poy = chunk.posy
                    py.draw.line(v.screen, (180, 180, 180), (self.posx + (200 - line), self.posy + 25), (end, poy + 25), 4)
                    py.draw.circle(v.screen, (180, 180, 180), (end, poy + 25), 5)
            
            if self.hovered:
                for chunk in v.chunks:
                    if chunk.c_id == self.c_goto:
                        poy = chunk.posy
                        py.draw.line(v.screen, (255, 0, 0), (self.posx + (200 - line), self.posy + 25), (end, poy + 25), 4)
                        py.draw.circle(v.screen, (255, 0, 0), (end, poy + 25), 5)
        
        for chunk in v.chunks:
            if chunk.hovered:
                if chunk.c_id == self.c_goto:
                    poy = chunk.posy
                    py.draw.line(v.screen, (0, 0, 255), (self.posx + (200 - line), self.posy + 25), (end, poy + 25), 4)
                    #py.draw.circle(v.screen, (0, 0, 255), (self.posx + (200 - line), poy + 25), 5)
        if self.c_end != "":
            if self.hovered:
                for chunk in v.chunks:
                    if chunk.c_id == self.c_end:
                        if int(self.c_end) > int(self.c_id):
                            line = 0
                            endmod = 0
                        if int(self.c_end) < int(self.c_id):
                            line = 200
                            endmod = 0
                        if int(self.c_end) == int(self.c_id):
                            line = 0
                        end = int(self.c_end) * 300 + line + endmod + 20
                        
                        poy = chunk.posy
                        py.draw.line(v.screen, (255, 0, 255), (self.posx + (200 - line), self.posy + 15), (end, poy + 15), 4)
                        #py.draw.circle(v.screen, (0, 0, 255), (self.posx + (200 - line), poy + 25), 5)
        if self.hovered:
            py.draw.rect(v.screen, (175, 175, 175), self.rect)
            for event in v.events:
                if event.type == py.MOUSEBUTTONDOWN:
                    v.chatEdit = editChunk(self.c_message, self.c_goto, self.c_id, self.c_charisma, self.c_buttons, self.c_changelike, self.c_end)
                    v.chunks.remove(self)
            self.buttons.update()
        else:
            py.draw.rect(v.screen, (200, 200, 200), self.rect)
        self.texts.update()


    class cButton(py.sprite.Sprite):
        
        def __init__(self, num, data, pos):
            self.text = data["Text"]
            self.ID = data["ID"]
            font = py.font.Font(None, 15)
            self.idRend = font.render(str(self.ID), 1, (0, 0, 0))
            self.rect = py.Rect(pos[0] + 5, pos[1] + 50, 40, 20)
            self.rect.x += (num % 2) * 45
            self.rect.y += int(num / 2) * 25
            self.hovered = False
        
        def update(self):
            if self.hovered:
                py.draw.rect(v.screen, (150, 150, 150), self.rect)
            else:
                py.draw.rect(v.screen, (100, 100, 100), self.rect)
            size = self.idRend.get_rect().size
            v.screen.blit(self.idRend, (self.rect.x - size[0]/2, self.rect.y - size[1]/2))
            if self.rect.collidepoint(py.mouse.get_pos()):
                self.hovered = True
            if self.hovered:
                py.draw.rect(v.screen, (100, 100, 100), (self.rect[0], self.rect[1] + 20, 40, 40))
        
        
        


def chatEdit():
    v.chunks = py.sprite.Group()
    v.chunkIDs['0'] = []
    v.chunkIDs['1'] = []
    v.chunkIDs['2'] = []
    
    v.chatEdit = editChunk()
    buttons = py.sprite.Group()
    buttons.add(mapMenuItems.button("ADD", (720, 50), 100, (150, 150, 150), (200, 200, 200), None, "add", bsize=(150, 150), centretext=True))
    
    texts = py.sprite.Group()
    texts.add(mapMenuItems.textLabel("ID:", (5, 250), (0, 0, 0), None, 40))

    boxes = py.sprite.Group()
    boxes.add(box(0))
    boxes.add(box(1))
    boxes.add(box(2))
         
    
    while True:
        v.screen.fill((250, 250, 250))
        v.events = []
        v.events = py.event.get()
        
        v.chunks.update()
        for ch in v.chunks:
            if ch.hovered:
                ch.update()
        v.chatEdit.update()
        buttons.update()
        texts.update()
        boxes.update()
        
        py.draw.line(v.screen, (0, 0, 0), (0, 290), (920, 290), 2)
        py.draw.line(v.screen, (0, 0, 0), (270, 290), (270, 630), 2)
        py.draw.line(v.screen, (0, 0, 0), (570, 290), (570, 630), 2)
        
        for event in v.events:
            if event.type == py.MOUSEBUTTONDOWN:
                for button in buttons:
                    if button.pressed():
                        if button.ID == "add":
                            if v.chatEdit.created == True:
                                v.chatEdit.save()
                                v.chunks.add(chatChunk(v.chatEdit.c_message, v.chatEdit.c_id, v.chatEdit.c_goto, v.chatEdit.c_charisma, v.chatEdit.c_buttons, v.chatEdit.c_changelike, v.chatEdit.c_end))
                                v.chatEdit = editChunk()
        py.display.flip()
        

class box(py.sprite.Sprite):
    
    def __init__(self, num):
        super().__init__()
        self.num = num

    def update(self):
        colour = (0, 0, 0)
        if self.num == 0:
            self.rect = py.Rect(50, 245, 220, 45)
        else:
            self.rect = py.Rect((self.num * 300) - 30, 245, 300, 45)
        if self.rect.collidepoint(py.mouse.get_pos()):
            colour = (100, 0, 0)
        for chunk in v.chunks:
            if chunk.hovered:
                if chunk.c_goto == str(self.num):
                    colour = (255, 0, 0)
        
        mapMenuItems.textLabel(str(self.num), ((self.num * 300) + 120, 250), colour, None, 40).update()
        py.draw.rect(v.screen, colour, self.rect, 2)