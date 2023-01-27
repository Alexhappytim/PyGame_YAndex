import pygame

from gun import Gun
from sprites import *
import math
from constant import *

kill_sprite = pygame.sprite.Group()


class killPlayer(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(kill_sprite)
        self.x = width // 2
        self.y = height // 2
        self.image = load_image("animation/enemy/front.png")
        self.sprite = AnimatedSprite(self.image, 9, 1, self.x, self.y)
        self.rect = self.sprite.rect.move(self.x, self.y)

    def update(self, *args):
        pass
