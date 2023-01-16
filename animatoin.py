import pygame
import os
import sys
import math

pygame.init()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()

start = True
clock = pygame.time.Clock()

FPS = 60
player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

# курсор вот так вот смешно делается
crosshair = (
    "      XXXXXXXXXX        ",
    "      XXXXXXXXXX        ",
    "    XX..........XX      ",
    "    XX..........XX      ",
    "  XX..XXXX..XXXX..XX    ",
    "  XX..XXXX..XXXX..XX    ",
    "XX..XX    XX    XX..XX  ",
    "XX..XX    XX    XX..XX  ",
    "XX..XX    XX    XX..XX  ",
    "XX..XX    XX    XX..XX  ",
    "XX....XXXX  XXXX....XX  ",
    "XX....XXXX  XXXX....XX  ",
    "XX..XX    XX    XX..XX  ",
    "XX..XX    XX    XX..XX  ",
    "XX..XX    XX    XX..XX  ",
    "XX..XX    XX    XX..XX  ",
    "  XX..XXXX..XXXX..XX    ",
    "  XX..XXXX..XXXX..XX    ",
    "    XX..........XX      ",
    "    XX..........XX      ",
    "      XXXXXXXXXX        ",
    "      XXXXXXXXXX        ",
    "                        ",
    "                        ",
)

cursor = pygame.cursors.compile(crosshair)
pygame.mouse.set_cursor((24, 24), (0, 0), *cursor)


def rot_center(image, rect, angle):
    """rotate an image while keeping its center"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


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
        pass
        # image = image.convert_alpha()

    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, flipped=False):
        super().__init__(all_sprites)
        self.visible = True
        self.frames = []
        self.flipped1 = flipped
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.freq = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.angle = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(pygame.transform.flip(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)), self.flipped1, False))

    def update(self):
        if self.visible:
            if self.freq == 6:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.image = pygame.transform.scale(self.frames[self.cur_frame],
                                                    (self.rect.width * 3, self.rect.height * 3))
                self.image = pygame.transform.rotate(self.image, self.angle)
                self.freq = 0
            else:
                self.freq += 1
        else:
            self.freq = 6
            self.image = load_image("animation/None.png")


class Gun:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x + 37
        self.y = pos_y + 45
        self.gun_x = pos_x + 33
        self.gun_y = pos_y + 34
        self.cur_sprite = 0
        self.frame = 0
        self.gun_sprite = [
            AnimatedSprite(load_image("animation/guns/uzi/uzi_idle_001.png"), 1, 1, self.gun_x,
                           self.gun_y),
            AnimatedSprite(load_image("animation/guns/uzi/uzi_shoot_001.png"), 1, 1, self.gun_x,
                           self.gun_y),
            AnimatedSprite(load_image("animation/guns/uzi/uzi_reload_001.png"), 1, 1, self.gun_x,
                           self.gun_y)
        ]
        self.hand_sprite = AnimatedSprite(load_image("animation/guns/hand.png"), 1, 1, self.gun_x,
                                          self.gun_y)
        self.set_sprite(0)

    def set_sprite(self, n):
        if self.frame == 5:
            for i in self.gun_sprite:
                i.visible = False
            self.gun_sprite[n].visible = True
            self.cur_sprite = n
            self.frame = 0
        else:
            self.frame += 1

    def update(self, args, x, y, is_rolling):
        if "LMB" in args:
            if self.cur_sprite:
                self.set_sprite(0)
            else:
                self.set_sprite(1)
        else:
            self.set_sprite(0)
        if is_rolling:
            self.hand_sprite.visible = False
            for i in self.gun_sprite:
                i.visible = False
        else:
            self.hand_sprite.visible = True
            self.set_sprite(self.cur_sprite)
            for i in self.gun_sprite:
                a, b = pygame.mouse.get_pos()
                if (b - self.y) != 0:
                    angle = math.asin((a - self.x) / ((b - self.y) ** 2 + (a - self.x) ** 2) ** (
                                1 / 2)) / math.pi * 180
                    i.angle = angle
                    print(angle)

            self.x = x + 37
            self.y = y + 45
            self.gun_x = x + 33
            self.gun_y = y + 34
            self.hand_sprite.rect.x = self.x
            self.hand_sprite.rect.y = self.y
            for i in self.gun_sprite:
                i.rect.x = self.gun_x
                i.rect.y = self.gun_y


class Player:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.sprite = [
            AnimatedSprite(load_image("animation/walking_with_weapon/back.png"), 6, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/front_45.png"), 6, 1, self.x,
                           self.y,
                           True),
            AnimatedSprite(load_image("animation/walking_with_weapon/front.png"), 6, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/front_45.png"), 6, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/back_45.png"), 6, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/back_45.png"), 6, 1, self.x,
                           self.y,
                           True),

            AnimatedSprite(load_image("animation/idle_with_weapon/back.png"), 6, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/idle_with_weapon/front_45.png"), 4, 1, self.x,
                           self.y,
                           True),
            AnimatedSprite(load_image("animation/idle_with_weapon/front.png"), 6, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/idle_with_weapon/front_45.png"), 4, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/idle_with_weapon/back_45.png"), 4, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/idle_with_weapon/back_45.png"), 4, 1, self.x,
                           self.y,
                           True),

            AnimatedSprite(load_image("animation/roll/back.png"), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/front_45.png"), 9, 1, self.x, self.y, True),
            AnimatedSprite(load_image("animation/roll/front.png"), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/front_45.png"), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/back_45.png"), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/back_45.png"), 9, 1, self.x, self.y, True),
        ]
        self.prev_sprite = 2
        self.set_sprite(2)
        self.speed = 4
        self.roll = 0
        self.direction = None
        self.gun = Gun(self.x, self.y)

    #
    def set_sprite(self, n):
        for i in self.sprite:
            i.visible = False
        self.sprite[n].visible = True
        if n < 12:
            self.prev_sprite = n

    def update(self, *args):

        if 's' in args[0] and 'w' in args[0]:
            del args[0][args[0].index('w')]
            del args[0][args[0].index('s')]
        if 'a' in args[0] and 'd' in args[0]:
            del args[0][args[0].index('a')]
            del args[0][args[0].index('d')]
        if not self.roll and not self.direction:
            if "space" in args[0] and (
                    "w" in args[0] or "a" in args[0] or "s" in args[0] or "d" in args[0]):
                self.roll = 56
                self.direction = args[0]
                if self.direction:
                    if "LBM" in self.direction:
                        self.direction.remove("LBM")
                    if "space" in self.direction:
                        self.direction.remove("space")
                if "w" in args[0] and "d" in args[0]:
                    self.set_sprite(16)
                elif "w" in args[0] and "a" in args[0]:
                    self.set_sprite(17)
                elif "w" in args[0]:
                    self.set_sprite(12)
                elif "a" in args[0]:
                    self.set_sprite(13)
                elif "d" in args[0]:
                    self.set_sprite(15)
                elif "s" in args[0]:
                    self.set_sprite(14)
            else:
                koef = 1
                if len(args[0]) > 1:
                    koef = 3 / 4
                if "s" in args[0]:
                    self.y += int(self.speed * koef)
                    self.set_sprite(2)
                if "a" in args[0]:
                    self.x -= int(self.speed * koef)
                    self.set_sprite(1)

                if "d" in args[0]:
                    self.x += int(self.speed * koef)
                    self.set_sprite(3)
                if "w" in args[0]:
                    self.y -= int(self.speed * koef)
                    if "a" in args[0] and "d" in args[0]:
                        self.set_sprite(0)
                    elif "a" in args[0]:
                        self.set_sprite(5)
                    elif "d" in args[0]:
                        self.set_sprite(4)
                    else:
                        self.set_sprite(0)

                if not args[0] or (len(args[0]) == 1 and "LMB" in args[0]):
                    if self.prev_sprite == 0 or self.prev_sprite == 12:
                        self.set_sprite(6)
                    if self.prev_sprite == 1 or self.prev_sprite == 13:
                        self.set_sprite(7)
                    if self.prev_sprite == 2 or self.prev_sprite == 14:
                        self.set_sprite(8)
                    if self.prev_sprite == 3 or self.prev_sprite == 15:
                        self.set_sprite(9)
                    if self.prev_sprite == 4 or self.prev_sprite == 16:
                        self.set_sprite(10)
                    if self.prev_sprite == 5 or self.prev_sprite == 17:
                        self.set_sprite(11)

                for i in self.sprite:
                    i.rect.x = self.x
                    i.rect.y = self.y
        else:
            # TODO Баг - противоположные кнопки
            koef = 1

            if len(self.direction) > 2:
                koef = koef * 3 / (4)
            if "s" in self.direction:
                self.y += int(self.speed * koef)
                # print(koef, self.speed, int(self.speed * koef), self.direction)
            if "a" in self.direction:
                self.x -= int(self.speed * koef)
            if "d" in self.direction:
                self.x += int(self.speed * koef)
            if "w" in self.direction:
                self.y -= int(self.speed * koef)
            for i in self.sprite:
                i.rect.x = self.x
                i.rect.y = self.y
            self.roll -= 1
            if self.roll == 0:
                self.direction = None
        self.gun.update(args[0], self.x, self.y, self.roll)


if __name__ == '__main__' and start:
    running = True
    k = 1
    all_sprites = pygame.sprite.Group()
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
        # player.sprite.update()
        clock.tick(FPS)
        pygame.display.flip()
else:
    print('Не подходит')
