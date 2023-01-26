import pygame
from sprites import load_image

clock = pygame.time.Clock()
horizontal_borders = pygame.sprite.Group()
vertical_borders = pygame.sprite.Group()
FPS = 60

size = height, width = 500, 500
tile_width = tile_height = 70
screen = pygame.display.set_mode(size)
tile_images = {
    'wall': load_image('decoration/pt.png'),
    'empty': load_image('decoration/grass.png')
}
