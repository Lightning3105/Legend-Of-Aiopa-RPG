import Variables as v
import pygame as py
import entityClasses
from random import randint
import MenuItems
from _ast import Num


class inventory():
    
    def __init__(self):
        self.size = 10
        self.contents = []
    
    def add(self, item):
        if not item == None:
            if not item in self.contents:
                self.contents.append(item)
                return True
        return False
    
    def remove(self, item):
        if item in self.contents:
            self.contents.remove(item)


class inventoryScreen():
    
    def __init__(self):
        self.grabbed = None
        self.grabbedOrigin = None
        self.hovering = None
        self.inventorySlots = py.sprite.Group()
        for i in range(0, 24):
            self.inventorySlots.add(self.inventorySlot(i, self))
        self.inventorySlots.add(self.discardSlot(self))
        self.equippedSlots = py.sprite.Group()
        self.equippedSlots.add(self.equippedSlot("Weapon", self))
        self.equippedSlots.add(self.equippedSlot("Helmet", self))
        self.equippedSlots.add(self.equippedSlot("Armour", self))
        self.equippedSlots.add(self.equippedSlot("Greaves", self))
        self.equippedSlots.add(self.equippedSlot("Boots", self))
        self.spellSlots = py.sprite.Group()
        for i in range(1, 7):
            self.spellSlots.add(self.spellSlot(i, self))
        self.attOptions = py.sprite.Group()
        AoX = 170
        for attribute in v.Attributes:
            self.attOptions.add(MenuItems.optionAttribute(AoX, attribute, 580, 0.8))
            AoX += 60
        
        self.attOptions.add(MenuItems.textLabel("Skill Points Remaining:", (576, 120), (100, 100, 100), "Resources/Fonts/RPGSystem.ttf", int(50)))
        self.attOptions.add(MenuItems.textLabel("skillPoints", (990, 120), (0, 255, 0), "Resources/Fonts/RPGSystem.ttf", int(50), True))
        
        self.quests = py.sprite.Group()
        n = 0
        for i in v.quests:
            self.quests.add(self.quest(n, i, self))
            n += 1
        
        self.openQuests = []
        
        self.tab = "Inventory"
        
        self.questScroll = 0
    
    def update(self):
        self.hovering = None
        self.grey()
        self.background()
        self.player()
        if self.tab == "Inventory":
            self.inventorySlots.update()
        if self.tab == "Attributes":
            self.attOptions.update()
        if self.tab == "Quests":
            self.openQuests = []
            for n in range(len(self.quests)):
                for i in self.quests:
                    if i.num == n:
                        i.update()
            self.scrollBar()
        
        self.tabs()
        self.equippedSlots.update()
        self.spellSlots.update()
        self.drag()
        if not self.hovering == None:
            if not self.hovering.item == None:
                if not self.grabbed == self.hovering.item:
                    font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
                    text = self.hovering.item.name
                    label = font.render(text, 1, (0, 0, 0))
                    Hrect = py.Rect(v.mouse_pos, font.size(text))
                    py.draw.rect(v.screen, (153, 76, 0), Hrect, 3)
                    py.draw.rect(v.screen, (255, 178, 102), Hrect)
                    v.screen.blit(label, Hrect)
    
    def save(self):
            for thing in self.inventorySlots:
                thing.save()
            for thing in self.equippedSlots:
                thing.save()
            for thing in self.spellSlots:
                thing.save()
    
    class quest(py.sprite.Sprite):
        
        def __init__(self, num, quest, master):
            super().__init__()
            self.num = num
            self.quest = quest
            self.master = master
            if self.quest.type == "Kill":
                self.image = py.image.load("Resources/Images/Inventory Icons/KillQuest.png").convert_alpha()
            
            self.image = py.transform.scale(self.image, (30, 30))
            font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
            self.titleLabel = font.render(self.quest.name, 1, (0, 0, 0))
            font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 20)
            self.progressLabel = font.render("Progress: " + str(self.quest.progress) + "/" + str(self.quest.data["Amount"]), 1, (0, 0, 0))
            self.open = False
            self.wait = False
        
        def update(self):
            ymod = 0
            num = self.num + self.master.questScroll
            if num > -1 and num < 5:
                for i in self.master.openQuests:
                    if i < num:
                        ymod += 30
                rect = py.Rect(280, 720 * 0.25 + (num * 60) + ymod, 250, 50)
                if self.open:
                    rect.height += 30
                if rect.collidepoint(v.mouse_pos):
                    c = (255, 255, 0)
                    if py.mouse.get_pressed()[0] and not self.wait:
                        self.open = not self.open
                        self.wait = True
                else:
                    c = (255, 178, 102)
                if not py.mouse.get_pressed()[0]:
                    self.wait = False
                
                py.draw.rect(v.screen, c, rect)
                py.draw.rect(v.screen, (153, 76, 0), rect, 2)
                v.screen.blit(self.image, (rect[0] + 5, rect[1] + 10))
                py.draw.rect(v.screen, (0, 0, 0), ((rect[0] + 5, rect[1] + 10), self.image.get_rect().size), 2)
                v.screen.blit(self.titleLabel, (rect[0] + 45, rect[1] + 10))
                if self.open:
                    v.screen.blit(self.progressLabel, (rect[0] + 45, rect[1] + 50))
                    self.master.openQuests.append(self.num)
            
    def scrollBar(self): #TODO: Add bar
        image = py.image.load("Resources/Images/Inventory Icons/Arrow.png").convert_alpha()
        image = py.transform.rotate(image, 180)
        rect = py.Rect(550, 90, 30, 30)
        image = py.transform.scale(image, rect.size)
        if self.questScroll > 0:
            if rect.collidepoint(v.mouse_pos):
                image.fill((255, 255, 0), special_flags=py.BLEND_RGB_MULT)
                image = py.transform.scale(image, (rect.width + 4, rect.height + 4))
                rect.height += 4
                rect.width += 4
                rect.centerx -= 2
                rect.centery -= 2
                for event in v.events:
                    if event.type == py.MOUSEBUTTONDOWN:
                        self.questScroll -= 1
                                       
        if self.questScroll <= 0:
            image.fill((100, 100, 100), special_flags=py.BLEND_RGB_MULT)
        v.screen.blit(image, rect)
        py.draw.rect(v.screen, (153, 76, 0), rect, 2)
        
        image = py.transform.rotate(image, 180)
        rect = py.Rect(550, 390, 30, 30)
        image = py.transform.scale(image, rect.size)
        if self.questScroll < len(v.quests) - 5:
            if rect.collidepoint(v.mouse_pos):
                image.fill((255, 255, 0), special_flags=py.BLEND_RGB_MULT)
                image = py.transform.scale(image, (rect.width + 4, rect.height + 4))
                rect.height += 4
                rect.width += 4
                rect.centerx -= 2
                rect.centery -= 2
                for event in v.events:
                    if event.type == py.MOUSEBUTTONDOWN:
                        self.questScroll += 1
        
        if self.questScroll > len(v.quests) - 5:
            image.fill((100, 100, 100), special_flags=py.BLEND_RGB_MULT)
        v.screen.blit(image, rect)
        py.draw.rect(v.screen, (153, 76, 0), rect, 2)
        
                
    def tabs(self):
        rect = py.Rect(560, 50, 160, 40)
        if rect.collidepoint(v.mouse_pos):
            c = (255, 255, 0)
            if py.mouse.get_pressed()[0]:
                self.tab = "Inventory"
        else:
            c = (255, 178, 102)
        if self.tab == "Inventory":
            o = (0, 0, 255)
        else:
            o = (153, 76, 0)
        py.draw.rect(v.screen, c, rect)
        py.draw.rect(v.screen, o, rect, 3)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
        label = font.render("Inventory", 1, (0, 0, 0))
        v.screen.blit(label, (rect[0] + 6, rect[1] + 3))
        
        
        rect = py.Rect(724, 50, 160, 40)
        if rect.collidepoint(v.mouse_pos):
            c = (255, 255, 0)
            if py.mouse.get_pressed()[0]:
                self.tab = "Attributes"
        else:
            c = (255, 178, 102)
        if self.tab == "Attributes":
            o = (0, 0, 255)
        else:
            o = (153, 76, 0)
        py.draw.rect(v.screen, c, rect)
        py.draw.rect(v.screen, o, rect, 3)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
        label = font.render("Attributes", 1, (0, 0, 0))
        v.screen.blit(label, (rect[0] + 6, rect[1] + 3))
        
        rect = py.Rect(888, 50, 160, 40)
        if rect.collidepoint(v.mouse_pos):
            c = (255, 255, 0)
            if py.mouse.get_pressed()[0]:
                self.tab = "Quests"
        else:
            c = (255, 178, 102)
        if self.tab == "Quests":
            o = (0, 0, 255)
        else:
            o = (153, 76, 0)
        py.draw.rect(v.screen, c, rect)
        py.draw.rect(v.screen, o, rect, 3)
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 30)
        label = font.render("Quests", 1, (0, 0, 0))
        v.screen.blit(label, (rect[0] + 6, rect[1] + 3))
    
    def grey(self):
        grey = py.Surface((v.screen.get_rect()[2], v.screen.get_rect()[3])).convert_alpha()
        grey.fill((20, 20, 20, 200))
        v.screen.blit(grey, (0, 0))
    
    def background(self):
        innerRect = py.Rect(200, 50, 880, 620)
        outerRect = py.Rect(190, 40, 900, 640)
        py.draw.rect(v.screen, (153, 76, 0), outerRect)
        py.draw.rect(v.screen, (255, 178, 102), innerRect)
    
    def player(self):
        pos = (300, 180)
        sheetImage = py.image.load(v.appearance["Body"]).convert_alpha()
        sheetImage.blit(py.image.load(v.appearance["Face"]), (0, 0))
        sheetImage.blit(py.image.load(v.appearance["Dress"]), (0, 0))
        sheetImage.blit(py.image.load(v.appearance["Hair"]), (0, 0))
        sheet = entityClasses.SpriteSheet(sheetImage, 4, 3)
        image = sheet.images[7]
        image = py.transform.scale(image, (image.get_rect().width * 7, image.get_rect().height * 7))
        v.screen.blit(image, pos)
    
    class equippedSlot(py.sprite.Sprite):
        
        def __init__(self, slot, master):
            super().__init__()
            self.hovered = False
            self.item = v.equipped[slot]
            self.size = (80, 80)
            self.master = master
            self.slot = slot
            self.equipType = slot
        
        def save(self):
            v.equipped[self.slot] = self.item
            v.inventory.remove(self.item)
            
        
        def update(self):
            if self.slot == "Weapon":
                self.pos = (220, 130)
                self.image = py.image.load("Resources/Images/Inventory Icons/Weapon.png").convert_alpha()
            if self.slot == "Helmet":
                self.pos = (460, 130)
                self.image = py.image.load("Resources/Images/Inventory Icons/Helmet.png").convert_alpha()
            if self.slot == "Armour":
                self.pos = (460, 220)
                self.image = py.image.load("Resources/Images/Inventory Icons/Breastplate.png").convert_alpha()
            if self.slot == "Greaves":
                self.pos = (460, 310)
                self.image = py.image.load("Resources/Images/Inventory Icons/Trousers.png").convert_alpha()
            if self.slot == "Boots":
                self.pos = (460, 400)
                self.image = py.image.load("Resources/Images/Inventory Icons/Boots.png").convert_alpha()
            image = py.transform.scale(self.image, self.size)
            rect = py.Rect(self.pos, self.size)
            py.draw.rect(v.screen, (255, 255, 255), rect, 3)
            if rect.collidepoint(v.mouse_pos):
                self.hovered = True
                self.master.hovering = self
            else:
                self.hovered = False
                image.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
            v.screen.blit(image, self.pos)
            
            if not self.item == None:
                icon = py.transform.scale(self.item.icon, (self.size[0] - 3, self.size[1] - 3))
                if self.master.grabbed == self.item:
                    icon.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(icon, self.pos)
                if self.hovered:
                    for event in v.events:
                        if event.type == py.MOUSEBUTTONDOWN:
                            self.master.grabbed = self.item
                            self.master.grabbedOrigin = self
        
    class spellSlot(py.sprite.Sprite):
        
        def __init__(self, num, master):
            super().__init__()
            self.size = (80, 80)
            self.hovered = False
            self.master = master
            try:
                self.item = v.abilities[str(num)]
            except KeyError:
                self.item = None
            self.equipType = "Spell"
            self.slotNum = num - 1
        
        def save(self):
            v.abilities[str(self.slotNum + 1)] = self.item
        
        def update(self):
            if self.item == None:
                image = py.image.load("Resources/Images/Inventory Icons/EmptySpell.png").convert_alpha()
            else:
                image = py.Surface(self.size).convert_alpha()
                image.fill((255, 255, 255))
            posx = 220 + (self.slotNum % 3) * 80
            posy = (int(self.slotNum / 3) * 80) + 490
            
            pos = (posx, posy)
            
            image = py.transform.scale(image, self.size)
            
            
            rect = py.Rect(pos, self.size)
            py.draw.rect(v.screen, (255, 255, 255), rect, 3)
            
            if rect.collidepoint(v.mouse_pos):
                self.hovered = True
                self.master.hovering = self
            else:
                self.hovered = False
                image.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
            v.screen.blit(image, pos)
            
            try:
                icon = py.transform.scale(py.image.load(self.item.icon).convert_alpha(), (self.size[0] - 4, self.size[1] - 4))
                icon.convert_alpha()
                if self.master.grabbed == self.item:
                    icon.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
                pos = (pos[0] + 3, pos[1] + 3)
                v.screen.blit(icon, pos)
                if self.hovered:
                    for event in v.events:
                        if event.type == py.MOUSEBUTTONDOWN:
                            self.master.grabbed = self.item
                            self.master.grabbedOrigin = self
            except:
                pass
            
            font = py.font.Font("Resources/Fonts/RPGSystem.ttf", 60)
            label = font.render(str(self.slotNum + 1), 1, (0, 0, 0))
            v.screen.blit(label, (pos[0] + 30, pos[1] + 15))
    
    
    class inventorySlot(py.sprite.Sprite):
        
        def __init__(self, slotNum, master):
            super().__init__()
            self.size = (80, 80)
            self.hovered = False
            self.slotNum = slotNum
            self.master = master
            try:
                self.item = v.inventory.contents[self.slotNum]
            except:
                self.item = None
            self.equipType = "Item"
        
        def save(self):
            v.inventory.add(self.item)
        
        def update(self):
            if self.item == None:
                image = py.image.load("Resources/Images/Inventory Icons/Empty.png").convert_alpha()
            else:
                image = py.Surface(self.size).convert_alpha()
                image.fill((255, 255, 255))
            posx = 570 + (self.slotNum % 6) * 80
            posy = (int(self.slotNum / 6) * 80) + 330
            
            pos = (posx, posy)
            
            image = py.transform.scale(image, self.size)
            
            
            rect = py.Rect(pos, self.size)
            py.draw.rect(v.screen, (255, 255, 255), rect, 3)
            
            if rect.collidepoint(v.mouse_pos):
                self.hovered = True
                self.master.hovering = self
            else:
                self.hovered = False
                image.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
            v.screen.blit(image, pos)
            
            try:
                icon = py.transform.scale(self.item.icon, (self.size[0] - 6, self.size[1] - 6))
                icon.convert_alpha()
                if self.master.grabbed == self.item:
                    icon.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
                v.screen.blit(icon, pos)
                if self.hovered:
                    for event in v.events:
                        if event.type == py.MOUSEBUTTONDOWN:
                            self.master.grabbed = self.item
                            self.master.grabbedOrigin = self
            except:
                pass
            
    class discardSlot(py.sprite.Sprite):
        
        def __init__(self, master):
            super().__init__()
            self.size = (80, 80)
            self.hovered = False
            self.master = master
            self.equipType = "Item"
            self.item = None
        
        def save(self):
            pass
        
        def update(self):
            image = py.image.load("Resources/Images/Inventory Icons/Discard.png").convert_alpha()
            
            posx = 490
            posy = 570
            
            pos = (posx, posy)
            image = py.transform.scale(image, self.size)
            
            rect = py.Rect(pos, self.size)
            py.draw.rect(v.screen, (255, 0, 0), rect, 3)
            
            if rect.collidepoint(v.mouse_pos):
                self.hovered = True
                self.master.hovering = self
                image.fill((200, 0, 0), special_flags=py.BLEND_RGBA_MULT)
            else:
                self.hovered = False
                image.fill((255, 255, 255, 100), special_flags=py.BLEND_RGBA_MULT)
            v.screen.blit(image, pos)
            if not self.item == None:
                v.inventory.remove(self.item)
                entityClasses.droppedItem(self.item, (v.playerPosX + randint(-5, 5), v.playerPosY + randint(-5, 5)))
                self.item = None
        
    def drag(self):
        if not self.grabbed == None:
            size = (80, 80)
            if type(self.grabbed.icon) == str:
                image = py.image.load(self.grabbed.icon).convert_alpha()
            else:
                image = self.grabbed.icon
            image = py.transform.scale(image, size)
            pos = v.mouse_pos
            v.screen.blit(image, pos)
            rect = py.Rect(pos, size)
            py.draw.rect(v.screen, (200, 200, 200), rect, 3)
            for event in v.events:
                if event.type == py.MOUSEBUTTONUP:
                    if not self.hovering == None:
                        if self.grabbed.equipType == self.hovering.equipType or self.hovering.equipType == "Item" and self.grabbed.equipType != "Spell":
                            old = self.grabbed
                            self.grabbedOrigin.item = self.hovering.item
                            self.hovering.item = old
                            self.grabbed = None
            if not py.mouse.get_pressed()[0]:
                self.grabbed = None
                self.grabbedOrigin = None
                                       
        
