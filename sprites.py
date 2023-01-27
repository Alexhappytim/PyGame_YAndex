import os
import sys
import pygame
from PIL import Image

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
bullet_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()
gun_sprites = pygame.sprite.Group()
xp_sprites = pygame.sprite.Group()


def rot_center(image, rect, angle):
    """Вращение спрайта с сохранением центра"""
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = rot_image.get_rect(center=rect.center)
    return rot_image, rot_rect


def load_image(name, front=1, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    if front == 0:
        fullname_new = '.'.join(i for i in fullname.split('.')[:-1]) + '#.' + fullname.split('.')[
            -1]
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
    return image


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, flipped=False, offset_x=0, offset_y=0, scale=3):
        super().__init__(all_sprites)

        self.visible = True
        self.flipped = flipped
        self.rot_flip = False

        self.frames = []
        self.cut_sheet(sheet, columns, rows, scale=scale)
        self.cur_frame = 0
        self.freq = 0

        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect(center=(x, y))

        # служебные переменные для вращения
        self.pos = pygame.math.Vector2(x, y)
        self.offset = pygame.math.Vector2(offset_x, offset_y)
        self.angle = 0

    def cut_sheet(self, sheet, columns, rows, scale=3):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(
                    pygame.transform.scale(pygame.transform.flip(sheet.subsurface(pygame.Rect(
                        frame_location, self.rect.size)), self.flipped, False),
                        (self.rect.width * scale, self.rect.height * scale)))
        self.frames = self.frames * (36 // len(self.frames))

    def rotate(self):
        """Вращение спрайта вокруг определенной точки"""
        self.image = pygame.transform.rotozoom(
            pygame.transform.flip(self.frames[self.cur_frame], False, self.rot_flip),
            -self.angle, 1)
        offset_rotated = self.offset.rotate(self.angle)
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)

    def update(self):
        if self.visible:
            # TODO Менять фреймрейт анимации в зависимости от колва кадров
            if self.freq == 6:
                self.cur_frame = (self.cur_frame + 1) % len(self.frames)
                self.freq = 0
            else:
                self.freq += 1
            self.rotate()
        else:
            self.freq = 6
            self.image = load_image("animation/None.png")
