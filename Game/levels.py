from sprites import *

class Mixin:
    def level_up(self):
        self.level +=1
        #If not levels left, end game
        if self.level > len(SOURCE) or  not self.player_sprite.active:
            self.current_state = END_PAGE
            self.setup_game_over()
        #Else Level up
        else:
            #Increase cloud damage and reset cloudss
            self.cloud_damage = self.cloud_damage * 2
            self.clouds_list = arcade.SpriteList()
            if not self.Test:
                self.lvl_up.play()

            #Reset health
            if self.player_sprite.active:
                self.player_sprite.health = 100

            if self.cpu_sprite.active:
                self.cpu_sprite.health = 100
            else:
                #Revive CPu if dead
                self.setup_cpu()# see runGame.py

            #Change to new background_setups
            self.source = SOURCE[self.level-1]
            self.background_setup()
