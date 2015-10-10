import pygame as py
from entityClasses import NPC


class conversation():
    
    def __init__(self, npc, material):
        self.material = material
        self.npc = npc
        self.npcName = npc.name
        self.npcIcon = npc.icon
    
    def say(self):
        pass