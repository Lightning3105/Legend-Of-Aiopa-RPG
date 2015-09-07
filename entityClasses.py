import pygame as py
import Variables as v
import math
from time import sleep

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
        for event in py.event.get():
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
            self.velX = -2
        if keys_pressed[py.K_d]:
            self.velX = 2
        if keys_pressed[py.K_s]:
            self.velY = -2
        if keys_pressed[py.K_w]:
            self.velY = 2

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

    def update(self):
        for thing in v.hitList:
            if self.rect.colliderect(thing.rect):
                if self.side == "Top":
                    v.playerPosY += -2
                if self.side == "Bottom":
                    v.playerPosY += 2
                if self.side == "Left":
                    v.playerPosX += 2
                if self.side == "Right":
                    v.playerPosX += -2


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
        self.attSpeed = 8
        self.posX = v.screen.get_rect()[2] / 2
        self.posY = v.screen.get_rect()[3] / 2

    def get_rend(self):
        self.rend = py.image.load(self.image)
        self.rend = py.transform.scale(self.rend, (int(20 * v.scale), int(20 * v.scale)))

    def update(self):
        self.get_rend()
        if self.attacking:
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

    def draw(self):
        self.update()
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

    def __init__(self, posx, posy):
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.direction = None
        self.pf_been = []
        self.pf_route = []
        v.allNpc.add(self)
        #v.hitList.add(self)

    def update(self):
        #print("NX: " + str(self.posx))
        #print("NY: " + str(self.posy))
        self.image = py.Surface((30 * v.scale, 30 * v.scale))
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.centerx = v.screen.get_rect()[2] / 2 + ((-v.playerPosX + (1 * self.posx)) * v.scale)
        self.rect.centery = v.screen.get_rect()[3] / 2 - ((-v.playerPosY + (1 * self.posy)) * v.scale)

        #self.move()

    def pathfind(self):
        open = []
        closed = []
        route = []
        end = (v.playerPosX, v.playerPosY)
        curpos = (self.posx, self.posy)
        runs = 0
        self.pf_been = []
        while True:
            print(runs)
            runs += 1
            surrounding = []
            surrounding = [node for node in v.pf_nodes if 15 > math.sqrt(((curpos[0] - node[0])**2) + ((curpos[1] - node[1])**2)) and not node == curpos and not node in self.pf_been]
            #for node in v.pf_nodes:
             #   if 15 > math.sqrt(((curpos[0] - node[0])**2) + ((curpos[1] - node[1])**2)):
             #       if not node == curpos:
             #           if not node in self.pf_been:
             #               surrounding.append(node)

            best = None
            bestDist = float("inf")
            for node in surrounding:
                dist = math.sqrt((node[0] - end[0])**2 + (node[1] - end[1])**2)
                if dist < bestDist:
                    best = node
                    bestDist= dist
            self.pf_route.append(best)
            self.pf_been.append(best)
            curpos = best

            if abs(curpos[0] - v.playerPosX) < 30: #TODO Adjust For Scale
                if abs(curpos[1] - v.playerPosY) < 30:
                    print("Got To Player")
                    print(self.pf_route)
                    self.pf_been = []
                    break
            if runs > 10:
                print("Force Exit Pathfind")
                break
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



    class node():
        #TODO: Add terrain and hitboxes

        def __init__(self, start, end, pos):
            self.start = start
            self.end = end
            self.pos = pos
        def terrain(self):

            return 0

        def G(self):
            #distance from start to position
            return math.sqrt((self.start[0] - self.pos[0])**2 + (self.start[1] - self.pos[1])**2)
        def H(self):
            #distance from position to end
            return math.sqrt((self.pos[0] - self.end[0])**2 + (self.pos[1] - self.end[1])**2)
        def F(self):
            #total score - the lower the better
            return self.G() + self.H() + self.terrain()



def create_nodes():
    mapWidth = len(v.map1[0]) * (30 * v.scale)
    mapHeight = len(v.map1) * (30 * v.scale)
    accuracy = 10
    for x in range(int(mapWidth / accuracy)):
        for y in range(int(mapHeight / accuracy)):
            nodex = -(mapWidth / 2) + (x * accuracy)
            nodey = -(mapHeight / 2) + (y * accuracy)
            for spr in v.hitList:
                if spr.rect.colliderect(py.Rect(nodex, nodey, 5, 5)) == False:
                    v.pf_nodes.append((nodex, nodey))