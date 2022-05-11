import sys
from time import sleep
import pygame
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
import sound_effects as se
from explosion_group import Explosion




class AlienInvasion:
    # Overall class to manage game assets and behaviour

    def __init__(self):
        # Initialising the game and creating resources
        pygame.init()
        self.settings = Settings()

        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        

        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )
        # self.screen to make it available to all methods in the class
        pygame.display.set_caption("Alien Invasion")
        self.bg_image = pygame.image.load("images/space_background.jpg")
        self.bg_image = pygame.transform.smoothscale(
            self.settings.bg_image, self.screen.get_size()
        )    
        # create instance to store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self._create_fleet()

        # make play button
        self.play_button = Button(self, "Play")

        self.explosion_group = pygame.sprite.Group()


    def run_game(self):
        # Starting the main loop for the game
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
        se.background_sound.play()


    def _check_events(self):
        # Respond to keypresses and mouse events.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        # Start a new game when the player clicks Play
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            self.stats.reset_stats()

            # Reset the game settings.          
            self.settings.initialize_dynamic_settings()

            # hide mouse cursor
            pygame.mouse.set_visible(False)

            #get rid of any remaining aliens + bullets
            self.aliens.empty()
            self.bullets.empty()

            # create new fleet + center the ship
            self._create_fleet()
            self.ship.center_ship()

            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()


            
    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            # self.ship.rect.x  = 1
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        # Create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        # update bullet position
        self.bullets.update()

        # Get rid of old bullets
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
                


        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # respond to bullet-alien collision
        # check for bullets that have hit aliens
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points
                explosion = Explosion(aliens[0].rect.centerx, aliens[0].rect.centery)
                self.explosion_group.add(explosion)          

            self.sb.prep_score()
            self.sb.check_high_score()
            se.alien_sound.play()

        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # inc level
            self.stats.level += 1
            self.sb.prep_level()

    def _fire_bullet(self):
        # create a new bullet and add it to the bullets group
        if len(self.bullets) < self.settings.bullet_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

            se.bullet_sound.play()

    def _update_aliens(self):
        # check if the fleet is at an edge, then update the position of all aliens in the fleet
        self._check_fleet_edges()
        self.aliens.update()

        # look out for alien/ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # look for aliens hitting bottom of screen
        self._check_aliens_bottom()


    def _check_aliens_bottom(self):
        # check if alien reached bottom of the screen

        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                #treat the same as if ship got hit
                self._ship_hit()
                break 


    def _ship_hit(self):
        # resp to ship being hit
        if self.stats.ships_left > 0:

        #decrement ships left + update scoreboard
            self.stats.ships_left -= 1 
            self.sb.prep_ships()

        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
            

        #get rid of any remaining aliens or bullets
        self.aliens.empty()
        self.bullets.empty()

        #create new fleet and center the ship
        self._create_fleet()
        self.ship.center_ship()
        se.hit_sound.play()

        #pause
        sleep(0.5)

    def _create_fleet(self):
        # Create an alien and find the number of aliens in a row.
        # Spacing between each alien is equal to one alien width.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        # Determine the number of rows of aliens that fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        #Create an alien and place it in the row.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = (alien.rect.height + 50) + 2 * alien.rect.height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        # respond appropriately if any aliens have reached an edge
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break


    def _change_fleet_direction(self):
        # drop the entire fleet & change direction
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1 


    def _update_screen(self):
        # update images on the screen   flip to the new screen
        self.screen.blit(self.settings.bg_image, (0, 0))
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen)
        self.explosion_group.draw(self.screen)
        self.explosion_group.update()

        # draw the score info
        self.sb.show_score()

        # Draw the play button if the game is inactive.
        if not self.stats.game_active:
            self.play_button.draw_button()

        # Making the most recently drawn screen visible
        self.ship.blitme()


        pygame.display.flip()


if __name__ == "__main__":
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()
