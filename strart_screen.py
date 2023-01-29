from sprites import *
from constant import FPS, width, height, screen, clock


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Красавчик в беде, липкая библиотека", "",
                  "Как играть",
                  "Ходи на WASD",
                  "Стреляй левой кнопкой мышки",
                  "Делай перекаты на пробел",
                  "И помоги красавчику выжить подольше!"]

    fon = pygame.transform.scale(load_image('background.png'), (500,200))
    screen.blit(fon, (0, 500))
    font = pygame.font.Font("data/pix_font.ttf", 25)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)
