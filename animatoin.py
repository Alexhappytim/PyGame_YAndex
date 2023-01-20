import pygame
import os
import sys
import math
import random
from PIL import Image

pygame.init()
size = height, width = 500, 500
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


def load_image(name, front=1, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    if front == 0:
        fullname_new = '.'.join(i for i in fullname.split('.')[:-1]) + '#.' + fullname.split('.')[-1]
        if not os.path.isfile(fullname_new):
            img = Image.open(fullname).convert('RGBA')
            pixdata = img.load()
            for y in range(img.size[1]):
                for x in range(img.size[0]):
                    alpha = pixdata[x, y][3]
                    if alpha:
                        pixdata[x, y] = (0, 0, 0, alpha)
            img.save(fullname_new)
            img.close()
        fullname = fullname_new
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
    def __init__(self, sheet, columns, rows, x, y, flipped=False, offset_x=0, offset_y=0):
        super().__init__(all_sprites)
        self.visible = True
        self.frames = []
        self.flipped1 = flipped
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.freq = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.rect = self.image.get_rect(center=(x, y))
        # служебные переменные для вращения
        self.pos = pygame.math.Vector2((x, y))
        self.offset = pygame.math.Vector2(offset_x, offset_y)
        self.angle = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(
                    pygame.transform.scale(pygame.transform.flip(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)), self.flipped1, False),
                        (self.rect.width * 3, self.rect.height * 3)))

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pygame.transform.rotozoom(self.frames[self.cur_frame], -self.angle, 1)

        # self.image = pygame.transform.scale(self.frames[self.cur_frame],
        #                                     (self.rect.width * 3, self.rect.height * 3))
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)

    def update(self):
        if self.visible:

            if self.freq == 6:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.freq = 0
            else:
                self.freq += 1

            self.rotate()
        else:
            self.freq = 6
            self.image = load_image("animation/None.png")


class Gun:
    def __init__(self, pos_x, pos_y):
        self.delta = [22, 15, 22, 15]
        self.x = pos_x + self.delta[0]
        self.y = pos_y + self.delta[1]
        self.gun_x = pos_x + self.delta[2]
        self.gun_y = pos_y + self.delta[3]
        self.start_x = pos_x
        self.start_y = pos_y
        self.cur_sprite = 0
        self.frame = 0
        self.gun_sprite = [
            AnimatedSprite(load_image("animation/guns/uzi/uzi_idle_001.png"), 1, 1, self.gun_x,
                           self.gun_y, offset_x=10),
            AnimatedSprite(load_image("animation/guns/uzi/uzi_shoot_001.png"), 1, 1, self.gun_x,
                           self.gun_y, offset_x=10),
            AnimatedSprite(load_image("animation/guns/uzi/uzi_reload_001.png"), 1, 1, self.gun_x,
                           self.gun_y, offset_x=10)
        ]
        self.rect = self.gun_sprite[0].rect.move(pos_x, pos_y)

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
            x1, y1 = pygame.mouse.get_pos()
            x1 += (x - 175)
            y1 += (y - 164)
            dx = x1+12 - self.x
            dy = y1+12 - self.y
            angle = math.degrees(math.atan2(-dy, dx) % (2 * math.pi))
            for i in self.gun_sprite:
                i.angle = -angle
            self.hand_sprite.angle = -angle

            self.x = x + self.delta[0]
            self.y = y + self.delta[1]
            self.gun_x = x + self.delta[2]
            self.gun_y = y + self.delta[3]
            self.hand_sprite.pos = (self.x, self.y)
            for i in self.gun_sprite:
                i.pos = (self.gun_x, self.gun_y)
        self.rect = pygame.rect.Rect(self.x, self.y, self.rect.w, self.rect.h)


class Player:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.start_x = pos_x
        self.start_y = pos_y
        self.sprite_shadow = [
            AnimatedSprite(load_image("animation/walking_with_weapon/back.png", front=0), 6, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/front_45.png", front=0), 6, 1, self.x,
                           self.y,
                           True),
            AnimatedSprite(load_image("animation/walking_with_weapon/front.png", front=0), 6, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/front_45.png", front=0), 6, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/back_45.png", front=0), 6, 1, self.x,
                           self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/back_45.png", front=0), 6, 1, self.x,
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

            AnimatedSprite(load_image("animation/roll/back.png", front=0), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/front_45.png", front=0), 9, 1, self.x, self.y, True),
            AnimatedSprite(load_image("animation/roll/front.png", front=0), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/front_45.png", front=0), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/back_45.png", front=0), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/back_45.png", front=0), 9, 1, self.x, self.y, True),
        ]
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
        self.rect = self.sprite[0].rect.move(pos_x, pos_y)
        self.prev_sprite = 2
        self.set_sprite(2)
        self.speed = 4
        self.roll = 0
        self.direction = None
        self.gun = Gun(self.x, self.y)

    def set_sprite(self, n):
        for i in self.sprite:
            i.visible = False
        for i in self.sprite_shadow:
            i.visible = False
        self.sprite[n].visible = True
        self.sprite_shadow[n].visible = True
        if n < 12:
            self.prev_sprite = n

    def update(self, *args):
        # TODO x1, y1 = pygame.mouse.get_pos()
        #             dx = x1+12 - self.x
        #             dy = y1+12 - self.y
        #             angle = math.degrees(math.atan2(-dy, dx) % (2 * math.pi))
        #             Слежка игрока за мышью, как и пушка
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

        else:
            koef = 1
            if len(self.direction) > 2:
                koef = koef * 3 / 4
            if "s" in self.direction:
                self.y += int(self.speed * koef)
            if "a" in self.direction:
                self.x -= int(self.speed * koef)
            if "d" in self.direction:
                self.x += int(self.speed * koef)
            if "w" in self.direction:
                self.y -= int(self.speed * koef)
            self.roll -= 1
            if self.roll == 0:
                self.direction = None
        for i in self.sprite_shadow:
            i.pos = (self.x - 10, self.y - 10)
        for i in self.sprite:
            i.pos = (self.x, self.y)
        self.rect = pygame.rect.Rect(self.x, self.y, self.rect.w, self.rect.h)
        self.gun.update(args[0], self.x, self.y, self.roll)


class Enemy:
    def __init__(self, pos_x, pos_y):
        self.x, self.y = pos_x, pos_y
        while pos_x - width // 2 < self.x < pos_x + width // 2 and pos_y - height // 2 < self.y < pos_y + height // 2:
            self.x = random.randrange(pos_x - width, pos_x + width)
            self.y = random.randrange(pos_x - height, pos_x + height)

        self.start_x = self.x
        self.start_y = self.y
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
        self.rect = self.sprite[0].rect.move(self.x, self.y)
        self.prev_sprite = 2
        self.set_sprite(2)
        self.speed = 4
        self.roll = 0
        self.direction = None

    def set_sprite(self, n):
        for i in self.sprite:
            i.visible = False
        self.sprite[n].visible = True
        if n < 12:
            self.prev_sprite = n

    def update(self, x, y):
        args = [[]]
        if self.x + 100 < x:
            args[0].append('d')
        elif self.x - 100 > x:
            args[0].append('a')
        if self.y + 100 < y:
            args[0].append('s')
        elif self.y - 100 > y:
            args[0].append('w')
        if not self.roll and not self.direction:
            koef = 1
            if len(args[0]) > 1:
                koef = 3 / 4
            koef *= 0.75
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
                i.pos = (self.x, self.y)
        else:
            koef = 1
            if len(self.direction) > 2:
                koef = koef * 3 / 4
            if "s" in self.direction:
                self.y += int(self.speed * koef)
            if "a" in self.direction:
                self.x -= int(self.speed * koef)
            if "d" in self.direction:
                self.x += int(self.speed * koef)
            if "w" in self.direction:
                self.y -= int(self.speed * koef)
            for i in self.sprite:
                i.pos = (self.x, self.y)
            self.roll -= 1
            if self.roll == 0:
                self.direction = None
        self.rect = pygame.rect.Rect(self.x, self.y, self.rect.w, self.rect.h)


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


if __name__ == '__main__' and start:
    running = True
    k = 1
    enemy = []
    for i in range(1):
        enemy.append(Enemy(50, 50))
    player = Player(50, 50)
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
        for i in enemy:
            i.update(player.x, player.y)
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)
        # pygame.draw.circle(screen, (255, 128, 0), [int(i) for i in player.gun.gun_sprite[0].pos], 3)
        # pygame.draw.circle(screen, (255, 0, 0), [int(i) for i in player.gun.hand_sprite.pos], 3)
        all_sprites.draw(screen)
        clock.tick(FPS * 10)
        print(clock.get_fps())
        pygame.display.flip()
else:
    print('Не подходит')
