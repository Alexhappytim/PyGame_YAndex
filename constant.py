import pygame
from sprites import load_image

clock = pygame.time.Clock()
FPS = 60

size = height, width = 500, 500
tile_width = tile_height = 256
min_enemy = 10
max_enemy = 30
screen = pygame.display.set_mode(size)
tile_images = {
    'wall': pygame.transform.scale(load_image('decoration/wall.png'), (tile_width, tile_height)),
    'empty': pygame.transform.scale(load_image('decoration/floor.png'), (tile_width, tile_height))
}

max_clip = 32
