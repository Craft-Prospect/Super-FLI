"""Satellite game where user competes against CPU to capture events while avoid clouds"""

import arcade
import os
import time

#Set sprite sizes
SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_FIRE = 1
SPRITE_SCALING_CLOUD = 1
SPRITE_SCALING_BUTTON = 1
BACKGROUND_SCALING = 1 

#Set number of elements to appear on screen (This will be removed when sprites are generated from co-ordinates)
#Window size
SCREEN_WIDTH = 1041
SCREEN_HEIGHT = 597 

#Sprite Speeds
MOVEMENT_SPEED = 2 #Player speeds
CPU_SPEED = 1.25 #Normal CPU speed
CPU_TRACK_SPEED = 0.5 #CPU speed when no emergency on screen and is tracking player movement
SCROLL_SPEED = 1 #Speed of background_sprite, clouds and fire sprites

#Variable for setting difficulty
CLOUD_DAMAGE = 0.1
HEALTH = 100

#Number of buttons in the menu
BUTTON = 2

#Image source (global variable so can be used in testing) 
SOURCE=["images/fire.jpg"]

#PLayer's score for saving in Highscore file
Final_score = 0

#Game states
INS0 = 0
INS1 = 1
INS2 = 2

#Initial game state
STATE = INS0  

#Player co-ordinates
PLAYER_START_X = 50
PLAYER_START_Y = 50

#CPU co-ordinates
CPU_START_X = 50
CPU_START_Y = SCREEN_HEIGHT - 50

#PLayer and CPU sprite class
class Satellite(arcade.Sprite):

    health = HEALTH
    score = 0
    active = True

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
    def cpu_update(self, Player, Fire = None):
        
        #If fire is there, track it else, track player

        #For X co-ordinates if the cpu is furhter left that the fire and there's a fire on the screen
        if (Fire and self.center_x <Fire.center_x and Fire.center_x < (SCREEN_WIDTH-10)):
            self.center_x += CPU_SPEED
        #Else if there's a fire on the screen and the CPU is to the right of it
        elif (Fire and self.center_x > Fire.center_x and Fire.center_x < (SCREEN_WIDTH-10)):
            self.center_x -= CPU_SPEED
        
        #Else if the fire is off-screen, follow the player
        else: 
            if (self.center_x <Player.center_x):
                self.center_x += CPU_TRACK_SPEED
            elif(self.center_x > Player.center_x):
                self.center_x -= CPU_TRACK_SPEED

        #Same as above except for Y co-ordinates
        if (Fire and self.center_y <Fire.center_y and Fire.center_x < (SCREEN_WIDTH-10)):
            self.center_y += CPU_SPEED
        elif (Fire and self.center_y > Fire.center_y and Fire.center_x < (SCREEN_WIDTH-10)):
            self.center_y -= CPU_SPEED
        else: 
            if (self.center_y <Player.center_y):
                self.center_y += CPU_TRACK_SPEED
            elif(self.center_y > Player.center_y):
                self.center_y -= CPU_TRACK_SPEED

#Fire sprite for satellites to capture (Will be replaced by emergencies)
class Fire(arcade.Sprite):

    #Refresh the sprite movement
    def update(self):

        # Move the fire
        self.center_x -= SCROLL_SPEED 

        # See if the fire has moved off the left side of the screen.If it is off screen remove it from the sprite list
        if self.right < 0:
            self.kill()

class Cloud(arcade.Sprite):

    #Scroll the clouds to the left
    def update(self):

        # Move the cloud
        self.center_x -= SCROLL_SPEED 

        # See if the cloud has fallen off the left of the screen, if so, remove it from the sprite list.
        if self.right < 0:
            self.kill()    

#Buttons for main menu, (they do nothin, just a graphical representation)
class Button(arcade.Sprite):

    def update(self):
        pass

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
        self.fire_list=None
        self.clouds_list = None
        
        # Set up the player info
        self.player_sprite = None
       
        #Set up CPU sprite
        self.cpu_sprite = None

        self.background = None

        #Game state
        self.current_state = STATE  

        self.update_count = 0
       
        self.setup()

    #Setgame variables
    def setup(self):

        # Sprite lists
        self.fire_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.cpu_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Satellite("images/satellite.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = PLAYER_START_X 
        self.player_sprite.center_y = PLAYER_START_Y 
        self.player_list.append(self.player_sprite)
        
        #Set up CPU
        self.cpu_sprite= Satellite("images/cpu.png", SPRITE_SCALING_PLAYER)
        self.cpu_sprite.center_x = CPU_START_X
        self.cpu_sprite.center_y = CPU_START_Y
        self.cpu_list.append(self.cpu_sprite)
  
        #Set up background
        self.background = arcade.load_texture("images/fire.jpg")
 
        self.add_sprite("Fire", (SCREEN_HEIGHT/2, SCREEN_WIDTH/2))
        self.add_sprite("Cloud", ((SCREEN_HEIGHT -100), SCREEN_WIDTH/3))
        self.add_sprite("Cloud", (SCREEN_HEIGHT/2, 2*SCREEN_WIDTH/3))
        self.add_sprite("Cloud", (100, SCREEN_WIDTH - 100))
        
    def draw_game(self):

        # This command has to happen before we start drawing
        arcade.start_render()
         
        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw all the sprites.
        self.fire_list.draw()
        self.player_list.draw()
        self.cpu_list.draw()
        self.clouds_list.draw()

        # Put the text on the screen.
         
        # Player Score
        score_player= f"Player Score: £{self.player_sprite.score}"
        arcade.draw_text(score_player, 10, 20, arcade.color.WHITE, 14)

        #CPU Score   
        score_cpu= f"CPU Money: £{self.cpu_sprite.score}"
        arcade.draw_text(score_cpu, SCREEN_WIDTH-200, 20, arcade.color.RED, 14)

        # Player Health
        player_health = round(self.player_sprite.health,1)
        
        #Stop player health being negative
        if player_health < 0:
            player_health = 0
        
        #Display player health on the screen
        health_player= f"Player Power: {player_health}"
        arcade.draw_text((health_player), 10, 50, arcade.color.WHITE, 14)

        #CPU Health   

        cpu_health = round(self.cpu_sprite.health, 1)
        
        #Stop CPU health being negative
        if cpu_health < 0:
            cpu_health = 0
        
        #Display cpu health on the screen
        health_cpu= f"CPU Power: {cpu_health}"
        arcade.draw_text(health_cpu, SCREEN_WIDTH-200, 50, arcade.color.RED, 14)


    def draw_ins0(self):
        text= "You will be controlling the blue satetlite.\n The neural network will be controlling the red Satellite. \n The aim of the game is to collect more money then the other Satellite"
        arcade.draw_text((text), SCREEN_WIDTH/2-200, SCREEN_HEIGHT/2-100, arcade.color.ORANGE, 14)


    def on_draw(self):
        # This command has to happen before we start drawing
        
        self.draw_game()

        if self.current_state == INS0:
            self.draw_ins0()
    #Refresh the screen
    def update(self, delta_time):
        if self.current_state == INS0:
            time.sleep(5)
            self.current_state = INS1

        if self.current_state == INS1:
            self.clouds_list.update()
            self.fire_list.update()

            self.update_count += 1

            if self.update_count == 20:
                self.update_count = 0
                self.current_state = INS0
            


    #Will be used by NN to generate newly identified events
    def add_sprite(self,event,coOrds):
        if coOrds[0] >= 0 and coOrds[1] >=0 and coOrds[1] < SCREEN_HEIGHT:
            if  event == "fire":
                # Create the fire instance
                detected = Fire("images/fire_sprite.png", SPRITE_SCALING_FIRE)

            else:
                #Create cloud instance
                detected=Cloud("images/clouds.png", SPRITE_SCALING_CLOUD)
            
                # Position the fire
                detected.center_x = coOrds[0] 
                detected.center_y = coOrds[1]
            
                if event == "fire":     
                    self.fire_list.append(detected)
                else:
                    self.clouds_list.append(detected)
#Run game
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    #window.set_update_rate(1/10)
    arcade.run()

if __name__ == "__main__":
    main()
