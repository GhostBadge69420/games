from sprite_object import *
from npc import *

class ObjectHandler:
    def __init__(self, game):
        self.game = game
        self.sprite_list = []
        self.npc_list = []
        self.kills = 0
        self.npc_sprite_path = resource_path('sprites', 'npc')
        self.static_sprite_path = resource_path('sprites', 'static_sprites')
        self.anim_sprite_path = resource_path('sprites', 'animated_sprites')
        add_sprite = self.add_sprite
        add_npc = self.add_npc
        self.npc_positions = {}

        self.add_sprite(SpriteObject(game))
        self.add_sprite(AnimatedSprite(game))
        self.add_sprite(AnimatedSprite(game, pos=(1.5, 1.5)))
        self.add_sprite(AnimatedSprite(game, pos=(1.5, 7.5)))
        self.add_sprite(AnimatedSprite(game, pos=(5.5, 3.25)))
        self.add_sprite(AnimatedSprite(game, pos=(5.5, 4.75)))
        self.add_sprite(AnimatedSprite(game, pos=(7.5, 2.5)))
        self.add_sprite(AnimatedSprite(game, pos=(7.5, 5.5)))
        self.add_sprite(AnimatedSprite(game, pos=(14.5, 1.5)))
        self.add_sprite(AnimatedSprite(game, path=resource_path('sprites', 'animated_sprites', 'red_light', '0.png'), pos=(14.5, 7.5)))
        self.add_sprite(AnimatedSprite(game, path=resource_path('sprites', 'animated_sprites', 'red_light', '0.png'), pos=(12.5, 7.5)))
        self.add_sprite(AnimatedSprite(game, path=resource_path('sprites', 'animated_sprites', 'red_light', '0.png'), pos=(9.5, 7.5)))

        add_npc(SoldierNPC(game, pos=(10.5, 5.5)))
        add_npc(SoldierNPC(game, pos=(11.5, 4.5)))
        add_npc(SoldierNPC(game, pos=(13.5, 2.5)))
        add_npc(CocoDemonNPC(game, pos=(13.5, 6.5)))
        add_npc(CyberDemonNPC(game, pos=(7.5, 6.5)))

    def update(self):
        self.npc_positions = {npc.map_pos for npc in self.npc_list if npc.alive}

        for sprite in self.sprite_list:
            sprite.update()

        for npc in self.npc_list:
            npc.update()

    def add_npc(self, npc):
        self.npc_list.append(npc)

    def add_sprite(self, sprite):
        self.sprite_list.append(sprite)

    @property
    def remaining_enemies(self):
        return sum(npc.alive for npc in self.npc_list)
