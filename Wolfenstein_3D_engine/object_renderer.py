import pygame as pg
import math
from settings import *

class ObjectRenderer:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        self.wall_textures = self.load_wall_textures()
        self.sky_image = self.get_texture(resource_path('textures', 'sky.png'), (WIDTH, HALF_WIDTH))
        self.sky_offset = 0
        self.blood_screen = self.get_texture(resource_path('textures', 'blood_screen.png'), RES)
        self.font = pg.font.SysFont('consolas', 28, bold=True)
        self.big_font = pg.font.SysFont('consolas', 72, bold=True)
        self.digit_size = 64
        self.digit_images = [
            self.get_texture(
                resource_path('textures', 'digits', f'{i}.png'),
                (self.digit_size, self.digit_size)
            )
            for i in range(11)
        ]
        self.digits = dict(zip(map(str, range(11)), self.digit_images))
        self.game_over_image = self.get_texture(resource_path('textures', 'game_over.png'), RES)
        self.win_image = self.get_texture(resource_path('textures', 'win.png'), RES)

    def draw(self):
        self.draw_background()
        self.render_game_objects()
        self.draw_player_damage()
        self.draw_crosshair()
        self.draw_minimap()
        self.draw_hud()

    def game_over(self):
        self.screen.blit(self.game_over_image, (0, 0))

    def win(self):
        self.screen.blit(self.win_image, (0, 0))

    def player_damage(self):
        self.screen.blit(self.blood_screen, (0, 0))

    def draw_player_damage(self):
        time_since = pg.time.get_ticks() - self.game.player.damage_time
        if time_since < 300:
            alpha = 255 - int(time_since * 0.8)
            self.blood_screen.set_alpha(alpha)
            self.screen.blit(self.blood_screen, (0, 0))

    def draw_background(self):
        self.sky_offset = (self.sky_offset + 4.0 * self.game.player.rel) % WIDTH
        self.screen.fill(CEILING_TINT)
        self.screen.blit(self.sky_image, (-self.sky_offset, 0))
        self.screen.blit(self.sky_image, (-self.sky_offset + WIDTH, 0)) 

        pg.draw.rect(self.screen, FLOOR_COLOR, (0, HALF_HEIGHT, WIDTH, HEIGHT))

    def render_game_objects(self):
        list_objects = sorted(self.game.raycasting.objects_to_render, key=lambda t: t[0], reverse=True)
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)

    def draw_crosshair(self):
        size = 10
        gap = 5
        color = (230, 225, 205)
        pg.draw.line(self.screen, color, (HALF_WIDTH - gap - size, HALF_HEIGHT), (HALF_WIDTH - gap, HALF_HEIGHT), 2)
        pg.draw.line(self.screen, color, (HALF_WIDTH + gap, HALF_HEIGHT), (HALF_WIDTH + gap + size, HALF_HEIGHT), 2)
        pg.draw.line(self.screen, color, (HALF_WIDTH, HALF_HEIGHT - gap - size), (HALF_WIDTH, HALF_HEIGHT - gap), 2)
        pg.draw.line(self.screen, color, (HALF_WIDTH, HALF_HEIGHT + gap), (HALF_WIDTH, HALF_HEIGHT + gap + size), 2)

    def draw_hud(self):
        health_ratio = max(0, self.game.player.health) / PLAYER_MAX_HEALTH
        bar_w, bar_h = 260, 24
        x, y = 24, HEIGHT - 54
        pg.draw.rect(self.screen, (18, 18, 18), (x - 3, y - 3, bar_w + 6, bar_h + 6))
        pg.draw.rect(self.screen, (70, 20, 20), (x, y, bar_w, bar_h))
        pg.draw.rect(self.screen, (190, 44, 36), (x, y, int(bar_w * health_ratio), bar_h))
        self.draw_text(f'HP {self.game.player.health:03}', (x, y - 34))

        weapon = self.game.weapon
        ammo_color = HUD_WARNING_COLOR if weapon.ammo == 0 else HUD_COLOR
        self.draw_text(f'AMMO {weapon.ammo}/{weapon.reserve_ammo}', (WIDTH - 260, HEIGHT - 54), ammo_color)
        enemies = self.game.object_handler.remaining_enemies
        self.draw_text(f'ENEMIES {enemies}', (WIDTH - 260, HEIGHT - 88))
        self.draw_text(f'KILLS {self.game.object_handler.kills}', (WIDTH - 260, HEIGHT - 120))
        mute_text = 'MUTE ON' if self.game.sound.muted else 'MUTE OFF'
        self.draw_text(mute_text, (WIDTH - 260, HEIGHT - 150), HUD_WARNING_COLOR if self.game.sound.muted else HUD_COLOR)
        if weapon.reloading and weapon.ammo == 0:
            self.draw_center_text('RELOADING', HEIGHT - 120, self.font, HUD_WARNING_COLOR)

    def draw_minimap(self):
        tile = 9
        pad = 16
        map_w = len(self.game.map.mini_map[0]) * tile
        map_h = len(self.game.map.mini_map) * tile
        surface = pg.Surface((map_w + pad * 2, map_h + pad * 2), pg.SRCALPHA)
        surface.fill((0, 0, 0, 110))
        for y, row in enumerate(self.game.map.mini_map):
            for x, value in enumerate(row):
                if value:
                    pg.draw.rect(surface, (145, 135, 115, 170), (pad + x * tile, pad + y * tile, tile - 1, tile - 1))
        for npc in self.game.object_handler.npc_list:
            if npc.alive:
                pg.draw.circle(surface, (210, 55, 45), (pad + int(npc.x * tile), pad + int(npc.y * tile)), 3)
        player_pos = (pad + int(self.game.player.x * tile), pad + int(self.game.player.y * tile))
        pg.draw.circle(surface, (80, 200, 110), player_pos, 4)
        look = (
            player_pos[0] + int(math.cos(self.game.player.angle) * 10),
            player_pos[1] + int(math.sin(self.game.player.angle) * 10)
        )
        pg.draw.line(surface, (80, 200, 110), player_pos, look, 2)
        self.screen.blit(surface, (WIDTH - surface.get_width() - 18, 18))

    def draw_pause(self):
        overlay = pg.Surface(RES, pg.SRCALPHA)
        overlay.fill((0, 0, 0, 145))
        self.screen.blit(overlay, (0, 0))
        self.draw_center_text('PAUSED', HALF_HEIGHT - 35, self.big_font)
        self.draw_center_text('Press P to resume', HALF_HEIGHT + 40, self.font)

    def draw_menu(self):
        overlay = pg.Surface(RES, pg.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        self.draw_center_text('WOLFENSTEIN 3D', HALF_HEIGHT - 80, self.big_font)
        self.draw_center_text('WASD / Arrow keys: Move', HALF_HEIGHT - 10, self.font)
        self.draw_center_text('Mouse: Look | Left Click: Shoot', HALF_HEIGHT + 30, self.font)
        self.draw_center_text('P: Pause | R: Restart | M: Mute | ESC: Quit', HALF_HEIGHT + 70, self.font)
        self.draw_center_text('Press any key to start', HALF_HEIGHT + 140, self.font)

    def draw_game_over(self):
        overlay = pg.Surface(RES, pg.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))
        self.draw_center_text('GAME OVER', HALF_HEIGHT - 35, self.big_font, pg.Color('red'))
        self.draw_center_text('Press R to restart or ESC to quit', HALF_HEIGHT + 40, self.font)

    def draw_victory(self):
        overlay = pg.Surface(RES, pg.SRCALPHA)
        overlay.fill((0, 0, 0, 190))
        self.screen.blit(overlay, (0, 0))
        self.draw_center_text('LEVEL CLEARED!', HALF_HEIGHT - 35, self.big_font, pg.Color('skyblue'))
        self.draw_center_text('Press R to play again or ESC to quit', HALF_HEIGHT + 40, self.font)

    def draw_text(self, text, pos, color=HUD_COLOR):
        image = self.font.render(text, True, color)
        self.screen.blit(image, pos)

    def draw_center_text(self, text, y, font, color=HUD_COLOR):
        image = font.render(text, True, color)
        self.screen.blit(image, image.get_rect(center=(HALF_WIDTH, y)))

    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)
    
    def load_wall_textures(self):
        return {
            1: self.get_texture(resource_path('textures', '1.png')),
            2: self.get_texture(resource_path('textures', '2.png')),
            3: self.get_texture(resource_path('textures', '3.png')),
            4: self.get_texture(resource_path('textures', '4.png')),
            5: self.get_texture(resource_path('textures', '5.png')),
        }
