import pygame, random
from spaceship import Spaceship
from obstacle import Obstacle
from obstacle import grid
from alien import Alien
from laser import Laser
from alien import MysteryShip

pygame.init()
font1 = pygame.font.Font("Font/monogram.ttf", 40)

SHOOT_LASER = pygame.USEREVENT

class Game:
    def __init__(self, screen_width, screen_height, offset):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset = offset
        self.spaceship_group = pygame.sprite.GroupSingle()
        self.spaceship_group.add(Spaceship(self.screen_width, self.screen_height, self.offset))
        self.obstacles = self.create_obstacles()
        self.aliens_group = pygame.sprite.Group()
        self.create_aliens()
        self.aliens_direction = 1
        self.alien_lasers_group = pygame.sprite.Group()
        self.mystery_ship_group = pygame.sprite.GroupSingle()
        self.lives = 3
        self.kill_count = 0
        self.level = 1
        self.enemy_shoot_rate = 1200
        self.run = False
        self.clear = False
        self.gameover = False
        self.score = 0
        self.highscore = 0
        self.load_highscore()
        self.laser_sound = pygame.mixer.Sound("Sounds/laser.ogg")
        self.explosion_sound = pygame.mixer.Sound("Sounds/explosion.ogg")
        self.level_surface_1 = font1.render(f'LEVEL 1', False, (255,220,60))
        self.level_surface_2 = font1.render(f'LEVEL 2', False, (255,220,60))
        self.level_surface_3 = font1.render(f'LEVEL 3', False, (255,220,60))
        self.level_surface_4 = font1.render(f'LEVEL 4', False, (255,220,60))
        self.level_surface_5 = font1.render(f'LEVEL 5', False, (255,220,60))
        self.level_surface_6 = font1.render(f'LEVEL 6', False, (255,220,60))
        self.level_surface_7 = font1.render(f'LEVEL 7', False, (255,220,60))
        self.level_surface_8 = font1.render(f'LEVEL 8', False, (255,220,60))
        self.level_surface_9 = font1.render(f'LEVEL 9', False, (255,220,60))
        self.level_surface_10 = font1.render(f'LEVEL 10', False, (255,220,60))
    
    # 障害物の生成
    def create_obstacles(self):
        obstacle_width = len(grid[0]) * 3
        gap = (self.screen_width + self.offset - (4 * obstacle_width))/5
        obstacles = []
        for i in range(4):
            offset_x = (i + 1) * gap + i * obstacle_width
            obstacle = Obstacle(offset_x, self.screen_height - 100)
            obstacles.append(obstacle)
        return obstacles
    
    
    # 敵機の生成
    def create_aliens(self):
        for row in range(5):
            for column in range(11):
                x = 75 + column * 55
                y = 110 + row * 55
                
                if row == 0:
                    alien_type = 3
                elif row in (1,2):
                    alien_type = 2
                else:
                    alien_type = 1
                
                alien = Alien(alien_type, x + self.offset/2, y)
                self.aliens_group.add(alien)
    
    # 敵機の移動
    def move_aliens(self):
        self.aliens_group.update(self.aliens_direction)
        alien_sprite = self.aliens_group.sprites()
        for alien in alien_sprite:
            if alien.rect.right >= self.screen_width + self.offset/2:
                self.aliens_direction = -1
                self.alien_move_down(2)
            elif alien.rect.left <= self.offset/2:
                self.aliens_direction = 1
                self.alien_move_down(2)
                
                
    def alien_move_down(self, distance):
        if self.aliens_group:
            for alien in self.aliens_group.sprites():
                alien.rect.y += distance
    
    # 敵機の射撃処理
    def alien_shoot_laser(self):
        if self.aliens_group.sprites():
            random_alien = random.choice(self.aliens_group.sprites())
            laser_sprite = Laser(random_alien.rect.center, -6, self.screen_height)
            self.alien_lasers_group.add(laser_sprite)
            self.laser_sound.play()
            pygame.mixer.Sound.set_volume(self.laser_sound, 0.2)
            
    # 特殊機の生成
    def create_mystery_ship(self):
        self.mystery_ship_group.add(MysteryShip(self.screen_width, self.offset))
    
    # 機体とレーザーの衝突処理
    def check_for_collisions(self):
        if self.spaceship_group.sprite.lasers_group:
            for laser_sprite in self.spaceship_group.sprite.lasers_group:
                
                aliens_hit = pygame.sprite.spritecollide(laser_sprite, self.aliens_group, True)
                if aliens_hit:
                    for alien in aliens_hit:
                        self.score += alien.type * 100
                        self.check_for_highscore()
                        laser_sprite.kill()
                        self.explosion_sound.play()
                        pygame.mixer.Sound.set_volume(self.explosion_sound, 0.5)
                        self.kill_count += 1
                        if self.kill_count >= 55:
                            self.level_clear()
                
                if pygame.sprite.spritecollide(laser_sprite, self.mystery_ship_group, True):
                    self.explosion_sound.play()
                    pygame.mixer.Sound.set_volume(self.explosion_sound, 0.5)
                    self.score += 500
                    self.check_for_highscore()
                    laser_sprite.kill()
                
                # 障害物とレーザーの衝突処理
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()
                        self.explosion_sound.play()
                        pygame.mixer.Sound.set_volume(self.explosion_sound, 0.1)
           
        # 敵機のレーザー処理             
        if self.alien_lasers_group:
            for laser_sprite in self.alien_lasers_group:
                if pygame.sprite.spritecollide(laser_sprite, self.spaceship_group, False):
                    self.explosion_sound.play()
                    pygame.mixer.Sound.set_volume(self.explosion_sound, 0.8)
                    laser_sprite.kill()
                    self.lives -= 1
                    if self.lives == 0:
                        self.game_over()
                        
                # 障害物とレーザーの衝突処理
                for obstacle in self.obstacles:
                    if pygame.sprite.spritecollide(laser_sprite, obstacle.blocks_group, True):
                        laser_sprite.kill()
                        self.explosion_sound.play()
                        pygame.mixer.Sound.set_volume(self.explosion_sound, 0.1)
        
        # 敵機の障害物への衝突処理
        if self.aliens_group:
            for alien in self.aliens_group:
                for obstacle in self.obstacles:
                    pygame.sprite.spritecollide(alien, obstacle.blocks_group, True)
                    
                # 敵機のプレイヤーへの衝突処理
                if pygame.sprite.spritecollide(alien, self.spaceship_group, False):
                    self.game_over()
            
    # レベルクリア処理
    def level_clear(self):
        self.clear = True
        self.run = False
        self.level += 1
        self.enemy_shoot_rate /= 2
        pygame.time.set_timer(SHOOT_LASER, int(self.enemy_shoot_rate))
            
    # リスタート処理 (新規レベルスタート時の処理)
    def restart(self):
        self.run = True
        self.spaceship_group.sprite.restart()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.kill_count = 0
        self.clear = False
            
    # ゲームオーバー処理
    def game_over(self):
        self.gameover = True
        self.clear = False
        self.run = False
        
    # リセット処理 (ゲームオーバー時にオブジェクトやスコアなどを初期値に戻す)
    def reset(self):
        self.run = True
        self.lives = 3
        self.spaceship_group.sprite.reset()
        self.aliens_group.empty()
        self.alien_lasers_group.empty()
        self.create_aliens()
        self.mystery_ship_group.empty()
        self.obstacles = self.create_obstacles()
        self.score = 0
        self.enemy_shoot_rate = 1200
        pygame.time.set_timer(SHOOT_LASER, int(self.enemy_shoot_rate))
        self.kill_count = 0
        self.clear = False
        self.level = 1
        self.gameover = False
    
    # ハイスコア更新時のスコアをハイスコアに代入
    def check_for_highscore(self):
        if self.score > self.highscore:
            self.highscore = self.score
            # ハイスコアの値をテキストファイルに記録
            with open("highscore.txt", "w") as file:
                file.write(str(self.highscore))
    
    # ゲーム起動時にハイスコア読み込み
    def load_highscore(self):
        try:
            with open("highscore.txt", "r") as file:
                self.highscore = int(file.read())
        except FileNotFoundError:
            self.highscore = 0
            