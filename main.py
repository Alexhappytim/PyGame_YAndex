import pygame
from PIL import Image

from player import Player
from sprites import *
from Enemy import *
from map import *

import random
from constant import *
from strart_screen import *
from bullet import *
from levels import levels_dict

level_x, level_y, start_x, start_y = generate_level(load_level('level/first.txt'))
start = True
player = None
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
time = 0.0
count_enemy = min_enemy
random_ups = []

"""---------Сетап измененного курсора----------"""
f = open("data/cursor.txt")
crosshair = tuple(map(lambda x: x + " " * (24 - len(x)), f.readlines()))
cursor = pygame.cursors.compile(crosshair)
pygame.mouse.set_cursor((24, 24), (0, 0), *cursor)
"""--------------------------------------------"""


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0

    def apply(self, obj):
        screen.fill(pygame.Color('black'))
        obj.rect.x = obj.rect.x + self.dx
        obj.rect.y = obj.rect.y + self.dy

    def apply_tiles(self, obj):
        screen.fill(pygame.Color('black'))
        obj.rect.x = width // 2 + (obj.start_x - start_x) - (player_group.sprites()[0].x - start_x)
        obj.rect.y = height // 2 + (obj.start_y - start_y) - (player_group.sprites()[0].y - start_y)
        # while obj.rect.x + obj.rect.w < 0:
        #     obj.rect.x += (level_x + 1) * tile_width
        # while obj.rect.y + obj.rect.h < 0:
        #     obj.rect.y += (level_y + 1) * tile_height
        # while obj.rect.x > width:
        #     obj.rect.x -= level_x * tile_width + tile_width
        # while obj.rect.y > height:
        #     obj.rect.y -= level_y * tile_height + tile_height

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
        self.x = -target.start_x + target.x
        self.y = -target.start_y + target.y


def draw_FPS(screen, fps):
    font = pygame.font.Font("data/pix_font.ttf", 35)
    text = font.render(str(fps), True, pygame.Color('green'))
    text_x = width - text.get_width()
    text_y = 0
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, pygame.Color('green'), (text_x, text_y, text_w, text_h), 1)

    text = font.render(str(int(time)), True, pygame.Color('green'))
    text_x = width - text.get_width()
    text_y = 40
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, pygame.Color('green'), (text_x, text_y, text_w, text_h), 1)

    text = font.render(str(player_group.sprites()[0].gun.clip), True, pygame.Color('green'))
    text_x = 0
    text_y = 80
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, pygame.Color('green'), (text_x, text_y, text_w, text_h), 1)


def draw_counted(screen):
    font = pygame.font.Font("data/pix_font.ttf", 35)
    text = font.render(str(time), True, pygame.Color('red'))
    text_x = width - text.get_width()
    text_y = 0
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, pygame.Color('green'), (text_x, text_y, text_w, text_h), 1)


if start:
    health = 100
    start_screen()
    running = True
    try:
        Player(start_x, start_y)
        for i in range(10):
            Enemy(start_x, start_y, 0)
        screen.fill(pygame.Color('black'))
        all_sprites.update()
        camera = Camera()
        # print(player_group.sprites()[0])
        camera.update(player_group.sprites()[0])
        for sprite in all_sprites:
            if sprite not in tiles_group.sprites() and sprite not in xp_sprites:
                camera.apply(sprite)
            else:
                camera.apply_tiles(sprite)
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            """------Список всех нажатых кнопок------"""
            ar = []
            if pygame.key.get_pressed()[pygame.K_w]:
                ar.append("w")
            if pygame.key.get_pressed()[pygame.K_a]:
                ar.append("a")
            if pygame.key.get_pressed()[pygame.K_s]:
                ar.append("s")
            if pygame.key.get_pressed()[pygame.K_d]:
                ar.append("d")
            if pygame.key.get_pressed()[pygame.K_SPACE]:
                ar.append("space")
            if pygame.mouse.get_pressed()[0]:
                ar.append("LMB")
            if len(enemy_sprites) < count_enemy:
                Enemy(player_group.sprites()[0].rect.x, player_group.sprites()[0].rect.y, time)
            flag = False

            if player_group.sprites()[0].check_level_up():
                flag = True
                if not random_ups:
                    a = list(range(1, len(levels_dict)+1))
                    random.shuffle(a)
                    random_ups = a[:3]

            else:
                ar, health = player_group.sprites()[0].update(ar)
                if health <= 0:
                    raise Exception('123')
                for enemy in enemy_sprites:
                    enemy.update(player_group.sprites()[0].rect)
                time += 1 / FPS
            camera.update(player_group.sprites()[0])
            if len(ar) - ar.count('LMB') > 0:
                for sprite in tiles_group:
                    camera.apply_tiles(sprite)
            for sprite in all_sprites:
                if sprite not in tiles_group.sprites():
                    camera.apply(sprite)

            """--------------------------------------"""

            count_enemy = min(max_enemy, min_enemy + int(time) // 30)

            all_sprites.draw(screen)
            all_sprites.update()
            bullet_sprites.update()
            bullet_sprites.draw(screen)

            if flag:
                s = pygame.Surface((750, 750), pygame.SRCALPHA)  # per-pixel alpha
                s.fill((0,0,0, 128))  # notice the alpha value in the color
                screen.blit(s, (0, 0))

                font = pygame.font.Font("data/pix_font.ttf", 30)
                text = font.render("Новый уровень!", True, pygame.Color('white'))
                screen.blit(text, (100, 100))
                text = font.render("Выбери одно из трех.", True, pygame.Color('white'))
                screen.blit(text, (100, 130))
                text = font.render("(Что бы выбрать, нажми кнопку 1,", True, pygame.Color('white'))
                screen.blit(text, (60, 175))
                text = font.render("2 или 3 соответственно)", True,
                                   pygame.Color('white'))
                screen.blit(text, (60, 205))
                for i in range(3):
                    text = font.render(levels_dict[random_ups[i]][0], True,
                                       pygame.Color('white'))
                    screen.blit(text, (100, 260+35*i))
                if pygame.key.get_pressed()[pygame.K_1]:
                    exec(levels_dict[random_ups[0]][1])
                    flag = False
                    random_ups = []
                    player_group.sprites()[0].leveled_up = False
                elif pygame.key.get_pressed()[pygame.K_2]:
                    exec(levels_dict[random_ups[1]][1])
                    flag = False
                    random_ups = []
                    player_group.sprites()[0].leveled_up = False
                elif pygame.key.get_pressed()[pygame.K_3]:
                    exec(levels_dict[random_ups[2]][1])
                    flag = False
                    random_ups = []
                    player_group.sprites()[0].leveled_up = False


            draw_FPS(screen, round(clock.get_fps()))
            player_group.sprites()[0].draw_health(screen)
            player_group.sprites()[0].draw_xp(screen)
            sound_update()

            clock.tick(FPS)
            pygame.display.flip()

    except Exception as ex:
        print(ex)
        screen = pygame.display.set_mode(size)
        screen.fill((255, 255, 255))
        player = AnimatedSprite(load_image("animation/death/full_death.png"), 9, 1, 250, 250)
        running = True
        while running:
            screen.fill((255, 255, 255))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            draw_counted(screen)
            player.update()
            screen.blit(player.image, (width // 2 - player.rect.w, height // 2 - player.rect.h))
            clock.tick(FPS)
            pygame.display.flip()
else:
    print('Не подходит')
