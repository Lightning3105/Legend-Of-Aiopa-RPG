import pygame as py
import Variables as v
import MenuItems
import entityClasses


class conversation():
    
    def __init__(self, npc, material, place=None):
        self.material = material
        self.npc = npc
        self.npcName = npc.name
        self.npcIcon = py.transform.scale(npc.icon, (int(150 / 640 * v.screenX), int(150 / 640 * v.screenX)))
        if place == None:
            self.place = material[0]
        else:
            self.place = place
        self.speechOutput = None
        self.searchDone = False
    
    def getLike(self):
        return self.npc.baseLike + self.npc.like + v.Attributes["Charisma"]
    
    def say(self):
        v.PAUSED = True
        v.pauseType = "Conversation"

        if self.speechOutput == "Goto":
            self.searchDone = False
            self.searchTree(self.place["Goto"], self.getLike(), self.material)
            self.speechOutput = None
        if self.speechOutput == "End":
            v.PAUSED = False
            self.speechOutput = None
        
        self.speech(self)
                
    def searchTree(self, target, like, tree={}):
        bestChar = -1 * float("inf")
        bestCharVal = None
        for value in tree:
            if value["ID"] == target:
                if "Charisma" in list(value.keys()):
                    if value["Charisma"] <= like and value["Charisma"] > bestChar:
                        bestChar = value["Charisma"]
                        bestCharVal = value
                else:
                    if bestChar == -1 * float("inf"):
                        bestCharVal = value
        self.place = bestCharVal
        return bestCharVal
            
        
    
    class speech():
        def __init__(self, master):
            print("Like:", master.getLike())
            #self.speechOutput = None
            self.message = master.place["Message"]
            self.master = master
            self.font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(25 / 640 * v.screenX))
            line = []
            self.lines = []
            for word in self.message.split(" "):
                line.append(word)
                if self.font.size(" ".join(line))[0] > 350 / 640 * v.screenX:
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
                if key == "Buttons":
                    for but in value:
                        self.buttons.add(MenuItems.Button(but["Text"], (220 / 640 * v.screenX + xmod, 250 / 640 * v.screenX + ymod), 40 / 640 * v.screenX, (255, 255, 100), (153, 76, 0), "Resources/Fonts/RPGSystem.ttf", but["ID"], bsize=(190 / 640 * v.screenX, 0)))
                        xmod += 210 / 640 * v.screenX
                        if xmod >= 420 / 640 * v.screenX:
                            xmod = 0
                            ymod -= 50 / 640 * v.screenX
                if key == "Quest":
                    quest(value[0], value[1], value[2])
            
            self.buts = True
            if len([k for k, v in self.master.place.items() if k[0] == "B"]) == 0:
                self.buts = False
                        
            
        
        def update(self):
            innerRect = py.Rect(220 / 640 * v.screenX, 300 / 640 * v.screenX, 400 / 640 * v.screenX, 150 / 640 * v.screenX)
            outerRect = py.Rect(218 / 640 * v.screenX, 298 / 640 * v.screenX, 404 / 640 * v.screenX, 154 / 640 * v.screenX)
            py.draw.rect(v.screen, (153, 76, 0), outerRect)
            py.draw.rect(v.screen, (255, 178, 102), innerRect)
            py.draw.rect(v.screen, (255, 178, 102), (50 / 640 * v.screenX, 298 / 640 * v.screenX, 150 / 640 * v.screenX, 150 / 640 * v.screenX))
            v.screen.blit(self.master.npcIcon, (50 / 640 * v.screenX, 298 / 640 * v.screenX))
            py.draw.rect(v.screen, (153, 76, 0), (50 / 640 * v.screenX, 298 / 640 * v.screenX, 150 / 640 * v.screenX, 150 / 640 * v.screenX), 2)
            py.draw.rect(v.screen, (0, 0, 0), (50 / 640 * v.screenX, 248 / 640 * v.screenX, 150 / 640 * v.screenX, 50 / 640 * v.screenX))
            py.draw.rect(v.screen, (153, 76, 0), (50 / 640 * v.screenX, 248 / 640 * v.screenX, 150 / 640 * v.screenX, 50 / 640 * v.screenX), 2)
            
            nameFont = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(35 / 640 * v.screenX))
            label = nameFont.render(self.master.npcName, 1, (255, 255, 255))
            v.screen.blit(label, (125 / 640 * v.screenX - nameFont.size(self.master.npcName)[0]/2, 273 / 640 * v.screenX - nameFont.size(self.master.npcName)[1]/2))
            
            self.buttons.update()
            yadd = 0
            for line in range(len(self.lines)):
                if line <= self.lineno:
                    xadd = 0
                    for letter in range(len(self.lines[line])):
                        if letter <= self.letterno or self.lineno > line:
                            label = self.font.render(self.lines[line][letter], 1, (255, 255, 255))
                            v.screen.blit(label, (230 / 640 * v.screenX + xadd, 310 / 640 * v.screenX + yadd))
                            xadd += self.font.size(self.lines[line][letter])[0]
                            
                    yadd += self.font.size(self.lines[line][letter])[1]
                
            if self.letterno < len(self.lines[self.lineno]):
                self.letterno += 1
            else:
                if self.lineno < len(self.lines) - 1:
                    self.lineno += 1
                    self.letterno = 0
            if self.buts == False:
                label = self.font.render("Continue - F", 1, (255, 100, 255))
                label.fill((255, 255, 255, self.alphaCycle), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(label, (480 / 640 * v.screenX, 425 / 640 * v.screenX))
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
                            if "ChangeLike" in self.master.place:
                                self.master.npc.like += self.master.place["ChangeLike"]
                            if not "End" in self.master.place:
                                self.master.say()
                            else:
                                v.PAUSED = False
                
                if event.type == py.MOUSEBUTTONDOWN:
                    if not len(self.buttons) == 0:
                        id = None
                        for but in self.buttons:
                            if but.rect.collidepoint(v.mouse_pos):
                                id = but.ID
                        
                        if not id == None:
                            self.searchDone = False
                            self.master.searchTree(id, self.master.getLike(), self.master.material)
                            self.master.say()
                        
class quest(py.sprite.Sprite):
    
    def __init__(self, name, Type, data={}):
        super().__init__()
        self.name = name
        self.type = Type
        self.data = data
        self.counted = []
        self.progress = 0
        self.completed = False
        v.quests.add(self)
        if "Progress" in data:
            self.progress = int(data["Progress"])
        if "Counted" in data:
            self.counted = data["Counted"]
    
    def save(self):
        self.data["Progress"] = self.progress
        self.data["Counted"] = self.counted
        save = {"Name": self.name,
                "Type": self.type,
                "Data": self.data,
                "Counted": self.counted
                }
        
        return save
    
    def update(self):
        if self.type == "Kill":
            for enemy in v.dyingEnemies:
                if enemy.name == self.data["Name"]:
                    if not enemy.npcID in self.counted:
                        self.progress += 1
                        self.counted.append(enemy.npcID)
            if self.progress >= self.data["Amount"]:
                self.completed = True
        #print("Amount:", self.progress)
        #print("Completed?:", self.completed)


def summon(npcType, pos):
    if npcType == "Guard":
        entityClasses.Enemy(pos[0], pos[1], 1, "Resources/Images/EnemySkins/GuardSheet.png", {"Name": "Guard Lvl. 100", "Health":100, "Attack":5, "Speed":1.5})            