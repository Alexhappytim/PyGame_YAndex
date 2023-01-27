import math
from sprites import *
from constant import *
from bullet import *

start_x, start_y = None, None


class Gun(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(gun_sprites)
        self.delta = [0, 15]
        self.x = pos_x + self.delta[0]
        self.y = pos_y + self.delta[1]
        self.gun_x = pos_x + self.delta[0]
        self.gun_y = pos_y + self.delta[1]
        self.start_x = pos_x
        self.start_y = pos_y
        self.cur_sprite = 0
        self.frame = 0
        self.gun_sprite = [
            AnimatedSprite(load_image("animation/guns/uzi/uzi_idle_001.png"), 1, 1, self.gun_x,
                           self.gun_y, offset_x=50),
            AnimatedSprite(load_image("animation/guns/uzi/uzi_shoot_001.png"), 1, 1, self.gun_x,
                           self.gun_y, offset_x=50),
            AnimatedSprite(load_image("animation/guns/uzi/uzi_reload_001.png"), 1, 1, self.gun_x,
                           self.gun_y, offset_x=50)
        ]
        self.rect = self.gun_sprite[0].rect.move(pos_x, pos_y)
        self.hand_sprite = AnimatedSprite(load_image("animation/guns/hand.png"), 1, 1, self.gun_x,
                                          self.gun_y, offset_x=40)
        self.set_sprite(0)
        self.delay = 0

    def set_sprite(self, n):
        """Смена спрайта на n-ый по счету в своем списке"""
        if self.frame == 5:
            for i in self.gun_sprite:
                i.visible = False
            self.gun_sprite[n].visible = True
            self.cur_sprite = n
            self.frame = 0
        else:
            self.frame += 1

    def update(self, args, rect, is_rolling):
        if "LMB" in args:
            if self.cur_sprite:
                self.set_sprite(0)
            else:
                self.set_sprite(1)

            x1, y1 = pygame.mouse.get_pos()
            x1 += (rect.x - width // 2 + 50)
            y1 += (rect.y - height // 2 + 50)
            dx = x1 + 12 - self.x
            dy = y1 + 12 - self.y
            angle = math.degrees(math.atan2(-dy, dx) % (2 * math.pi))
            if self.delay == 5:
                Bullet(math.cos(angle * math.pi / 180), math.sin(angle * math.pi / 180), rect)
                self.delay = 0
            else:
                self.delay += 1
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
            # print(x1, y1)
            x1 += (rect.x - width // 2 + 50)
            y1 += (rect.y - height // 2 + 50)
            dx = x1 + 12 - self.x
            dy = y1 + 12 - self.y
            angle = math.degrees(math.atan2(-dy, dx) % (2 * math.pi))
            for i in self.gun_sprite:
                i.angle = -angle
                i.rot_flip = 90 <= abs(angle) <= 270
            self.hand_sprite.angle = -angle

            self.x = rect.x + self.delta[0]
            self.y = rect.y + self.delta[1]
            self.gun_x = rect.x + self.delta[0]
            self.gun_y = rect.y + self.delta[1]
            self.hand_sprite.pos = pygame.math.Vector2(self.x, self.y)
            for i in self.gun_sprite:
                i.pos = pygame.math.Vector2(self.gun_x, self.gun_y)
        self.rect = pygame.rect.Rect(self.x, self.y, self.rect.w, self.rect.h)

    def killed(self):
        for i in self.gun_sprite + [self.hand_sprite]:
            i.kill()
        self.kill()
