import pygame as py
import Variables as v
import math
import time
from random import randint

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
        self.sprite_sheet = py.image.load(file_name).convert_alpha()


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
        self.posx = v.screen.get_rect()[2] / 2
        self.posy = v.screen.get_rect()[3] / 2
        self.direction = "Down"
        v.playerDirection = self.direction
        self.moving = False
        self.view = "DownC"
        self.sheetImage = "Resources\Images"


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
    def draw(self):
        self.set_rect()
        self.get_view()
        skin = self.views[self.view]
        size = skin.get_rect()
        image = py.transform.scale(skin, (int(size.width * v.scale), int(size.height * v.scale)))
        self.rect.centerx = self.posx
        self.rect.centery = self.posy
        v.screen.blit(image, self.rect)

    def get_view(self):
        for event in v.events:
            if event.type == py.USEREVENT:
                if self.view == self.direction + "C":
                    self.view = self.direction + "R"
                elif self.view == self.direction + "R":
                    self.view = self.direction + "L"
                elif self.view == self.direction + "L":
                    self.view = self.direction + "R"
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

    def move(self):
        if not v.playerStopped:
            py.event.pump()
            moveRight = True
            moveLeft = True
            moveUp = True
            moveDown = True
            preX = v.playerPosX
            preY = v.playerPosY
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
                self.velX = -v.playerSpeed
            if keys_pressed[py.K_d]:
                self.velX = v.playerSpeed
            if keys_pressed[py.K_s]:
                self.velY = -v.playerSpeed
            if keys_pressed[py.K_w]:
                self.velY = v.playerSpeed

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

            #print("\n", self.velX, self.velY)

            for hit in v.hits:
                self.velX, self.velY = hit.update((self.velX, self.velY))

            #print(self.velX, self.velY)

            v.playerPosX += self.velX
            v.playerPosY += self.velY
            v.playerDirection = self.direction



            """for wall in v.hitList:
                if self.rect.colliderect(wall.rect):
                    print("COLLIDE")
                    if self.rect.right > wall.rect.left:
                        v.playerPosX = preX
                        self.draw()"""


class HitBox(py.sprite.Sprite):

    def __init__(self, x, y, w, h, side):
        super().__init__()
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.side = side
        self.rect = py.Rect(x, y, w, h)
        self.image = py.Surface((w, h))
        self.image.fill((255, 0, 0))

    def draw(self):
        py.draw.rect(v.screen, (255, 0, 0), self.rect)

    def update(self, velocity): # use new positition
        velX, velY = velocity
        newrect = self.rect
        hit = False
        for thing in v.hitList:
            if newrect.colliderect(thing.rect):
                hit = True
        for thing in v.allNpc:
            if newrect.colliderect(thing.rect):
                hit = True
        if hit:
            if self.side == "Top":
                velY += -v.playerSpeed
            if self.side == "Bottom":
                velY += v.playerSpeed
            if self.side == "Left":
                velX += v.playerSpeed
            if self.side == "Right":
                velX += -v.playerSpeed
        return velX, velY


class Tile(py.sprite.Sprite):

    def __init__(self, tilePosition, skin, terrain, wall=False):
        super().__init__()
        self.tilePosX = tilePosition[0]
        self.tilePosY = tilePosition[1]
        self.posX = 0
        self.posY = 0
        self.skin = skin
        self.wall = wall
        if wall:
            v.hitList.add(self)
        v.allTiles.add(self)

    def draw(self):
        self.set_rect()
        v.screen.blit(self.rend, self.rect)

    def update(self):
        self.image = py.transform.scale(self.skin, (int(30 * v.scale), int(30 * v.scale)))
        self.rect = self.image.get_rect()
        self.rect.centerx = v.screen.get_rect()[2] / 2 + ((-v.playerPosX + (30 * self.tilePosX)) * v.scale)
        self.rect.centery = v.screen.get_rect()[3] / 2 + ((v.playerPosY + (30 * self.tilePosY)) * v.scale)
        #self.rect.width = self.rect.width * v.scale
        #self.rect.height = self.rect.height * v.scale


class Sword:

    def __init__(self):
        self.image = None
        self.attacking = False
        self.attCyclePos = 0
        self.attSpeed = 16
        self.posX = v.screen.get_rect()[2] / 2
        self.posY = v.screen.get_rect()[3] / 2

    def get_rend(self):
        self.rend = py.image.load(self.image)
        self.rend = py.transform.scale(self.rend, (int(20 * v.scale), int(20 * v.scale)))

    def update(self):
        self.get_rend()
        if self.attacking:
            v.playerAttacking = True
            v.playerStopped = True
            if v.playerDirection == "Up":
                angleMod = -90
            elif v.playerDirection == "Down":
                angleMod = 90
            elif v.playerDirection == "Left":
                angleMod = 0
            elif v.playerDirection == "Right":
                angleMod = 180
            if self.attCyclePos == 0:
                self.rect = self.rend.get_rect()
                self.rect.center = (self.posX, self.posY)
                self.rend = rot_center(self.rend, angleMod + 180)
                self.rect.center = arc((centre()[0], centre()[1]), 20 * v.scale, angleMod)
                self.attCyclePos += self.attSpeed
            else:
                self.rend = rot_center(self.rend, angleMod + 180 - self.attCyclePos)
                self.rect.center = arc((centre()[0], centre()[1]), 20 * v.scale, angleMod - self.attCyclePos)
                self.attCyclePos += self.attSpeed
                if self.attCyclePos > 180:
                    self.attacking = False
                    self.attCyclePos = 0
        else:
            self.rend = None
            self.rect = None
            v.playerAttacking = False
            v.playerStopped = False

    def draw(self):
        #self.update()
        if self.attacking:
            v.screen.blit(self.rend, self.rect)

def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
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
    return v.screen.get_rect()[2] / 2, v.screen.get_rect()[3] / 2

class NPC(py.sprite.Sprite):

    def __init__(self, posx, posy, health):
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.direction = "Down"
        self.view = "DownC"
        self.moving = False
        self.pf_tried = []
        self.sheetImage = "Resources/Images/Generic Goblin.png"
        self.maxHealth = health
        self.health = health
        self.invulnCooldown = 0
        self.invulnLength = 30
        self.damaged = False
        self.damage_alpha = 0
        self.damage_fade = False
        self.dead = False
        self.firstDeath = True
        self.particles = py.sprite.Group()
        v.allNpc.add(self)
        self.initSheet()
        #v.hitList.add(self)

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
        #print(self.direction)
        #print(self.view)
        for event in v.events:
            if event.type == py.USEREVENT:
                if self.view == self.direction + "C":
                    self.view = self.direction + "R"
                elif self.view == self.direction + "R":
                    self.view = self.direction + "L"
                elif self.view == self.direction + "L":
                    self.view = self.direction + "R"
                else:
                    self.view = self.direction + "C"
        if self.moving == False:
            self.view = self.direction + "C"


    def update(self):
        #print("NX: " + str(self.posx))
        #print("NY: " + str(self.posy))
        py.event.pump()
        if not self.dead:
            self.pathfind()
            self.get_direction()
            self.get_view()
            self.image = self.views[self.view]
            self.image = py.transform.scale(self.image, (int(24 * v.scale), int(32 * v.scale)))
            self.rect = self.image.get_rect()
            self.damage_knockback()
            self.rect.centerx = v.screen.get_rect()[2] / 2 + ((-v.playerPosX + (1 * self.posx)) * v.scale)
            self.rect.centery = v.screen.get_rect()[3] / 2 - ((-v.playerPosY + (1 * self.posy)) * v.scale)
            for thing in v.hitList:
                if self.rect.colliderect(thing.rect) == True or self.rect.colliderect(v.p_class.rect) == True:
                    self.posx = self.prevX
                    self.posy = self.prevY
                    self.pf_tried.append((self.posx, self.posy))
                    self.moving = False
                    self.view = self.direction + "C"
                    self.image = self.views[self.view]
                    self.image = py.transform.scale(self.image, (int(24 * v.scale), int(32 * v.scale)))
            if self.invulnCooldown > 0:
                self.invulnCooldown -= 1
            elif self.invulnCooldown == 0:
                if v.playerAttacking:
                    if self.rect.colliderect(v.cur_weapon.rect): # TODO: Add cooldown for damage
                        self.health -= 2
                        self.invulnCooldown = self.invulnLength
                        self.damaged = True
            else:
                self.invulnCooldown = 0

        self.damage_animation()
        if self.health <= 0:
            self.dead = True
        else:
            self.healthbar()

        self.death()




        #self.move()

    def healthbar(self):
        py.draw.rect(v.screen, (0,0,0), (self.rect.left, self.rect.top - 10, self.rect.width, 3))
        py.draw.rect(v.screen, (255,0,0), (self.rect.left, self.rect.top - 10, (self.health/self.maxHealth * self.rect.width), 3))
    def death(self):
        if self.dead:
            self.rect.centerx = v.screen.get_rect()[2] / 2 + ((-v.playerPosX + (1 * self.posx)) * v.scale)
            self.rect.centery = v.screen.get_rect()[3] / 2 - ((-v.playerPosY + (1 * self.posy)) * v.scale)
            if self.firstDeath:
                self.damage_alpha = 255
                self.firstDeath = False
                self.oldimage = self.views["DownC"]
                self.oldimage = py.transform.scale(self.oldimage, (int(24 * v.scale), int(32 * v.scale)))
            v.particles.add(Particle((self.posx + randint(-5, 5), self.posy + randint(-5, 5)), (25, 25, 0), 2, randint(10, 20)))
            self.image = self.oldimage.convert_alpha()
            self.image.fill((255, 0, 0, self.damage_alpha), special_flags=py.BLEND_RGBA_MULT)
            #self.image.blit(damage_image, (0,0))
            self.damage_alpha -= 10
            print(self.damage_alpha)
            if self.damage_alpha <= 0:
                v.allNpc.remove(self)
                print("Killed")

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
        if self.damage_fade and self.damaged and not self.dead:
            self.moving = False
            if self.direction == "Up":
                self.prevX = self.posx
                self.prevY = self.posy
                self.posx, self.posy = (self.prevX, self.prevY - 4)
            if self.direction == "Down":
                self.prevX = self.posx
                self.prevY = self.posy
                self.posx, self.posy = (self.prevX, self.prevY + 4)
            if self.direction == "Right":
                self.prevX = self.posx
                self.prevY = self.posy
                self.posx, self.posy = (self.prevX - 4, self.prevY)
            if self.direction == "Left":
                self.prevX = self.posx
                self.prevY = self.posy
                self.posx, self.posy = (self.prevX + 4, self.prevY)

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

        surrounding = []
        surrounding.append((self.posx + 1, self.posy + -1))
        surrounding.append((self.posx + 1, self.posy + 0))
        surrounding.append((self.posx + 1, self.posy + 1))
        surrounding.append((self.posx + 0, self.posy + -1))
        surrounding.append((self.posx + 1, self.posy + 1))
        surrounding.append((self.posx + -1, self.posy + -1))
        surrounding.append((self.posx + -1, self.posy + 0))
        surrounding.append((self.posx + -1, self.posy + 1))

        if len(self.pf_tried) == len(surrounding):
            self.pf_tried = []

        best = None
        bestDist = float("inf")

        for pos in surrounding:
            dist = math.sqrt((pos[0] - v.playerPosX)**2 + (pos[1] - v.playerPosY)**2)
            if dist < bestDist:
                if not pos in self.pf_tried:
                    best = pos
                    bestDist = dist

        self.prevX = self.posx
        self.prevY = self.posy
        self.posx, self.posy = best

        self.moving = True



        if abs(self.posx - v.playerPosX) < 30:
            if abs(self.posy - v.playerPosY) < 40:
                self.posx = self.prevX
                self.posy = self.prevY
                self.moving = False

        """if abs(curpos[0] - v.playerPosX) < 30: #TODO Adjust For Scale
            if abs(curpos[1] - v.playerPosY) < 30:
                print("Got To Player")
                print(self.pf_route)
                self.pf_been = []
                break
        if runs > 10:
            print("Force Exit Pathfind")
            break"""
    def move(self):
        try:
            end = (v.playerPosX, v.playerPosY)
            surrounding = []
            surrounding.append((self.posx + 1, self.posy + -1))
            surrounding.append((self.posx + 1, self.posy + 0))
            surrounding.append((self.posx + 1, self.posy + 1))
            surrounding.append((self.posx + 0, self.posy + -1))
            surrounding.append((self.posx + 1, self.posy + 1))
            surrounding.append((self.posx + -1, self.posy + -1))
            surrounding.append((self.posx + -1, self.posy + 0))
            surrounding.append((self.posx + -1, self.posy + 1))
            best = None
            bestDist = float("inf")
            for pos in surrounding:
                dist = math.sqrt((pos[0] - self.pf_route[0][0])**2 + (pos[1] - self.pf_route[0][1])**2)
                if dist < bestDist:
                    best = pos
                    bestDist = dist

            self.posx = best[0]
            self.posy = best[1]
            if math.sqrt((self.posx - self.pf_route[0][0])**2 + (self.posy - self.pf_route[0][1])**2) < 2:
                self.pf_route.pop(0)
        except:
            self.pathfind()

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
                self.rect = py.Rect(0, 0, 2 *v.scale, 2 *v.scale)
                self.rect.centerx = v.screen.get_rect()[2] / 2 + ((-v.playerPosX + (1 * self.posx)) * v.scale)
                self.rect.centery = v.screen.get_rect()[3] / 2 - ((-v.playerPosY + (1 * self.posy)) * v.scale)
                py.draw.rect(v.screen, self.colour, self.rect)
                if self.timer <= 0:
                    self.alive = False