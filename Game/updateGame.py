from sprites import *

class Mixin:
    def game_update(self):
        #Update sprites and clouds
        self.fire_list.update()
        self.clouds_list.update()

        #Update background
        update = self.background_even.update()
        update -= self.background_odd.update()
        self.game_background_update(update)

        #If player is alive, update
        if self.player_sprite.active:
            # Update the position according to the game controller
            if self.joystick:
                self.game_joystick_update()

            self.player_list.update()
            self.cloud_damages(self.player_sprite)

        #Update CPU satellite
        if self.cpu_sprite.active:
            if len(self.fire_list)> 0:
                self.cpu_sprite.cpu_update(self.player_sprite,self.fire_list[0])
            else:
                self.cpu_sprite.cpu_update(self.player_sprite)
                self.cpu_list.update()

            self.cloud_damages(self.cpu_sprite)

            self.check_fire_collison(self.cpu_sprite)

        if not self.cpu_sprite.active and not self.player_sprite.active:
            self.current_state=END_PAGE

        if len(self.clouds_list) <3 and len(self.cloud_data) > 0:
            item = self.cloud_data.pop(0)
            self.add_sprite(item[0], item[1])





    def game_joystick_update(self):
        # Set a "dead zone" to prevent drive from a centered joystick
        if abs(self.joystick.x) < DEAD_ZONE:
            self.player_sprite.change_x = 0
        else:
            self.player_sprite.change_x = self.joystick.x * self.player_sprite.speed
            # Set a "dead zone" to prevent drive from a centered joystick
            if abs(self.joystick.y) < DEAD_ZONE:
                self.player_sprite.change_y = 0
            else:
                self.player_sprite.change_y = -self.joystick.y * self.player_sprite.speed

    def game_background_update(self, update):

        if(self.final_background):
            if (update == 1):
                return
            elif (update == -1):
                self.current_state = END_PAGE
                return

        elif(update != 0):
            background =  Background(self.source[self.background_index], BACKGROUND_SCALING)
            background.center_x = SCREEN_WIDTH + SCREEN_WIDTH/2
            background.center_y = SCREEN_HEIGHT/2

            if(update == 1):
                #Else create a new even background, off screen, to scroll after the next odd one
                self.background_even = background
                self.background_list.append(self.background_even)

            #If the odd background has reached the end of the screen
            elif(update == -1):
                #Create a new odd background, opff screen, ready to scroll in after the next even one
                self.background_odd = background
                self.background_list.append(self.background_odd)

            self.background_index += 1
            self.add_new_data()
            #If there's no backgrounds left
            if (self.background_index == len(self.source)):
                self.final_background = True


    def cloud_damages(self,sprite):
        hit_list = arcade.check_for_collision_with_list(sprite,self.clouds_list)
        # Loop through each colliding cloud, decrease CPU health.
        for cloud in hit_list:
            sprite.health -= cloud.damage
            if sprite.health <= 0:
                sprite.active = False
                sprite.kill()
