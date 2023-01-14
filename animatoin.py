import pygame
import os
import sys

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
                self.freq = 0
            else:
                self.freq += 1
        else:
            self.freq = 6
            self.image = load_image("animation/None.png")


class Player:
    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.sprite = [
            AnimatedSprite(load_image("animation/walking_with_weapon/back.png"), 6, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/front_45.png"), 6, 1, self.x, self.y,
                           True),
            AnimatedSprite(load_image("animation/walking_with_weapon/front.png"), 6, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/front_45.png"), 6, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/back_45.png"), 6, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/walking_with_weapon/back_45.png"), 6, 1, self.x, self.y,
                           True),

            AnimatedSprite(load_image("animation/idle_with_weapon/back.png"), 6, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/idle_with_weapon/front_45.png"), 4, 1, self.x, self.y,
                           True),
            AnimatedSprite(load_image("animation/idle_with_weapon/front.png"), 6, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/idle_with_weapon/front_45.png"), 4, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/idle_with_weapon/back_45.png"), 4, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/idle_with_weapon/back_45.png"), 4, 1, self.x, self.y,
                           True),

            AnimatedSprite(load_image("animation/roll/back.png"), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/front_45.png"), 9, 1, self.x, self.y, True),
            AnimatedSprite(load_image("animation/roll/front.png"), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/front_45.png"), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/back_45.png"), 9, 1, self.x, self.y),
            AnimatedSprite(load_image("animation/roll/back_45.png"), 9, 1, self.x, self.y, True),
        ]
        # walk_w walk_a walk_s walk_d
        self.prev_sprite = 2
        self.set_sprite(2)
        self.speed = 3
        self.roll = 0
        self.direction = None

    #
    def set_sprite(self, n):
        for i in self.sprite:
            i.visible = False
        self.sprite[n].visible = True
        if n < 12:
            self.prev_sprite = n

    def update(self, *args):
        if not self.roll and not self.direction:
            if "space" in args[0]:
                self.roll = 56
                self.direction = args[0]
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
                if "s" in args[0]:
                    self.y += self.speed
                    self.set_sprite(2)
                if "a" in args[0]:
                    self.x -= self.speed
                    self.set_sprite(1)

                if "d" in args[0]:
                    self.x += self.speed
                    self.set_sprite(3)
                if "w" in args[0]:
                    self.y -= self.speed
                    if "a" in args[0] and "d" in args[0]:
                        self.set_sprite(0)
                    elif "a" in args[0]:
                        self.set_sprite(5)
                    elif "d" in args[0]:
                        self.set_sprite(4)
                    else:
                        self.set_sprite(0)

                if not args[0]:
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
            if "s" in self.direction:
                self.y += int(self.speed * 1.75)
            if "a" in self.direction:
                self.x -= int(self.speed * 1.75)
            if "d" in self.direction:
                self.x += int(self.speed * 1.75)
            if "w" in self.direction:
                self.y -= int(self.speed * 1.75)
            for i in self.sprite:
                i.rect.x = self.x
                i.rect.y = self.y
            self.roll -= 1
            if self.roll == 0:
                self.direction = None


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
        player.update(ar)
        # player.sprite.update()
        clock.tick(FPS)
        pygame.display.flip()
else:
    print('Не подходит')
