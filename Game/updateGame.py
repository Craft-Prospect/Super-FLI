from sprites import *
import random
import subprocess
import sys

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

            self.check_fire_collison(self.cpu_sprite) #see spriteFunc.py

        #End game when both sprite and player are dead
        if not self.cpu_sprite.active and not self.player_sprite.active:
            self.current_state=END_PAGE
            self.setup_game_over() # see runGame.py

        #Add new clouds if clouds have scorlled off
        if len(self.clouds_list) <=self.clouds_limit:
            self.add_sprite("cloud") #see spriteFunc.py

    #Update the player if the joystick moves
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

        if(self.final_background_odd and self.final_background_even):
            self.level_up()
            return


        #Else if background has scrolled off
        elif(update != 0):

            if (self.final_background_odd or self.final_background_even):
                self.final_background_even = True
                self.final_background_odd = True
                return

            background =  Background(self.source[self.background_index], BACKGROUND_SCALING)
            background.center_x = SCREEN_WIDTH + SCREEN_WIDTH/2
            background.center_y = SCREEN_HEIGHT/2

            self.background_index += 1

            if(update == 1):
                #Else create a new even background, off screen, to scroll after the next odd one
                self.background_even = background
                self.background_list.append(self.background_even)

                if (self.background_index == len(self.source)):
                    self.final_background_even = True

            #If the odd background has reached the end of the screen
            elif(update == -1):
                #Create a new odd background, opff screen, ready to scroll in after the next even one
                self.background_odd = background
                self.background_list.append(self.background_odd)

                if (self.background_index == len(self.source)):
                    self.final_background_odd = True


            #look one image further ahead and run it through the network
            text_file = 'background%d-fire.txt' % (self.background_index+1)

            #if image exits and not running heedless tests, run Neural Network
            if self.background_index < len(self.source) and not self.Test:
                picture = self.source[self.background_index]
                NN_command = COMMAND + [picture]

                with open("NNData/"+text_file, "wb") as out:
                    subprocess.Popen(NN_command, stdout=out)

            #Get NN data and add fires
            self.add_new_data()


    #Check if sprite damaged by cloud
    def cloud_damages(self,sprite):
        #Get colliding clouds
        hit_list = arcade.check_for_collision_with_list(sprite,self.clouds_list)
        # Loop through each colliding cloud, decrease sprite health.
        for cloud in hit_list:
            sprite.health -= cloud.damage
            if sprite.health <= 0:
                #If player dies, update player final score
                if sprite == self.player_sprite:
                    self.player_score = sprite.score
                sprite.active = False
                sprite.kill()

            #Take note of how CPU should avoid clouds
            if sprite == self.cpu_sprite:
                self.avoid_cloud(sprite,cloud)

        #If no clouds to avoid, reset avoid
        if sprite == self.cpu_sprite and len(hit_list) == 0:
            sprite.avoid = None

    #Decided how CPU should avoid cloud
    def avoid_cloud(self,sprite,cloud):

        if sprite.center_x <= cloud.center_x:
            sprite.avoid = ["left"]
        else:
            sprite.avoid = ["right"]

        if sprite.center_y <= cloud.center_y:
            sprite.avoid.append("down")
        else:
            sprite.avoid.append("up")
