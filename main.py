from player import Player
from sprites import *
from Enemy import *
import random

pygame.init()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()


start = True
clock = pygame.time.Clock()
FPS = 60
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
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
        self.x = -target.start_x + target.x
        self.y = -target.start_y + target.y


if start:
    running = True
    enemy = []
    for i in range(10):
        enemy.append(Enemy(start_x, start_y))
    player = Player(start_x, start_y)

    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('white'))
    all_sprites.update()
    camera = Camera()
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    while running:
        screen.fill(pygame.Color('white'))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.draw(screen)
        all_sprites.update()

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
        player.update(ar)
        for i in enemy:
            i.update(player.x, player.y)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

        print(clock.get_fps())
        # print(camera.x, camera.y, player.rect)
        """--------------------------------------"""

        """Отладочные координаты оси вращения оружия"""
        # pygame.draw.circle(screen, (255, 128, 0), [int(i) for i in player.gun.gun_sprite[0].pos], 3)
        # pygame.draw.circle(screen, (255, 0, 0), [int(i) for i in player.gun.hand_sprite.pos], 3)
        all_sprites.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
else:
    print('Не подходит')
