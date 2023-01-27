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
        screen.fill(pygame.Color('white'))
        obj.rect.x = obj.rect.x + self.dx
        obj.rect.y = obj.rect.y + self.dy

    def apply_tiles(self, obj):
        screen.fill(pygame.Color('white'))
        obj.rect.x = width // 2 + (obj.start_x - start_x) - (player.x - start_x)
        obj.rect.y = height // 2 + (obj.start_y - start_y) - (player.y - start_y)
        while obj.rect.x + obj.rect.w < 0:
            obj.rect.x += (level_x + 1) * tile_width
        while obj.rect.y + obj.rect.h < 0:
            obj.rect.y += (level_y + 1) * tile_height
        while obj.rect.x > width:
            obj.rect.x -= level_x * tile_width + tile_width
        while obj.rect.y > height:
            obj.rect.y -= level_y * tile_height + tile_height

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
        self.x = -target.start_x + target.x
        self.y = -target.start_y + target.y


def draw_FPS(screen, fps):
    font = pygame.font.Font(None, 40)
    text = font.render(str(fps), True, (0, 0, 0))
    text_x = width - text.get_width()
    text_y = 0
    text_w = text.get_width()
    text_h = text.get_height()
    screen.blit(text, (text_x, text_y))
    pygame.draw.rect(screen, (0, 0, 0), (text_x, text_y,
                                           text_w, text_h), 1)


if start:
    start_screen()
    running = True
    for i in range(10):
        Enemy(start_x, start_y)
    player = Player(start_x, start_y)
    screen.fill(pygame.Color('white'))
    all_sprites.update()
    camera = Camera()
    camera.update(player)
    for sprite in all_sprites:
        if sprite not in tiles_group.sprites():
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
        ar = player.update(ar)
        for enemy in enemy_sprites:
            enemy.update(player.x, player.y)
        camera.update(player)
        if len(ar) - ar.count('LMB') > 0:
            for sprite in tiles_group:
                camera.apply_tiles(sprite)
        for sprite in all_sprites:
            if sprite not in tiles_group.sprites():
                camera.apply(sprite)

        # print(clock.get_fps())
        # print(camera.x, camera.y, player.rect, player.start_x, player.start_y, player.x, player.y)

        # print(camera.dx, camera.dy, tiles_group.sprites()[0].rect, tiles_group.sprites()[0].start_x)
        # print(player.rect, tiles_group.sprites()[0].rect)
        # print(tiles_group.sprites())
        # for i in all_sprites:
        #     if i == all_sprites.sprites()
        #     print(i)
        """--------------------------------------"""

        """Отладочные координаты оси вращения оружия"""
        # pygame.draw.circle(screen, (255, 128, 0), [int(i) for i in player.gun.gun_sprite[0].pos], 3)
        # pygame.draw.circle(screen, (255, 0, 0), [int(i) for i in player.gun.hand_sprite.pos], 3)
        all_sprites.draw(screen)
        all_sprites.update()
        bullet_sprites.update()
        bullet_sprites.draw(screen)
        draw_FPS(screen, round(clock.get_fps()))
        player.draw_health(screen)
        clock.tick(FPS)
        pygame.display.flip()
        print('enemy', len(enemy_sprites))
else:
    print('Не подходит')
