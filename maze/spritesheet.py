import pygame
 
class Sprite_sheet(object):
    """ Class used to grab images out of a sprite sheet. """
    # This points to our sprite sheet image
    sprite_sheet = None
 
    def __init__(self, file_name):
        """ Constructor. Pass in the file name  bof the sprite sheet. """
 
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()
 
 
    def get_image(self, location_rectangle):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite as an array. """
 
        # Create a new blank image
        image = pygame.Surface([location_rectangle[2], location_rectangle[3]]).convert()
 
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (location_rectangle[0], location_rectangle[1], location_rectangle[2], location_rectangle[3]))
 
        # Assuming black works as the transparent color
        # image.set_colorkey(constants.BLACK)
 
        # Return the image
        return image