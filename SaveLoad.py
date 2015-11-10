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
            "equipped": v.equipped
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
    v.playerPosX = save["playerPosX"]
    v.playerPosY = save["playerPosY"]
    v.playerDirection = save["playerDirection"]
    v.playerHealth = save["playerHealth"]
    v.playerMana = save["playerMana"]
    v.experience = save["experience"]
    v.xpMod = save["xpMod"]
    v.skillPoints = save["skillPoints"]
    v.appearance = save["appearance"]
    v.equipped = save["equipped"]
    
    savefile = open("Saves/Entities.save", "rb")
    save = pickle.load(savefile)
    
    for thing in save:
        print(thing)
        if thing["ID"] == "enemy":
            ne = entityClasses.Enemy(blank=True)
            print("create enemy")
            ne.load(thing)
        #n = entityClasses.Enemy(blank=True) # Create blank enemy here
        #n.load()


#Save()
#Load()