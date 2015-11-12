import entityClasses
import spellClasses
import weaponClasses
import Variables as v
import pygame as py

class weapon():
    
    def __init__(self, name, icon, attType, image, attributes = {}):
        self.name = name
        self.attType = attType
        self.attributes = {"Damage": 0, "Knockback": 1, "InvulnMod": 1}
        self.attributes.update(attributes)
        self.image = image
        if type(icon) == list:
            self.icon = py.image.fromstring(icon[0], icon[1], 'RGBA')
        else:
            self.icon = icon
        self.equipType = "Weapon"
        if self.attType == "swing":
            self.object = weaponClasses.Sword(self.image, self)
        if self.attType == "manaOrb":
            self.object = weaponClasses.manaOrb(self.image, self)
        if self.attType == "shoot":
            self.object = weaponClasses.shooter(self.image, self)
    
    def save(self):
        save = {}
        save["name"] = self.name
        save["icon"] = [py.image.tostring(self.icon, 'RGBA'), self.icon.get_rect().size]
        save["attType"] = self.attType
        save["image"] = self.image
        save["attributes"] = self.attributes
        save["equipType"] = self.equipType
        return save
    

class spell():
    
    def __init__(self, name, spellType, spellImage, castImage, attributes = {}): #TODO: icon
        self.name = name
        self.spellType = spellType
        self.spellImage = spellImage
        self.castImage = castImage
        self.attributes = {"Damage": 0, "Knockback": 1, "InvulnMod": 1}
        self.attributes.update(attributes)
        if self.spellType == "beam":
            self.object = spellClasses.beam(self.spellImage, self.castImage, self)
            v.equippedSpells.add(self.object)
    
    def save(self):
        save = {}
        save["name"] = self.name
        save["spellType"] = self.spellType
        save["spellImage"] = self.spellImage
        save["castImage"] = self.castImage
        save["attributes"] = self.attributes
        return save

class item():
    
    def __init__(self, name, icon):
        self.name = name
        self.equipType = "Item"
        if type(icon) == list:
            self.icon = py.image.fromstring(icon[0], icon[1], 'RGBA')
        else:
            self.icon = icon
    
    def save(self):
        save = {}
        save["name"] = self.name
        save["equipType"] = self.equipType
        save["icon"] = [py.image.tostring(self.icon, 'RGBA'), self.icon.get_rect().size]
        return save