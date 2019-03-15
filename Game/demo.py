from sprites import *

class Mixin:
    #Setgame variables
    def demo_setup(self):
        # Sprite lists
        self.fire_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.cpu_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Satellite(IMG_PLAYER, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = STARTX
        self.player_sprite.center_y = STARTY
        self.player_list.append(self.player_sprite)

        #Set up CPU
        self.cpu_sprite= Satellite(IMG_CPU, SPRITE_SCALING_PLAYER)
        self.cpu_sprite.center_x = CPU_START_X
        self.cpu_sprite.center_y = CPU_START_Y
        self.cpu_list.append(self.cpu_sprite)

        self.add_sprite("cloud",(300,520))
        self.add_sprite("cloud",(300,50))

        #Set up background
        self.background = arcade.load_texture(IMG_DEMO)

        #For counting when the next instruction shoul be displayed
        self.update_count = 0

        self.level = "Demo"

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

        self.draw_game_text() #Defined in runGame.py

    #Draw instruction on screen
    def draw_ins(self,text):
        arcade.draw_text((text),SCREEN_WIDTH//2-450,SCREEN_HEIGHT//2-100,arcade.color.ORANGE, 15)
        arcade.draw_text(("Click" + BUTTON2 + "to get skip current instruction"),SCREEN_WIDTH-450,SCREEN_HEIGHT-60,arcade.color.ORANGE, 15)
        arcade.draw_text(("Click" + BUTTON1 + "to start"),SCREEN_WIDTH-350,SCREEN_HEIGHT-80,arcade.color.ORANGE, 15)
    #Draw various instructions, dependant on what the state is
    def draw_ins_state(self):
            if self.current_state == INS0:
                self.draw_ins("You will be controlling the blue satellite. \nThe neural network will be controlling the red satellite.")

            elif self.current_state == INS1:
                self.draw_ins("The aim of the game is collect the most money. \nCapture fires to collect money")

            elif self.current_state == INS2:
                self.draw_ins("The Neural Network will detect fires\n It will add a sprite to help you capture the fires")

            elif self.current_state == INS4:
                self.draw_ins("Clouds will drain your power. \nIf you have no power left, your satellite will disapear")

            elif self.current_state == INS7:
                self.draw_ins("Capture a fire by pressing the" + BUTTON2 + "button\n Your score will increase by " + SYMBOL +"100")

            elif self.current_state == INS9:
                self.draw_ins("Press" + BUTTON1 + "to to start!")
