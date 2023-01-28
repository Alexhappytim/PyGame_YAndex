import pygame

# pygame.mixer.pre_init(44100, 32, 1, 4096)
pygame.init()

shot_sound = pygame.mixer.Sound('data/sounds/shot.wav')
blob_die_sound = pygame.mixer.Sound('data/sounds/blob_die.wav')
reload_sound = pygame.mixer.Sound('data/sounds/reload.wav')
roll1_sound = pygame.mixer.Sound('data/sounds/dodge_01.wav')
roll2_sound = pygame.mixer.Sound('data/sounds/dodge_02.wav')
walk_sound = pygame.mixer.Sound('data/sounds/step/boot_stone_01.wav')
hurt_sound = pygame.mixer.Sound('data/sounds/hurt.wav')
sound_queue = []


def play_sound(sound):
    sound_queue.append(sound)


def sound_update():
    print(sound_queue)
    if sound_queue:
        sound_queue[0].play(0)
        del sound_queue[0]
