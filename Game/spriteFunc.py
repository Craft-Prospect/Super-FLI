from sprites import *
import pygame

class Mixin:
    #Will be used by NN to generate newly identified events
    def add_sprite(self,event,coOrds):

     if coOrds[0] >= 0 and coOrds[1] >=0 and coOrds[1] < SCREEN_HEIGHT:

                if  event == "fire":
                    # Create the fire instance
                    detected = Fire("images/fire_sprite.png", SPRITE_SCALING_FIRE)

                else:
                    #Create cloud instance
                    detected=Cloud("images/clouds.png", SPRITE_SCALING_CLOUD)
                    detected.damage = self.cloud_damage

                # Position the fire
                detected.center_x = coOrds[0]
                detected.center_y = coOrds[1]

                if event == "fire":
                    self.fire_list.append(detected)
                else:
                    self.clouds_list.append(detected)

    def add_new_data(self):
        fileName = self.NNDir + "background" + str(self.background_index) + "-fire.txt"

        with open(fileName) as f:
            lines = f.readlines()

            line = lines[-1].strip()
            line = eval(line, {"__builtins__": {}})
            self.add_sprite("fire",(line[0] + SCREEN_WIDTH, SCREEN_HEIGHT - line[1]))

    def check_fire_collison(self,sprite):
        # Generate a list of all emergencies that collided with the satellite.
        hit_list = arcade.check_for_collision_with_list(sprite,self.fire_list)

        if sprite == self.player_sprite:
            sound = arcade.sound.load_sound("Music/sounds/Ching.wav")
        else:
            sound = arcade.sound.load_sound("Music/sounds/beep.wav")

        # Loop through each colliding fire, remove it, and add to the cpu_score.
        for fire in hit_list:
            if not self.Test:
                arcade.sound.play_sound(sound)
            fire.kill()
            sprite.score += 100
