import pygame as py
import Variables as v


class conversation():
    
    def __init__(self, npc, material):
        self.material = material
        self.npc = npc
        self.npcName = npc.name
        self.npcIcon = npc.icon
        self.place = material
    
    def say(self):
        self.speech(self.place["Message"], self)
        v.PAUSED = True
        v.pauseType = "Conversation"
        
    
    class speech():
        def __init__(self, message, master):
            self.message = message
            self.master = master
            self.font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 20)
            line = []
            self.lines = []
            for word in self.message.split(" "):
                line.append(word)
                print(line)
                print(self.lines)
                if self.font.size(" ".join(line))[0] > 200:
                    line.remove(word)
                    self.lines.append(" ".join(line))
                    line = [word]
            
            v.conversationClass = self
            
        
        def update(self):
            innerRect = py.Rect(100, 300, 400, 150)
            outerRect = py.Rect(98, 298, 404, 154)
            py.draw.rect(v.screen, py.Color(153, 76, 0), outerRect)
            py.draw.rect(v.screen, py.Color(255, 178, 102), innerRect)
            add = 0
            for line in self.lines:
                label = self.font.render(" ".join(line), 1, (255, 255, 255))
                v.screen.blit(label, (110, 310 + add))
                add += 20
            
            for event in v.events:
                if event.type == py.KEYDOWN:
                    if event.key == py.K_f:
                        v.conversationClass = None
                        try:
                            self.master.place = self.master.place["Next"]
                            self.master.say()
                        except:
                            v.PAUSED = False
            