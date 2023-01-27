import pygame
from sprites import load_image

clock = pygame.time.Clock()
FPS = 60

size = height, width = 500, 500
tile_width = tile_height = 70
count_enemy = 1
screen = pygame.display.set_mode(size)
tile_images = {
    'wall': load_image('decoration/wall.png'),
    'empty': load_image('decoration/floor.png')
}
