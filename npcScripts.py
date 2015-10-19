import pygame as py
import Variables as v
import MenuItems
import entityClasses


class conversation():
    
    def __init__(self, npc, material):
        self.material = material
        self.npc = npc
        self.npcName = npc.name
        self.npcIcon = py.transform.scale(npc.icon, (150, 150))
        self.place = material[0]
        self.speechOutput = None
        self.searchDone = False
    
    def say(self):
        v.PAUSED = True
        v.pauseType = "Conversation"

        if self.speechOutput == "Goto":
            self.searchDone = False
            self.searchTree(self.place["Goto"], self.material)
            self.speechOutput = None
        if self.speechOutput == "End":
            v.PAUSED = False
            self.speechOutput = None
        
        self.speech(self)
                
    def searchTree(self, target, tree={}):
        for value in tree:
            if value["ID"] == target:
                self.place = value
                return
            
        
    
    class speech():
        def __init__(self, master):
            #self.speechOutput = None
            self.message = master.place["Message"]
            self.master = master
            self.font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 25)
            line = []
            self.lines = []
            for word in self.message.split(" "):
                line.append(word)
                #print(word)
                if self.font.size(" ".join(line))[0] > 350:
                    line.remove(word)
                    self.lines.append(" ".join(line))
                    line = [word]
            self.lines.append(" ".join(line))
            
            v.conversationClass = self
            self.lineno = 0
            self.letterno = 0
            self.alphaCycle = 0
            self.alphaDirection = True
            
            self.buttons = py.sprite.Group()
            xmod = 0
            ymod = 0
            for key, value in self.master.place.items():
                if key[0] == "B":
                    self.buttons.add(MenuItems.Button(value["Text"], (220 + xmod, 200 + ymod), 40, (255, 255, 100), (153, 76, 0), "Resources/Fonts/RPGSystem.ttf", value["ID"], bsize=(190, 0)))
                    xmod += 210
                    if xmod >= 420:
                        xmod = 0
                        ymod += 50
            
            self.buts = True
            if len([k for k, v in self.master.place.items() if k[0] == "B"]) == 0:
                self.buts = False
                        
            
        
        def update(self):
            innerRect = py.Rect(220, 300, 400, 150)
            outerRect = py.Rect(218, 298, 404, 154)
            py.draw.rect(v.screen, py.Color(153, 76, 0), outerRect)
            py.draw.rect(v.screen, py.Color(255, 178, 102), innerRect)
            py.draw.rect(v.screen, (255, 178, 102), (50, 298, 150, 150))
            v.screen.blit(self.master.npcIcon, (50, 298))
            py.draw.rect(v.screen, (153, 76, 0), (50, 298, 150, 150), 2)
            py.draw.rect(v.screen, (0, 0, 0), (50, 248, 150, 50))
            py.draw.rect(v.screen, (153, 76, 0), (50, 248, 150, 50), 2)
            
            nameFont = py.font.Font("Resources/Fonts/RPGSystem.ttf", 35)
            label = nameFont.render(self.master.npcName, 1, (255, 255, 255))
            v.screen.blit(label, (125 - nameFont.size(self.master.npcName)[0]/2, 273 - nameFont.size(self.master.npcName)[1]/2))
            
            self.buttons.update()
            yadd = 0
            for line in range(len(self.lines)):
                if line <= self.lineno:
                    xadd = 0
                    for letter in range(len(self.lines[line])):
                        if letter <= self.letterno or self.lineno > line:
                            label = self.font.render(self.lines[line][letter], 1, (255, 255, 255))
                            v.screen.blit(label, (230 + xadd, 310 + yadd))
                            xadd += self.font.size(self.lines[line][letter])[0]
                            
                    yadd += self.font.size(self.lines[line][letter])[1]
                
            #print(self.lines)
            if self.letterno < len(self.lines[self.lineno]):
                self.letterno += 1
            else:
                if self.lineno < len(self.lines) - 1:
                    self.lineno += 1
                    self.letterno = 0
            #py.time.wait(10)
            if self.buts == False:
                label = self.font.render("Continue - F", 1, (255, 100, 255))
                label.fill((255, 255, 255, self.alphaCycle), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (480, 425))
            if self.alphaDirection:
                self.alphaCycle += 5
            else:
                self.alphaCycle -= 5
            
            if self.alphaCycle >= 250:
                self.alphaDirection = False
            if self.alphaCycle <= 100:
                self.alphaDirection = True
                
            
            for event in v.events:
                if event.type == py.KEYDOWN:
                    if self.buts == False:
                        if event.key == py.K_f:
                            v.conversationClass = None
                            if "Goto" in self.master.place:
                                self.master.speechOutput = "Goto"
                            else:
                                self.master.speechOutput = "End"
                            if not "End" in self.master.place:
                                self.master.say()
                            else:
                                v.PAUSED = False
                
                if event.type == py.MOUSEBUTTONDOWN:
                    if not len(self.buttons) == 0:
                        id = None
                        for but in self.buttons:
                            if but.rect.collidepoint(py.mouse.get_pos()):
                                id = but.ID
                        
                        if not id == None:
                            self.searchDone = False
                            self.master.searchTree(id, self.master.material)
                            self.master.say()
                        
def summon(npcType, pos):
    if npcType == "Guard":
        entityClasses.Enemy(pos[0], pos[1], "Resources/Images/GuardSheet.png", {"Name": "Guard Lvl. 100", "Health":100, "Attack":5})            