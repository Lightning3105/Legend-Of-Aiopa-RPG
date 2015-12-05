import Variables as v
import pickle
import entityClasses
import itemClasses
import pygame as py
import guiClasses
import Map
import os
import npcScripts

def Save():
    global v
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
            "playerName": v.playerName,
            "mapNum" : v.mapNum,
            
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
    aSave = {}
    qSave = []
    
    for k, va in v.equipped.items():
        if va != None:
            eSave[k] = va.save()
    
    for item in v.inventory.contents:
        iSave.append(item.save())
    
    for k, item in v.abilities.items():
        if item != None:
            aSave[k] = item.save()
    
    for item in v.quests:
        qSave.append(item.save())
    
    save["eSave"] = eSave
    save["iSave"] = iSave
    save["aSave"] = aSave
    save["qSave"] = qSave
    pickle.dump(save, savefile)
    
    """for k, v in Map.Maps.items():
        saveMap(k)"""

def saveMap(mapNum):
    if not v.savedMap == None:
        current = pickle.loads(v.savedMap)
    else:
        current = {}
     
    current[mapNum] = []
    
    for thing in v.droppedItems:
        current[mapNum].append(thing.save())
    for thing in v.NPCs:
        current[mapNum].append(thing.save())
    
    v.savedMap = pickle.dumps(current)

def loadMap(mapNum):
    if not v.savedMap == None:
        save = pickle.loads(v.savedMap)
        if mapNum in save:
            save = save[mapNum]
            
            for thing in save:
                if thing["ID"] == "npc":
                    ne = entityClasses.NPC(blank=True)
                    ne.load(thing)
                if thing["ID"] == "dropped":
                    ne = entityClasses.droppedItem(blank=True)
                    ne.load(thing)

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
    v.playerName = save["playerName"]
    v.mapNum = save["mapNum"]
    
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

    print(save["aSave"])
    for k, item in save["aSave"].items():
        v.abilities[k] = itemClasses.spell(item["name"], item["spellType"], item["spellImage"], item["castImage"], item["icon"], item["attributes"])

    for item in save["qSave"]:
        npcScripts.quest(item["Name"], item["Type"], item["Data"])

#Save()
#Load()