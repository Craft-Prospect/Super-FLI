from sprites import *
import pygame
import subprocess

class Mixin:
   #Setgame variables
    def game_setup(self):
        #Play main game music if not running tests with not display(headless)
        if not self.Test:
                pygame.mixer.music.load(SND_GAME)
                pygame.mixer.music.play(-1)

        # Sprite lists
        self.fire_list = arcade.SpriteList()
        self.clouds_list = arcade.SpriteList()
        self.cpu_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = Satellite(IMG_PLAYER, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_list.append(self.player_sprite)

        self.level = 1
        self.source = self.SOURCE[0] #Load first level

        self.setup_cpu()

        #Set up background
        self.background_setup()

        #Add clouds
        for i in range(0,self.clouds_limit):
                self.add_sprite("cloud")

    #Handles drawing main game
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
        self.draw_game_text()

    #Setup game over music and store player highscore
    def setup_game_over(self):
        if not self.Test:
            pygame.mixer.stop()
            pygame.mixer.music.load(SND_END)
            pygame.mixer.music.play(-1)

        if self.player_sprite.active:
            self.player_score = self.player_sprite.score

    #Draw game over screen
    def draw_game_over(self):

        output = "Game Over"
        arcade.draw_text(output, 240, 400, arcade.color.WHITE, 54)

        output = "Press" + BUTTON1 + "to restart"
        arcade.draw_text(output, 310, 300, arcade.color.WHITE, 24)

    #Draw all text displayed during game
    def draw_game_text(self):
        # Player Score
        score_player= f"Player Score: {SYMBOL}{self.player_sprite.score}"
        arcade.draw_text(score_player, 10, 20, arcade.color.WHITE, 14)

        #CPU Score
        score_cpu= f"Neural Network Score: {SYMBOL}{self.cpu_sprite.score}"
        arcade.draw_text(score_cpu, SCREEN_WIDTH-300, 20, arcade.color.RED, 14)

        # Player Health
        player_health = self.round_health(self.player_sprite)

        #CPU Health
        cpu_health = self.round_health(self.cpu_sprite)

        #Display cpu health on the screen
        health_cpu= f"Neural Network Power: {cpu_health} %"
        arcade.draw_text(health_cpu, SCREEN_WIDTH-300, 50, arcade.color.RED, 14)

        #Display player health on the screen
        health_player= f"Player Power: {player_health} %"
        arcade.draw_text((health_player), 10, 50, arcade.color.WHITE, 14)

        lvl= f"Level: {self.level}"
        arcade.draw_text((lvl), SCREEN_WIDTH//2-10, SCREEN_HEIGHT-20, arcade.color.WHITE, 14)

        if not self.player_sprite.active:
            arcade.draw_text(("Press"+ BUTTON1 + "to end game"), SCREEN_WIDTH//2-200,SCREEN_HEIGHT//2, arcade.color.BLIZZARD_BLUE,20)
    #Round sprite's help to stop negative scores appearing (weird glitch wer eplayer dies with -0.1 health)
    def round_health(self,sprite):
        # Player Health
        health = round(sprite.health,1)

        #Stop player health being negative
        if health < 0:
            health = 0

        return health

    #Configure CPU (also used in levels.py)
    def setup_cpu(self):
        #Set up CPU
        self.cpu_sprite= Satellite(IMG_CPU, SPRITE_SCALING_PLAYER)
        self.cpu_sprite.center_x = CPU_START_X
        self.cpu_sprite.center_y = CPU_START_Y
        self.cpu_sprite.speed = CPU_SPEED
        self.cpu_list.append(self.cpu_sprite)

    #Setup first two backgrounds (also used in levels.py)
    def background_setup(self):
        #Set up background sprites
        self.background_list = arcade.SpriteList()

        self.background_even= Background(self.source[0], BACKGROUND_SCALING)
        self.background_even.center_x = SCREEN_WIDTH/2
        self.background_even.center_y = SCREEN_HEIGHT/2

        self.background_odd = Background(self.source[1], BACKGROUND_SCALING)
        self.background_odd.center_x = SCREEN_WIDTH + SCREEN_WIDTH/2
        self.background_odd.center_y= SCREEN_HEIGHT/2

        self.background_list.append(self.background_even)
        self.background_list.append(self.background_odd)

        self.background_index = 1
        self.final_background_odd = False
        self.final_background_even = False


        self.runNN() #see spriteFunc.py


    def runNN(self):
        #look one image further ahead and run it through the network
        text_file = 'background%d-fire.txt' % (self.background_index+1)

        #if image exits and not running heedless tests, run Neural Network
        if self.background_index < len(self.source) and not self.Test:
            picture = self.source[self.background_index]
            NN_command = COMMAND + [picture]

            with open(self.NNDir+text_file, "wb") as out:
                subprocess.Popen(NN_command, stdout=out)

        #Get NN data and add fires
        self.add_new_data()
