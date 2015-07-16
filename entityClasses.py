import pygame as py

class basicSprite(py.sprite.Sprite):
    def __init__(self, image_file, location):
        py.sprite.Sprite.__init__(self)  #call Sprite initializer
        self.image = py.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """

        # Load the sprite sheet.
        self.sprite_sheet = py.image.load(file_name).convert()


    def get_image(self, x, y, width, height):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """

        # Create a new blank image
        image = py.Surface([width, height]).convert()

        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))

        # Return the image
        return image

class Player:

    def __init__(self):
        self.posx = 0
        self.posy = 0
        self.sheet = "Resources\"
        self.views = {"DownC": }