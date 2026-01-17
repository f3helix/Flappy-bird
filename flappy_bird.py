from pygame import *
from random import randint

init()
window_size = (1200, 800)
window = display.set_mode(window_size)
display.set_caption("Flappy Bird")

clock = time.Clock()

pipe_texture = image.load("celinder.png").convert_alpha()
bird_texture = image.load("bird.png").convert_alpha()

rect_player = Rect(150, window_size[1]//2 - 100, 100, 100)
bird_texture = transform.scale(bird_texture, (rect_player.width, rect_player.height))

def generate_pipe(count, pipe_width=120, gap=200, min_height=50, max_height=440, distance=650):
    pipes = []
    start_x = window_size[0]
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(start_x, 0 , pipe_width, height)
        bottom_pipe = Rect(start_x, height + gap, pipe_width, window_size[1] - (height + gap))
        pipes.append((top_pipe, True))
        pipes.append((bottom_pipe, False))
        start_x += distance
    return pipes

pipes = generate_pipe(150)
main_font = font.Font(None, 100)
score = 0
lose = False
y_vel = 2

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()

    window.fill("SkyBlue")

    window.blit(bird_texture, rect_player)

    for pie, is_top in pipes:
        if not lose:
            pie.x -= 10
        pipe_img = transform.scale(pipe_texture, (pie.width, pie.height))

        if is_top:
            pipe_img = transform.flip(pipe_img, False, True)
        window.blit(pipe_img, pie)

        if pie.x <= - pie.width:
            pipes.remove((pie, is_top))
            score += 0.5

        if rect_player.colliderect(pie):
            lose = True

    if len(pipes) < 20:
        pipes += generate_pipe(20)

    score_text = main_font.render(f'{int(score)}', True, "black")
    center_text = window_size[0]//2 - score_text.get_rect().w // 2
    window.blit(score_text, (center_text, 40))

    keys = key.get_pressed()
    if keys[K_w] and not lose:
        rect_player.y -= 15
    if keys[K_s] and not lose:
        rect_player.y += 15   

    if keys[K_r] and lose:
        lose = False
        score = 0
        pipes = generate_pipe(150)
        rect_player.y =  window_size[1]//2 - 100
        y_vel = 2

    if rect_player.y >= window_size[1] - rect_player.height:
        lose = True

    if lose:
        rect_player.y += y_vel
        y_vel *= 1.1
        if y_vel > 50:
            y_vel = 50

    display.update()
    clock.tick(60)