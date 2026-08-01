
from pygame import *
from random import randint
import sounddevice as sd
import numpy as np

sr = 16000
block = 256
mic_level = 0.01

def audio_cb(indata, frames, time, status):
    global mic_level
    if status:
        return
    rms = float(np.sqrt(np.mean(indata**2)))
    mic_level = 0.85 * mic_level + 0.15 * rms



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
y_vel = 0.0

wait = 40
gravity = 0.6
THRESH = 0.001
IMPUSE = -8.0

with sd.InputStream(callback=audio_cb, channels=1, samplerate=sr, blocksize=block):
    while True:
        for e in event.get():
            if e.type == QUIT:
                quit()

        if mic_level > THRESH:
            y_vel = IMPUSE

        y_vel += gravity
        player_rect.y +=  int(y_vel)

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

        display.update()
        clock.tick(60)

        keys = key.get_pressed() 

        if keys[K_r] and lose:
            lose = False
            score = 0
            pies = generate_pipes(150)
            player_rect.y = window_size[1]//2 - 100
            y_vel = 0.0

        if player_rect.bottom >= window_size[1]:
            player_rect.bottom = window_size[1]
            y_vel = 0.0

        if player_rect.top <= 0:
            player_rect.top = 0
            if y_vel < 0:
                y_vel = 0.0

        if lose and wait > 1:
            for pie, _ in pies:
                pie.x += 8
            wait -= 1
        else:
            lose = False
            wait = 40
    
       
