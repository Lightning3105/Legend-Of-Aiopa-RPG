import Variables as v
import itemClasses
import entityClasses
import pygame as py
import guiClasses
import inventoryScreen

def newGame():
    v.playerHealth = v.Attributes["Max Health"]
    v.p_class.prevHealth = v.playerHealth
    v.playerMana = v.Attributes["Max Mana"]
    #entityClasses.Enemy(0, -60, 1, "Resources/Images/EnemySkins/Generic Goblin.png", {"Name": "Groblin Lvl. 1", "Health":5, "Attack":5, "Speed":1.5})
    cn = [{"Message": "Greetings. Why not press a button? Who knows, you might win a prize!", "B1": {"Text": "Button 1", "ID": 1}, "B2": {"Text": "Button 2", "ID": 2}, "B3": {"Text": "Button 3", "ID": 3}, "B4": {"Text": "Button 4", "ID": 4}, "ID":0}, {"Message": "You pressed Button 1", "Goto":5, "ID": 1}, {"Message": "You pressed Button 2", "Goto":5, "ID": 2}, {"Message": "You pressed Button 3", "Goto":5, "ID": 3}, {"Message": "You pressed Button 4", "Goto":5, "ID": 4}, {"Message": "Congratulations. You won.", "ID": 5, "End":True}]
    #entityClasses.NPC((0, 30, "Down", 1), "Resources/Images/NpcSkins/Spritesheets/Male_Basic.png", {"Name":"Fred", "Conversation":cn})
    fb = itemClasses.spell("Fire Beam", "beam", "Resources/Images/fireBeam.png", "Resources/Images/redCastCircle.png", {"Damage": 0.2, "Knockback": "S", "Cooldown": 5, "Mana": 10, "InvulnMod": 0})
    v.abilityButtons.add(guiClasses.ability(fb, "Resources/Images/Spell Icons/fireBeam.png", 0))  
    v.inventory.add(itemClasses.item("Thing", py.image.load("Resources/Images/XPOrb.png")))
    v.inventory.add(itemClasses.weapon("Magic Orb", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[56], "manaOrb", "Resources/Images/castOrbPurple.png", {"Damage":2, "Knockback": 10}))
    v.inventory.add(itemClasses.weapon("Broken Sword", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[0], "swing", "Resources/Images/Sword_1.png", {"Damage":2, "Knockback": 10}))
    v.inventory.add(itemClasses.weapon("Short Bow", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[72], "shoot", "Resources/Images/Arrow.png", {"Damage":2, "Knockback": 10})) 
    entityClasses.droppedItem(itemClasses.item("Thing", py.image.load("Resources/Images/XPOrb.png")), (0, 0))
    ls = itemClasses.spell("Lightning Storm", "lightning", "Resources/Images/lightningStorm.png", "Resources/Images/blueCastCircle.png", {"Damage": 0.4, "Knockback": 1, "Cooldown": 5, "Mana": 10, "InvulnMod": 0})
    v.abilityButtons.add(guiClasses.ability(ls, "Resources/Images/Spell Icons/chainLightning.png", 1))
def initSound():
    py.mixer.init()

def setAttributes():
    if not v.playerClass in v.classAttributes:
        from MenuItems import notImplimented
        notImplimented()
        import gameScreens
        gameScreens.mainMenu()
    v.Attributes = v.classAttributes[v.playerClass]
    if v.playerClass == "Mage":
        v.equipped["Weapon"] = itemClasses.weapon("Magic Orb", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[56], "manaOrb", "Resources/Images/castOrbPurple.png", {"Damage":2, "Knockback": 10})
    if v.playerClass == "Paladin":
        v.equipped["Weapon"] = itemClasses.weapon("Broken Sword", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[0], "swing", "Resources/Images/Sword_1.png", {"Damage":2, "Knockback": 10})
    if v.playerClass == "Ranger":
        v.equipped["Weapon"] = itemClasses.weapon("Short Bow", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[72], "shoot", "Resources/Images/Arrow.png", {"Damage":2, "Knockback": 10})

def createGroups():
    v.damagesNPCs = py.sprite.Group()
    v.hitList = py.sprite.Group()
    v.allTiles = py.sprite.Group()
    v.topTiles = py.sprite.Group()
    v.allNpc = py.sprite.Group()
    v.NPCs = py.sprite.Group()
    v.dyingEnemies = py.sprite.Group()
    v.quests = py.sprite.Group()
    v.particles = py.sprite.Group()
    v.currentSpells = py.sprite.Group()
    v.equippedSpells = py.sprite.Group()
    v.abilityButtons = py.sprite.Group()
    v.xpGroup = py.sprite.Group()
    v.droppedItems = py.sprite.Group()
    v.inventory = inventoryScreen.inventory()

def defaultVariables():
    v.playerPosX = 0
    v.playerPosY = 0
    v.playerDirection = ""
    v.playerHealth = 20
    v.playerMana = 20
    v.experience = {"XP": 0, "XPL": 1, "XPtoL": 10}
    v.xpMod = 1.5
    v.npcID = 1
    v.scale = v.screenScale
    v.skillPoints = 5
    v.equipped = {"Weapon": None}
    v.appearance = {"Body": "Resources/Images/Character Customisation/Body/white.png",
                  "Face": "Resources/Images/Character Customisation/Face/whiteNormal.png",
                  "Dress": "Resources/Images/Character Customisation/Dress/cloakBrown.png",
                  "Hair": "Resources/Images/Character Customisation/Hair/Brown1.png"
                  }
    v.Attributes = {"Speed": 0,
                  "Max Health": 0,
                  "Defence": 0,
                  "Strength": 0,
                  "Max Mana": 0,
                  "Magical Strength": 0,
                  "Luck": 0,
                  "Charisma": 0
                  }