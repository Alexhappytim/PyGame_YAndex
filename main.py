import pygame

from player import Player
from sprites import *
from Enemy import *
from map import *

import random
from constant import *
from strart_screen import *
from bullet import *

pygame.init()
level_x, level_y, start_x, start_y = generate_level(load_level('level/first.txt'))
start = True
player = None
pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])
time = 0.0
count_enemy = min_enemy

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
    font = pygame.font.Font(None, 40)
    text = font.render(str(fps), True, pygame.Color('green'))
    text_x = width - text.get_width()
    text_y = 0
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, pygame.Color('green'), (text_x, text_y, text_w, text_h), 1)

    text = font.render(str(int(time)), True, pygame.Color('green'))
    text_x = width - text.get_width()
    text_y = 30
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
    font = pygame.font.Font(None, 40)
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
            Enemy(start_x, start_y)
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
            # screen.fill(pygame.Color('white'))
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
                Enemy(player_group.sprites()[0].rect.x, player_group.sprites()[0].rect.y)
            ar, health = player_group.sprites()[0].update(ar)
            if health <= 0:
                raise Exception('123')
            for enemy in enemy_sprites:
                enemy.update(player_group.sprites()[0].rect)
            camera.update(player_group.sprites()[0])
            if len(ar) - ar.count('LMB') > 0:
                for sprite in tiles_group:
                    camera.apply_tiles(sprite)
            for sprite in all_sprites:
                if sprite not in tiles_group.sprites():
                    camera.apply(sprite)

            """--------------------------------------"""

            """Отладочные координаты оси вращения оружия"""
            # pygame.draw.circle(screen, (255, 128, 0), [int(i) for i in player.gun.gun_sprite[0].pos], 3)
            # pygame.draw.circle(screen, (255, 0, 0), [int(i) for i in player.gun.hand_sprite.pos], 3)
            all_sprites.draw(screen)
            all_sprites.update()
            bullet_sprites.update()
            bullet_sprites.draw(screen)

            time += 1 / FPS
            count_enemy = min(max_enemy, min_enemy + int(time) // 30)
            # print(count_enemy)

            draw_FPS(screen, round(clock.get_fps()))
            player_group.sprites()[0].draw_health(screen)
            player_group.sprites()[0].draw_xp(screen)

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
            # print(player.rect, player.visible)
            draw_counted(screen)
            player.update()
            screen.blit(player.image, (width // 2 - player.rect.w, height // 2 - player.rect.h))
            clock.tick(FPS)
            pygame.display.flip()
else:
    print('Не подходит')
