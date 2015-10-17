import Variables as v
import pickle
import entityClasses

def Save():
    savefile = open("Saves/Variables.save", "wb")
    
    save = {
            "Attributes": v.Attributes,
            "playerPosX": v.playerPosX,
            "playerPosY": v.playerPosY,
            "playerDirection": v.playerDirection,
            "playerHealth": v.playerHealth,
            "playerMana": v.playerMana,
            "experience": v.experience,
            "xpMod": v.xpMod,
            "skillPoints": v.skillPoints,
            "appearance": v.appearance,
            }
    
    pickle.dump(save, savefile)
    
    savefile = open("Saves/Entities.save", "wb")
    
    save = []
    
    for thing in v.allNpc:
        save.append(thing.save())
        
    pickle.dump(save, savefile)

def Load():
    savefile = open("Saves/Variables.save", "rb")
    save = pickle.load(savefile)
    v.Attributes = save["Attributes"]
    
    savefile = open("Saves/Entities.save", "wb")
    save = pickle.load(savefile)
    
    for thing in save:
        entityClasses.Enemy() # Create blank enemy here


Save()
Load()