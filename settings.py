import pygame


class Settings:

    # This class stores all settings for AI

    def __init__(self):

        # Initializing game's static settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_image = pygame.image.load('images/space_background.jpg')
        self.bg_color = (0,0,0)


        # ship settings
        self.ship_limit = 3

        #bullet settings

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (232,97,0)
        self.bullet_allowed = 3

        # alien settings
        self.fleet_drop_speed = 10

        # how quickly the game speeds up
        self.speedup_scale = 1.1
        # 1 represents right, -1 represents left
        self.fleet_direction = 1
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        #Initialize settings that change throughout the game.
        self.ship_speed = 4
        self.bullet_speed = 5.0
        self.alien_speed = 2.0

        # scoring
        self.alien_points = 50

    def increase_speed(self):
        #Increase speed settings and alien point values.
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)







