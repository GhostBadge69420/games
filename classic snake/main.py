import pygame as pg
from random import randrange

WINDOW = 1000
TILE_SIZE = 50
GRID_SIZE = WINDOW // TILE_SIZE
START_SPEED = 110
MAX_SPEED = 40
ACCELERATION = 2

COLORS = {
    'background': pg.Color('black'),
    'snake': pg.Color('green'),
    'food': pg.Color('red'),
    'text': pg.Color('white'),
    'grid': pg.Color(30, 30, 30),
}


def get_random_position(exclude=None):
    exclude = exclude or set()
    while True:
        pos = (randrange(GRID_SIZE) * TILE_SIZE + TILE_SIZE // 2,
               randrange(GRID_SIZE) * TILE_SIZE + TILE_SIZE // 2)
        if pos not in exclude:
            return pos


def draw_text(surface, text, font, color, pos, center=True):
    text_surface = font.render(text, True, color)
    rect = text_surface.get_rect(center=pos) if center else text_surface.get_rect(topleft=pos)
    surface.blit(text_surface, rect)


def draw_grid(surface):
    for x in range(0, WINDOW, TILE_SIZE):
        pg.draw.line(surface, COLORS['grid'], (x, 0), (x, WINDOW))
    for y in range(0, WINDOW, TILE_SIZE):
        pg.draw.line(surface, COLORS['grid'], (0, y), (WINDOW, y))


def reset_game():
    snake = pg.Rect(0, 0, TILE_SIZE - 2, TILE_SIZE - 2)
    snake.center = get_random_position()
    segments = [snake.copy()]
    food = pg.Rect(0, 0, TILE_SIZE - 2, TILE_SIZE - 2)
    food.center = get_random_position(exclude={tuple(s.center) for s in segments})
    return snake, segments, food, 1, (0, 0), START_SPEED


def main():
    pg.init()
    screen = pg.display.set_mode((WINDOW, WINDOW))
    clock = pg.time.Clock()
    small_font = pg.font.Font(None, 40)
    large_font = pg.font.Font(None, 80)

    snake, segments, food, length, snake_dir, time_step = reset_game()
    last_move = pg.time.get_ticks()
    score = 0
    high_score = 0
    paused = False
    game_over = False
    show_start = True

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                return

            if event.type == pg.KEYDOWN:
                if show_start:
                    show_start = False
                    continue

                if game_over:
                    if event.key == pg.K_r:
                        snake, segments, food, length, snake_dir, time_step = reset_game()
                        score = 0
                        game_over = False
                        paused = False
                        last_move = pg.time.get_ticks()
                    elif event.key == pg.K_q:
                        pg.quit()
                        return
                    continue

                if event.key in (pg.K_p, pg.K_SPACE):
                    paused = not paused
                if not paused:
                    if event.key in (pg.K_w, pg.K_UP) and snake_dir != (0, TILE_SIZE):
                        snake_dir = (0, -TILE_SIZE)
                    elif event.key in (pg.K_s, pg.K_DOWN) and snake_dir != (0, -TILE_SIZE):
                        snake_dir = (0, TILE_SIZE)
                    elif event.key in (pg.K_a, pg.K_LEFT) and snake_dir != (TILE_SIZE, 0):
                        snake_dir = (-TILE_SIZE, 0)
                    elif event.key in (pg.K_d, pg.K_RIGHT) and snake_dir != (-TILE_SIZE, 0):
                        snake_dir = (TILE_SIZE, 0)

        screen.fill(COLORS['background'])
        draw_grid(screen)

        if show_start:
            draw_text(screen, 'Classic Snake', large_font, COLORS['text'], (WINDOW // 2, WINDOW // 3))
            draw_text(screen, 'Use WASD or arrows to move', small_font, COLORS['text'], (WINDOW // 2, WINDOW // 2))
            draw_text(screen, 'Press any key to start', small_font, COLORS['text'], (WINDOW // 2, WINDOW * 2 // 3))
            draw_text(screen, 'P = Pause | R = Restart | Q = Quit', small_font, COLORS['text'], (WINDOW // 2, WINDOW * 5 // 6))
            pg.display.flip()
            clock.tick(60)
            continue

        if not game_over and not paused and snake_dir != (0, 0):
            current_time = pg.time.get_ticks()
            if current_time - last_move >= time_step:
                last_move = current_time
                snake = snake.move(snake_dir)
                segments.append(snake.copy())
                segments = segments[-length:]

                if snake.left < 0 or snake.right > WINDOW or snake.top < 0 or snake.bottom > WINDOW:
                    game_over = True
                elif snake.collidelist(segments[:-1]) != -1:
                    game_over = True

                if not game_over and snake.center == food.center:
                    length += 1
                    score += 1
                    time_step = max(START_SPEED - ACCELERATION * (length - 1), MAX_SPEED)
                    occupied = {tuple(segment.center) for segment in segments}
                    food.center = get_random_position(exclude=occupied)

        if snake.center == food.center and not game_over:
            occupied = {tuple(segment.center) for segment in segments}
            food.center = get_random_position(exclude=occupied)

        if game_over:
            high_score = max(high_score, score)
            draw_text(screen, 'Game Over', large_font, COLORS['text'], (WINDOW // 2, WINDOW // 3))
            draw_text(screen, f'Score: {score}', small_font, COLORS['text'], (WINDOW // 2, WINDOW // 2))
            draw_text(screen, f'High Score: {high_score}', small_font, COLORS['text'], (WINDOW // 2, WINDOW // 2 + 50))
            draw_text(screen, 'Press R to restart or Q to quit', small_font, COLORS['text'], (WINDOW // 2, WINDOW * 2 // 3))
        else:
            draw_text(screen, f'Score: {score}', small_font, COLORS['text'], (10, 10), center=False)
            draw_text(screen, f'High: {high_score}', small_font, COLORS['text'], (10, 40), center=False)
            draw_text(screen, 'PAUSED' if paused else 'Press P to pause', small_font, COLORS['text'], (WINDOW - 10, 10), center=False)

        pg.draw.rect(screen, COLORS['food'], food)
        for segment in segments:
            pg.draw.rect(screen, COLORS['snake'], segment)

        pg.display.flip()
        clock.tick(60)


if __name__ == '__main__':
    main()
