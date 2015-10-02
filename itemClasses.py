import entityClasses
import spellClasses
import weaponClasses
import Variables as v

class weapon():
    
    def __init__(self, name, icon, attType, image, attributes = {}):
        self.name = name
        self.attType = attType
        self.image = image
        self.attributes = attributes
        self.icon = icon
        self.equipType = "Weapon"
        if self.attType == "swing":
            self.object = weaponClasses.Sword(self.image, self)
        if self.attType == "manaOrb":
            self.object = weaponClasses.manaOrb(self.image, self)
        if self.attType == "shoot":
            self.object = weaponClasses.shooter(self.image, self)

class spell():
    
    def __init__(self, name, spellType, spellImage, castImage, attributes = {}): #TODO: icon
        self.name = name
        self.spellType = spellType
        self.spellImage = spellImage
        self.castImage = castImage
        self.attributes = attributes
        if self.spellType == "beam":
            self.object = spellClasses.beam(self.spellImage, self.castImage, self)
            v.equippedSpells.add(self.object)

class item():
    
    def __init__(self, name, icon):
        self.name = name
        self.icon = icon
        self.equipType = "Item"