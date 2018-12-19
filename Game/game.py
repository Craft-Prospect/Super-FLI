"""Satellite game where user competes against CPU to capture events while avoid clouds"""

import arcade
import os
import random

#Set sprite sizes
SPRITE_SCALING_PLAYER = 0.25
SPRITE_SCALING_FIRE = 0.01
SPRITE_SCALING_CLOUD = 0.05
BACKGROUND_SCALING = 1 

#Set number of elements to appear on screen (This will be removed when sprites are generated from co-ordinates)
CLOUD_COUNT = 3
FIRE_COUNT = 0
#Window size
SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 587 

#Sprite Speeds
MOVEMENT_SPEED = 2  #Player speeds
CPU_SPEED = 1.25  #Normal CPU speed
CPU_TRACK_SPEED = 0.5 #CPU speed when no emergency on screen and is tracking player movement
SCROLL_SPEED = 1  #Speed of background, clouds and fire sprites

#Sprite co-ordinates
points = [("fire", (0,150)),("fire", (120,12)),("fire", (170,800)),("fire", (1200,13)),("fire", (1500,450)),("fire", (1740,12)),("cloud", (0,0)),("cloud", (20,300)),("cloud", (100,342)),("cloud", (500,200)),("cloud", (1000,10)),("cloud", (1300,200)),("cloud", (1600,0)),("cloud", (1653,500)),("cloud", (1800,0))]
 
#PLayer and CPU sprite class
class Satellite(arcade.Sprite):

    #Normal update called when screen is refreshed
    def update(self):
        #Change satellite position to new x and y
        self.center_x += self.change_x
        self.center_y += self.change_y

        #Ensure satellite doesn't run off screen
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

    #Addtional update called for CPU player. Moves CPU towards Fire or Player
    def cpu_update(self, Fire,Player):
        
        """If fire is there, track it else, track player"""

        #X co-ordinates
        if (self.center_x <Fire.center_x and Fire.center_x < SCREEN_WIDTH):
            self.center_x += CPU_SPEED
        elif (self.center_x > Fire.center_x and Fire.center_x < SCREEN_WIDTH):
            self.center_x -= CPU_SPEED
        
        else: 
            if (self.center_x <Player.center_x):
                self.center_x += CPU_TRACK_SPEED
            else:
                self.center_x -= CPU_TRACK_SPEED

           
        #Y co-ordinates
        if (self.center_y <Fire.center_y and Fire.center_x < SCREEN_WIDTH):
            self.center_y += CPU_SPEED
        elif (self.center_y > Fire.center_y and Fire.center_x < SCREEN_WIDTH):
            self.center_y -= CPU_SPEED
        else: 
            if (self.center_y <Player.center_y):
                self.center_y += CPU_TRACK_SPEED
            else:
                self.center_y -= CPU_TRACK_SPEED


class Background(arcade.Sprite):
    def update(self):

        # Move the fire
        self.center_x -= SCROLL_SPEED 

        if self.left < 0:
            pass
           #Game will end here 

#Fire sprite for satellites to capture (Will be replaced by emergencies)
class Fire(arcade.Sprite):

    #Refresh the sprite movement
    def update(self):

        # Move the fire
        self.center_x -= SCROLL_SPEED 

        # See if the fire has movded off the side of the screen.
        # If so, reset it

        global FIRE_COUNT
        if self.left < 0:
            self.kill()
            FIRE_COUNT -=1


class Cloud(arcade.Sprite):

    #Scroll the clouds to the left
    def update(self):

        # Move the cloud
        self.center_x -= SCROLL_SPEED 

        # See if the cloud has fallen off the left of the screen.
        # If so, reset it.
        global CLOUD_COUNT
        if self.left < 0:
            self.kill()    
            CLOUD_COUNT -=1

#Main window
class MyGame(arcade.Window):
    #Initalise game variables and window
    def __init__(self, width, height):

        # Call the parent class initialise to window
        super().__init__(width, height)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold the sprite lists
        self.player_list = None

        self.fire_list=None
        self.cpu_list = None 

        self.clouds_list = None
        
        # Set up the player info
        self.player_sprite = None
        self.player_score = 0

        #Set up CPU sprite
        self.cpu_sprite = None
        self.cpu_score = 0

        # Background image will be stored in this variable
        self.background = None

    #Setgame variables
    def setup(self):
        
        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.fire_list = arcade.SpriteList()
        self.cpu_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()

        # Set up the player
        self.player = True
        self.player_score = 0
        self.player_sprite = Satellite("images/satellite.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        self.player_health = 100
        
        #Set up CPU
        self.cpu = True
        self.cpu_score = 0
        self.cpu_health = 100
        self.cpu_sprite = Satellite("images/cpu.png", SPRITE_SCALING_PLAYER)
        self.cpu_sprite.center_x = SCREEN_WIDTH - 50
        self.cpu_sprite.center_y = SCREEN_HEIGHT - 50
        self.cpu_list.append(self.cpu_sprite)
       
        #Set up background
        self.background=Background("images/fire_long.jpg", BACKGROUND_SCALING)
        self.background.center_y=SCREEN_HEIGHT/2
        # Create the fires
        
        global FIRE_COUNT
        global CLOUD_COUNT

        for item in points:
            detected = None

            #Check for in valid values
            if item[1][0] < 0 or item[1][1] < 0 or item[1][1] > SCREEN_HEIGHT:
                break


            if item[0] == "fire":
                # Create the fire instance
                detected = Fire("images/fire.png", SPRITE_SCALING_FIRE)
                FIRE_COUNT += 1

            else:
                #Create cloud instance
                detected=Cloud("images/clouds.png", SPRITE_SCALING_CLOUD)

            
            # Position the fire
            detected.center_x = item[1][0] 
            detected.center_y = item[1][1]
            
            if item[0] == "fire":     
                self.fire_list.append(detected)
            else:
                self.clouds_list.append(detected)

    #Generate sprites and load window
    def on_draw(self):

        # This command has to happen before we start drawing
        arcade.start_render()
        
        #Draw background
        self.background.draw()
        
        # Draw all the sprites.
        self.fire_list.draw()
        self.player_list.draw()
        self.cpu_list.draw()
        self.clouds_list.draw()

        # Put the text on the screen.
         
        # Player Score
        score_player= f"Player Score: {self.player_score}"
        arcade.draw_text(score_player, 10, 20, arcade.color.WHITE, 14)

        #CPU Score   
        score_cpu= f"CPU Score: {self.cpu_score}"
        arcade.draw_text(score_cpu, SCREEN_WIDTH-155, 20, arcade.color.RED, 14)

        # Player Health
        player_health = int(self.player_health)
        health_player= f"Player Health: {player_health}"
        arcade.draw_text((health_player), 10, 50, arcade.color.WHITE, 14)

        #CPU Health   
        cpu_health = int(self.cpu_health)
        health_cpu= f"CPU Health: {cpu_health}"
        arcade.draw_text(health_cpu, SCREEN_WIDTH-155, 50, arcade.color.RED, 14)


    #Refresh the screen
    def update(self, delta_time):
        #If player is alive, update 
        if self.player:
            self.player_list.update()
        
        #Update sprites and clouds
        self.fire_list.update()
        
        self.clouds_list.update()
        self.background.update()

        #Update CPU satellite
        global FIRE_COUNT
        if self.cpu:
            for cpu in self.cpu_list:
                if FIRE_COUNT > 1:
                    cpu.cpu_update(self.fire_list[0],self.player_list[0])
            self.cpu_list.update()

            # Generate a list of all emergencies that collided with the satellite.
            hit_list = arcade.check_for_collision_with_list(self.cpu_sprite,self.fire_list)

            # Loop through each colliding fire, remove it, and add to the cpu_score.
            for fire in hit_list:
                fire.kill()
                FIRE_COUNT -= 1
                self.cpu_score += 1

            # Generate a list of all clouds that collided with the CPU.
            hit_list = arcade.check_for_collision_with_list(self.cpu_sprite,self.clouds_list)

            # Loop through each colliding cloud, decrease CPU health.
            for cloud in hit_list:
                self.cpu_health -= 0.1

                #If the CPU is dead, remove it
                if self.cpu_health <0:
                    self.cpu_sprite.kill()
                    self.cpu = False

        #If the player is there
        if self.player:
            # Generate a list of all clouds that collided with the player.
            hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.clouds_list)

            # Loop through each colliding sprite, remove it, and add to the player_score.
            for cloud in hit_list:
                self.player_health -= 0.1

                #If player dead, remove it
                if self.player_health <0:
                    self.player_sprite.kill()
                    self.player = False





    #Player controls
    def on_key_press(self, key, modifiers):

        """Pressing arrow keys """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        
        #PLayer attempts to capture
        elif key == arcade.key.SPACE:

            # Generate a list of all sprites that collided with the player.
            hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.fire_list)
            global FIRE_COUNT
            # Loop through each colliding sprite, remove it, and add to the player_score.
            for fire in hit_list:
                fire.kill()
                FIRE_COUNT -= 1
                self.player_score += 1



    #Allows for continouse update
    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

#Run game
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
