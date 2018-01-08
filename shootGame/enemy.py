import pygame
from pygame.sprite import Sprite

class Enemy(Sprite):
    '''enemy class'''

    def __init__(self, ai_settings, screen):
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load enemy image
        self.image = pygame.image.load('trump.bmp')
        self.rect = self.image.get_rect()

        # enemy initial position
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height
        self.x = float(self.rect.x)

    def blitme(self):
        '''draw enemy at certain location'''
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.x += self.ai_settings.enemy_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def check_edge(self):
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left < 0:
            return True