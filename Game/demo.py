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
