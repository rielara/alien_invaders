import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_game):
        # initialising the shit and the position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.moving_right = False

        # load the ship image and get its rect
        self.image = pygame.image.load('images/spaceship.png')
        self.rect = self.image.get_rect()

        # always spawn a ship in the middle
        self.rect.midbottom = self.screen_rect.midbottom

        # start ship at bottom of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        #store a decimal value for the ship's horizontal position
        self.x = float(self.rect.x)

        # movement flags
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on movement flags."""
        # Update the ship's x value, not the rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update rect object from self.x.
        self.rect.x = self.x
        

    def blitme(self):
        # draw the ship at current location
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        # center ship on screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
