import entityClasses
import Variables as v

class weapon():
    
    def __init__(self, name, attType, image):
        self.name = name
        self.attType = attType
        self.image = image
        if self.attType == "Swing":
            self.object = entityClasses.Sword(self.image)
        if self.attType == "manaOrb":
            self.object = entityClasses.manaOrb(self.image)
