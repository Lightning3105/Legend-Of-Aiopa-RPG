import Variables as v
import pickle
import entityClasses
import itemClasses
import pygame as py
import guiClasses
import Map
import os
import npcScripts
import urllib
import hashlib
import requests
import MenuItems

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
    print("LOADED:", save)
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

def getAccount(username, password):
    page = urllib.request.urlopen(v.url + "accounts/")
    accounts = page.read()
    accounts = pickle.loads(accounts)
    
    for un, vals in accounts.items():
        if un == username:
            hash_object = hashlib.md5(password.encode())
            hash = hash_object.hexdigest()
            if hash == vals["password"]:
                return vals
            else:
                return "PASSWORD"
    return "USERNAME"

def uploadSave():
    MenuItems.shiftingGradient((0, 0, 'x')).draw()
    MenuItems.textLabel("Uploading Save", (v.screenX * 0.5, v.screenY * 0.5), (255, 255, 255), "Resources/Fonts/RPGSystem.ttf", int(30/640 * v.screenX), variable=False, centred=True).update()  
    py.display.flip()
    import json
    url = v.url + "senddata/"
    save = {}
    with open("Saves/Entities.save", "rb") as s:
        d = s.read()
        save["Entities"] = d
    with open("Saves/Inventory.save", "rb") as s:
        d = s.read()
        save["Inventory"] = d
    with open("Saves/Variables.save", "rb") as s:
        d = s.read()
        save["Variables"] = d
        xp = pickle.loads(d)["experience"]["Total"]
    
    payload = {'username': v.username, 'password': v.password, 'save': "save", 'xp': xp}

    jpayload = json.dumps(str(payload))

    # GET
    #r = requests.get(url)

    # GET with params in URL
    #r = requests.get(url, params=payload)
    
    # POST with form-encoded data
    #r = requests.post(url, data=payload)
    
    # POST with JSON 
    
    r = requests.post(url, data=jpayload)
    
    # Response, status etc
    #print(r.text)
    print(r.status_code)

def downloadSave(): #TODO: test this
    MenuItems.shiftingGradient((0, 0, 'x')).draw()
    MenuItems.textLabel("Downloading Save", (v.screenX * 0.5, v.screenY * 0.5), (255, 255, 255), "Resources/Fonts/RPGSystem.ttf", int(30/640 * v.screenX), variable=False, centred=True).update()  
    py.display.flip()
    
    page = urllib.request.urlopen(v.url + "accounts/")
    accounts = page.read()
    accounts = pickle.loads(accounts)
    
    for un, vals in accounts.items():
        if un == v.username:
            if v.password == vals["password"]:
                print(vals.keys())
                print(vals["xp"])
                if 'save' in vals.keys():
                    save = vals['save']
                    with open("Saves/Entities.save", "wb") as s:
                        #pickle.dump(save["Entities"], s)
                        s.write(save["Entities"])
                    with open("Saves/Inventory.save", "wb") as s:
                        #pickle.dump(save["Inventory"], s)
                        s.write(save["Inventory"])
                    with open("Saves/Variables.save", "wb") as s:
                        #pickle.dump(save["Variables"], s)
                        s.write(save["Variables"])
            else:
                return "PASSWORD"
    return "USERNAME"