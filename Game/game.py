"""Satellite game where user competes against CPU to capture events while avoid clouds"""

import arcade
import os

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
MOVEMENT_SPEED = 2 + RASP  #Player speeds
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
HIGH_SCORE_PAGE = 5

#Initial game state
STATE = START_PAGE

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
        self.fire_data = fire_data 
        
        global cloud_data 
        self.cloud_data = cloud_data
        
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
        self.fire_data = fire_data 
        
        global cloud_data 
        self.cloud_data = cloud_data
        
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
            if len(fire_data) > 0:
                item = fire_data.pop(0)
                self.add_sprite(item[0],item[1])
            if len(cloud_data) > 0:
                item = cloud_data.pop(0)
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
        
        elif self.current_state == HIGH_SCORE_PAGE:
            self.draw_high_score()


    #Change between game pages (e.g instructions and high score)
    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_state == START_PAGE:
            #Change state depending on button selected
            if self.selected == self.inst_button:
                self.current_state = INSTRUCT1
            else:
                self.setup()
                self.current_state = GAME_PAGE

        elif self.current_state == INSTRUCT1:
            self.current_state = INSTRUCT2

        elif self.current_state == INSTRUCT2:
            self.setup()
            self.current_state = GAME_PAGE

        elif self.current_state == END_PAGE:
            self.current_state = HIGH_SCORE_PAGE
        
        elif self.current_state == HIGH_SCORE_PAGE:
            self.start_page_setup()
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

            if len(self.fire_list) <3 and len(fire_data) > 0:
                item = fire_data.pop(0)
                self.add_sprite(item[0], item[1])
            if len(self.clouds_list) <3 and len(cloud_data) > 0:
                item = cloud_data.pop(0) 
                self.add_sprite(item[0], item[1])

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
    #window.set_update_rate(1/10)
    arcade.run()

if __name__ == "__main__":
    main()
    name = input("Enter your name: \n")
    add_high_score(name)
  

