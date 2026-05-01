import pygame as pg
import sys
from settings import *
from map import *
from player import *
from raycasting import *
from object_renderer import *
from sprite_object import *
from object_handler import *
from weapon import *
from sound import *
from pathfinding import *


class Game:
    def __init__(self):
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.global_trigger = False
        self.paused = False
        self.won = False
        self.game_over = False
        self.start_screen = True
        self.global_event = pg.USEREVENT + 0
        pg.time.set_timer(self.global_event, 40)
        self.sound = Sound(self)
        self.new_game()

    def new_game(self):
        self.paused = False
        self.won = False
        self.game_over = False
        self.map = Map(self)
        self.player = Player(self)
        self.object_renderer = ObjectRenderer(self)
        self.raycasting = RayCasting(self)
        self.object_handler = ObjectHandler(self)
        self.weapon = Weapon(self)
        self.pathfinding = PathFinding(self)

    def update(self):
        if self.paused or self.won or self.game_over or self.start_screen:
            self.delta_time = self.clock.tick(FPS)
            return

        self.player.update()
        self.raycasting.update()
        self.object_handler.update()
        self.weapon.update()
        self.check_win()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f'Wolfenstein 3D Engine | {self.clock.get_fps():.1f} FPS')

    def draw(self):
        self.object_renderer.draw()
        self.weapon.draw()

        if self.start_screen:
            self.object_renderer.draw_menu()
        elif self.paused:
            self.object_renderer.draw_pause()
        elif self.game_over:
            self.object_renderer.draw_game_over()
        elif self.won:
            self.object_renderer.draw_victory()

        pg.display.flip()

    def check_win(self):
        if self.object_handler.remaining_enemies == 0 and not self.won:
            self.won = True

    def toggle_sound(self):
        self.sound.toggle_mute()

    def check_events(self):
        self.global_trigger = False
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            if event.type == pg.KEYDOWN:
                if self.start_screen:
                    self.start_screen = False
                    continue

                if event.key == pg.K_p and not self.game_over and not self.won:
                    self.paused = not self.paused
                    continue

                if event.key == pg.K_m:
                    self.toggle_sound()
                    continue

                if event.key == pg.K_r and (self.game_over or self.won):
                    self.new_game()
                    self.start_screen = False
                    continue

            if event.type == self.global_event:
                self.global_trigger = True

            if not self.paused and not self.won and not self.game_over and not self.start_screen:
                self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == '__main__':
    game = Game()
    game.run()
