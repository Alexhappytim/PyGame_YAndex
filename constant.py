import pygame

from sprites import load_image

horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
size = height, width = 500, 500
tile_width = tile_height = 70
start_x, start_y = 50, 50
tile_images = {
    'wall': load_image('decoration/pt.png'),
    'empty': load_image('decoration/grass.png')
}
