import pygame as pg
from settings import resource_path

class Sound:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.shotgun = pg.mixer.Sound(resource_path('sound', 'shotgun.wav'))
        self.npc_pain = pg.mixer.Sound(resource_path('sound', 'npc_pain.wav'))
        self.npc_death = pg.mixer.Sound(resource_path('sound', 'npc_death.wav'))
        self.npc_shot = pg.mixer.Sound(resource_path('sound', 'npc_attack.wav'))
        self.player_pain = pg.mixer.Sound(resource_path('sound', 'player_pain.wav'))
        self.theme = pg.mixer.Sound(resource_path('sound', 'theme.mp3'))
        self.theme.set_volume(0.25)
        self.theme.play(loops=-1)
        self.muted = False

    def toggle_mute(self):
        self.muted = not self.muted
        volume = 0.0 if self.muted else 1.0
        self.shotgun.set_volume(volume)
        self.npc_pain.set_volume(volume)
        self.npc_death.set_volume(volume)
        self.npc_shot.set_volume(volume)
        self.player_pain.set_volume(volume)
        self.theme.set_volume(0.0 if self.muted else 0.25)
