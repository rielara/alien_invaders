import pygame
from pygame.sprite import Sprite



class Alien(Sprite):
    # A class to represent a single alien in the fleet
    def __init__(self, ai_game):
        # init the alien and its starting position
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.image = pygame.image.load('images/alien.png')
        self.rect = self.image.get_rect()

    def check_edges(self):
        # return true if alien is at edge of screen
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        # move alien left or right
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x

    # Store alien's exact horizontal position
        self.x = float(self.rect.x)


