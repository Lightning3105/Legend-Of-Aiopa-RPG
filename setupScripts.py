import Variables as v
import itemClasses
import entityClasses
import pygame as py

def setAttributes():
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
    v.allNpc = py.sprite.Group()
    v.particles = py.sprite.Group()
    v.currentSpells = py.sprite.Group()
    v.equippedSpells = py.sprite.Group()
    v.abilityButtons = py.sprite.Group()
    v.xpGroup = py.sprite.Group()
    v.droppedItems = py.sprite.Group()