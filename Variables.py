playerPosX = 0
playerPosY = 0
playerDirection = ""
playerHealth = 20
hitList = None
allTiles = None
allNpc = None
damagesNPCs = None
scale = 2
screen = None
ticks = 0
map1 = []
hits = None
p_class = None
cur_weapon = None
playerAttacking = False
playerStopped = False
clock = None
events = []
particles = None
attackerDirection = "Down"
characterHovered = False
playerClass = None
custimizationStage = None
skillPoints = 5
appearanceTab = "Body"
appearancePrevNum = 7
equipped = {"Weapon": None}
appearance = {"Body": "Resources/Images/Character Customisation/Body/white.png",
              "Face": "Resources/Images/Character Customisation/Face/whiteNormal.png",
              "Dress": "Resources/Images/Character Customisation/Dress/cloakBrown.png"
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
classAttributes = {"Paladin":{"Speed": 2,
                              "Max Health": 20,
                              "Defence": 5,
                              "Strength": 4,
                              "Max Mana": 10,
                              "Magical Strength": 2,
                              "Luck": 7,
                              "Charisma": 5
                              }, # 55
                   "Mage":{"Speed": 2,
                          "Max Health": 10,
                          "Defence": 3,
                          "Strength": 2,
                          "Max Mana": 20,
                          "Magical Strength": 4,
                          "Luck": 10,
                          "Charisma": 4
                          } # 55
                   
                   }