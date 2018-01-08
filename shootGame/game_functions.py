import sys
import pygame
from time import sleep
from bullet import Bullet
from enemy import Enemy



def check_keydown_events(event, ai_settings, screen, tank, bullets):
    if event.key == pygame.K_RIGHT:
        tank.moving_right = True
    elif event.key == pygame.K_LEFT:
        tank.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, tank, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, tank):
    if event.key == pygame.K_RIGHT:
        tank.moving_right = False
    elif event.key == pygame.K_LEFT:
        tank.moving_left = False

def check_events(ai_settings, screen, stats, scoreboard, btn_play, tank, enemies, bullets):
    '''keyboard and mouse events'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, tank, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, tank)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_btn_play(ai_settings, screen, stats, scoreboard, btn_play, tank, enemies, bullets, mouse_x, mouse_y)

def check_btn_play(ai_settings, screen, stats, scoreboard, btn_paly, tank, enemies, bullets, mouse_x, mouse_y):
    '''click on the play btn to start'''
    buttob_clicked = btn_paly.rect.collidepoint(mouse_x, mouse_y)
    if buttob_clicked and not stats.game_active:
        # make mouse point invisible
        pygame.mouse.set_visible(False)
        # reset game settings
        ai_settings.initialize_dynamic_settings()

        stats.reset_stats()
        stats.game_active = True
        scoreboard.prep_level()
        scoreboard.prep_high_score()
        scoreboard.prep_score()
        scoreboard.prep_tanks()

        enemies.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, tank, enemies)
        tank.center_tank()

def update_screen(ai_settings, screen, stats, scoreboard, tank, enemies, bullets, btn_play):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    tank.blitme()
    enemies.draw(screen)
    # show the score
    scoreboard.show_score()
    # update the display
    if not stats.game_active:
        btn_play.draw_button()
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, scoreboard, tank, bullets, enemies):

    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_enemy_collisions(ai_settings, screen, stats, scoreboard, tank, bullets, enemies)


    #print(len(bullets))

def check_bullet_enemy_collisions(ai_settings, screen, stats, scoreboard, tank, bullets, enemies):
    collisions = pygame.sprite.groupcollide(bullets, enemies, True, True)
    if collisions:
        for enemies in collisions.values():
            stats.score += ai_settings.enemy_points*len(enemies)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)
    #print('Enemies left ' + str(len(enemies)))
    if len(enemies) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, tank, enemies)

        # increase the level
        stats.level += 1
        scoreboard.prep_level()

def fire_bullets(ai_settings, screen, tank, bullets):
    if len(bullets) < ai_settings.bullets_number:
        new_bullet = Bullet(ai_settings, screen, tank)
        bullets.add(new_bullet)

def create_fleet(ai_settings, screen, tank, enemies):
    '''create enemies fleet'''
    enemy = Enemy(ai_settings, screen)
    enemies_number_col = get_enemies_number_x(ai_settings, enemy.rect.width)
    enemies_number_row = get_enemies_number_y(ai_settings, tank.rect.height, enemy.rect.height)
    # add new enemy after checking the width
    for col_number in range(enemies_number_col):
        for row_number in range(enemies_number_row):
            create_enemy(ai_settings, screen, enemies, col_number, row_number)

def get_enemies_number_x(ai_settings, enemy_width):
    available_space_x = ai_settings.screen_width - 2 * enemy_width
    enemies_number_col = int(available_space_x / enemy_width)
    #print(ai_settings.screen_width, enemy_width, enemies_number_col)
    return enemies_number_col

def create_enemy(ai_settings, screen, enemies, enemies_number_col, enemies_number_row):
    enemy = Enemy(ai_settings, screen)
    enemy_width = enemy.rect.width
    enemy.x = enemy_width + enemy_width * enemies_number_col
    enemy.y = enemy.rect.height + enemy.rect.height * enemies_number_row
    enemy.rect.x = enemy.x
    enemy.rect.y = enemy.y
    enemies.add(enemy)

def get_enemies_number_y(ai_settings, tank_height, enemy_height):
    available_space_y = ai_settings.screen_height - 3 * enemy_height - tank_height
    enemies_number_row = int(available_space_y / enemy_height)
    #print(ai_settings.screen_height, enemy_height, enemies_number_row, tank_height)
    return enemies_number_row

def check_fleet_edges(ai_settings, enemies):
    for enemy in enemies.sprites():
        if enemy.check_edge():
            change_fleet_direction(ai_settings, enemies)
            break

def change_fleet_direction(ai_settings, enemies):
    for enemy in enemies.sprites():
        enemy.rect.y += ai_settings.fleet_speed_factor
    ai_settings.fleet_direction *= -1

def update_enemies(ai_settings, stats, scoreboard, screen, tank, enemies, bullets):
    check_fleet_edges(ai_settings, enemies)
    enemies.update()
    # check thge collision of tank and enemies
    if pygame.sprite.spritecollideany(tank, enemies):
        print('tank crushed!!!')
        tank_hit(ai_settings, stats, scoreboard, screen, tank, enemies, bullets)
    check_enemies_bottom(ai_settings, stats, scoreboard, screen, tank, enemies, bullets)

def tank_hit(ai_settings, stats, scoreboard, screen, tank, enemies, bullets):
    ''' tank hited by enemies'''
    if stats.tanks_left > 0:
        stats.tanks_left -= 1
        # update scoreboard
        scoreboard.prep_tanks()

        enemies.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, tank, enemies)
        tank.center_tank()
        # pause for a while
        sleep(0.5)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_enemies_bottom(ai_settings, stats, scoreboard, screen, tank, enemies, bullets):
    '''when enemies touch the bottom'''
    screen_rect = screen.get_rect()
    for enemy in enemies.sprites():
        if enemy.rect.bottom >= screen_rect.bottom:
            tank_hit(ai_settings, stats, scoreboard, screen, tank, enemies, bullets)
            break

def check_high_score(stats, scoreboard):
    '''check whether this is the highest score'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()