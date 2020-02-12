import pygame
import os
import random
import sprites
from config import *
os.environ['SDL_VIDEO_WINDOW_POS'] = '0,30'


class Game:# Класс игры, чтобы хранить в нём всякую всячину и функции игры
    def __init__(self):
        pygame.mixer.init()
        pygame.init()
        pygame.mixer.music.load('data/theme-remix-1.wav')
        pygame.mixer.music.play(-1)
        self.fullscreen = False
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("RPG Arena Pro: Rebirth")
        pygame.display.set_icon(sprites.load_image('icon-new.png'))
        self.clock = pygame.time.Clock()
        self.lvl = 0
        self.end = ''
        self.bg_color = (105, random.randrange(150, 255, 15), 105)
        self.next_l = 0
        self.hpx, self.hpy = 400, 400
        self.x, self.u = None, None
        self.transportC = None
        self.all_sprites = pygame.sprite.Group()
        self.player = sprites.Player(self)
        self.chst = sprites.Chest(self)
        #self.skel = Skeletron(self)
        self.running = True
        self.run()

    def run(self):# Отрисовка
        while self.running:
            self.update()
            self.draw()
            self.clock.tick(FPS)
        pygame.quit()

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_F11:
                    self.fullscreen = not self.fullscreen
                    if self.fullscreen:
                        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    else:
                        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.all_sprites.update()
    
    def draw(self):# Отрисовка
        self.screen.fill(self.bg_color)
        pygame.draw.polygon(self.screen, BLACK, [[40, 40], [WIDTH - 40, 40], [WIDTH - 40, HEIGHT - 40], [40, HEIGHT - 40]], 3)
        
        font = pygame.font.Font('data/joker.ttf', 30)
        
        # Обучение
        if self.lvl == 0:
            ui_tutorial_wasd = ui_end = font.render('Use W, A, S, D to move', 1, RED)
            self.screen.blit(ui_tutorial_wasd, (200, 100))
            
            ui_tutorial_wasd = ui_end = font.render('Use SHIFT to sprint', 1, RED)
            self.screen.blit(ui_tutorial_wasd, (200, 150))
        
        self.all_sprites.draw(self.screen)
        
        # Интерфейс
        ui_level = font.render(f'Level: {self.lvl}', 1, RED) 
        self.screen.blit(ui_level, (650, 10))
        ui_damage = font.render(f'Damage: {self.player.damage}', 1, RED)
        self.screen.blit(ui_damage, (500, 10))
        ui_armor = font.render(f'Armor: {self.player.armor}', 1, RED)
        self.screen.blit(ui_armor, (350, 10))
        ui_hp = font.render(f'Life: {self.player.life}', 1, RED)
        self.screen.blit(ui_hp, (200, 10))
        ui_money = font.render(f'Money: {self.player.money}$', 1, RED)
        self.screen.blit(ui_money, (50, 10))
        ui_end = font.render(self.end, 1, RED)
        self.screen.blit(ui_end, (300, 300))
            
        pygame.display.flip()

game = Game()