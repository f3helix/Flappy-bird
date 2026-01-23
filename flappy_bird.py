
from pygame import *
from random import randint
# Ініціалізація всіх модулів pygame
init()
# Розмір вікна гри
window_size = 1200, 800
window = display.set_mode(window_size)
# Таймер для контролю FPS
clock = time.Clock()
# Завантаження текстур труб та пташки
pipe_texture = image.load('celinder.png').convert_alpha()
bird_texture = image.load('bird.png').convert_alpha()
# Створення прямокутника гравця (позиція та розмір)
player_rect = Rect(150, window_size[1]//2 - 100, 100, 100)
# Масштабування текстури пташки під розмір прямокутника
bird_texture = transform.scale(bird_texture, (player_rect.width, player_rect.height))
# ------------------------- ФУНКЦІЯ ГЕНЕРАЦІЇ ТРУБ -------------------------
def generate_pipes(count, pipe_width=150, gap=280, min_height=50, max_height=440, distance=650):
    """
    Генерує набір труб (верхня + нижня) на певній відстані одна від одної.
    count — кількість пар труб
    pipe_width — ширина труби
    gap — проміжок між верхньою та нижньою трубою
    min_height/max_height — випадкова висота верхньої труби
    distance — відстань між парами труб
    """
    pipes = []
    start_x = window_size[0]  # Початкова позиція труб за межами екрану праворуч
    for i in range(count):
        height = randint(min_height, max_height)  # Випадкова висота верхньої труби
        # Верхня труба (росте вниз)
        top_pipe = Rect(start_x, 0, pipe_width, height)
        # Нижня труба (росте вверх)
        bottom_pipe = Rect(start_x, height + gap, pipe_width, window_size[1] - (height + gap))
        # Додаємо труби у список:
        # True — верхня труба (її треба віддзеркалити)
        # False — нижня труба
        pipes.append((top_pipe, True))
        pipes.append((bottom_pipe, False))
        start_x += distance  # Зсуваємо наступну пару труб далі вправо
    return pipes
# ---------------------------------------------------------------------------
# Генеруємо перші 150 труб
pies = generate_pipes(150)
# Шрифт для відображення рахунку
main_font = font.Font(None, 100)
score = 0      # Рахунок
lose = False   # Статус програшу
y_vel = 2      # Початкова швидкість падіння при програші
# =============================== ГОЛОВНИЙ ЦИКЛ ГРИ ===============================
while True:
    # Обробка подій (вихід з гри)
    for e in event.get():
        if e.type == QUIT:
            quit()
    # Фон
    window.fill('sky blue')
    # Малюємо пташку
    window.blit(bird_texture, player_rect)
    # ------------------------- ОБРОБКА ТРУБ -------------------------
    for pie, is_top in pies[:]:
        # Якщо не програли — труби рухаються вліво
        if not lose:
            pie.x -= 10
        # Масштабуємо текстуру під точний розмір труби
        pipe_img = transform.scale(pipe_texture, (pie.width, pie.height))
        # Якщо труба верхня — віддзеркалюємо по вертикалі
        if is_top:
            pipe_img = transform.flip(pipe_img, False, True)
        # Малюємо трубу
        window.blit(pipe_img, pie)
        # Якщо труба повністю вийшла за межі екрану — видаляємо її
        if pie.x <= -pie.width:
            pies.remove((pie, is_top))
            score += 0.5  # За кожну пару труб +1 (по 0.5 за кожну)
        # Перевірка зіткнення з трубою
        if player_rect.colliderect(pie):
            lose = True
    # ----------------------------------------------------------------
    # Якщо труб стало мало — генеруємо нові
    if len(pies) < 20:
        pies += generate_pipes(20)
    # ------------------------- ВІДОБРАЖЕННЯ РАХУНКУ -------------------------
    score_text = main_font.render(f'{int(score)}', True, 'black')
    center_text = window_size[0]//2 - score_text.get_rect().w // 2
    window.blit(score_text, (center_text, 40))
    # -------------------------------------------------------------------------
    # ------------------------- КЕРУВАННЯ ГРАВЦЕМ -------------------------
    keys = key.get_pressed()
    # Рух вгору
    if keys[K_w] and not lose:
        player_rect.y -= 15
    # Рух вниз
    if keys[K_s] and not lose:
        player_rect.y += 15
    # ---------------------------------------------------------------------
    # ------------------------- ПЕРЕЗАПУСК ГРИ -------------------------
    if keys[K_r] and lose:
        lose = False
        score = 0
        pies = generate_pipes(150)
        player_rect.y = window_size[1]//2 - 100
        y_vel = 2
    # ------------------------------------------------------------------
    # Якщо пташка торкнулась землі — програш
    if player_rect.y >= window_size[1] - player_rect.height:
        lose = True
    # ------------------------- АНІМАЦІЯ ПАДІННЯ -------------------------
    if lose:
        player_rect.y += y_vel      # Пташка падає вниз
        y_vel *= 1.1                # Прискорення падіння
        if y_vel > 50:              # Обмеження максимальної швидкості
            y_vel = 50
    # --------------------------------------------------------------------
    # Оновлення екрану
    display.update()

    # Обмеження FPS до 60 кадрів
    clock.tick(60)
# ======================================================================
