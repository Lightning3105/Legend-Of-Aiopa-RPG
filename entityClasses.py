import pygame as py

screen = None

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
        self.sprite_sheet = py.image.load(file_name).convert()


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
                print(w)
                image = py.Surface([width, height], py.SRCALPHA, 32).convert_alpha()
                image.blit(self.sprite_sheet, (0, 0), (w * width, h * height, width, height))
                all.append(image)
        self.images = all


class Player:

    def __init__(self):
        self.posx = 20
        self.posy = 20
        self.direction = "Down"
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
        screen.blit(self.views[self.view], self.rect)

    def get_view(self):
        print(self.view)
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

    def move(self):
        py.event.pump()
        keys_pressed = py.key.get_pressed()
        if keys_pressed[py.K_a]:
            self.posx += -2
        if keys_pressed[py.K_d]:
            self.posx += 2
        if keys_pressed[py.K_s]:
            self.posy += 2
        if keys_pressed[py.K_w]:
            self.posy += -2

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
