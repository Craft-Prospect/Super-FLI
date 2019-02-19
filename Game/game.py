"""Satellite game where user competes against CPU to capture events while avoid clouds"""

import arcade
import os
import glob
import time
import sys

#Scaling for sprites
SPRITE_SCALING_POINTER = 1
SPRITE_SCALING_KEY = 1

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

#Raspberry Pi speeds
RASP = 0
#RASP = 20

#Sprite Speeds
MOVEMENT_SPEED = 1.5 + RASP  #Player speeds
CPU_SPEED = 1.25 + RASP #Normal CPU speed
CPU_TRACK_SPEED = 0.5 + RASP #CPU speed when no emergency on screen and is tracking player movement
SCROLL_SPEED = 1 + RASP #Speed of background_sprite, clouds and fire sprites

#Variable for setting difficulty
CLOUD_DAMAGE = 0.1*(RASP +1)
HEALTH = 100

#Number of buttons in the menu
BUTTON = 2

#Sprite co-ordinates (will be replaced by NN)
fire_data = [("fire",(150,400))]
 
cloud_data = [("cloud", (0,150)),("cloud", (420,300)),("cloud", (700,742)),("cloud", (1000,200)),("cloud", (1500,10)),("cloud", (1800,200)),("cloud", (2000,0)),("cloud", (1500,10)),("cloud", (1800,200)),("cloud", (2000,0)),("cloud", (1500,10)),("cloud", (1800,200)),("cloud", (2000,0))]


#Image source (global variable so can be used in testing) 
SOURCE=["images/fire.jpg", "images/forest.png", "images/fire.jpg", "images/forest.png","images/sea.png"]
NNDir = "NNData/"
#PLayer's score for saving in Highscore file
Final_score = 0

#Game states
START_PAGE = 0
INSTRUCT1 = 1
INSTRUCT2 = 2
GAME_PAGE = 3
END_PAGE = 4
ENTER_NAME = 5
HIGH_SCORE_PAGE = 6
FEEDBACK_PAGE = 7

#Demo states
#Game states
INS0 = 10
INS1 = 11
INS2 = 12
INS3 = 13
INS4 = 14
INS5 = 15
INS6 = 16
INS7 = 17
INS8 = 18
INS9 = 19

#Initial game state
STATE = START_PAGE

#Player co-ordinates
PLAYER_START_X = 50
PLAYER_START_Y = 50

#Demo co-ordinates
STARTX= 50
STARTY = 50

#CPU co-ordinates
CPU_START_X = 50
CPU_START_Y = SCREEN_HEIGHT - 50

#Variables used for joystick movement
DEAD_ZONE = 0.02

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


#Class for scrolling back ground image
class Background(arcade.Sprite):
    def update(self):

        # Move the fire
        self.center_x -= SCROLL_SPEED 

        #If background has finsished scrolling(No image left to show), end the game
        if self.right <0:
            self.kill()
            return 1 

        return 0 


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

#Class for each Key contains it's 'Character'
class Key(arcade.Sprite):
    character = ""

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

        global fire_data
        self.fire_data = fire_data.copy()
        
        global cloud_data 
        self.cloud_data = cloud_data.copy()
        
        # Set up the player info
        self.player_sprite = None
       
        #Set up CPU sprite
        self.cpu_sprite = None

        #Background sprites
        self.background_list = None
        self.background_even = None
        self.background_odd = None
        self.background_index = 0
        self.final_background = False
        self.background = None

        #For screenshot timings
        self.frame = 800
        self.frame_count = 0
        self.picture = 0

        #Game state
        self.current_state = STATE  

        #Instruction pages
        self.instructions = []

        #Setup background textures
        texture = arcade.load_texture("images/menu.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/instruct_0.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/instruct_1.png")
        self.instructions.append(texture)
        #Menu buttons
        self.buttons = None
        self.start_button = None
        self.inst_button = None

        #Currently selected buttons
        self.selected = None

        #Pointer into button list
        self.selected_index = None

        #Sprite to show which button is selected
        self.pointer_list = None
        self.pointer = None
        
        self.start_page_setup()


        #Keyboard values
        self.key_list = None
 
        # Get a list of all the game controllers that are plugged in
        joysticks = arcade.get_joysticks()

        # If we have a game controller plugged in, grab it and
        # make an instance variable out of it.
        joysticks = arcade.get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
            self.joystick.on_joybutton_press = self.on_joybutton_press
            self.joystick.on_joybutton_release = self.on_joybutton_release
            self.joystick.on_joyhat_motion = self.on_joyhat_motion

        else:
            self.joystick = None

    def start_page_setup(self):

        #Setup up lists for buttons
        self.buttons = arcade.SpriteList()
        self.pointer_list = arcade.SpriteList()

        #Setup button for launching game
        self.start_button = Button("images/button(blank).png", SPRITE_SCALING_BUTTON)
        self.start_button.center_x = SCREEN_WIDTH//2 
        self.start_button.center_y = SCREEN_HEIGHT//2 + 50
        
        #Setup button for displaying instructions
        self.inst_button = Button("images/button(blank).png", SPRITE_SCALING_BUTTON)
        self.inst_button.center_x = SCREEN_WIDTH//2 
        self.inst_button.center_y = SCREEN_HEIGHT//2 - 50
 
        self.buttons.append(self.start_button)
        self.buttons.append(self.inst_button)

        #Set up indicator for selected button
        self.pointer = Button("images/arrow.png", SPRITE_SCALING_BUTTON)
        self.pointer.center_y = self.start_button.center_y
        self.pointer.center_x = self.start_button.center_x - 100

        self.pointer_list.append(self.pointer)

        #Start off with the start game button being selected
        self.selected = self.start_button
        self.selected_index = 0

    #Setgame variables
    def setup(self):

        global fire_data
        self.fire_data = fire_data.copy() 
        
        global cloud_data 
        self.cloud_data = cloud_data.copy()
        
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
        self.background_list = arcade.SpriteList()
        
        self.background_even= Background(SOURCE[0], BACKGROUND_SCALING)
        self.background_even.center_x = SCREEN_WIDTH/2
        self.background_even.center_y = SCREEN_HEIGHT/2
        
        self.background_odd = Background(SOURCE[1], BACKGROUND_SCALING)
        self.background_odd.center_x = SCREEN_WIDTH + SCREEN_WIDTH/2
        self.background_odd.center_y= SCREEN_HEIGHT/2
        
        self.background_list.append(self.background_even)
        self.background_list.append(self.background_odd)

        self.background_index = 2
        self.add_new_data()

        for i in range(0,3):
            if len(self.fire_data) > 0:
                item = self.fire_data.pop(0)
                self.add_sprite(item[0],item[1])
            if len(self.cloud_data) > 0:
                item = self.cloud_data.pop(0)
                self.add_sprite(item[0],item[1])
        
    def draw_game(self):

        # This command has to happen before we start drawing
        arcade.start_render()
        
        #Backgrounds
        self.background_list.draw()
        
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


    #Draw main menu
    def draw_start_page(self):
        
        #Load background image
        page_texture = self.instructions[0] 
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

        #Draw buttons
        self.buttons.draw()
        self.pointer_list.draw()

        #Add text for title and buttons
        arcade.draw_text(("Working Title"),SCREEN_WIDTH//2 - 100 , (5*(SCREEN_HEIGHT//6)), arcade.color.RED, 30)
        arcade.draw_text(("Start Game"),SCREEN_WIDTH//2-55 , ((SCREEN_HEIGHT//2+50)), arcade.color.BLACK, 15)
        arcade.draw_text(("Instructions"),SCREEN_WIDTH//2-55 , ((SCREEN_HEIGHT//2-50)), arcade.color.BLACK, 15)

    #Draw instruction page
    def draw_page(self, page_number):

        #Load background image
        page_texture = self.instructions[page_number] 
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
        #Load test for insturction pages
        if page_number == 1:
            arcade.draw_text(("Control your satellite \nwith the joystick"),SCREEN_WIDTH - 500 , (5*(SCREEN_HEIGHT//6)), arcade.color.BLACK, 25)
            arcade.draw_text(("Capture fire by \npressing the button"),SCREEN_WIDTH - 500 , (13*(SCREEN_HEIGHT//24)), arcade.color.BLACK, 25)
            arcade.draw_text(("Avoid clouds which \ndrain your power"),SCREEN_WIDTH - 500 , (6*(SCREEN_HEIGHT//24)), arcade.color.BLACK, 25)

        elif page_number == 2:
            arcade.draw_text(("You will be competing \nagainst a computer, acting \nas a satellite powered  \nby a Neural Network."),SCREEN_WIDTH - 600 , (2*(SCREEN_HEIGHT//3)), arcade.color.BLACK, 30)

    #Draw game over screen
    def draw_game_over(self):
        output = "Game Over"
        arcade.draw_text(output, 240, 400, arcade.color.WHITE, 54)

        output = "Click to restart"
        arcade.draw_text(output, 310, 300, arcade.color.WHITE, 24)

        if self.player_sprite.active:
            global Final_score
            Final_score = self.player_sprite.score
    #Display high scores
    def draw_high_score(self):
        page_texture = arcade.load_texture("images/hs.jpeg")
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
 
        arcade.draw_text(("HIGH SCORES"), SCREEN_WIDTH//2-200, 3*SCREEN_HEIGHT/4, arcade.color.RED, 40)


        #Get top ten high scores from file
        i = 1 
        
        with open('scores.txt', 'r') as f:
            while i <11:
                line = f.readline()
                line = str(i) + ". " + line
                
                #Display highscores opn screen
                arcade.draw_text((line),SCREEN_WIDTH//2-150 , (3*SCREEN_HEIGHT/4-(40*i)), arcade.color.WHITE, 30)
                i += 1

    def draw_feedback(self):
        page_texture = arcade.load_texture("images/feedback.png")
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, page_texture.width, page_texture.height, page_texture, 0)
        
        arcade.draw_text(("Please leave some feedback"), SCREEN_WIDTH//2-400, 3*SCREEN_HEIGHT/4, arcade.color.RED, 40)


    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()
        
        #Draw different events dependant on stage

        if self.current_state == START_PAGE:
            self.draw_start_page()

        elif self.current_state == INSTRUCT1:
            self.draw_page(1)

        elif self.current_state == INSTRUCT2:
            self.draw_page(2)

        elif self.current_state == GAME_PAGE:
            self.draw_game()

        elif self.current_state == END_PAGE:
            self.draw_game()
            self.draw_game_over()

        elif self.current_state == ENTER_NAME:
            self.keyboard_on_draw()
        
        elif self.current_state == HIGH_SCORE_PAGE:
            self.draw_high_score()

        elif self.current_state == FEEDBACK_PAGE:
            self.draw_feedback()
        
        elif self.current_state >= 10:
            self.draw_demo()

            #Draw different text depending on stage 
            if self.current_state == INS0:
                self.draw_ins("You will be controlling the blue satellite. \nThe neural network will be controlling the red satellite.")
        
            elif self.current_state == INS1:
                self.draw_ins("The aim of the game is collect the most money. \nCapture fires to collect money")

            elif self.current_state == INS2:
                self.draw_ins("The Neural Network will detect fires\n It will add a sprite to help you capture the fires")
        
            elif self.current_state == INS4:
                self.draw_ins("Clouds will drain your power. \nIf you have no power left, your satellite will disapear")
        
            elif self.current_state == INS7:
                self.draw_ins("Capture a fire by pressing the [] button\n Your score will increase by £100")


    #Change between game pages (e.g instructions and high score)
    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_state == START_PAGE:
            #Change state depending on button selected
            if self.selected == self.inst_button:
                self.current_state = INSTRUCT1
            else:
                self.demo_setup()
                self.draw_demo()
                self.current_state = INS0

        elif self.current_state == INSTRUCT1:
            self.current_state = INSTRUCT2

        elif self.current_state == INSTRUCT2:
                self.demo_setup()
                self.draw_demo()
                self.current_state = INS0

        elif self.current_state == END_PAGE:
            self.current_state = ENTER_NAME
            self.keyboard_setup()
        
        elif self.current_state == HIGH_SCORE_PAGE:
            self.current_state = FEEDBACK_PAGE
    
        elif self.current_state == FEEDBACK_PAGE:
            self.start_page_setup()
            self.current_state = START_PAGE

        elif self.current_state >= 10:
            global PLAYER_START_X
            PLAYER_START_X = self.player_sprite.center_x

            global PLAYER_START_Y 
            PLAYER_START_Y = self.player_sprite.center_y

            self.setup()
            self.current_state = GAME_PAGE



    #Refresh the screen
    def update(self, delta_time):

        if self.current_state == GAME_PAGE:

            # Update the position according to the game controller
            if self.joystick:

                # Set a "dead zone" to prevent drive from a centered joystick
                if abs(self.joystick.x) < DEAD_ZONE:
                    self.player_sprite.change_x = 0
                else:
                    self.player_sprite.change_x = self.joystick.x * MOVEMENT_SPEED

            # Set a "dead zone" to prevent drive from a centered joystick
                if abs(self.joystick.y) < DEAD_ZONE:
                    self.player_sprite.change_y = 0
                else:
                    self.player_sprite.change_y = -self.joystick.y * MOVEMENT_SPEED

            self.player_sprite.update()



            #If player is alive, update
            if self.player_sprite.active:
                self.player_list.update()
        
            #Update sprites and clouds
            self.fire_list.update()
        
            self.clouds_list.update()

            update = self.background_even.update()
            update -= self.background_odd.update()

            #If the even background sprite have reached the end of the screen
            if(update == 1):
                
                #If there's no more backgrounds, don't make another
                if(self.final_background):
                    pass


                else:
                    #Else create a new even background, off screen, to scroll after the next odd one
                    self.background_even = Background(SOURCE[self.background_index], BACKGROUND_SCALING)
                    self.background_index += 1
                    self.background_even.center_x = SCREEN_WIDTH + SCREEN_WIDTH/2
                    self.background_even.center_y = SCREEN_HEIGHT/2
                    self.background_list.append(self.background_even)
                    self.add_new_data()

                #If there is no more backgrounds left
                if (self.background_index == len(SOURCE)):
                    self.final_background = True 

            #If the odd background has reached the end of the screen
            elif(update == -1):
                
                #If it's the final background, end the game (This code may need to be added to the even side, if an even number of bacgkrounds is used)
                if(self.final_background):
                    self.current_state = END_PAGE

                else:
                    #Create a new odd background, opff screen, ready to scroll in after the next even one
                    self.background_odd = Background(SOURCE[self.background_index], BACKGROUND_SCALING)
                    self.background_index += 1
                    self.background_odd.center_x = SCREEN_WIDTH + SCREEN_WIDTH/2
                    self.background_odd.center_y = SCREEN_HEIGHT/2

                    self.background_list.append(self.background_odd)
                    self.add_new_data()

                    #If there's no backgrounds left
                    if (self.background_index == len(SOURCE)):
                        self.final_background = True 
            
            #Update CPU satellite
            if self.cpu_sprite.active:
                if len(self.fire_list)> 0:
                    self.cpu_sprite.cpu_update(self.player_sprite,self.fire_list[0])
                else:
                    self.cpu_sprite.cpu_update(self.player_sprite)
                self.cpu_list.update()

                # Generate a list of all emergencies that collided with the satellite.
                hit_list = arcade.check_for_collision_with_list(self.cpu_sprite,self.fire_list)
                # Loop through each colliding fire, remove it, and add to the cpu_score.
                for fire in hit_list:
                    fire.kill()
                    self.cpu_sprite.score += 100
              

                # Generate a list of all clouds that collided with the CPU.
                hit_list = arcade.check_for_collision_with_list(self.cpu_sprite,self.clouds_list)

                # Loop through each colliding cloud, decrease CPU health.
                for cloud in hit_list:
                    self.cpu_sprite.health -= CLOUD_DAMAGE 

                    if self.cpu_sprite.health <= 0:
                        self.cpu_sprite.active = False
                        self.cpu_sprite.kill()

                        if not self.player_sprite.active:
                            self.current_state = END_PAGE

            #If the player is there
            if self.player_sprite.active:
                # Generate a list of all clouds that collided with the player.
                hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.clouds_list)

                # Loop through each colliding sprite, remove it, and add to the player_score.
                for cloud in hit_list:
                    self.player_sprite.health -= CLOUD_DAMAGE

                    if self.player_sprite.health <=0:
                        self.player_sprite.active = False
                        global Final_score 
                        Final_score = self.player_sprite.score
                        self.player_sprite.kill()

                        if not self.cpu_sprite.active:
                            self.current_state=END_PAGE

            if len(self.fire_list) <3 and len(self.fire_data) > 0:
                item = self.fire_data.pop(0)
                self.add_sprite(item[0], item[1])
            if len(self.clouds_list) <3 and len(self.cloud_data) > 0:
                item = self.cloud_data.pop(0) 
                self.add_sprite(item[0], item[1])
        
        #If the game is in a text instruction, pause for ~5 secs
        elif self.current_state == INS0 or self.current_state == INS1 or self.current_state == INS4 or self.current_state == INS7:
            if self.update_count == 400:
                self.update_count = 0
                self.current_state += 1 
            else:
                self.update_count += 1
        
        #Generate the sprite for the fire after ~2 secs and display text for ~5 secs
        elif self.current_state == INS2:
            if self.update_count == 400:
                self.update_count = 0
                self.current_state += 1

            elif self.update_count == 200:
                self.add_sprite("fire",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
                self.add_sprite("fire",(2700,200))
            self.update_count += 1

        #Move the clouds close the player 
        elif self.current_state == INS3:
            self.clouds_list.update()

            self.update_count += 1

            if self.update_count == 80:
                self.update_count = 0
                self.current_state += 1
       
        #Do cloud damage to the player
        elif self.current_state == INS5:
            self.clouds_list.update()

            players = [self.cpu_sprite, self.player_sprite]
            for sat in players: 
                # Generate a list of all clouds that collided with the CPU.
                hit_list = arcade.check_for_collision_with_list(sat,self.clouds_list)

                # Loop through each colliding cloud, decrease CPU health.
                for cloud in hit_list:
                    sat.health -= CLOUD_DAMAGE 
            self.update_count += 1

            if self.update_count == 400:
                self.update_count = 0
                self.current_state += 1 

        #Move player close to fire
        elif self.current_state == INS6:
            self.player_sprite.cpu_update(self.cpu_sprite, self.fire_list[0])
            self.update_count += 1

            if self.update_count == 340:
                self.update_count = 0
                self.current_state += 1
        
        #Capture fire and add to player score 
        elif self.current_state == INS8:
            self.fire_list[0].kill()
            self.player_sprite.score += 100
            self.current_state += 1

        elif self.current_state == ENTER_NAME:
            if self.joystick:

                # Set a "dead zone" to prevent drive from a centered joystick
                if abs(self.joystick.x) < DEAD_ZONE:
                    self.pointer_sprite.change_x = 0
                    self.check = 0

                elif self.check == 0:
                    #Joystick movement to the right update position
                    if self.joystick.x == 1:
                        self.pointer_sprite.change_x +=50
                    #Joystick movement to the left update postion
                    else:
                        self.pointer_sprite.change_x -= 50
                    self.check = 1
                    time.sleep(0.2)

                #if statements to ensure pointer always on the keyboard // Replace with case statement?
                if self.pointer_sprite._position[0] >500:
                    self.pointer_sprite._position[0] = 50

                if self.pointer_sprite._position[0] <50:
                    self.pointer_sprite._position[0] = 500

                if self.pointer_sprite._position[0] > 400 and self.pointer_sprite._position[1] == 100:
                    self.pointer_sprite._position[0] = 50

                if self.pointer_sprite._position[0] <50 and self.pointer_sprite._position[1] == 100:
                    self.pointer_sprite._position[0] = 400


                # Set a "dead zone" to prevent drive from a centered joystick
                # Movement value must be greater than dead zone for movement to be registered by the joystick
                if abs(self.joystick.y) < DEAD_ZONE:
                    self.pointer_sprite.change_y = 0
                    self.check_y = 0

                elif self.check_y == 0:
                    if self.joystick.y == -1:
                        self.pointer_sprite.change_y +=50
                    else:
                        self.pointer_sprite.change_y -= 50
                    self.check_y = 1
                    time.sleep(0.2)

                #Scroll back if sprite is moving off the keyboard
                if self.pointer_sprite._position[1] > 200:
                    self.pointer_sprite._position[1] = 100

                if self.pointer_sprite._position[1] <100:
                    self.pointer_sprite._position[1] = 200

            self.pointer_sprite.update()
         
    #Player controls
    def on_key_press(self, key, modifiers):
        if self.current_state == GAME_PAGE:
            if self.player_sprite.active:
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
                    # Loop through each colliding sprite, remove it, and add to the player_score.
                    for fire in hit_list:
                        fire.kill()
                        self.player_sprite.score += 100
        
        elif self.current_state == START_PAGE:
            if key == arcade.key.SPACE:
                self.selected_index = (self.selected_index+1)%2
                self.selected = self.buttons[self.selected_index]
                self.pointer.center_y = self.selected.center_y
        
        elif self.current_state == ENTER_NAME:
            # 65293 value for **ENTER**
            if key == 65293:
                add_high_score(self.name)
                self.current_state = HIGH_SCORE_PAGE

            #If value over 2^16 is selected as it causes a crash
            if key> 65536:
                return

            #Value for shift instead of printing value return
            elif key == 65506:
                return

            #Value for caps key, boolean turned on and off if selected
            elif key == 65509:
                self.caps_on = not self.caps_on
                return

            #Value for delete key
            elif key == 65288:
                self.name = self.name[0:-1]

            #If caps is on append in upper case otherwise in lowercase z
            elif len(self.name) <= 3:

                if self.caps_on:
                    self.name.append(chr(key).upper())

                else:
                    self.name.append(chr(key))

    #Allows for continouse update
    def on_key_release(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

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

    def add_new_data(self):
        fileName = NNDir + "background" + str(self.background_index-1) + "-fire.txt"

        with open(fileName) as f:
            lines = f.readlines()

            for line in lines:
                line[-1].strip()
                line = eval(line, {"__builtins__": {}})                
                self.add_sprite("fire",(line[0] + SCREEN_WIDTH, line[1])) 


#Keyboard code ========================================================================================================================================

    def keyboard_setup(self):
        
        arcade.set_background_color(arcade.color.AMAZON)
        #String taking input
        self.name = []

        #Boolean for CapsLock toggle
        self.caps_on = False

        #Character list tracking variable
        self.key_position = 0

        #Check variable for joystick
        self.check = 0
        self.check_y = 0


        #Sprite lists
        self.pointer_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()

        #Set up pointer
        # Set up the player
        self.pointer_sprite = arcade.Sprite('keyboard_images/icons8-unchecked-checkbox-filled-50.png', SPRITE_SCALING_POINTER)
        self.pointer_sprite.center_x = 50
        self.pointer_sprite.center_y = 200
        self.pointer_list.append(self.pointer_sprite)

        #Setup Delete button
        self.key_sprite = Key('keyboard_images/icons8-clear-symbol-26.png',SPRITE_SCALING_KEY)
        self.key_sprite.center_x = 500
        self.key_sprite.center_y = 150
        self.key_sprite.character = '-'  # use '-' as identifier for backspace
        self.key_list.append(self.key_sprite)

        #Setup enter button
        self.key_sprite = Key('keyboard_images/icons8-enter-26.png',SPRITE_SCALING_KEY)
        self.key_sprite.center_x = 400
        self.key_sprite.center_y = 100
        self.key_sprite.character = ';'  # use ';' as identifier for enter
        self.key_list.append(self.key_sprite)

        #Setup keys
        x = 0
        y = 0
        count = 0
        #for filename in os.listdir('keyboard_images/characters'):
        #Loops through file containing characters and adds creates a 'Key' object for each character
        for filename in sorted(glob.glob('keyboard_images/characters/*.png')):
            if filename.endswith(".png"):
                if count == 10:
                    x = 0
                    y = -50
                if count == 19:
                    x = 0
                    y = -100


                self.key_sprite = Key(filename, SPRITE_SCALING_KEY)
                self.key_sprite.center_x = 50 + x
                self.key_sprite.center_y = 200 + y
                self.key_sprite.character = filename[29]


                count += 1

                x+=50
                self.key_list.append(self.key_sprite)


    def keyboard_on_draw(self):

        arcade.start_render()

        #Print question:
        arcade.draw_text("Enter player name?",50,500,arcade.color.BLACK,20)

        #Prints input text
        arcade.draw_text(''.join(self.name),350,350, arcade.color.BLACK, 40)

        
        
        # Call draw() on all your sprite lists below
        self.pointer_list.draw()
        self.key_list.draw()



    def on_joybutton_press(self, joystick, button):
        print("Button {} down".format(button))

        # If there is a collision between a 'Key' object and the pointer. The Key is added to the hit list
        # Hit list is then iterated through and character value from Key object is added to string  thats printed to the screen 
        if self.current_state == ENTER_NAME:
            character_hit_list = arcade.check_for_collision_with_list(self.pointer_sprite,self.key_list)

            for Key in character_hit_list:
                if Key.character == ';':
                    add_high_score(self.name)
                    self.current_state = HIGH_SCORE_PAGE

                if Key.character == '-':
                    self.name = self.name[0:-1]

                elif len(self.name) <= 3:self.name.append(Key.character.upper())

        if self.current_state == GAME_PAGE:
            # Generate a list of all sprites that collided with the player.
                    hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.fire_list)
                    # Loop through each colliding sprite, remove it, and add to the player_score.
                    for fire in hit_list:
                        fire.kill()
                        self.player_sprite.score += 100
            
            


    #Keeping unused joystick functions for testing
    def on_joybutton_release(self, joystick, button):
        print("Button {} up".format(button))


    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        print("Hat ({}, {})".format(hat_x, hat_y)) 

#====================================================================================================



#Demo code ===============================================================================================================================================
    #Setgame variables
    def demo_setup(self):

        # Sprite lists
        self.fire_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.cpu_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Satellite("images/satellite.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = STARTX 
        self.player_sprite.center_y = STARTY 
        self.player_list.append(self.player_sprite)
        
        #Set up CPU
        self.cpu_sprite= Satellite("images/cpu.png", SPRITE_SCALING_PLAYER)
        self.cpu_sprite.center_x = CPU_START_X
        self.cpu_sprite.center_y = CPU_START_Y
        self.cpu_list.append(self.cpu_sprite)
  
        self.add_sprite("cloud",(300,520))
        self.add_sprite("cloud",(300,50))

        #Set up background
        self.background = arcade.load_texture("images/fire.jpg")

        self.update_count = 0
        
    def draw_demo(self):

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

        player_health = round(self.player_sprite.health,1)
        
        #Display player health on the screen
        health_player= f"Player Power: {player_health}"
        arcade.draw_text((health_player), 10, 50, arcade.color.WHITE, 14)

        cpu_health = round(self.cpu_sprite.health, 1)
        
        #Display cpu health on the screen
        health_cpu= f"CPU Power: {cpu_health}"
        arcade.draw_text(health_cpu, SCREEN_WIDTH-200, 50, arcade.color.RED, 14)

        arcade.draw_text(("Click {} to start"),SCREEN_WIDTH//2-50,50,arcade.color.ORANGE, 15)

    #Draw instruction on screen
    def draw_ins(self,text):
        arcade.draw_text((text),SCREEN_WIDTH//2-450,SCREEN_HEIGHT//2-100,arcade.color.ORANGE, 15)


#helper sort function
def get_number(line):
    return line.split('£')[1]

#When game closes, get player high score and store it in file. Will be included in states with Ibrahim's program
def add_high_score(name):
    #Add name to file

    name = ''.join(name)

    with open('scores.txt', 'a') as f:
        store = (name + " : £" + str(Final_score))
        f.write("%s\n" % store )

    sorted_lines = ''
    
    #Sort file
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        sorted_lines = sorted(lines, key=get_number, reverse = True)
    #Stored sorted file
    with open('scores.txt', 'w') as f:
       f.writelines(sorted_lines)


#Run game
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    #window.set_update_rate(1/10)
    arcade.run()

if __name__ == "__main__":
    main()
  

