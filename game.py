
from pygame import *
from random import randint

init()
window_size = 1200, 800
window = display.set_mode(window_size)
clock = time.Clock()

pipe_texture = image.load("celinder.png").convert_alpha()
bird_texture = image.load("bird.png").convert_alpha()

player_rect = Rect(150, window_size[1]//2 - 100, 100, 100)
bird_texture = transform.scale(bird_texture, (player_rect.width, player_rect.height))

def generate_pipes(count, pipe_width=150, gap=280, min_height=50, max_height=440, distance=650):
    pipes = []
    startr_x = window_size[0]
    for i in range(count):
        height = randint(min_height, max_height)
        top_pipe = Rect(startr_x, 0, pipe_width, height)
        bottom_pipe = Rect(startr_x, height+gap, pipe_width, window_size[1]-(height+gap))
        pipes.append((top_pipe, True))
        pipes.append((bottom_pipe, False))
        startr_x += distance
    return pipes


pies = generate_pipes(150)
main_font = font.Font(None, 100)
score = 0
lose = False
y_vel = 2

while True:
    for e in event.get():
        if e.type == QUIT:
            quit()
    window.fill("skyblue")
    window.blit(bird_texture, player_rect)

    for pie, is_top in pies[:]:
        if not lose:
            pie.x -= 10
        pipe_img = transform.scale(pipe_texture, (pie.width, pie.height))
        if is_top:
            pipe_img = transform.flip(pipe_img, False, True)
        window.blit(pipe_img, pie)

        if pie.x <= -pie.width:
            pies.remove((pie, is_top))
            score += 0.5

        if player_rect.colliderect(pie):
            lose = True

    if len(pies) < 20:
        pies+= generate_pipes(20)

    score_text = main_font.render(f"{int(score)}", True, "black") 
    center_text = window_size[0]//2-score_text.get_rect().w//2 
    window.blit(score_text, (center_text, 40))

    keys = key.get_pressed() 

    if keys[K_w] and not lose:
        player_rect.y -= 15
    if keys[K_s] and not lose:
        player_rect.y += 15

    if keys[K_r] and lose:
        lose = False
        score = 0
        pies = generate_pipes(150)
        player_rect.y = window_size[1]//2 - 100
        y_vel = 2

    if player_rect.y >= window_size[1] - player_rect.height:
        lose = True

    if lose:
        player_rect.y += y_vel
        y_vel *= 1.1
        if y_vel > 50:
            y_vel = 50
        
    display.update()
    clock.tick(60)
    
       
