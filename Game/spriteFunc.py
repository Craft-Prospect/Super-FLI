from sprites import *
import pygame
import random
import os
import subprocess

class Mixin:
    #dd clouds and fire to game
    def add_sprite(self,event,coOrds = None):
     #Check coOrds are valid clouds and fire to game (coOrds = None is used to random generate a sprite's coOrds)
     if (coOrds == None) or (coOrds[0] >= 0 and coOrds[1] >=0 and coOrds[1] < SCREEN_HEIGHT):

                if event == "fire":
                    # Create the fire instance
                    detected = Fire(IMG_FIRE, SPRITE_SCALING_FIRE)

                else:
                    #Create cloud instance
                    detected=Cloud(IMG_CLOUD, SPRITE_SCALING_CLOUD)
                    detected.damage = self.cloud_damage
                    detected.points = ((-161, 0), (-128.5, 26.0), (-91.5, 51.0), (-66.5, 50.0),(-11.5,50), (33.5,66), (65.5,47), (120.5,26),(144.5,-26),(133.5,-78),(-47.5,-73),(-74.5,-39), (-114.5,-20), (-128.5, -26.0))

                # Position the sprite using coOrds
                if coOrds != None:
                    detected.center_x = coOrds[0]
                    detected.center_y = coOrds[1]
                #Randomly generate spirte's coOrds
                else:
                    detected.center_y = random.randrange(0,SCREEN_HEIGHT )
                    detected.center_x = SCREEN_WIDTH + random.randrange(0,SCREEN_WIDTH)

                #Add Sprite to relevant list
                if event == "fire":
                    self.fire_list.append(detected)
                else:
                    self.clouds_list.append(detected)

    #Helper function used by NN. Adds fires based on results included in file
    def add_new_data(self):
        #Relevant file names
        fileName = self.NNDir + "background" + str(self.background_index) + "-fire.txt"
        picture =  self.source[self.background_index-1]

        with open(fileName) as f:
            lines = f.readlines()
            line = lines[-1].strip()

            #Check to see if fire detected. If so, add fire sprite
            if line[0] == '(':
                line = eval(line, {"__builtins__": {}})
                self.add_sprite("fire",(line[0] + SCREEN_WIDTH, SCREEN_HEIGHT - line[1]))

    #Check if sprite is colliding with fire(trigger by CPU on update but by player on button press)
    def check_fire_collison(self,sprite):
        # Generate a list of all emergencies that collided with the satellite.
        hit_list = arcade.check_for_collision_with_list(sprite,self.fire_list)

        #Setup right sound effect
        if sprite == self.player_sprite:
            sound = self.player_sound
        else:
            sound = self.cpu_sound

        # Loop through each colliding fire, remove it, and add to the sprite's score.
        for fire in hit_list:
            #If not testing with headless setup(no display)
            if not self.Test:
                sound.play()
            fire.kill()
            sprite.score += SCOREINC
