import pygame as py
import Variables as v
import math
import time
from random import randint
import gameScreens
import SaveLoad
from profilehooks import profile

try:
    import npcScripts
except:
    pass

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None
    images = None

    def __init__(self, file_name, rows, columns):
        """ Constructor. Pass in the file name of the sprite sheet. """

        self.rows = rows
        self.columns = columns

        # Load the sprite sheet.
        if type(file_name) is py.Surface:
            self.sprite_sheet = file_name.convert_alpha()
        else:
            self.sprite_sheet = py.image.load(file_name).convert_alpha()
        self.getGrid()


    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = py.Surface([width, height], py.SRCALPHA, 32).convert_alpha()
        image = image.convert_alpha()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Return the image
        return image

    def getGrid(self):
        width = self.sprite_sheet.get_size()[0] / self.columns
        height = self.sprite_sheet.get_size()[1] / self.rows
        all = []
        for h in range(self.rows):
            for w in range(self.columns):
                image = py.Surface([width, height], py.SRCALPHA, 32).convert_alpha()
                image.blit(self.sprite_sheet, (0, 0), (w * width, h * height, width, height))
                all.append(image)
        self.images = all


class Player(py.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.posx = 640
        self.posy = 360
        self.direction = "Down"
        v.playerDirection = self.direction
        self.moving = False
        self.movFlip = True
        self.view = "DownC"
        self.sheetImage = "Resources\Images"
        self.damaged = False
        self.damage_alpha = 0
        self.damage_fade = True
        self.prevHealth = v.playerHealth
        self.dead = False
        self.invulnLength = 30
        self.combineImages()
        self.rect = py.Rect(0, 0, 0, 0)


    def initSheet(self):
        self.sheet = SpriteSheet(self.sheetImage, 4, 3)
        self.sheet.getGrid()
        self.views = {"UpL": self.sheet.images[0],
                      "UpC": self.sheet.images[1],
                      "UpR": self.sheet.images[2],
                      "RightL": self.sheet.images[3],
                      "RightC": self.sheet.images[4],
                      "RightR": self.sheet.images[5],
                      "DownL": self.sheet.images[6],
                      "DownC": self.sheet.images[7],
                      "DownR": self.sheet.images[8],
                      "LeftL": self.sheet.images[9],
                      "LeftC": self.sheet.images[10],
                      "LeftR": self.sheet.images[11]}
    def combineImages(self):
        self.sheetImage = py.image.load(v.appearance["Body"]).convert_alpha()
        self.sheetImage.blit(py.image.load(v.appearance["Face"]), (0, 0))
        self.sheetImage.blit(py.image.load(v.appearance["Dress"]), (0, 0))
        self.sheetImage.blit(py.image.load(v.appearance["Hair"]), (0, 0))
        #v.screen.blit(self.sheetImage, (0, 0))
        self.initSheet()
    def draw(self):
        self.set_rect()
        self.get_view()
        skin = self.views[self.view]
        size = skin.get_rect()
        self.image = py.transform.scale(skin, (int(size.width * v.scale), int(size.height * v.scale)))
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        self.damage_animation()
        self.damage_knockback()
        v.screen.blit(self.image, self.rect)
        

    def damage_knockback(self):
        if self.damage_fade and self.damaged and not self.dead:
            self.moving = False
            v.playerStopped = True
            if v.attackerDirection == "Up":
                v.playerPosY += 2
            if v.attackerDirection == "Down":
                v.playerPosY += -2
            if v.attackerDirection == "Right":
                v.playerPosX += 2
            if v.attackerDirection == "Left":
                v.playerPosX + -2

    def damage_animation(self): #TODO: Finish
        if self.damaged and not self.dead:
            damage_image = self.image
            damage_image.fill((255, 0, 0, self.damage_alpha), special_flags=py.BLEND_RGBA_MULT)
            self.image.blit(damage_image, (0,0))
            if self.damage_fade:
                self.damage_alpha += 255 / (self.invulnLength / 2)
                if self.damage_alpha >= 255:
                    self.damage_fade = False
                    self.damage_alpha = 255
            elif not self.damage_fade:
                self.damage_alpha -= 255 / (self.invulnLength / 2)
                if self.damage_alpha <= 0:
                    self.damage_alpha = 0
                    self.damaged = False
                    self.damage_fade = True

    def get_view(self):
        for event in v.events:
            if event.type == py.USEREVENT:
                if self.view == self.direction + "C":
                    if self.movFlip:
                        self.view = self.direction + "R"
                        self.movFlip = not self.movFlip
                    else:
                        self.view = self.direction + "L"
                        self.movFlip = not self.movFlip
                elif self.view == self.direction + "R":
                    self.view = self.direction + "C"
                elif self.view == self.direction + "L":
                    self.view = self.direction + "C"
                else:
                    self.view = self.direction + "C"
        if self.moving == False:
            self.view = self.direction + "C"


    def set_rect(self):
        self.rend = self.sheet.images[0]
        self.rect = self.rend.get_rect()
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        self.rect.width = self.rend.get_rect().width * v.scale
        self.rect.height = self.rend.get_rect().height * v.scale

    def update(self):
        if v.playerHealth < self.prevHealth:
            self.damaged = True
            self.prevHealth = v.playerHealth
        if not v.playerStopped:
            py.event.pump()
            moveRight = True
            moveLeft = True
            moveUp = True
            moveDown = True
            self.prevX = v.playerPosX
            self.prevY = v.playerPosY
            self.velX = 0
            self.velY = 0
            """for wall in v.wallHitList:
                if self.rect.colliderect(wall.rect):
                    if self.rect.right > wall.rect.left:
                        moveRight = False
                    if self.rect.left < wall.rect.right:
                        moveLeft = False
                    if self.rect.top < wall.rect.bottom:
                        moveUp = False
                    if self.rect.bottom > wall.rect.top:
                        moveDown = False"""
            keys_pressed = py.key.get_pressed()
            if keys_pressed[py.K_a]:
                self.velX = -v.Attributes["Speed"] / 2
            if keys_pressed[py.K_d]:
                self.velX = v.Attributes["Speed"] / 2
            if keys_pressed[py.K_s]:
                self.velY = -v.Attributes["Speed"] / 2
            if keys_pressed[py.K_w]:
                self.velY = v.Attributes["Speed"] / 2
            
            

            if keys_pressed[py.K_s]:
                self.direction = "Down"
                self.moving = True
            elif keys_pressed[py.K_w]:
                self.direction = "Up"
                self.moving = True
            elif keys_pressed[py.K_a]:
                self.direction = "Left"
                self.moving = True
            elif keys_pressed[py.K_d]:
                self.direction = "Right"
                self.moving = True
            else:
                self.moving = False

            self.velX *= v.fpsAdjuster
            self.velY *= v.fpsAdjuster
            vx = self.velX
            vy = self.velY

            for hit in v.hits:
                velmod = hit.update()
                self.velX += velmod[0]
                self.velY += velmod[1]

            v.playerPosX += self.velX
            v.playerPosY += self.velY
            v.playerDirection = self.direction

class mask: #TODO: Remoe and replace with something more efficient
    
    def __init__(self):
        super().__init__()
        self.posx = 640
        self.posy = 360
        self.direction = "Down"
        v.playerDirection = self.direction
        self.moving = False
        self.movFlip = True
        self.view = "DownC"
        self.sheetImage = "Resources\Images"
        self.damaged = False
        self.damage_alpha = 0
        self.damage_fade = True
        self.prevHealth = v.Attributes["Max Health"]
        self.dead = False
        self.invulnLength = 30
        self.combineImages()
        self.rect = py.Rect(0, 0, 0, 0)


    def initSheet(self):
        self.sheet = SpriteSheet(self.sheetImage, 4, 3)
        self.sheet.getGrid()
        self.views = {"UpL": self.sheet.images[0],
                      "UpC": self.sheet.images[1],
                      "UpR": self.sheet.images[2],
                      "RightL": self.sheet.images[3],
                      "RightC": self.sheet.images[4],
                      "RightR": self.sheet.images[5],
                      "DownL": self.sheet.images[6],
                      "DownC": self.sheet.images[7],
                      "DownR": self.sheet.images[8],
                      "LeftL": self.sheet.images[9],
                      "LeftC": self.sheet.images[10],
                      "LeftR": self.sheet.images[11]}
    def combineImages(self):
        self.sheetImage = py.image.load(v.appearance["Body"]).convert_alpha()
        self.sheetImage.blit(py.image.load(v.appearance["Face"]), (0, 0))
        self.sheetImage.blit(py.image.load(v.appearance["Dress"]), (0, 0))
        self.sheetImage.blit(py.image.load(v.appearance["Hair"]), (0, 0))
        #v.screen.blit(self.sheetImage, (0, 0))
        self.initSheet()
    def draw(self):
        if v.mask:
            self.set_rect()
            self.get_view()
            skin = self.views[v.p_class.view]
            size = skin.get_rect()
            self.image = py.transform.scale(skin, (int(size.width * v.scale), int(size.height * v.scale)))
            self.rect.centerx = self.posx
            self.rect.centery = self.posy
            self.damage_animation()
            self.damage_knockback()
            self.image.fill((200, 200, 200, 80), special_flags=py.BLEND_RGBA_MULT)
            v.screen.blit(self.image, self.rect)
        

    def damage_knockback(self):
        if self.damage_fade and self.damaged and not self.dead:
            self.moving = False
            v.playerStopped = True
            if v.attackerDirection == "Up":
                v.playerPosY += 2
            if v.attackerDirection == "Down":
                v.playerPosY += -2
            if v.attackerDirection == "Right":
                v.playerPosX += 2
            if v.attackerDirection == "Left":
                v.playerPosX + -2

    def damage_animation(self): #TODO: Finish
        if self.damaged and not self.dead:
            damage_image = self.image
            damage_image.fill((255, 0, 0, self.damage_alpha), special_flags=py.BLEND_RGBA_MULT)
            self.image.blit(damage_image, (0,0))
            if self.damage_fade:
                self.damage_alpha += 255 / (self.invulnLength / 2)
                if self.damage_alpha >= 255:
                    self.damage_fade = False
                    self.damage_alpha = 255
            elif not self.damage_fade:
                self.damage_alpha -= 255 / (self.invulnLength / 2)
                if self.damage_alpha <= 0:
                    self.damage_alpha = 0
                    self.damaged = False
                    self.damage_fade = True

    def get_view(self):
        for event in v.events:
            if event.type == py.USEREVENT:
                if self.view == self.direction + "C":
                    if self.movFlip:
                        self.view = self.direction + "R"
                        self.movFlip = not self.movFlip
                    else:
                        self.view = self.direction + "L"
                        self.movFlip = not self.movFlip
                elif self.view == self.direction + "R":
                    self.view = self.direction + "C"
                elif self.view == self.direction + "L":
                    self.view = self.direction + "C"
                else:
                    self.view = self.direction + "C"
        if self.moving == False:
            self.view = self.direction + "C"


    def set_rect(self):
        self.rend = self.sheet.images[0]
        self.rect = self.rend.get_rect()
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        self.rect.width = self.rend.get_rect().width * v.scale
        self.rect.height = self.rend.get_rect().height * v.scale

    def update(self):
        if v.playerHealth < self.prevHealth:
            self.damaged = True
            self.prevHealth = v.playerHealth
        
        keys_pressed = py.key.get_pressed()
        if keys_pressed[py.K_s]:
            self.direction = "Down"
            self.moving = True
        elif keys_pressed[py.K_w]:
            self.direction = "Up"
            self.moving = True
        elif keys_pressed[py.K_a]:
            self.direction = "Left"
            self.moving = True
        elif keys_pressed[py.K_d]:
            self.direction = "Right"
            self.moving = True
        else:
            self.moving = False
        
class playerGhost():
    def __init__(self):
        self.posx = 640
        self.posy = 360
        self.direction = v.p_class.direction
        v.playerDirection = self.direction
        self.moving = False
        self.movFlip = True
        self.view = v.p_class.view
        self.sheetImage = "Resources\Images"
        self.combineImages()
        self.rect = py.Rect(0, 0, 0, 0)
        self.cycle = 100
    
    def initSheet(self):
        self.sheet = SpriteSheet(self.sheetImage, 4, 3)
        self.sheet.getGrid()
        self.views = {"UpL": self.sheet.images[0],
                      "UpC": self.sheet.images[1],
                      "UpR": self.sheet.images[2],
                      "RightL": self.sheet.images[3],
                      "RightC": self.sheet.images[4],
                      "RightR": self.sheet.images[5],
                      "DownL": self.sheet.images[6],
                      "DownC": self.sheet.images[7],
                      "DownR": self.sheet.images[8],
                      "LeftL": self.sheet.images[9],
                      "LeftC": self.sheet.images[10],
                      "LeftR": self.sheet.images[11]}
    def combineImages(self):
        #self.sheetImage = py.image.load(v.appearance["Body"])
        self.sheetImage = py.image.load("Resources/Images/ghostSheet.png").convert_alpha()
        self.sheetImage.blit(py.image.load(v.appearance["Face"]), (0, 0))
        #self.sheetImage.blit(py.image.load(v.appearance["Dress"]), (0, 0))
        self.sheetImage.blit(py.image.load(v.appearance["Hair"]), (0, 0))
        #v.screen.blit(self.sheetImage, (0, 0))
        self.initSheet()
    def update(self):
        if v.playerDead:
            self.set_rect()
            self.get_view()
            skin = self.views[v.p_class.view]
            size = skin.get_rect()
            self.image = py.transform.scale(skin, (int(size.width * v.scale * (self.cycle/100)), int(size.height * v.scale * (self.cycle/100))))
            self.rect.centerx = self.posx + randint(-1, 1)
            self.rect.centery = self.posy - self.cycle + 100
            #self.image = self.image.set_alpha(255 - self.cycle + 100)
            #self.damage_animation()
            #self.damage_knockback()
            #self.image.fill((200, 200, 200, 80), special_flags=py.BLEND_RGBA_MULT)
            v.screen.blit(self.image, self.rect)
    
    def get_view(self):
        for event in v.events:
            if event.type == py.USEREVENT:
                if self.view == self.direction + "C":
                    if self.movFlip:
                        self.view = self.direction + "R"
                        self.movFlip = not self.movFlip
                    else:
                        self.view = self.direction + "L"
                        self.movFlip = not self.movFlip
                elif self.view == self.direction + "R":
                    self.view = self.direction + "C"
                elif self.view == self.direction + "L":
                    self.view = self.direction + "C"
                else:
                    self.view = self.direction + "C"
        if self.moving == False:
            self.view = self.direction + "C"
    
    def set_rect(self):
        self.rend = self.sheet.images[0]
        self.rect = self.rend.get_rect()
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        self.rect.width = self.rend.get_rect().width * v.scale * (self.cycle / 100)
        self.rect.height = self.rend.get_rect().height * v.scale * (self.cycle / 100)

class HitBox(py.sprite.Sprite):

    def __init__(self, side):
        super().__init__()
        self.side = side
        self.ID = "playerHitbox"

    def draw(self):
        py.draw.rect(v.screen, (255, 0, 0), self.rect)

    def update(self): #TODO: use new positition
        if self.side == "Top":
            self.rect = py.Rect(640 - (3 * v.scale), 360 + (6 * v.scale), (8 * v.scale), (2 * v.scale))
        if self.side == "Bottom":
            self.rect = py.Rect(640 - (3 * v.scale), 360 + (16 * v.scale), (8 * v.scale), (2 * v.scale))
        if self.side == "Left":
            self.rect = py.Rect(640 - (5 * v.scale), 360 + (7 * v.scale), (2 * v.scale), (9 * v.scale))
        if self.side == "Right":
            self.rect = py.Rect(640 + (5 * v.scale), 360 + (7 * v.scale), (2 * v.scale), (9 * v.scale))
        self.image = py.Surface((self.rect.width, self.rect.height))
        self.image.fill((255, 0, 0))
        newrect = self.rect
        hit = False
        for thing in v.hitList:
            if newrect.colliderect(thing.rect):
                hit = True
        for thing in v.allNpc:
            if newrect.colliderect(thing.rect):
                hit = True
        velX = 0
        velY = 0
        if hit:
            if self.side == "Top":
                velY = -v.Attributes["Speed"] / 2
            elif self.side == "Bottom":
                velY = v.Attributes["Speed"] / 2
            elif self.side == "Left":
                velX = v.Attributes["Speed"] / 2
            elif self.side == "Right":
                velX = -v.Attributes["Speed"] / 2
            else:
                print("how did I get here?")
        
            velX *= v.fpsAdjuster
            velY *= v.fpsAdjuster
        else:
            velX = 0
            velY = 0
        
        for tile in v.topTiles:
            if self.rect.colliderect(tile.rect):
                v.mask = True
        
        return velX, velY


class Tile(py.sprite.Sprite):

    def __init__(self, tilePosition, terrain, wall=False, top=False, image=None, teleport=None):
        super().__init__()
        self.tilePosX = tilePosition[0]
        self.tilePosY = tilePosition[1]
        self.posX = 0
        self.posY = 0
        self.wall = wall
        if wall:
            v.hitList.add(self)
        v.allTiles.add(self)
        self.ID = "tile"
        self.oldScale = "Nope"  
        self.oldx = "Nope"
        self.oldy = "Nope"
        self.top = top
        if top:
            v.topTiles.add(self)
            temp = py.PixelArray(image)
            temp.replace((97, 90, 114), (0, 0, 0, 0), 0.02)
            self.skin = temp.make_surface()
            #self.skin = image
        self.teleport = teleport

    def update(self): #TODO: Make more efficient
        self.rect = py.Rect(0, 0, int(30 * v.scale), int(30 * v.scale))
        self.rect.centerx = 1280 / 2 + ((-v.playerPosX + (30 * self.tilePosX)) * v.scale)
        self.rect.centery = 360 + ((v.playerPosY + (30 * self.tilePosY)) * v.scale)
        
        if self.top:
            self.image = py.transform.scale(self.skin, self.rect.size)
        
        if self.teleport != None:
            if self.rect.colliderect(v.p_class.rect):
                SaveLoad.saveMap(v.mapNum)
                tp = self.teleport
                v.mapNum = tp[0]
                v.playerPosX = tp[1]
                v.playerPosY = tp[2]
                gameScreens.game()

def rot_center(image, angle):
    """rotate an image while keeping its centre and size"""
    orig_rect = image.get_rect()
    rot_image = py.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def arc(point, radius, degrees):
    import math as m
    out = (point[0] + (m.sin(m.radians(degrees)) * radius), point[1] + (m.cos(m.radians(degrees)) * radius))
    return out

def centre():
    return 640, 360

class Enemy(py.sprite.Sprite):

    def __init__(self, posx=None, posy=None, posm=None, sImage=None, attributes={}, blank = False):
        super().__init__()
        if not blank:
            self.newStats(posx, posy, posm, sImage, attributes)
    
    def save(self):
        data = {
                "attributes": self.attributes,
                "name": self.name,
                "posx": self.posx,
                "posy": self.posy,
                "direction": self.direction,
                "view": self.view,
                "sheetImage": self.sheetImage,
                "maxHealth": self.maxHealth,
                "health": self.health,
                "invulnLength": self.invulnLength,
                "ID": self.ID,
                "npcID": self.npcID,
                "speed": self.speed,
                "att": self.att
                }
        return data
    
    def load(self, dic):
        self.attributes = dic["attributes"]
        self.name = dic["name"]
        self.posx = dic["posx"]
        self.posy = dic["posy"]
        self.direction = dic["direction"]
        self.view = dic["view"]
        self.sheetImage = dic["sheetImage"]
        self.maxHealth = dic["maxHealth"]
        self.health = dic["health"]
        self.speed = dic["speed"]
        self.att = dic["att"]
        self.invulnLength = dic["invulnLength"]
        self.ID = dic["ID"]
        self.npcID = dic["npcID"]
        
        self.setConstants()
    
    def newStats(self, posx=None, posy=None, posm=None, sImage=None, attributes={}):
        self.attributes = attributes
        self.name = attributes["Name"]
        self.posx = posx
        self.posy = posy
        self.direction = "Down"
        self.view = "DownC"
        self.sheetImage = sImage
        self.maxHealth = attributes["Health"]
        self.health = attributes["Health"]
        self.speed = attributes["Speed"]
        self.att = attributes["Attack"]
        self.invulnLength = 30
        self.ID = "enemy"
        self.npcID = v.npcID
        v.npcID += 1
        
        self.setConstants()
        
    def setConstants(self):
        self.moving = False
        self.movFlip = True
        self.xp = 5
        self.invulnCooldown = 0
        self.knockback = 0
        self.damaged = False
        self.damage_alpha = 0
        self.damage_fade = True
        self.dead = False
        self.firstDeath = True
        self.attCount = -float("inf")
        self.damagedPlayer = False
        v.allNpc.add(self)
        v.enemies.add(self)
        self.initSheet()
        #v.hitList.add(self)
        self.rect = py.Rect(0, 0, 0, 0)
        self.image = py.Surface((0, 0))
        self.stopped = False
        self.attImage = py.image.load("Resources/Images/ClawSlash.png").convert_alpha()
        font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(10 * v.scale))
        self.label = font.render(self.name, 1, (255,255,255))

    def initSheet(self):
        self.sheet = SpriteSheet(self.sheetImage, 4, 3)
        self.sheet.getGrid()
        self.views = {"UpL": self.sheet.images[9],
                      "UpC": self.sheet.images[10],
                      "UpR": self.sheet.images[11],
                      "RightL": self.sheet.images[6],
                      "RightC": self.sheet.images[7],
                      "RightR": self.sheet.images[8],
                      "DownL": self.sheet.images[0],
                      "DownC": self.sheet.images[1],
                      "DownR": self.sheet.images[2],
                      "LeftL": self.sheet.images[3],
                      "LeftC": self.sheet.images[4],
                      "LeftR": self.sheet.images[5]}
    def get_view(self):
        for event in v.events:
            if event.type == py.USEREVENT:
                if self.view == self.direction + "C":
                    if self.movFlip:
                        self.view = self.direction + "R"
                        self.movFlip = not self.movFlip
                    else:
                        self.view = self.direction + "L"
                        self.movFlip = not self.movFlip
                elif self.view == self.direction + "R":
                    self.view = self.direction + "C"
                elif self.view == self.direction + "L":
                    self.view = self.direction + "C"
                else:
                    self.view = self.direction + "C"
        if self.moving == False:
            self.view = self.direction + "C"

    @profile
    def update(self):
        py.event.pump()
        if not self.dead:
            self.pathfind()
            self.get_direction()
            self.get_view()
            self.image = self.views[self.view]
            self.image = py.transform.scale(self.image, (int(24 * v.scale), int(32 * v.scale)))
            self.rect = self.image.get_rect()
            self.stopped = False
            self.damage_knockback()
            self.rect.centerx = 640 + ((-v.playerPosX + (1 * self.posx)) * v.scale)
            self.rect.centery = 360 - ((-v.playerPosY + (1 * self.posy)) * v.scale)
            self.rect.height = 27 * v.scale
            self.rect.width = 21 * v.scale
            hitlist = list(v.hitList) + list(v.allNpc)
            top = py.Rect(self.rect.topleft, (self.rect.width, 2))
            bottom = py.Rect(self.rect.bottomleft, (self.rect.width, 2))
            left = py.Rect(self.rect.topleft, (2, self.rect.height))
            right = py.Rect(self.rect.topright, (2, self.rect.height))
            yStopped = False
            xStopped = False
            cancel = False
            for thing in hitlist:
                if thing.ID == "enemy":
                    if thing.npcID == self.npcID:
                        cancel = True
                if not cancel:
                    if bottom.colliderect(thing.rect) == True or bottom.colliderect(v.p_class.rect) == True:
                        self.posy = self.prevY
                        yStopped = True
                        
                    if top.colliderect(thing.rect) == True or top.colliderect(v.p_class.rect) == True:
                        self.posy = self.prevY
                        yStopped = True
                        
                    if left.colliderect(thing.rect) == True or left.colliderect(v.p_class.rect) == True:
                        self.posx = self.prevX
                        xStopped = True
                        
                    if right.colliderect(thing.rect) == True or right.colliderect(v.p_class.rect) == True:
                        self.posx = self.prevX
                        xStopped = True
                        
                    if xStopped and yStopped:
                        self.view = self.direction + "C"
                        self.image = self.views[self.view]
                        self.image = py.transform.scale(self.image, (int(24 * v.scale), int(32 * v.scale)))
            
            if self.invulnCooldown > 0:
                self.invulnCooldown -= 1
            elif self.invulnCooldown == 0:
                for thing in v.damagesNPCs:
                    if self.rect.colliderect(thing.rect): # TODO: Add cooldown for damage
                        self.health -= thing.master.attributes["Damage"]
                        self.knockback = thing.master.attributes["Knockback"]
                        self.invulnCooldown = (self.invulnLength * thing.master.attributes["InvulnMod"]) + 1
                        self.damaged = True
            else:
                self.invulnCooldown = 0
            
            self.attack()

        self.damage_animation()
        if self.health <= 0:
            self.dead = True
        else:
            self.healthbar()
            self.title()

        self.death()

        #self.move()

    def healthbar(self):
        if v.scale > 0.7:
            py.draw.rect(v.screen, (0,0,0), (self.rect.left, self.rect.top - (5 * v.scale), self.rect.width, 2 * v.scale))
            py.draw.rect(v.screen, (255,0,0), (self.rect.left, self.rect.top - (5 * v.scale), (self.health/self.maxHealth * self.rect.width), 2 * v.scale))
    def title(self):
        if v.scale > 0.7:
            size = self.label.get_rect().size
            v.screen.blit(self.label, (self.rect.centerx - size[0] / 2, self.rect.top - (15 * v.scale)))
    
    def attack(self):
        self.attImage = py.transform.scale(self.attImage, (int(20 * v.scale), int(20 * v.scale)))
        self.attImage.fill((255, 255, 255, 255), special_flags=py.BLEND_RGBA_MULT)

        if abs(self.posx - v.playerPosX) < 30:
            if abs(self.posy - v.playerPosY) < 30:
                if self.attCount <= -20:
                    self.attCount = int(25 * v.scale)
                    self.attPos = (v.playerPosX, v.playerPosY)
                    self.damagedPlayer = False
                    
        if self.attCount > int(-20 * v.scale):
            self.attCount -= int(1.5 * v.scale)
            self.posx = self.prevX
            self.posy = self.prevY
            self.moving = False
            v.attackerDirection = self.direction
        if self.attCount <= int(15 * v.scale) and self.attCount > int(-10 * v.scale):
            pos = (640 + int((-v.playerPosX + (self.attPos[0])) * v.scale) - self.attCount - int(10 * v.scale), 360 - int((-v.playerPosY + (self.attPos[1])) * v.scale) + self.attCount)
            v.screen.blit(self.attImage, pos)
        if abs(self.posx - v.playerPosX) < 32:
            if abs(self.posy - v.playerPosY) < 32:
                if self.attCount <= int(7.5 * v.scale) and self.damagedPlayer == False and self.attCount > int(-10 * v.scale):
                    v.playerHealth -= int(self.att)
                    self.damagedPlayer = True
    def death(self):
        if self.dead:
            v.dyingEnemies.add(self)
            self.rect.centerx = 640 + int((-v.playerPosX + (1 * self.posx)) * v.scale)
            self.rect.centery = 360 - int((-v.playerPosY + (1 * self.posy)) * v.scale)
            if self.firstDeath:
                self.damage_alpha = 255
                self.firstDeath = False
                self.oldimage = self.views["DownC"]
                self.oldimage = py.transform.scale(self.oldimage, (int(24 * v.scale), int(32 * v.scale)))
            v.particles.add(Particle((self.posx + randint(-5, 5), self.posy + randint(-5, 5)), (25, 25, 0), 2, randint(10, 20))) #TODO: scale
            self.image = self.oldimage.convert_alpha()
            self.image.fill((255, 0, 0, self.damage_alpha), special_flags=py.BLEND_RGBA_MULT)
            self.damage_alpha -= 10
            if self.damage_alpha <= 0:
                v.allNpc.remove(self)
                v.dyingEnemies.remove(self)
                orbs = randint(2, 7)
                amount = self.xp / orbs
                for i in range(orbs):
                    v.xpGroup.add(xp(self.posx + randint(-10, 10), self.posy + randint(-10, 10), amount))

    def get_direction(self):
        if self.posy - v.playerPosY < -25:
            self.direction = "Up"
        elif self.posy - v.playerPosY > 25:
            self.direction = "Down"
        elif self.posx - v.playerPosX < -25:
            self.direction = "Right"
        elif self.posx - v.playerPosX > 25:
            self.direction = "Left"

    def damage_knockback(self):
        distance = 4
        if not self.damaged:
            self.knockback = None
        elif self.knockback == "S" and self.damaged and not self.dead:
            self.stopped = True
        elif self.knockback < 1 and self.knockback > 0:
            distance = self.knockback
            self.knockback = 1
        elif self.knockback > 0 and self.damaged and not self.dead:
            self.moving = False
            self.knockback -= 1
            if self.direction == "Up":
                self.prevX = self.posx
                self.prevY = self.posy
                self.posx, self.posy = (self.prevX, self.prevY - distance)
            if self.direction == "Down":
                self.prevX = self.posx
                self.prevY = self.posy
                self.posx, self.posy = (self.prevX, self.prevY + distance)
            if self.direction == "Right":
                self.prevX = self.posx
                self.prevY = self.posy
                self.posx, self.posy = (self.prevX - distance, self.prevY)
            if self.direction == "Left":
                self.prevX = self.posx
                self.prevY = self.posy
                self.posx, self.posy = (self.prevX + distance, self.prevY)

    def damage_animation(self):
        if self.damaged and not self.dead:
            damage_image = self.image
            damage_image.fill((255, 0, 0, self.damage_alpha), special_flags=py.BLEND_RGBA_MULT)
            self.image.blit(damage_image, (0,0))
            if self.damage_fade:
                self.damage_alpha += 255 / (self.invulnLength / 2)
                if self.damage_alpha >= 255:
                    self.damage_fade = False
                    self.damage_alpha = 255
            elif not self.damage_fade:
                self.damage_alpha -= 255 / (self.invulnLength / 2)
                if self.damage_alpha <= 0:
                    self.damage_alpha = 0
                    self.damaged = False
                    self.damage_fade = True

    def pathfind(self):
        if not self.stopped:
            distance = self.speed * v.fpsAdjuster
            surrounding = []
            surrounding.append((self.posx + distance, self.posy + -distance))
            surrounding.append((self.posx + distance, self.posy + 0))
            surrounding.append((self.posx + distance, self.posy + distance))
            surrounding.append((self.posx + 0, self.posy + -distance))
            surrounding.append((self.posx + distance, self.posy + distance))
            surrounding.append((self.posx + -distance, self.posy + -distance))
            surrounding.append((self.posx + -distance, self.posy + 0))
            surrounding.append((self.posx + -distance, self.posy + distance))
    
            best = None
            bestDist = float("inf")
    
            for pos in surrounding:
                dist = math.sqrt((pos[0] - v.playerPosX)**2 + (pos[1] - v.playerPosY)**2)
                if dist < bestDist:
                    best = pos
                    bestDist = dist
    
            self.prevX = self.posx
            self.prevY = self.posy
            self.posx, self.posy = best
    
            self.moving = True
    
    
            if abs(self.posx - v.playerPosX) < 20:
                if abs(self.posy - v.playerPosY) < 20:
                    self.posx = self.prevX
                    self.posy = self.prevY
                    self.moving = False

class Particle(py.sprite.Sprite):

    def __init__(self, pos, colour, jump, life):
        super().__init__()
        self.posx, self.posy = pos
        self.colour = colour
        self.alive = True
        self.timer = life
        self.jump = jump
    def update(self):
        if self.alive:
            self.timer -= 1
            self.posx += randint(-self.jump, self.jump)
            self.posy += randint(-self.jump, self.jump)
            self.rect = py.Rect(0, 0, int(2 *v.scale), int(2 *v.scale))
            self.rect.centerx = 640 + int((-v.playerPosX + (1 * self.posx)) * v.scale)
            self.rect.centery = 360 - int((-v.playerPosY + (1 * self.posy)) * v.scale)
            py.draw.rect(v.screen, self.colour, self.rect)
            if self.timer <= 0:
                self.alive = False

class xp(py.sprite.Sprite):
    
    def __init__(self, posx, posy, amount):
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.amount = amount
        self.skin = py.image.load("Resources/Images/XPOrb.png").convert_alpha()
        v.xpGroup.add(self)
        self.wait = randint(25, 35)
        self.velocity = 1
        
    def update(self):
        self.image = py.transform.scale(self.skin, (int(8 * v.scale), int(8 * v.scale)))
        if self.wait <= 0:
            if abs(self.posx - v.playerPosX) < int(40 * v.scale):
                if abs(self.posy - v.playerPosY) < int(40 * v.scale):
                    
                    if self.posx > v.playerPosX:
                        self.posx -= self.velocity
                    if self.posx < v.playerPosX:
                        self.posx += self.velocity
                    if self.posy > v.playerPosY:
                        self.posy -= self.velocity
                    if self.posy < v.playerPosY:
                        self.posy += self.velocity
                    self.velocity += 0.2
        else:
            self.wait -= 1
        
        if abs(self.posx - v.playerPosX) < 20:
            if abs(self.posy - v.playerPosY) < 30:
                v.xpGroup.remove(self)
                v.experience["XP"] += self.amount
        
        self.rect = self.image.get_rect()
        self.rect.centerx = 640 + int((-v.playerPosX + self.posx) * v.scale)
        self.rect.centery = 360 - int((-v.playerPosY + self.posy) * v.scale)

class droppedItem(py.sprite.Sprite):
    
    def __init__(self, item=None, pos=None, blank=False):
        super().__init__()
        if not blank:
            self.newStats(item, pos)
    
    def newStats(self, item, pos):
        self.item = item
        self.posx = pos[0]
        self.posy = pos[1]
        v.droppedItems.add(self)
        self.justNear = False
    def update(self):
        self.image = py.transform.scale(self.item.icon, (int(12 * v.scale), int(12 * v.scale)))
        self.rect = self.image.get_rect()
        self.rect.centerx = 640 + int((-v.playerPosX + self.posx) * v.scale)
        self.rect.centery = 360 - int((-v.playerPosY + self.posy) * v.scale)
        actionString = "Pickup " + str(self.item.name) + " - Press F"
        if abs(self.posx - v.playerPosX) < 20:
            if abs(self.posy - v.playerPosY) < 30:
                self.justNear = True
                if not actionString in v.actionQueue:
                    v.actionQueue.append(actionString)
                for event in v.events:
                    if event.type == py.KEYDOWN:
                        if event.key == py.K_f and not "F" in v.actionsDone:
                            v.actionsDone.append("F")
                            if v.actionQueue[0] == actionString:
                                if v.inventory.add(self.item) == True:
                                    v.droppedItems.remove(self)
                                    v.actionQueue.remove(actionString)
            else:
                try:
                    if self.justNear:
                        v.actionQueue.remove(actionString)
                        self.justNear = False
                except:
                    pass
        else:
            try:
                if self.justNear:
                    v.actionQueue.remove(actionString)
                    self.justNear = False
            except:
                    pass
    
    def save(self):
        save = {"posx": self.posx,
                "posy": self.posy,
                "item": self.item.save(),
                "ID": "dropped"}
        return save
    
    def load(self, dic):
        import itemClasses
        self.posx = dic["posx"]
        self.posy = dic["posy"]
        self.item = dic["item"]
        if dic["item"]["equipType"] == "Item":
            self.item = itemClasses.item(dic["item"]["name"], dic["item"]["icon"])
        if dic["item"]["equipType"] == "Weapon":
            self.item = itemClasses.weapon(dic["item"]["name"], dic["item"]["icon"], dic["item"]["attType"], dic["item"]["image"], dic["item"]["attributes"])
        v.droppedItems.add(self)
        self.justNear = False
        
class NPC(py.sprite.Sprite):
    
    def __init__(self, pos=None, image=None, attributes={}, blank=False):
        super().__init__()
        if not blank:
            self.newStats(pos, image, attributes)
    
    def newStats(self, pos=None, image=None, attributes={}):
        self.posx = pos[0]
        self.posy = pos[1]
        self.direction = pos[2]
        self.name = attributes["Name"]
        self.sheetImage = image
        self.view = "DownC" #TODO: Direction
        self.ID = "npc"
        self.npcID = v.npcID
        v.allNpc.add(self)
        v.NPCs.add(self)
        self.initSheet()
        self.justNear = False
        self.icon = py.image.load("Resources/Images/NpcSkins/Faces/Basic_Man.png").convert_alpha()
        self.conversation = npcScripts.conversation(self, attributes["Conversation"])
        self.summonedGuard = False
        self.baseLike = attributes["Base Like"]
        self.like = self.baseLike
        self.alignment = attributes["Alignment"]
    
    def load(self, dic):
        
        self.name = dic["name"]
        self.posx = dic["posx"]
        self.posy = dic["posy"]
        self.direction = dic["direction"]
        self.view = dic["view"]
        self.sheetImage = dic["sheetImage"]
        self.ID = dic["ID"]
        self.npcID = dic["npcID"]
        self.baseLike = dic["Base Like"]
        self.like = dic["Like"]
        self.alignment = dic["Alignment"]
        
        v.allNpc.add(self)
        v.NPCs.add(self)
        self.initSheet()
        self.justNear = False
        self.icon = py.image.load("Resources/Images/NpcSkins/Faces/Basic_Man.png").convert_alpha()
        self.summonedGuard = False
        
        self.conversation = npcScripts.conversation(self, dic["conversation"], dic["convoPlace"])
        
    def save(self):
        data = {
                "conversation": self.conversation.material,
                "convoPlace": self.conversation.place,
                "name": self.name,
                "posx": self.posx,
                "posy": self.posy,
                "direction": self.direction,
                "view": self.view,
                "sheetImage": self.sheetImage,
                "ID": self.ID,
                "npcID": self.npcID,
                "baseLike": self.baseLike,
                "like": self.like,
                "alignment": self.alignment
                }
        return data
    
    def initSheet(self):
        self.sheet = SpriteSheet(self.sheetImage, 4, 3)
        self.sheet.getGrid()
        self.views = {"UpL": self.sheet.images[0],
                      "UpC": self.sheet.images[1],
                      "UpR": self.sheet.images[2],
                      "RightL": self.sheet.images[3],
                      "RightC": self.sheet.images[4],
                      "RightR": self.sheet.images[5],
                      "DownL": self.sheet.images[6],
                      "DownC": self.sheet.images[7],
                      "DownR": self.sheet.images[8],
                      "LeftL": self.sheet.images[9],
                      "LeftC": self.sheet.images[10],
                      "LeftR": self.sheet.images[11]}
        
    def get_view(self):
        for event in v.events:
            if event.type == py.USEREVENT:
                if self.view == self.direction + "C":
                    if self.movFlip:
                        self.view = self.direction + "R"
                        self.movFlip = not self.movFlip
                    else:
                        self.view = self.direction + "L"
                        self.movFlip = not self.movFlip
                elif self.view == self.direction + "R":
                    self.view = self.direction + "C"
                elif self.view == self.direction + "L":
                    self.view = self.direction + "C"
                else:
                    self.view = self.direction + "C"
        if self.moving == False:
            self.view = self.direction + "C"
    
    def title(self):
        if v.scale > 0.7:
            font = py.font.Font("Resources/Fonts/RPGSystem.ttf", int(10 * v.scale)) #TODO: Scale
            label = font.render(self.name, 1, (255,255,255))
            v.screen.blit(label, (self.rect.centerx - (font.size(self.name)[0] / 2), self.rect.top - (5 * v.scale)))
    
    def update(self):
        self.image = self.views[self.view]
        self.image = py.transform.scale(self.image, (int(24 * v.scale), int(32 * v.scale)))
        self.rect = self.image.get_rect()
        self.rect.centerx = 640 + ((-v.playerPosX + (1 * self.posx)) * v.scale)
        self.rect.centery = 360 - ((-v.playerPosY + (1 * self.posy)) * v.scale)
        self.title()
        if self.nearPlayer():
            self.talk()
        
        for thing in v.damagesNPCs:
            if self.rect.colliderect(thing.rect):
                if not self.summonedGuard:
                    npcScripts.summon("Guard", (self.posx - 50, self.posy - 50))
                    self.summonedGuard = True
    
    def nearPlayer(self):
        actionString = "Talk to " + str(self.name) + " - Press F"
        if abs(self.posx - v.playerPosX) < 20:
            if abs(self.posy - v.playerPosY) < 30:
                self.justNear = True
                if not actionString in v.actionQueue:
                    v.actionQueue.append(actionString)
                for event in v.events:
                    if event.type == py.KEYDOWN:
                        if event.key == py.K_f and not "F" in v.actionsDone:
                            v.actionsDone.append("F")
                            if v.actionQueue[0] == actionString:
                                return True
            else:
                try:
                    if self.justNear:
                        v.actionQueue.remove(actionString)
                        self.justNear = False
                except:
                    pass
        else:
            try:
                if self.justNear:
                    v.actionQueue.remove(actionString)
                    self.justNear = False
            except:
                    pass
        return False
    
    def talk(self):
        v.justPaused = True
        self.conversation.say()