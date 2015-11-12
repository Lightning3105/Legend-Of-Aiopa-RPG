import Variables as v
import pickle
import entityClasses
import itemClasses
import pygame as py
import guiClasses

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
    
    savefile = open("Saves/Inventory.save", "wb")
    
    save = {}
    eSave = {}
    iSave = []
    aSave = []
    
    for k, va in v.equipped.items():
        eSave[k] = va.save()
    
    for item in v.inventory.contents:
        iSave.append(item.save())
    
    for item in v.abilityButtons:
        aSave.append(item.save())
    
    save["eSave"] = eSave
    save["iSave"] = iSave
    save["aSave"] = aSave
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
    
    savefile = open("Saves/Entities.save", "rb")
    save = pickle.load(savefile)
    
    for thing in save:
        if thing["ID"] == "enemy":
            ne = entityClasses.Enemy(blank=True)
            ne.load(thing)
        if thing["ID"] == "npc":
            ne = entityClasses.NPC(blank=True)
            ne.load(thing)
    
    savefile = open("Saves/Inventory.save", "rb")
    save = pickle.load(savefile)
    
    for k, va in save["eSave"].items():
        if k == "Weapon":
            v.equipped[k] = itemClasses.weapon(va["name"], va["icon"], va["attType"], va["image"], va["attributes"])
    
    for item in save["iSave"]:
        if item["equipType"] == "Item":
            v.inventory.contents.append(itemClasses.item(item["name"], item["icon"]))
        if item["equipType"] == "Weapon":
            v.inventory.contents.append(itemClasses.weapon(item["name"], item["icon"], item["attType"], item["image"], item["attributes"]))

    for item in save["aSave"]:
        spell = itemClasses.spell(item["ability"]["name"], item["ability"]["spellType"], item["ability"]["spellImage"], item["ability"]["castImage"], item["ability"]["attributes"])
        v.abilityButtons.add(guiClasses.ability(spell, item["icon"], item["num"]))
#Save()
#Load()