from player import Player
from sprites import *

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

if __name__ == '__main__' and start:
    running = True
    player = Player(50, 50)
    size = height, weight = 1000, 1000
    screen = pygame.display.set_mode(size)
    screen.fill(pygame.Color('white'))
    all_sprites.update()
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
        """--------------------------------------"""

        """Отладочные координаты оси вращения оружия"""
        # pygame.draw.circle(screen, (255, 128, 0), [int(i) for i in player.gun.gun_sprite[0].pos], 3)
        # pygame.draw.circle(screen, (255, 0, 0), [int(i) for i in player.gun.hand_sprite.pos], 3)

        clock.tick(FPS)
        pygame.display.flip()
else:
    print('Не подходит')
