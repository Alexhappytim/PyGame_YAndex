import random

from sprites import *
from constant import *
# from levels import *


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(enemy_sprites)
        self.x, self.y = pos_x, pos_y
        # print(pos_x, pos_y)
        while pos_x - width // 2 < self.x < pos_x + width // 2 and pos_y - height // 2 < self.y < pos_y + height // 2:
            self.x = random.randrange(pos_x - width, pos_x + width)
            self.y = random.randrange(pos_x - height, pos_x + height)

        self.start_x = self.x
        self.start_y = self.y
        self.sprite = AnimatedSprite(load_image("animation/enemy/front.png"), 2, 1, self.x, self.y)
        self.rect = self.sprite.rect.move(self.x, self.y)
        self.mask = pygame.mask.from_surface(self.sprite.image)

        self.speed = 2
        self.error = 2
        self.go = 50
        self.health = 10

    def update(self, rect):
        x, y = rect.x, rect.y
        args = [[]]
        if self.x < 308:
            self.x = 308
        if self.x > 1284:
            self.x = 1284
        if self.y < 320:
            self.y = 320
        if self.y > 1279:
            self.y = 1270
        if self.x + self.go < x:
            args[0].append('d')
        elif self.x - self.go > x:
            args[0].append('a')
        if self.y + self.go < y:
            args[0].append('s')
        elif self.y - self.go > y:
            args[0].append('w')
        koef = 1
        if len(args[0]) > 1:
            koef = 3 / 4
        koef *= 0.75
        if "s" in args[0]:
            self.y += int(random.randrange(self.speed - self.error, self.speed + self.error) * koef)
        if "a" in args[0]:
            self.x -= int(random.randrange(self.speed - self.error, self.speed + self.error) * koef)
        if "d" in args[0]:
            self.x += int(random.randrange(self.speed - self.error, self.speed + self.error) * koef)
        if "w" in args[0]:
            self.y -= int(random.randrange(self.speed - self.error, self.speed + self.error) * koef)
        self.sprite.pos = (self.x, self.y)
        self.rect = self.sprite.rect
        # print(self.rect)
        # self.rect = pygame.rect.Rect(self.x, self.y, self.rect.w, self.rect.h)
        if self.health < 1:
            dx = -(rect.x + rect.w // 2 - width // 2)
            dy = -(rect.y + rect.h // 2 - height // 2)
            self.rect.x = self.rect.x + dx
            self.rect.y = self.rect.y + dy
            # print(123, self.rect)
            for player in player_group:
                player.xp += 1
            self.sprite.kill()
            self.kill()

        for player in player_group:
            if pygame.sprite.collide_mask(self, player):
                if not player.roll:
                    player.health -= 0.5
