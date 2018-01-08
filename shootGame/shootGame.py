import sys
import pygame
from settings import Settings
from tank import Tank
import game_functions as gf
from pygame.sprite import Group
from enemy import Enemy
from button import Button
from game_stats import Game_stats
from scoreboard import Scoreboard

def run_game():
    # initiate a screen object
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Shoot Trump, Save the World')

    # create play button
    btn_play = Button(ai_settings, screen, 'Play')

    # create a tank
    tank = Tank(ai_settings, screen)
    # create bullet group
    bullets = Group()
    # create enemy
    enemies = Group()
    gf.create_fleet(ai_settings, screen, tank, enemies)
    # create game stats instance
    stats =Game_stats(ai_settings)
    scoreboard = Scoreboard(ai_settings, screen, stats)

    # game main loop
    while True:
        # moniter keyboard and mouse event
        gf.check_events(ai_settings, screen, stats, scoreboard, btn_play, tank, enemies, bullets)
        if stats.game_active:
            tank.update()
            gf.update_bullets(ai_settings, screen, stats, scoreboard, tank, bullets, enemies)
            gf.update_enemies(ai_settings, stats, scoreboard, screen, tank, enemies, bullets)

        gf.update_screen(ai_settings, screen, stats, scoreboard, tank, enemies, bullets, btn_play)
            #print(len(enemies))


run_game()
