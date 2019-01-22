"""Satellite game where user competes against CPU to capture events while avoid clouds"""

import arcade
import os

#Set sprite sizes
SPRITE_SCALING_PLAYER = 0.25
SPRITE_SCALING_FIRE = 0.01
SPRITE_SCALING_CLOUD = 0.05
BACKGROUND_SCALING = 1 

#Set number of elements to appear on screen (This will be removed when sprites are generated from co-ordinates)
#Window size
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 587 

#Sprite Speeds
MOVEMENT_SPEED = 2  #Player speeds
CPU_SPEED = 1.25 #Normal CPU speed
CPU_TRACK_SPEED = 0.5 #CPU speed when no emergency on screen and is tracking player movement
SCROLL_SPEED = 1  #Speed of background_sprite, clouds and fire sprites

CLOUD_DAMAGE = 0.1
HEALTH = 100

#Sprite co-ordinates (will be replaced by NN)
points = [("cloud", (0,150)),("fire", (120,12)),("fire", (170,800)),("fire", (1200,13)),("fire", (1500,450)),("fire", (1740,12)),("cloud", (0,0)),("cloud", (20,300)),("cloud", (100,342)),("cloud", (500,200)),("cloud", (1000,10)),("cloud", (1300,200)),("cloud", (1600,0)),("cloud", (1653,500)),("cloud", (1800,0)),("cloud", (1900,150)),("fire", (1920,12)),("fire", (2100,800)),("fire", (2400,13)),("fire", (2750,450)),("fire", (3000,12)),("cloud", (2400,400)),("cloud", (2420,100)),("cloud", (2600,342)),("cloud", (2700,200)),("cloud", (3000,10)),("cloud", (3100,200)),("cloud", (3400,0)),("cloud", (3653,500)),("cloud", (3800,0))]
 
#Image source (global variable so can be used in testing) 
SOURCE="images/fire_long.jpg"

#PLayer's score for saving in Highscore file
Final_score = 0

#Game states
START_PAGE = 0
INSTRUCT1 = 1
INSTRUCT2 = 2
GAME_PAGE = 3
END_PAGE = 4
HIGH_SCORE_PAGE = 5


STATE = START_PAGE

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

        
        #X co-ordinates
        if (Fire and self.center_x <Fire.center_x and Fire.center_x < (SCREEN_WIDTH-10)):
            self.center_x += CPU_SPEED
        elif (Fire and self.center_x > Fire.center_x and Fire.center_x < (SCREEN_WIDTH-10)):
            self.center_x -= CPU_SPEED
        
        else: 
            if (self.center_x <Player.center_x):
                self.center_x += CPU_TRACK_SPEED
            elif(self.center_x > Player.center_x):
                self.center_x -= CPU_TRACK_SPEED

           
        #Y co-ordinates
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

        #If background has finsished scrolling, end game
        if self.right <0:
            return END_PAGE

        return GAME_PAGE


#Fire sprite for satellites to capture (Will be replaced by emergencies)
class Fire(arcade.Sprite):

    #Refresh the sprite movement
    def update(self):

        # Move the fire
        self.center_x -= SCROLL_SPEED 

        # See if the fire has movded off the side of the screen.
        # If so, remove it

        if self.right < 0:
            self.kill()


class Cloud(arcade.Sprite):

    #Scroll the clouds to the left
    def update(self):

        # Move the cloud
        self.center_x -= SCROLL_SPEED 

        # See if the cloud has fallen off the left of the screen.
        # If so, remove it.
        if self.right < 0:
            self.kill()    

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

        # Static Background image will be stored in this variable(currently unused)
        self.background = None

        #Background sprite
        self.background_sprite = None

        #For screenshot timings
        self.frame = 800
        self.frame_count = 0
        self.picture = 0

        #Game state
        self.current_state = STATE  

        #Instruction pages
        self.instructions = []

        texture = arcade.load_texture("images/menu.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/instruct_0.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/instruct_1.png")
        self.instructions.append(texture)


    #Setgame variables
    def setup(self):
        
        # Sprite lists
        self.fire_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.cpu_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Satellite("images/satellite.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        
        #Set up CPU
        self.cpu_sprite= Satellite("images/cpu.png", SPRITE_SCALING_PLAYER)
        self.cpu_sprite.center_x = 50
        self.cpu_sprite.center_y = SCREEN_HEIGHT - 50
        self.cpu_list.append(self.cpu_sprite)
  
        #Set up background
        self.background_sprite=Background(SOURCE, BACKGROUND_SCALING)
        self.background_sprite.center_y=SCREEN_HEIGHT/2
        
        # Create the fires and clouds
        for i in range (0,len(points)):
            item = points[i]

            self.add_sprite(item[0], item[1])

    def draw_game(self):

        # This command has to happen before we start drawing
        arcade.start_render()
        
        #Draw background
        self.background_sprite.draw()
        
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
        if player_health < 0:
            player_health = 0
        health_player= f"Player Power: {player_health}"
        arcade.draw_text((health_player), 10, 50, arcade.color.WHITE, 14)

        #CPU Health   
        cpu_health = round(self.cpu_sprite.health, 1)
        if cpu_health < 0:
            cpu_health = 0

        health_cpu= f"CPU Power: {cpu_health}"
        arcade.draw_text(health_cpu, SCREEN_WIDTH-200, 50, arcade.color.RED, 14)

    #Draw instruction page
    def draw_page(self, page_number):

        page_texture = self.instructions[page_number] 
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

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
                arcade.draw_text((line),SCREEN_WIDTH//2-150 , (3*SCREEN_HEIGHT/4-(40*i)), arcade.color.WHITE, 30)
                i += 1

    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        #Draw different events dependant on stage

        if self.current_state == START_PAGE:
            self.draw_page(0)

        elif self.current_state == INSTRUCT1:
            self.draw_page(1)

        elif self.current_state == INSTRUCT2:
            self.draw_page(2)

        elif self.current_state == GAME_PAGE:
            self.draw_game()

        elif self.current_state == END_PAGE:
            self.draw_game()
            self.draw_game_over()
        
        elif self.current_state == HIGH_SCORE_PAGE:
            self.draw_high_score()


    #Change between game pages (e.g instructions and high score)
    def on_mouse_press(self, x, y, button, modifiers):
        # Change states as needed.

        if self.current_state == START_PAGE:
            self.current_state = INSTRUCT1

        elif self.current_state == INSTRUCT1:
            self.current_state = INSTRUCT2

        elif self.current_state == INSTRUCT2:
            self.setup()
            self.current_state = GAME_PAGE

        elif self.current_state == END_PAGE:
            self.current_state = HIGH_SCORE_PAGE
        
        elif self.current_state == HIGH_SCORE_PAGE:
            self.current_state = START_PAGE
            

    #Refresh the screen
    def update(self, delta_time):

        if self.current_state == GAME_PAGE:

            #If player is alive, update
            if self.player_sprite.active:
                self.player_list.update()
        
            #Update sprites and clouds
            self.fire_list.update()
        
            self.clouds_list.update()
            self.current_state = self.background_sprite.update()

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


      #Currently screenshots slow down game. May need better solution

            #Get screeshot for NN
            #if self.frame_count > self.frame:
             #   image = arcade.draw_commands.get_image(x=0, y=0, width=None, height=None)
              #  image.save(("data/screenshot"+ str(self.picture)) + ".png", "PNG")
               # self.frame_count = 0
                #self.picture += 1
            #else:
             #   self.frame_count +=1
    
    
    #Player controls
    def on_key_press(self, key, modifiers):
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
                    detected = Fire("images/fire.png", SPRITE_SCALING_FIRE)

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
#helper sort function
def get_number(line):
    return line.split('£')[1]

#When game closes, get player high score and store it in file. Will be included in states with Ibrahim's program
def add_high_score(name):
    #Add name to file
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
    arcade.run()

if __name__ == "__main__":
    main()
    name = input("Enter your name: \n")
    add_high_score(name)
  

