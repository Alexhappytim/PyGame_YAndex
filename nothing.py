import pygame
import os
import sys

pygame.init()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

start = True
clock = pygame.time.Clock()

FPS = 50
player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    # print(type(image))
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))

tile_width = tile_height = 50
try:
    level = load_level('level/' + input())
    size = width, height = len(level[0]) * tile_width, len(level) * tile_height
except:
    start = False
    size = width, height = 50, 55

screen = pygame.display.set_mode(size)
screen.fill(pygame.Color('black'))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]
    intro_text = ["ЗАСТАВКА"]

    fon = pygame.transform.scale(load_image('decoration/pt.png'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


def generate_level(level):
    new_player, x, y = None, None, None
    x1, y1 = 0, 0
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                x1, y1 = x, y
    new_player = Player(x1, y1)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.tile_type = tile_type
        self.pos_x = pos_x
        self.pos_y = pos_y
    #
    # def update(self):
    #     self.rect.x = tile_width * self.pos_x + 15
    #     self.rect.y = tile_height * self.pos_y + 5


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.tile_type = 'player'
        self.start_x = pos_x
        self.start_y = pos_y
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.dx = 0
        self.dy = 0

    def update(self):
        self.rect.x += tile_width * self.dx
        self.rect.y += tile_height * self.dy
        self.dx = 0
        self.dy = 0


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.x = 0
        self.y = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        screen.fill(pygame.Color('black'))
        obj.rect.x = obj.rect.x + self.dx
        obj.rect.y = obj.rect.y + self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        # print(self.dx, self.dy)
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
        self.x = -target.start_x + target.pos_x
        self.y = -target.start_y + target.pos_y
        # print(self.dx, self.dy, self.x, self.y)
        # target.rect.x += self.dx
        # target.rect.y += self.dy


tile_images = {
    'wall': load_image('decoration/pt.png'),
    'empty': load_image('decoration/grass.png')
}
player_image = load_image('decoration/pt.png')


if __name__ == '__main__' and start:
    running = True
    k = 1

    start_screen()
    camera = Camera()
    player, level_x, level_y = generate_level(level)
    x, y = player.pos_x, player.pos_y
    camera.update(player)
    for sprite in all_sprites:
        camera.apply(sprite)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    y -= 1
                if event.key == pygame.K_DOWN:
                    y += 1
                if event.key == pygame.K_LEFT:
                    x -= 1
                if event.key == pygame.K_RIGHT:
                    x += 1
        if x != player.pos_x or y != player.pos_y:
            for i in all_sprites:
                if i.tile_type == 'wall' and y == i.pos_y and x == i.pos_x:
                    x = player.pos_x
                    y = player.pos_y
                    break
            else:
                if 0 <= x < len(level[0]) and 0 <= y < len(level):
                    player.dx = (x - player.pos_x)
                    player.dy = (y - player.pos_y)
                    player.pos_x = x
                    player.pos_y = y
                    player.update()
                    camera.update(player)
                    for sprite in all_sprites:
                        camera.apply(sprite)
                else:
                    x = player.pos_x
                    y = player.pos_y
        print(camera.dx, camera.dy)

        all_sprites.draw(screen)
        # all_sprites.update()
        clock.tick(FPS)
        pygame.display.flip()
else:
    print('Не подходит')
