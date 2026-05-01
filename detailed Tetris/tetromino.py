from settings import *
import pygame as pg
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.alive = True
        super().__init__(tetromino.tetris.sprite_group)
        self.image = tetromino.image
        self.rect = self.image.get_rect()

    def set_rect_pos(self):
        self.rect.topleft = self.pos * TILE_SIZE

    def update(self):
        self.set_rect_pos()

class Tetromino:
    def __init__(self, tetris, current=True):
        self.tetris = tetris
        self.shape = random.choice(list(TETROMINOES.keys()))
        self.image = random.choice(tetris.app.images)
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.landing = False
        self.current = current

    def is_collide(self, positions):
        for pos in positions:
            x, y = int(pos.x), int(pos.y)
            if not (0 <= x < FIELD_W and y < FIELD_H):
                return True
            if y >= 0 and self.tetris.field_array[y][x]:
                return True
        return False

    def rotate(self):
        pivot = self.blocks[0].pos
        new_positions = [(block.pos - pivot).rotate(90) + pivot for block in self.blocks]
        if not self.is_collide(new_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_positions[i]

    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_positions = [block.pos + move_direction for block in self.blocks]
        if not self.is_collide(new_positions):
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            self.landing = True

    def update(self):
        self.move('down')