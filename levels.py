from sprites import *
from constant import *


class Xp(pygame.sprite.Sprite):
    image = load_image("decoration/xp.png")
    pygame.transform.scale(image, (10, 10))

    def __init__(self, x, y, rect, x1, y1):
        super().__init__(xp_sprites, all_sprites)
        self.image = Xp.image
        self.rect = self.image.get_rect()
        # self.rect.x, self.rect.y = (width // 2 - rect.w // 2 + self.rect.w * x * 10, height // 2 - rect.h // 2 - self.rect.h * y * 10)
        self.rect.x, self.rect.y = rect.x, rect.y
        self.start_x, self.start_y = rect.x, rect.y
        self.start_p_x, self.start_p_y = x1, y1
        self.mask = pygame.mask.from_surface(self.image)
        # print(x1, y1, player_group.sprites()[0].rect)

        # print('**************************', self.rect, self.start_x, self.start_y, player_group.sprites()[0].rect,  player_group.sprites()[0].xp)


    def update(self):
        # print(self.rect, self.start_x, self.start_y, player_group.sprites()[0].rect,  player_group.sprites()[0].xp)

        for player in player_group:
            if pygame.sprite.collide_mask(self, player):
                player.xp += 1
                self.kill()
        # if self.rect.x > width or self.rect.x < 0 or self.rect.y > height or self.rect.y < 0:
        #     self.kill()
