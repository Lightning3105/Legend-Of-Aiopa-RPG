import logging
curFunc = None
try:
    logging.basicConfig(filename='logs/log.log',level=logging.DEBUG)
except FileNotFoundError:
    from os import mkdir
    mkdir("logs")
def debug(*args):
    out = ""
    for i in args:
        out = out + " " + i
    print(out)
    logging.debug(out)

PAUSED = False
load = None
newGame = True
fullScreen = False
screenX = 848
screenY = 477
oldResolution = (1280, 720)
screenStart = (1280, 720)
smoothScale = False
mouse_pos = (0, 0)
aspectRatio = (16, 9)
mouseImage = None
fpsLock = 30
fpsAdjuster = 1
pauseType = "Pause"
justPaused = True
playerPosX = 0
playerPosY = 0
playerDirection = ""
playerHealth = 20
playerMana = 20
playerName = "Bob"
experience = {"XP": 0, "XPL": 1, "XPtoL": 10, "Total": 0}
xpGroup = None
xpMod = 1.5
hitList = None
allTiles = None
allNpc = None
NPCs = None
dyingEnemies = None
quests = None
npcID = 1
textNum = 0
account = {}
username = ""
password = ""
#url = "http://127.0.0.1:5000/"
url = "http://socket-lightning3105.rhcloud.com/"
conversationClass = None
damagesNPCs = None
droppedItems = None
scale = 3
screen = None
screenDisplay = None
music = None
sounds = None
ticks = 0
map1 = []
MAP = None
mapNum = 1
savedMap = None
mapMeta = {"Biome": None, "Name": None}
topTiles = None
hits = None
p_class = None
mask = False
cur_weapon = None
playerActing = False
playerStopped = False
playerDead = False
clock = None
events = []
actionQueue = []
actionsDone = []
weaponCooldown = 1
particles = None
currentSpells = None
attackerDirection = "Down"
characterHovered = False
playerClass = None
custimizationStage = None
skillPoints = 5
appearanceTab = "Body"
appearancePrevNum = 7
equipped = {"Weapon": None, "Helmet": None, "Armour": None, "Greaves": None, "Boots": None}
abilities = {"1": None, "2": None}
equippedSpells = None
abilityButtons = None
inventory = None
appearance = {"Body": "Resources/Images/Character Customisation/Body/white.png",
              "Face": "Resources/Images/Character Customisation/Face/whiteNormal.png",
              "Dress": "Resources/Images/Character Customisation/Dress/cloakBrown.png",
              "Hair": "Resources/Images/Character Customisation/Hair/Brown1.png"
              }
testAppearance = {"Body": None,
              "Face": None,
              "Dress": None,
              "Hair": None
              }
Attributes = {"Speed": 0,
              "Max Health": 0,
              "Defence": 0,
              "Strength": 0,
              "Max Mana": 0,
              "Magical Strength": 0,
              "Luck": 0,
              "Charisma": 0
              }
classAttributes = {"Paladin":{"Speed": 4,
                              "Max Health": 20,
                              "Defence": 5,
                              "Strength": 4,
                              "Max Mana": 10,
                              "Magical Strength": 2,
                              "Luck": 7,
                              "Charisma": 5
                              }, # 57
                   "Mage":{"Speed": 4,
                          "Max Health": 10,
                          "Defence": 3,
                          "Strength": 2,
                          "Max Mana": 20,
                          "Magical Strength": 4,
                          "Luck": 10,
                          "Charisma": 4
                          }, # 57
                   "Ranger":{"Speed": 7,
                          "Max Health": 15,
                          "Defence": 2,
                          "Strength": 3,
                          "Max Mana": 16,
                          "Magical Strength": 3,
                          "Luck": 8,
                          "Charisma": 3
                          }, # 57
                   "Rogue":{"Speed": 10,
                          "Max Health": 15,
                          "Defence": 1,
                          "Strength": 3,
                          "Max Mana": 13,
                          "Magical Strength": 3,
                          "Luck": 10,
                          "Charisma": 2
                          }, # 57
                   "Necromancer":{"Speed": 3,
                          "Max Health": 10,
                          "Defence": 4,
                          "Strength": 4,
                          "Max Mana": 18,
                          "Magical Strength": 5,
                          "Luck": 10,
                          "Charisma": 2
                          }, #57
                   "Barbarian":{"Speed": 3,
                              "Max Health": 25,
                              "Defence": 6,
                              "Strength": 6,
                              "Max Mana": 9,
                              "Magical Strength": 1,
                              "Luck": 5,
                              "Charisma": 2
                              }, # 57
                   "Voyant":{"Speed": 5,
                          "Max Health": 8,
                          "Defence": 2,
                          "Strength": 2,
                          "Max Mana": 18,
                          "Magical Strength": 3,
                          "Luck": 15,
                          "Charisma": 5
                          }, # 57
                   
                   }
