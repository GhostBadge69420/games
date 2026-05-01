from settings import *
from tetris import Tetris, Text
import sys
import pathlib
import pygame as pg

class App:
    def __init__(self):
        pg.init()
        pg.display.set_caption('Tetris')
        self.screen = pg.display.set_mode(WIN_RES)
        self.clock = pg.time.Clock()
        self.images = self.load_images()
        self.tetris = Tetris(self)
        self.text = Text(self)

    def load_images(self):
        files = [item for item in pathlib.Path(SPRITE_DIR_PATH).rglob('*.png') if item.is_file()]
        print("SPRITE_DIR_PATH:", SPRITE_DIR_PATH)
        print("FILES FOUND:", files)
        images = [pg.image.load(file).convert_alpha() for file in files]
        images = [pg.transform.scale(image, (TILE_SIZE, TILE_SIZE)) for image in images]
        if not images:
            raise ValueError("No images loaded! check SPRITE_DIR_PATH.")
        return images

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                self.tetris.control(pressed_key=event.key)

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(BG_COLOR)
        self.screen.fill(FIELD_COLOR, rect=(0, 0, *FIELD_RES))
        self.tetris.draw()
        self.text.draw()
        pg.display.flip()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()

if __name__ == '__main__':
    app = App()
    app.run()