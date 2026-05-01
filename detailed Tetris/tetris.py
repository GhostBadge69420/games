from settings import *
import math
from tetromino import Tetromino
import pygame.freetype as ft
import pygame as pg


class Text:
    def __init__(self, app):
        self.app = app
        self.font = ft.Font(FONT_PATH)

    def get_color(self):
        time = pg.time.get_ticks() * 0.001
        n_sin = lambda t: (math.sin(t) * 0.5 + 0.5) * 255
        return n_sin(time * 0.5), n_sin(time * 0.2), n_sin(time * 0.9)

    def draw(self):
        self.font.render_to(self.app.screen, (WIN_W * 0.595, WIN_H * 0.02),
                            text='TETRIS', fgcolor=self.get_color(),
                            size=TILE_SIZE * 1.65, bgcolor='black')
        self.font.render_to(self.app.screen, (WIN_W * 0.64, WIN_H * 0.8),
                            text=f'{self.app.tetris.score}', fgcolor='white',
                            size=TILE_SIZE * 1.8)


class Tetris:
    def __init__(self, app):
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = [[0 for _ in range(FIELD_W)] for _ in range(FIELD_H)]
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current=False)
        self.speed_up = False

        self.score = 0
        self.full_lines = 0
        self.points_per_lines = {0:0, 1:100, 2:300, 3:700, 4:1500}

        self.last_drop_time = pg.time.get_ticks()

    def put_tetromino_blocks_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block

    def check_full_lines(self):
        row = FIELD_H - 1
        for y in range(FIELD_H - 1, -1, -1):
            for x in range(FIELD_W):
                self.field_array[row][x] = self.field_array[y][x]
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)
            if sum(bool(b) for b in self.field_array[y]) < FIELD_W:
                row -= 1
            else:
                for x in range(FIELD_W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                self.full_lines += 1

    def get_score(self):
        self.score += self.points_per_lines[self.full_lines]
        self.full_lines = 0

    def is_game_over(self):
        return self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET.y

    def check_tetromino_landing(self):
        if self.tetromino.landing:
            if self.is_game_over():
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.put_tetromino_blocks_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current=False)

    def control(self, pressed_key):
        if pressed_key == pg.K_LEFT:
            self.tetromino.move('left')
        elif pressed_key == pg.K_RIGHT:
            self.tetromino.move('right')
        elif pressed_key == pg.K_UP:
            self.tetromino.rotate()
        elif pressed_key == pg.K_DOWN:
            self.speed_up = True

    def draw_grid(self):
        for x in range(FIELD_W):
            for y in range(FIELD_H):
                pg.draw.rect(self.app.screen, 'black',
                             (x*TILE_SIZE, y*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

    def update(self):
        current_time = pg.time.get_ticks()
        interval = FAST_ANIM_TIME_INTERVAL if self.speed_up else ANIM_TIME_INTERVAL
        if current_time - self.last_drop_time >= interval:
            self.tetromino.update()
            self.last_drop_time = current_time
            self.check_full_lines()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()

    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)