import pygame
import random
import os
from config import *

def load_image(name, colorkey=None): # Функция загрузки изображения в игру
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname).convert()
    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Player(pygame.sprite.Sprite): # Класс игрока
    def __init__(self, game):
        super().__init__(game.all_sprites)
        self.game = game
        self.tik = 0 # Переменная, указывающая на то, сколько прошло времени (для анимации персонажа)
        self.lvl = 0
        self.life = 100
        self.damage = 2
        self.armor = 1
        self.money = 0
        # Инициализация используемых спрайтов
        self.image1_down = load_image('P1_down.png', -1)
        self.image2_down = load_image('P2_down.png', -1)
        self.image3_down = load_image('P3_down.png', -1)
        self.image1_up = load_image('P1_up.png', -1)
        self.image2_up = load_image('P2_up.png', -1)
        self.image3_up = load_image('P3_up.png', -1)
        self.image1_right = load_image('P1_right.png', -1)
        self.image2_right = load_image('P2_right.png', -1)
        self.image3_right = load_image('P3_right.png', -1)
        self.image1_left = load_image('P1_left.png', -1)
        self.image2_left = load_image('P2_left.png', -1)
        self.image3_left = load_image('P3_left.png', -1)
        self.image = self.image1_down
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 400
        # Инициализация движения
        self.go_up = 0
        self.go_down = 0
        self.go_left = 0
        self.go_right = 0
        self.go_fast = 0
        self.attack = None # С кем сражается персонаж
        self.alive = True # Жив ли персонаж

    def update(self):
        self.lvl = self.game.lvl
        go_fast = self.go_fast
        
        self.go_up = 0
        self.go_down = 0
        self.go_left = 0
        self.go_right = 0
        self.go_fast = 0
        # Считывание клавиш для управления
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            self.go_fast = 1
        if keys[pygame.K_a]:
            self.go_left = 1
        elif keys[pygame.K_d]:
            self.go_right = 1
        if keys[pygame.K_w]:
            self.go_up = 1
        elif keys[pygame.K_s]:
            self.go_down = 1
        
        if self.alive == True:
            self.tik += 1
            if self.tik == 41:
                self.tik = 0
            if self.go_up == 1:
                if self.tik == 10:
                    self.image = self.image2_up
                if self.tik == 20:
                    self.image = self.image1_up
                if self.tik == 30:
                    self.image = self.image3_up
                if self.tik == 40:
                    self.image = self.image1_up
                if go_fast == 1:
                    self.rect.y -= 3
                else:
                    self.rect.y -= 1
            elif self.go_down == 1:
                if self.tik == 10:
                    self.image = self.image2_down
                if self.tik == 20:
                    self.image = self.image1_down
                if self.tik == 30:
                    self.image = self.image3_down
                if self.tik == 40:
                    self.image = self.image1_down
                if go_fast == 1:
                    self.rect.y += 3
                else:
                    self.rect.y += 1
            if self.go_left == 1:
                if self.tik == 10:
                    self.image = self.image2_left
                if self.tik == 20:
                    self.image = self.image1_left
                if self.tik == 30:
                    self.image = self.image3_left
                if self.tik == 40:
                    self.image = self.image1_left
                if go_fast == 1:
                    self.rect.x -= 3
                else:
                    self.rect.x -= 1
            elif self.go_right == 1:
                if self.tik == 10:
                    self.image = self.image2_right
                if self.tik == 20:
                    self.image = self.image1_right
                if self.tik == 30:
                    self.image = self.image3_right
                if self.tik == 40:
                    self.image = self.image1_right
                if go_fast == 1:
                    self.rect.x += 3
                else:
                    self.rect.x += 1
            
            if self.rect.x < -32:
                self.game.transportC = 'l'
                self.rect.x = WIDTH - 1
                self.game.lvl += 1
                self.game.bg_color = (random.randrange(150, 255, 15), random.randrange(150, 255, 15), random.randrange(150, 255, 15))
            elif self.rect.x > WIDTH:
                self.game.transportC = 'r'
                self.rect.x = -31
                self.game.lvl += 1
                self.game.bg_color = (random.randrange(150, 255, 15), random.randrange(150, 255, 15), random.randrange(150, 255, 15))
            elif self.rect.y < -46:
                self.game.transportC = 'u'
                self.rect.y = HEIGHT - 1
                self.game.lvl += 1
                self.game.bg_color = (random.randrange(150, 255, 15), random.randrange(150, 255, 15), random.randrange(150, 255, 15))
            elif self.rect.y > HEIGHT:
                self.game.transportC = 'd'
                self.rect.y = -45
                self.game.lvl += 1
                self.game.bg_color = (random.randrange(150, 255, 15), random.randrange(150, 255, 15), random.randrange(150, 255, 15))
            
            if self.game.next_l == 2:
                self.game.transportC = None
                self.game.next_l = 0
                
        if self.life <= 0:
            self.attack = None
            self.game.end = 'Game Over!'
        if self.game.lvl == -110:
            if self.money >= 40:
                self.game.end = 'You win!'
            else:
                self.game.end = 'You lose!'
        if self.game.end != '':
            self.alive = False

class Chest(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites)
        self.game = game
        self.image = load_image('chest1.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = -1000
        self.rect.y = -1000

    def update(self):
        if self.game.player.alive == True:
            blocks_hit_list = pygame.sprite.spritecollide(self, self.game.all_sprites, False)
            if len(blocks_hit_list) > 1:
                if '[<Player sprite(in 1 groups)>, <Chest sprite(in 1 groups)>]' == str(blocks_hit_list):
                    self.rect.x = -1000
                    self.rect.y = -1000
                    if self.game.lvl // 10 == 0:
                        j = random.random()
                        if j >= 0.5:
                            rnd = random.randint(1, 100)
                            if 0 < rnd < 60:
                                self.game.x = WEAPONS_COMMON[0].split(':')
                            elif 60 < rnd < 90:
                                self.game.x = WEAPONS_COMMON[1].split(':')
                            elif 90 < rnd < 100:   
                                self.game.x = WEAPONS_COMMON[2].split(':')

                            if self.game.player.damage < int(self.game.x[1]):
                                self.game.player.damage = int(self.game.x[1])
                                print('-------------------------')
                                print(f'you picked {self.game.x[0]} with damage {self.game.x[1]}')
                                print('-------------------------')
                            elif self.game.player.damage >= int(self.game.x[1]):
                                m = (int(self.game.x[1]) // 2)
                                self.game.player.money += m
                                print('-------------------------')
                                print(f'you find {m}$')
                                print('-------------------------')
                                
                        elif j < 0.5:
                            rnd = random.randint(1, 100)
                            if 0 < rnd < 60:
                                self.game.u = ARMOR_COMMON[0].split(':')
                            elif 60 < rnd < 90:
                                self.game.u = ARMOR_COMMON[1].split(':')
                            elif 90 < rnd < 100:   
                                self.game.u = ARMOR_COMMON[2].split(':')

                            if self.game.player.armor < int(self.game.u[1]):
                                self.game.player.armor = int(self.game.u[1])
                                print('-------------------------')
                                print(f'you picked {self.game.u[0]} with protection {self.game.u[1]}')
                                print('-------------------------')
                            elif self.game.player.armor >= int(self.game.u[1]):
                                lm = (int(self.game.u[1]) // 2)
                                self.game.player.money += lm
                                print('-------------------------')
                                print(f'you find {lm}$')
                                print('-------------------------')
                    
                    if self.game.lvl // 10 == 1 or self.game.lvl == 20:
                        j = random.random()
                        if j >= 0.5:
                            rnd = random.randint(1, 100)
                            if 0 < rnd < 60:
                                self.game.x = WEAPONS_RARE[0].split(':')
                            elif 60 < rnd < 90:
                                self.game.x = WEAPONS_RARE[1].split(':')
                            elif 90 < rnd < 100:   
                                self.game.x = WEAPONS_RARE[2].split(':')

                            if self.game.player.damage < int(self.game.x[1]):
                                self.game.player.damage = int(self.game.x[1])
                                print('-------------------------')
                                print(f'you picked {self.game.x[0]} with damage {self.game.x[1]}')
                                print('-------------------------')
                            elif self.game.player.damage >= int(self.game.x[1]):
                                m = (int(self.game.x[1]) // 3)
                                self.game.player.money += m
                                print('-------------------------')
                                print(f'you find {m}$')
                                print('-------------------------')

                        elif j < 0.5:
                            rnd = random.randint(1, 100)
                            if 0 < rnd < 60:
                                self.game.u = ARMOR_RARE[0].split(':')
                            elif 60 < rnd < 90:
                                self.game.u = ARMOR_RARE[1].split(':')
                            elif 90 < rnd < 100:   
                                self.game.u = ARMOR_RARE[2].split(':')

                            if self.game.player.armor < int(self.game.u[1]):
                                self.game.player.armor = int(self.game.u[1])
                                print('-------------------------')
                                print(f'you picked {self.game.u[0]} with protection {self.game.u[1]}')
                                print('-------------------------')
                            elif self.game.player.armor >= int(self.game.u[1]):
                                lm = (int(self.game.u[1]) // 3)
                                self.game.player.money += lm
                                print('-------------------------')
                                print(f'you find {lm}$')
                                print('-------------------------')
            if self.game.transportC != None:
                self.rect.x = random.randrange(40, 730)
                self.rect.y = random.randrange(40, 730)
                self.game.next_l += 1
            
        
class Skeletron(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites)
        self.game = game
        self.image1_down = load_image('skel1_down.png', -1)
        self.image2_down = load_image('skel2_down.png', -1)
        self.image3_down = load_image('skel3_down.png', -1)
        self.image1_up = load_image('skel1_up.png', -1)
        self.image2_up = load_image('skel2_up.png', -1)
        self.image3_up = load_image('skel3_up.png', -1)
        self.image1_right = load_image('skel1_right.png', -1)
        self.image2_right = load_image('skel2_right.png', -1)
        self.image3_right = load_image('skel3_right.png', -1)
        self.image1_left = load_image('skel1_left.png', -1)
        self.image2_left = load_image('skel2_left.png', -1)
        self.image3_left = load_image('skel3_left.png', -1)
        self.image = self.image1_down
        self.rect = self.image.get_rect()
        self.rect.x = -400
        self.rect.y = -400
        self.tik = 0
        self.damage = 1
        self.armor = 1
        self.life = 5
        self.k = 0
        self.at = 0
        self.bat = 1
        self.no = 0

    def update(self):
        if self.game.player.alive == True:
            blocks_hit_list = pygame.sprite.spritecollide(self, self.game.all_sprites, False)
            if len(blocks_hit_list) > 1:
                if '[<Player sprite(in 1 groups)>, <Skeletron sprite(in 1 groups)>]' == str(blocks_hit_list):
                    self.k = 1
            else:
                self.k = 0
            
            if self.game.transportC != None:
                self.rect.x = random.randrange(40, 710)
                self.rect.y = random.randrange(40, 710)
                self.damage = (self.game.lvl // 5) + 1
                self.armor = (self.game.lvl // 10) + 1
                self.life = (self.game.lvl // 2) + 5
                self.game.next_l += 1
            
            self.tik += 1
            if self.tik == 41:
                self.tik = 0
            hpx, hpy = self.game.player.rect.x, self.game.player.rect.y
            if (self.rect.x - 250 < hpx < self.rect.x + 250 and self.rect.y - 250 < hpy < self.rect.y + 250) and self.k == 0:
                if hpx > self.rect.x:
                    self.rect.x += 1
                    if self.tik == 20:
                        self.image = self.image2_right
                    if self.tik == 40:
                        self.image = self.image3_right
                elif hpx < self.rect.x:
                    self.rect.x -= 1
                    if self.tik == 20:
                        self.image = self.image2_left
                    if self.tik == 40:
                        self.image = self.image3_left
                elif hpy > self.rect.y:
                    self.rect.y += 1
                    if self.tik == 20:
                        self.image = self.image2_down
                    if self.tik == 40:
                        self.image = self.image3_down
                elif hpy < self.rect.y:
                    self.rect.y -= 1
                    if self.tik == 20:
                        self.image = self.image2_up
                    if self.tik == 40:
                        self.image = self.image3_up
            elif self.k == 1:
                self.game.player.attack = 'skel'
                if self.game.player.attack == 'skel':
                    if self.life <= 0:
                        self.rect.x = 3000
                        self.rect.y = 3000
                        self.game.player.attack = None
                    if pygame.mouse.get_pressed() and self.bat == 1:
                        self.bat = 0
                        self.life -= self.game.player.damage
                        print('-------------------------')
                        print(f'you caused damage {self.game.player.damage}')
                        if self.life > 0:
                            print(f'enemy lives {self.life}')
                        else:
                            print(f'enemy dies')
                            print('you find 2$')
                            self.game.player.money += 2
                        print('-------------------------')
                    self.at += 1
                    if self.at == 200:
                        if self.game.player.armor > random.randint(0, 100) > 0:
                            self.game.player.life -= self.damage // 2
                            print('-------------------------')
                            print(f'you get damage {self.damage // 2}')
                            print('-------------------------')
                        else:
                            self.game.player.life -= self.damage
                            print('-------------------------')
                            print(f'you get damage {self.damage}')
                            print('-------------------------')
                        self.at = 0
                        self.bat = 1
            elif self.k == 0:
                self.game.player.attack = None
        else:
            self.image = self.image1_down