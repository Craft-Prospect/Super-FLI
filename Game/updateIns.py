from sprites import *

class Mixin:
    def ins_update(self):

        #If the game is in a text instruction, pause for ~5 secs
        if self.current_state == INS0 or self.current_state == INS1 or self.current_state == INS4 or self.current_state == INS7:
            self.counting(200)

        #Generate the sprite for the fire after ~2 secs and display text for ~5 secs
        elif self.current_state == INS2:
            self.counting(200)

            if self.update_count == 80:
                self.add_sprite("fire",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))

        #Move the clouds close the player
        elif self.current_state == INS3:
            self.clouds_list.update()
            self.counting(80)

        #Do cloud damage to the player
        elif self.current_state == INS5:
            self.clouds_list.update()

            players = [self.cpu_sprite, self.player_sprite]
            for sat in players:
                # Generate a list of all clouds that collided with the CPU.
                hit_list = arcade.check_for_collision_with_list(sat,self.clouds_list)

                # Loop through each colliding cloud, decrease CPU health.

            self.counting(200)

        #Move player close to fire
        elif self.current_state == INS6:
            self.player_sprite.cpu_update(self.cpu_sprite, self.fire_list[0])
            self.update_count += 1

            self.counting(300)

        #Capture fire and add to player score
        elif self.current_state == INS8:
            self.fire_list[0].kill()
            self.player_sprite.score += 100
            self.current_state += 1

        elif self.current_state == SPLASH:
            self.counting(100)
            if self.update_count == 99:
                self.start_page_setup()

    def counting(self,t):
        self.update_count += 1
        if self.update_count >= t:
                self.update_count = 0
                self.current_state += 1
