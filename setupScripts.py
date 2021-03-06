import Variables as v
import itemClasses
import entityClasses
import pygame as py
import guiClasses
import inventoryScreen
import npcScripts

def newGame():
    v.playerHealth = v.Attributes["Max Health"]
    v.p_class.prevHealth = v.playerHealth
    v.playerMana = v.Attributes["Max Mana"]
    #entityClasses.Enemy(0, -60, 1, "Resources/Images/EnemySkins/Generic Goblin.png", {"Name": "Groblin Lvl. 1", "Health":5, "Attack":5, "Speed":1.5})
    #entityClasses.NPC((0, 30, "Down", 1), "Resources/Images/NpcSkins/Spritesheets/Male_Basic.png", {"Name":"Fred", "Conversation":cn})
    
    v.inventory.add(itemClasses.item("Thing", py.image.load("Resources/Images/XPOrb.png").convert_alpha()))
    v.inventory.add(itemClasses.weapon("Magic Orb", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[56], "manaOrb", "Resources/Images/castOrbPurple.png", {"Damage":2, "Knockback": 10, "Cooldown": 60}))
    v.inventory.add(itemClasses.weapon("Broken Sword", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[0], "swing", "Resources/Images/Sword_1.png", {"Damage":2, "Knockback": 10, "Cooldown": 30, "AttSpeed": 16}))
    v.inventory.add(itemClasses.weapon("Short Bow", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[72], "shoot", "Resources/Images/Arrow.png", {"Damage":2, "Knockback": 10, "Cooldown": 20, "Range": 20})) 
    entityClasses.droppedItem(itemClasses.item("Thing", py.image.load("Resources/Images/XPOrb.png").convert_alpha()), (0, 0))
    
    fb = itemClasses.spell("Fire Beam", "beam", "Resources/Images/fireBeam.png", "Resources/Images/redCastCircle.png", "Resources/Images/Spell Icons/fireBeam.png", {"Damage": 0.2, "Knockback": "S", "Cooldown": 5, "Mana": 10, "InvulnMod": 0})
    ls = itemClasses.spell("Lightning Storm", "lightning", "Resources/Images/lightningStorm.png", "Resources/Images/blueCastCircle.png", "Resources/Images/Spell Icons/chainLightning.png", {"Damage": 0.4, "Knockback": 1, "Cooldown": 5, "Mana": 10, "InvulnMod": 0.5})
    v.abilities["1"] = fb
    v.abilities["2"] = ls
    
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
        v.equipped["Weapon"] = itemClasses.weapon("Magic Orb", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[56], "manaOrb", "Resources/Images/castOrbPurple.png", {"Damage":2, "Knockback": 10, "Cooldown": 60})
    if v.playerClass == "Paladin":
        v.equipped["Weapon"] = itemClasses.weapon("Broken Sword", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[0], "swing", "Resources/Images/Sword_1.png", {"Damage":2, "Knockback": 10, "Cooldown": 30, "AttSpeed": 16})
    if v.playerClass == "Ranger":
        v.equipped["Weapon"] = itemClasses.weapon("Short Bow", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[72], "shoot", "Resources/Images/Arrow.png", {"Damage":2, "Knockback": 10, "Cooldown": 20, "Range": 20})
    if v.playerClass == "Rogue":
        v.equipped["Weapon"] = itemClasses.weapon("Blunt Shruikans", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[35], "shoot", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[35], {"Damage":1, "Knockback": 5, "Cooldown": 10, "Range": 10, "Rotate": True})
    if v.playerClass == "Barbarian":
        v.equipped["Weapon"] = itemClasses.weapon("Small Club", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[48], "swing", "Resources/Images/Club_1.png", {"Damage":3, "Knockback": 15, "Cooldown": 60, "AttSpeed": 10})
    if v.playerClass == "Necromancer":
        v.equipped["Weapon"] = itemClasses.weapon("Necrotic Staff", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[57], "manaOrb", "Resources/Images/castOrbRed.png", {"Damage": 3, "Knockback": 8, "Cooldown": 60})
    if v.playerClass == "Voyant":
        v.equipped["Weapon"] = itemClasses.weapon("Light Caster", entityClasses.SpriteSheet("Resources/Images/WeaponIcons.png", 8, 12).images[41], "manaOrb", "Resources/Images/castOrbCyan.png", {"Damage": 1, "Knockback": 10, "Cooldown": 30, "Orbs": 3})

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
    for i in range(1, 7):
        v.abilityButtons.add(guiClasses.ability(i))

def defaultVariables():
    v.playerPosX = 0
    v.playerPosY = 0
    v.playerDirection = ""
    v.playerHealth = 20
    v.playerMana = 20
    v.experience = {"XP": 0, "XPL": 1, "XPtoL": 10, "Total": 0}
    v.xpMod = 1.5
    v.npcID = 1
    v.scale = 4
    v.skillPoints = 5
    v.equipped = {"Weapon": None, "Helmet": None, "Armour": None, "Greaves": None, "Boots": None}
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