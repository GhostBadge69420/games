import os
import pygame as pg
from random import choice, randrange

BASE_DIR = os.path.dirname(__file__)
FONT_PATH = os.path.join(BASE_DIR, 'font', 'font.ttf')
BG_PATH = os.path.join(BASE_DIR, 'img', 'bg.jpg')
BG2_PATH = os.path.join(BASE_DIR, 'img', 'bg2.jpg')
RECORD_PATH = os.path.join(BASE_DIR, 'record')

W, H = 10, 20
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 750, 940
FPS = 60

pg.init()
sc = pg.display.set_mode(RES)
clock = pg.time.Clock()

def load_image(path, size=None):
    try:
        image = pg.image.load(path).convert()
        if size:
            image = pg.transform.scale(image, size)
        return image
    except Exception:
        return None

bg = load_image(BG_PATH, RES)
game_bg = load_image(BG2_PATH, GAME_RES)

try:
    main_font = pg.font.Font(FONT_PATH, 65)
    side_font = pg.font.Font(FONT_PATH, 45)
    small_font = pg.font.Font(FONT_PATH, 30)
except Exception:
    main_font = pg.font.Font(None, 65)
    side_font = pg.font.Font(None, 45)
    small_font = pg.font.Font(None, 30)

TITLE_COLOR = pg.Color('darkorange')
SCORE_COLOR = pg.Color('green')
RECORD_COLOR = pg.Color('purple')
TEXT_COLOR = pg.Color('white')
GRID_COLOR = pg.Color(40, 40, 40)

scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}

FIGURES = [
    [(0, 1), (1, 1), (-1, 1), (-2, 1)],  # I
    [(0, 0), (1, 0), (0, 1), (1, 1)],   # O
    [(-1, 0), (0, 0), (1, 0), (1, 1)],  # L
    [(-1, 1), (-1, 0), (0, 0), (1, 0)], # J
    [(-1, 0), (0, 0), (0, 1), (1, 1)],  # S
    [(-1, 1), (0, 1), (0, 0), (1, 0)],  # Z
    [(-1, 0), (0, 0), (1, 0), (0, 1)],  # T
]


def get_color():
    return randrange(30, 256), randrange(30, 256), randrange(30, 256)


def rotate_shape(shape):
    return [(-y, x) for x, y in shape]


def get_record():
    if not os.path.exists(RECORD_PATH):
        with open(RECORD_PATH, 'w') as file:
            file.write('0')
        return 0
    try:
        with open(RECORD_PATH, 'r') as file:
            return int(file.readline().strip() or 0)
    except Exception:
        return 0


def set_record(score):
    record = get_record()
    if score > record:
        with open(RECORD_PATH, 'w') as file:
            file.write(str(score))


def draw_text(surface, text, font, color, pos, center=True):
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=pos) if center else rendered.get_rect(topleft=pos)
    surface.blit(rendered, rect)


def draw_grid(surface):
    for x in range(0, GAME_RES[0], TILE):
        pg.draw.line(surface, GRID_COLOR, (x, 0), (x, GAME_RES[1]))
    for y in range(0, GAME_RES[1], TILE):
        pg.draw.line(surface, GRID_COLOR, (0, y), (GAME_RES[0], y))


def new_figure():
    shape = choice(FIGURES)
    return {'shape': shape, 'x': W // 2, 'y': 0, 'color': get_color()}


def figure_positions(figure):
    return [(figure['x'] + dx, figure['y'] + dy) for dx, dy in figure['shape']]


def valid_position(figure, field):
    for x, y in figure_positions(figure):
        if x < 0 or x >= W or y < 0 or y >= H:
            return False
        if field[y][x]:
            return False
    return True


def freeze_figure(figure, field):
    for x, y in figure_positions(figure):
        if 0 <= y < H and 0 <= x < W:
            field[y][x] = figure['color']


def clear_lines(field):
    lines_cleared = 0
    new_field = [row for row in field if any(cell == 0 for cell in row)]
    lines_cleared = H - len(new_field)
    while len(new_field) < H:
        new_field.insert(0, [0] * W)
    return new_field, lines_cleared


def draw_field(surface, field):
    block_rect = pg.Rect(0, 0, TILE - 2, TILE - 2)
    for y, row in enumerate(field):
        for x, color in enumerate(row):
            if color:
                block_rect.x = x * TILE
                block_rect.y = y * TILE
                pg.draw.rect(surface, color, block_rect)


def draw_figure(surface, figure, offset=(0, 0)):
    block_rect = pg.Rect(0, 0, TILE - 2, TILE - 2)
    ox, oy = offset
    for dx, dy in figure_positions(figure):
        block_rect.x = dx * TILE + ox
        block_rect.y = dy * TILE + oy
        pg.draw.rect(surface, figure['color'], block_rect)


def main():
    field = [[0 for _ in range(W)] for _ in range(H)]
    next_figure = new_figure()
    current_figure = new_figure()
    current_figure['color'] = next_figure['color']
    current_figure['shape'] = next_figure['shape']
    next_figure = new_figure()
    score = 0
    lines = 0
    level = 1
    record = get_record()
    running = True
    paused = False
    game_over = False
    start_screen = True
    drop_event = pg.USEREVENT + 1
    drop_speed = 800
    pg.time.set_timer(drop_event, drop_speed)

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if start_screen:
                    start_screen = False
                    continue
                if game_over:
                    if event.key == pg.K_r:
                        return main()
                    if event.key == pg.K_q:
                        running = False
                    continue
                if event.key in (pg.K_p, pg.K_SPACE):
                    paused = not paused
                if not paused:
                    if event.key in (pg.K_LEFT, pg.K_a):
                        moved = {'x': current_figure['x'] - 1, 'y': current_figure['y'], 'shape': current_figure['shape'], 'color': current_figure['color']}
                        if valid_position(moved, field):
                            current_figure['x'] -= 1
                    elif event.key in (pg.K_RIGHT, pg.K_d):
                        moved = {'x': current_figure['x'] + 1, 'y': current_figure['y'], 'shape': current_figure['shape'], 'color': current_figure['color']}
                        if valid_position(moved, field):
                            current_figure['x'] += 1
                    elif event.key in (pg.K_DOWN, pg.K_s):
                        moved = {'x': current_figure['x'], 'y': current_figure['y'] + 1, 'shape': current_figure['shape'], 'color': current_figure['color']}
                        if valid_position(moved, field):
                            current_figure['y'] += 1
                    elif event.key in (pg.K_UP, pg.K_w):
                        rotated = {'x': current_figure['x'], 'y': current_figure['y'], 'shape': rotate_shape(current_figure['shape']), 'color': current_figure['color']}
                        if valid_position(rotated, field):
                            current_figure['shape'] = rotated['shape']
            elif event.type == drop_event and not paused and not game_over and not start_screen:
                dropped = {'x': current_figure['x'], 'y': current_figure['y'] + 1, 'shape': current_figure['shape'], 'color': current_figure['color']}
                if valid_position(dropped, field):
                    current_figure['y'] += 1
                else:
                    freeze_figure(current_figure, field)
                    field, removed = clear_lines(field)
                    if removed:
                        lines += removed
                        score += scores[removed] * level
                        level = 1 + lines // 10
                        drop_speed = max(100, 800 - (level - 1) * 60)
                        pg.time.set_timer(drop_event, drop_speed)
                    current_figure = next_figure
                    next_figure = new_figure()
                    if not valid_position(current_figure, field):
                        game_over = True
                        set_record(score)
                        record = get_record()

        sc.fill(pg.Color('black'))
        if bg:
            sc.blit(bg, (0, 0))
        game_surface = pg.Surface(GAME_RES)
        if game_bg:
            game_surface.blit(game_bg, (0, 0))
        else:
            game_surface.fill(pg.Color('black'))

        draw_grid(game_surface)
        draw_field(game_surface, field)
        if not start_screen:
            draw_figure(game_surface, current_figure)

        sc.blit(game_surface, (20, 20))
        draw_text(sc, 'TETRIS', main_font, TITLE_COLOR, (585, 60))
        draw_text(sc, 'Next:', side_font, TEXT_COLOR, (585, 230))

        preview_surface = pg.Surface((TILE * 5, TILE * 5), pg.SRCALPHA)
        preview_surface.fill((0, 0, 0, 0))
        preview_figure = {'x': 2, 'y': 1, 'shape': next_figure['shape'], 'color': next_figure['color']}
        draw_figure(preview_surface, preview_figure, offset=(0, 0))
        sc.blit(preview_surface, (500, 260))

        draw_text(sc, f'Score: {score}', side_font, SCORE_COLOR, (575, 450), center=False)
        draw_text(sc, f'Lines: {lines}', side_font, SCORE_COLOR, (575, 520), center=False)
        draw_text(sc, f'Level: {level}', side_font, SCORE_COLOR, (575, 590), center=False)
        draw_text(sc, 'Record:', side_font, RECORD_COLOR, (575, 660), center=False)
        draw_text(sc, str(record), side_font, TEXT_COLOR, (575, 720), center=False)
        draw_text(sc, 'P = Pause | R = Restart | Q = Quit', small_font, TEXT_COLOR, (575, 820), center=False)

        if start_screen:
            draw_text(sc, 'Press any key to start', side_font, TEXT_COLOR, (375, 500))
        elif paused:
            draw_text(sc, 'PAUSED', main_font, TEXT_COLOR, (375, 500))
        elif game_over:
            draw_text(sc, 'GAME OVER', main_font, pg.Color('red'), (375, 450))
            draw_text(sc, 'Press R to restart or Q to quit', side_font, TEXT_COLOR, (375, 550))

        pg.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
