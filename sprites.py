import pygame
import random
import math
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
        self.hp = 20
        self.max_hp = 20
        self.damage = 2
        self.armor = 1
        self.money = 0
        # Инициализация используемых спрайтов
        self.image1_down = load_image(CHARSET + '1_down.png', -1)
        self.image2_down = load_image(CHARSET + '2_down.png', -1)
        self.image3_down = load_image(CHARSET + '3_down.png', -1)
        self.image1_up = load_image(CHARSET + '1_up.png', -1)
        self.image2_up = load_image(CHARSET + '2_up.png', -1)
        self.image3_up = load_image(CHARSET + '3_up.png', -1)
        self.image1_right = load_image(CHARSET + '1_right.png', -1)
        self.image2_right = load_image(CHARSET + '2_right.png', -1)
        self.image3_right = load_image(CHARSET + '3_right.png', -1)
        self.image1_left = load_image(CHARSET + '1_left.png', -1)
        self.image2_left = load_image(CHARSET + '2_left.png', -1)
        self.image3_left = load_image(CHARSET + '3_left.png', -1)
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
        self.target = None # С кем сражается персонаж
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
        
        if self.alive:
            self.tik = (self.tik + 1) % 41
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
                self.rect.x = WIDTH - 1
                self.game.next_level()
            elif self.rect.x > WIDTH:
                self.rect.x = -31
                self.game.next_level()
            elif self.rect.y < -46:
                self.rect.y = HEIGHT - 1
                self.game.next_level()
            elif self.rect.y > HEIGHT:
                self.rect.y = -45
                self.game.next_level()
        loot_hits = pygame.sprite.spritecollide(self, self.game.loots, False)
        if loot_hits:
            loot_hits[0].loot()
        
        enemy_hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if enemy_hits:
            enemy_hits[0].in_fight = True
            enemy_hits[0].sleeping = True
        
        if self.hp > self.max_hp:
            self.hp = self.max_hp
        
        if self.hp <= 0:
            self.hp = 0
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
        self.game.loots.add(self)
        self.image = load_image(CHARSET + '_chest.png', -1)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(40, 731)
        self.rect.y = random.randrange(40, 531)

    def loot(self):
        if random.random() <= 1 - (self.game.lvl * 0.05): # Шанс выпадения редкого предмета
            if random.random() >= 0.5: # Броня или оружие
                pool = WEAPONS_COMMON
            else:
                pool = ARMOR_COMMON
        else:
            if random.random() >= 0.5:
                pool = WEAPONS_RARE
            else:
                pool = ARMOR_RARE
        chance = int(random.random() * (len(pool) - 1)) # Выбор предмета из определённого множества
        found_item = pool[chance].split(':')
        if pool in [WEAPONS_COMMON, WEAPONS_RARE]:
            if self.game.player.damage < int(found_item[1]):
                self.game.player.damage = int(found_item[1])
                self.game.console(f"You've found {found_item[0]}, which has {found_item[1]} damage.")
            else:
                self.game.player.money += int(found_item[1])
                self.game.console(f"You've found {found_item[1]}$")
        else:
            if self.game.player.armor < int(found_item[1]):
                self.game.player.armor = int(found_item[1])
                self.game.console(f"You've found {found_item[0]}, which has {found_item[1]} armor.")
            else:
                self.game.player.money += int(found_item[1])
                self.game.console(f"You've found {found_item[1]}$.")
        self.kill()


class Mushroom(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites)
        self.game = game
        self.game.loots.add(self)
        self.image1 = load_image(CHARSET + '1_mushroom.png', -1)
        self.image2 = load_image(CHARSET + '2_mushroom.png', -1)
        self.image3 = load_image(CHARSET + '3_mushroom.png', -1)
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(40, 744)
        self.rect.y = random.randrange(40, 544)
        self.tik = 0
    
    def update(self):
        self.tik = (self.tik + 1) % 31
        if self.tik == 0:
            self.image = self.image1
        if self.tik == 10:
            self.image = self.image2
        if self.tik == 20:
            self.image = self.image3
    
    def loot(self):
        healed = (self.game.lvl // 5) + random.randint(1, 5)
        self.game.player.hp += healed
        self.game.console(f"You've found a mushroom which restored {healed} of your health.")
        self.kill()

        
class Skeleton(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__(game.all_sprites)
        self.game = game
        self.game.enemies.add(self)
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
        self.rect.x = random.randrange(40, 728)
        self.rect.y = random.randrange(40, 514)
        self.damage = (self.game.lvl // 5) + 1
        self.armor = (self.game.lvl // 10) + 1
        self.hp = (self.game.lvl // 2) + 5
        self.tik = 0
        
        self.at = 0
        self.bat = 1
        
        self.sleeping = True
        self.in_fight = False

    def update(self):
        if not self.game.player.alive:
            self.kill()
        target_x, target_y = self.game.player.rect.x, self.game.player.rect.y
        if math.sqrt((self.rect.x - target_x) ** 2 + (self.rect.y - target_y) ** 2) <= 200 and self.sleeping:
            self.sleeping = False
        if (not self.sleeping) and (not self.in_fight):
            self.tik = (self.tik + 1) % 41
            if target_x > self.rect.x:
                self.rect.x += 1
                if self.tik == 0:
                    self.image = self.image1_right
                if self.tik == 20:
                    self.image = self.image2_right
                if self.tik == 40:
                    self.image = self.image3_right
            elif target_x < self.rect.x:
                self.rect.x -= 1
                if self.tik == 0:
                    self.image = self.image1_left
                if self.tik == 20:
                    self.image = self.image2_left
                if self.tik == 40:
                    self.image = self.image3_left
            if target_y > self.rect.y:
                self.rect.y += 1
                if self.tik == 0:
                    self.image = self.image1_down
                if self.tik == 20:
                    self.image = self.image2_down
                if self.tik == 40:
                    self.image = self.image3_down
            elif target_y < self.rect.y:
                self.rect.y -= 1
                if self.tik == 0:
                    self.image = self.image1_up
                if self.tik == 20:
                    self.image = self.image2_up
                if self.tik == 40:
                    self.image = self.image3_up
        elif self.in_fight:
            if self.hp <= 0:
                self.kill()
                self.game.player.target = None
            if pygame.mouse.get_pressed() and self.bat == 1:
                self.bat = 0
                self.hp -= self.game.player.damage
                print('-------------------------')
                print(f'you caused damage {self.game.player.damage}')
                if self.hp > 0:
                    print(f'enemy lives {self.hp}')
                else:
                    print('enemy dies')
                    loot = (self.game.lvl // 2) + random.randint(2, 4)
                    self.game.player.money += loot
                    self.game.console(f"You've found {loot}$.")
            self.at += 1
            if self.at == 200:
                if self.game.player.armor > random.randint(0, 100) > 0:
                    self.game.player.hp -= self.damage // 2
                    print('-------------------------')
                    print(f'you get damage {self.damage // 2}')
                    print('-------------------------')
                else:
                    self.game.player.hp -= self.damage
                    print('-------------------------')
                    print(f'you get damage {self.damage}')
                    print('-------------------------')
                self.at = 0
                self.bat = 1
        else:
            self.game.player.target = None