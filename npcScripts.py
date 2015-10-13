import pygame as py
import Variables as v


class conversation():
    
    def __init__(self, npc, material):
        self.material = material
        self.npc = npc
        self.npcName = npc.name
        self.npcIcon = npc.icon
        self.place = material["O1"]
        self.speechOutput = None
        self.searchDone = False
    
    def say(self):
        v.PAUSED = True
        v.pauseType = "Conversation"
        print(self.speechOutput)
        if self.speechOutput == "Next":
            self.place = self.place["Next"]
            self.speechOutput = None
        if self.speechOutput == "Goto":
            self.searchDone = False
            self.searchTree(self.material)
            print("DONE SEARCHING!!!!!!!!!!!!!")
            self.speechOutput = None
        if self.speechOutput == "End":
            v.PAUSED = False
            self.speechOutput = None
        
        self.speech(self.place["Message"], self)
                
    def searchTree(self, tree={}):
        print("BEGIN#####")
        print(tree)
        print(type(tree))
        for key, value in tree.items():
            print("LOOP~~~~~~")
            print(key, value)
            if self.searchDone:
                return
            if key == "ID":
                if value == self.place["Goto"]:
                    self.place = tree
                    print("DONE")
                    self.searchDone = True
                    return
            if key[0] == "O":
                self.searchTree(value)
            
        
    
    class speech():
        def __init__(self, message, master):
            #self.speechOutput = None
            self.message = message
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
            
        
        def update(self):
            innerRect = py.Rect(100, 300, 400, 150)
            outerRect = py.Rect(98, 298, 404, 154)
            py.draw.rect(v.screen, py.Color(153, 76, 0), outerRect)
            py.draw.rect(v.screen, py.Color(255, 178, 102), innerRect)
            yadd = 0
            for line in range(len(self.lines)):
                if line <= self.lineno:
                    xadd = 0
                    for letter in range(len(self.lines[line])):
                        if letter <= self.letterno or self.lineno > line:
                            label = self.font.render(self.lines[line][letter], 1, (255, 255, 255))
                            v.screen.blit(label, (110 + xadd, 310 + yadd))
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
            label = self.font.render("Continue - F", 1, (255, 100, 255))
            label.fill((255, 255, 255, self.alphaCycle), special_flags=py.BLEND_RGBA_MULT)
            v.screen.blit(label, (380, 425))
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
                    if event.key == py.K_f:
                        v.conversationClass = None
                        if "Next" in self.master.place:
                            self.master.speechOutput = "Next"
                        elif "Goto" in self.master.place:
                            self.master.speechOutput = "Goto"
                        else:
                            self.mater.speechOutput = "End"
                        if not "End" in self.master.place:
                            self.master.say()
                        else:
                            v.PAUSED = False
            