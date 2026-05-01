from sprite_object import *

class Weapon(AnimatedSprite):
    def __init__(self, game, path=None, scale=0.4, animation_time=90):
        path = path or resource_path('sprites', 'weapon', 'shotgun', '0.png')
        super().__init__(game=game, path=path, scale=scale, animation_time=animation_time)
        self.images = deque(
            [pg.transform.smoothscale(img, (self.image.get_width() * scale, self.image.get_height() * scale))
             for img in self.images])
        self.weapon_pos = (HALF_WIDTH - self.images[0].get_width() // 2, HEIGHT - self.images[0].get_height())
        self.reloading = False
        self.num_images = len(self.images)
        self.frame_counter = 0
        self.damage = 50
        self.mag_size = WEAPON_MAG_SIZE
        self.ammo = self.mag_size
        self.reserve_ammo = WEAPON_RESERVE_AMMO

    def fire(self):
        if self.reloading or self.ammo <= 0:
            return False
        self.ammo -= 1
        self.game.sound.shotgun.play()
        self.game.player.shot = True
        self.reloading = True
        return True

    def reload(self):
        if self.reloading or self.ammo == self.mag_size or self.reserve_ammo <= 0:
            return
        needed = self.mag_size - self.ammo
        loaded = min(needed, self.reserve_ammo)
        self.ammo += loaded
        self.reserve_ammo -= loaded

    def animate_shot(self):
        if self.reloading:
            self.game.player.shot = False
            if self.animation_trigger:
                self.images.rotate(-1)
                self.image = self.images[0]
                self.frame_counter += 1
                if self.frame_counter == self.num_images:
                    self.reloading = False
                    self.frame_counter = 0
                    if self.ammo == 0:
                        self.reload()

    def draw(self):
        self.game.screen.blit(self.images[0], self.weapon_pos)

    def update(self):
        self.check_animation_time()
        self.animate_shot()
