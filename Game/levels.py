from sprites import *

class Mixin:
    def level_up(self):
        self.level +=1
        if self.level > len(self.SOURCE) or not self.player_sprite.active:
            self.level = 1
            self.game_over_setup()
            self.current_state = END_PAGE
        else:
            self.cloud_damage = self.cloud_damage * 2
            self.clouds_list = arcade.SpriteList()
            self.source = self.SOURCE[self.level-1]
            if not self.Test:
                self.lvl_up.play()
            if self.player_sprite.active:
                self.player_sprite.health = 100

            if self.cpu_sprite.active:
                self.cpu_sprite.health = 100
            else:
                self.setup_cpu()

            self.background_setup()
