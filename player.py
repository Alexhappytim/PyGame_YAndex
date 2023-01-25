from gun import Gun
from sprites import *
import math
from Enemy import size, height, width, start_x, start_y


class Player:

    def __init__(self, pos_x, pos_y):
        self.x = pos_x
        self.y = pos_y
        self.start_x = pos_x
        self.start_y = pos_y
        self.sprite_shadow = []
        self.sprite = []
        self.image = [["animation/walking_with_weapon/back.png", 6, 1, False],
                      ["animation/walking_with_weapon/front_45.png", 6, 1, True],
                      ["animation/walking_with_weapon/front.png", 6, 1, False],
                      ["animation/walking_with_weapon/front_45.png", 6, 1, False],
                      ["animation/walking_with_weapon/back_45.png", 6, 1, False],
                      ["animation/walking_with_weapon/back_45.png", 6, 1, True],
                      ["animation/idle_with_weapon/back.png", 6, 1, False],
                      ["animation/idle_with_weapon/front_45.png", 4, 1, True],
                      ["animation/idle_with_weapon/front.png", 6, 1, False],
                      ["animation/idle_with_weapon/front_45.png", 4, 1, False],
                      ["animation/idle_with_weapon/back_45.png", 4, 1, False],
                      ["animation/idle_with_weapon/back_45.png", 4, 1, True],
                      ["animation/roll/back.png", 9, 1, False],
                      ["animation/roll/front_45.png", 9, 1, True],
                      ["animation/roll/front.png", 9, 1, False],
                      ["animation/roll/front_45.png", 9, 1, False],
                      ["animation/roll/back_45.png", 9, 1, False],
                      ["animation/roll/back_45.png", 9, 1, True]
                      ]
        for i in self.image:
            print(i)
            self.sprite_shadow.append(
                AnimatedSprite(load_image(i[0], front=0), i[1], i[2], self.x, self.y, i[3],
                               scale=3.5))
            self.sprite.append(
                AnimatedSprite(load_image(i[0]), i[1], i[2], self.x, self.y, i[3], scale=3))

        self.cur_sprite = 2
        self.set_sprite(2)
        self.speed = 4
        self.roll = 0
        self.rect = self.sprite[0].rect.move(pos_x, pos_y)
        self.direction = None
        self.gun = Gun(self.x, self.y)

    def set_sprite(self, n):
        for _ in [self.sprite, self.sprite_shadow]:
            for i in _:
                i.visible = False
        self.sprite[n].visible = True
        self.sprite_shadow[n].visible = True
        self.cur_sprite = n

    def update(self, *args):
        # Почистим массив кнопок от противоположных
        if 's' in args[0] and 'w' in args[0]:
            del args[0][args[0].index('w')]
            del args[0][args[0].index('s')]
        if 'a' in args[0] and 'd' in args[0]:
            del args[0][args[0].index('a')]
            del args[0][args[0].index('d')]

        # Развилка, в перекате ли мы
        if not self.roll and not self.direction:
            # Проверка, войти ли в перекат
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
                # Движение
                if len(args[0]) > 1:
                    koef = 3 / 4
                if "s" in args[0]:
                    self.y += int(self.speed * koef)
                if "a" in args[0]:
                    self.x -= int(self.speed * koef)
                if "d" in args[0]:
                    self.x += int(self.speed * koef)
                if "w" in args[0]:
                    self.y -= int(self.speed * koef)

                x1, y1 = pygame.mouse.get_pos()
                x1 += (self.x - height // 2 + start_x)
                y1 += (self.y - width // 2 + start_y)

                dx = x1 + 12 - self.x
                dy = y1 + 12 - self.y
                angle = math.degrees(math.atan2(-dy, dx) % (2 * math.pi))
                if 0 <= angle <= 45:
                    self.set_sprite(4)
                elif 45 < angle <= 135:
                    self.set_sprite(0)
                elif 135 < angle <= 180:
                    self.set_sprite(5)
                elif 180 < angle <= 240:
                    self.set_sprite(1)
                elif 240 < angle <= 300:
                    self.set_sprite(2)
                elif 300 < angle < 360:
                    self.set_sprite(3)

                # Спрайты на АФК
                if not args[0] or (len(args[0]) == 1 and "LMB" in args[0]):
                    if self.cur_sprite == 0 or self.cur_sprite == 12:
                        self.set_sprite(6)
                    if self.cur_sprite == 1 or self.cur_sprite == 13:
                        self.set_sprite(7)
                    if self.cur_sprite == 2 or self.cur_sprite == 14:
                        self.set_sprite(8)
                    if self.cur_sprite == 3 or self.cur_sprite == 15:
                        self.set_sprite(9)
                    if self.cur_sprite == 4 or self.cur_sprite == 16:
                        self.set_sprite(10)
                    if self.cur_sprite == 5 or self.cur_sprite == 17:
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
            for i in self.sprite:
                i.pos = (self.x, self.y)
            self.roll -= 1
            if self.roll == 0:
                self.direction = None
        for i in self.sprite_shadow:
            i.pos = (self.x - 1, self.y - 1)
        for i in self.sprite:
            i.pos = (self.x, self.y)
        self.rect = pygame.rect.Rect(self.x, self.y, self.rect.w, self.rect.h)
        self.gun.update(args[0], self.x, self.y, self.roll)
