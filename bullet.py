from sprites import *
from constant import *


class Bullet(pygame.sprite.Sprite):
    image = load_image("decoration/bullet_1.png")
    pygame.transform.scale(image, (10, 10))

    def __init__(self, x, y, rect):
        super().__init__(bullet_sprites)
        self.speed_x = x * 10
        self.speed_y = -y * 10
        self.image = Bullet.image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = (width // 2 - rect.w // 2 + self.rect.w * x * 10, height // 2 - rect.h // 2 - self.rect.h * y * 10)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x, self.rect.y = (self.rect.x + self.speed_x, self.rect.y + self.speed_y)
        for enemy in enemy_sprites:
            if pygame.sprite.collide_mask(self, enemy):
                enemy.health -= 1
                self.kill()
        if self.rect.x > width or self.rect.x < 0 or self.rect.y > height or self.rect.y < 0:
            self.kill()

