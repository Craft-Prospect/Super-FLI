from sprites import *
import pygame

class Mixin:
   #Setgame variables
    def setup(self):

        #s = arcade.sound.load_sound("Music/ResistorAnthems/test.mp3")
        #arcade.sound.play_sound(s)
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
        self.cpu_sprite.speed = CPU_SPEED
        self.cpu_list.append(self.cpu_sprite)

        #Set up background
        self.background_list = arcade.SpriteList()

        self.background_even= Background(self.source[0], BACKGROUND_SCALING)
        self.background_even.center_x = SCREEN_WIDTH/2
        self.background_even.center_y = SCREEN_HEIGHT/2

        self.background_odd = Background(self.source[1], BACKGROUND_SCALING)
        self.background_odd.center_x = SCREEN_WIDTH + SCREEN_WIDTH/2
        self.background_odd.center_y= SCREEN_HEIGHT/2

        self.background_list.append(self.background_even)
        self.background_list.append(self.background_odd)

        self.background_index = 2
        self.final_background = False
        self.add_new_data()


        #Display up to three fires and clouds at a time (for performance)
        self.fire_data = self.init_fire_data.copy()
        self.cloud_data = self.init_cloud_data.copy()

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
        player_health = self.round_health(self.player_sprite)

        #CPU Health
        cpu_health = self.round_health(self.cpu_sprite)

        #Display cpu health on the screen
        health_cpu= f"CPU Power: {cpu_health}"
        arcade.draw_text(health_cpu, SCREEN_WIDTH-200, 50, arcade.color.RED, 14)

        #Display player health on the screen
        health_player= f"Player Power: {player_health}"
        arcade.draw_text((health_player), 10, 50, arcade.color.WHITE, 14)


    #Draw game over screen
    def draw_game_over(self):
        pygame.mixer.stop()
        pygame.mixer.music.load("Music/ResistorAnthemsII/end.mp3")
        pygame.mixer.music.play(-1)


        output = "Game Over"
        arcade.draw_text(output, 240, 400, arcade.color.WHITE, 54)

        output = "Click to restart"
        arcade.draw_text(output, 310, 300, arcade.color.WHITE, 24)

        if self.player_sprite.active:
            self.player_score = self.player_sprite.score

    def round_health(self,sprite):
        # Player Health
        health = round(sprite.health,1)

        #Stop player health being negative
        if health < 0:
            health = 0

        return health
