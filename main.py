import pygame, sys, random
from game import Game

pygame.init()

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 700
OFFSET = 50

font1 = pygame.font.Font("Font/monogram.ttf", 40)
font2 = pygame.font.Font("Font/monogram.ttf", 80)

level_clear_surface = font2.render("LEVEL CLEAR", False, (255,255,255))
start_key_surface = font2.render("Press (N) key to Start", False, (255,255,255))
continue_key_surface = font1.render("Press (N) key to Continue", False, (255,255,255))
game_over_surface = font2.render("GAME OVER", False, (255,50,50))
restart_key_surface = font2.render("Press (N) key to Restart", False, (255,255,255))
score_text_surface = font1.render("SCORE", False, (200,180,90))
highscore_text_surface = font1.render("HIGH SCORE", False, (200,180,90))

screen = pygame.display.set_mode((SCREEN_WIDTH + OFFSET, SCREEN_HEIGHT + 2*OFFSET))
pygame.display.set_caption("Space Invaders 2")

clock = pygame.time.Clock()

game = Game(SCREEN_WIDTH, SCREEN_HEIGHT, OFFSET)

pygame.init()

SHOOT_LASER = pygame.USEREVENT
pygame.time.set_timer(SHOOT_LASER, int(game.enemy_shoot_rate))

MYSTERYSHIP = pygame.USEREVENT + 1
pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SHOOT_LASER and game.run:
            game.alien_shoot_laser()

        if event.type == MYSTERYSHIP and game.run:
            game.create_mystery_ship()
            pygame.time.set_timer(MYSTERYSHIP, random.randint(4000,8000))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_n] and game.run == False and game.clear == True:
            game.restart()
        elif keys[pygame.K_n] and game.run == False and game.gameover == True:
            game.reset()
        elif keys[pygame.K_n] and game.run == False:
            game.reset()

    # 更新（gameのrunがTrueの間だけ）
    if game.run:
        game.spaceship_group.update()
        game.move_aliens()
        game.alien_lasers_group.update()
        game.mystery_ship_group.update()
        game.check_for_collisions()

    ## 描画 ##
    screen.fill((25,25,23))
    
    # UI
    pygame.draw.rect(screen, (200,180,90), (10,10,780,780),2,0,60,60,60,60)
    pygame.draw.line(screen, (200,180,90), (25,730), (775,730), 3)
    
    if game.run:
        pass
    elif game.clear:
        screen.blit(level_clear_surface, ((SCREEN_WIDTH + OFFSET)/2 - 170, SCREEN_HEIGHT/2 - 100))
        screen.blit(continue_key_surface, ((SCREEN_WIDTH + OFFSET)/2 - 170 - 20, SCREEN_HEIGHT/2 - 100 + 100))
    elif game.gameover:
        screen.blit(game_over_surface, ((SCREEN_WIDTH + OFFSET)/2 - 170 + 20,720,50,50))
        screen.blit(restart_key_surface, (40,50,50,50))
    else:
        screen.blit(start_key_surface, (70,450,50,50))
    x = 50
    for life in range(game.lives):
        screen.blit(game.spaceship_group.sprite.image, (x, 745))
        x += 50
    
    # レベル表示
    if game.level == 1:
        screen.blit(game.level_surface_1, (570,740,50,50))
    elif game.level == 2:
        screen.blit(game.level_surface_2, (570,740,50,50))
    elif game.level == 3:
        screen.blit(game.level_surface_3, (570,740,50,50))
    elif game.level == 4:
        screen.blit(game.level_surface_4, (570,740,50,50))
    elif game.level == 5:
        screen.blit(game.level_surface_5, (570,740,50,50))
    elif game.level == 6:
        screen.blit(game.level_surface_6, (570,740,50,50))
    elif game.level == 7:
        screen.blit(game.level_surface_7, (570,740,50,50))
    elif game.level == 8:
        screen.blit(game.level_surface_8, (570,740,50,50))
    elif game.level == 9:
        screen.blit(game.level_surface_9, (570,740,50,50))
    elif game.level == 10:
        screen.blit(game.level_surface_10, (570,740,50,50))
            
    screen.blit(score_text_surface, (50,15,50,50))
    formatted_score = str(game.score).zfill(5)
    score_surface = font1.render(formatted_score, False, (200,180,90))
    screen.blit(score_surface, (50,40,50,50))
    screen.blit(highscore_text_surface, (600,15,50,50))
    formatted_highscore = str(game.highscore).zfill(5)
    highscore_surface = font1.render(formatted_highscore, False, (200,180,90))
    screen.blit(highscore_surface, (675,40,50,50))
    
    game.spaceship_group.draw(screen)
    game.spaceship_group.sprite.lasers_group.draw(screen)
    for obstacle in game.obstacles:
        obstacle.blocks_group.draw(screen)
    game.aliens_group.draw(screen)
    game.alien_lasers_group.draw(screen)
    game.mystery_ship_group.draw(screen)
    
    pygame.display.update()
    clock.tick(60)