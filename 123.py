import pygame as pg
from pygame.math import Vector2
import os
import sys


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pg.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        pass
        # image = image.convert_alpha()

    return image


class Entity(pg.sprite.Sprite):

    def __init__(self, pos):
        super().__init__()
        self.image = load_image("animation/guns/uzi/uzi_idle_001.png")
        # A reference to the original image to preserve the quality.

        self.rect = self.image.get_rect(center=pos)
        print(self.rect)
        self.image = pg.transform.scale(self.image,
                                        (self.rect.width * 10, self.rect.height * 10))
        self.orig_image = self.image
        self.pos = Vector2(pos)  # The original center position/pivot point.
        self.offset = Vector2(50, 0)  # We shift the sprite 50 px to the right.
        self.angle = 0

    def update(self):
        self.angle += 2
        self.rotate()

    def rotate(self):
        """Rotate the image of the sprite around a pivot point."""
        # Rotate the image.
        self.image = pg.transform.rotozoom(self.orig_image, -self.angle, 1)
        # Rotate the offset vector.
        offset_rotated = self.offset.rotate(self.angle)
        # Create a new rect with the center of the sprite + the offset.
        self.rect = self.image.get_rect(center=self.pos + offset_rotated)


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()
    entity = Entity((320, 240))
    all_sprites = pg.sprite.Group(entity)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        keys = pg.key.get_pressed()
        if keys[pg.K_d]:
            entity.pos.x += 5
        elif keys[pg.K_a]:
            entity.pos.x -= 5

        all_sprites.update()
        screen.fill((30, 30, 30))
        all_sprites.draw(screen)
        pg.draw.circle(screen, (255, 128, 0), [int(i) for i in entity.pos], 3)
        pg.draw.rect(screen, (255, 128, 0), entity.rect, 2)
        pg.draw.line(screen, (100, 200, 255), (0, 240), (640, 240), 1)
        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
