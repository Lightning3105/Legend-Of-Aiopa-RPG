import entityClasses
import spellClasses
import Variables as v

class weapon():
    
    def __init__(self, name, attType, image, attributes = {}):
        self.name = name
        self.attType = attType
        self.image = image
        self.attributes = attributes
        if self.attType == "swing":
            self.object = entityClasses.Sword(self.image, self)
        if self.attType == "manaOrb":
            self.object = entityClasses.manaOrb(self.image, self)
        if self.attType == "shoot":
            self.object = entityClasses.shooter(self.image, self)

class spell():
    
    def __init__(self, name, spellType, image, attributes = {}):
        self.name = name
        self.spellType = spellType
        self.image = image
        self.attributes = attributes
        if self.spellType == "beam":
            self.object = spellType.beam(self.image, self)