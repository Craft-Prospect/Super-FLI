""" Simple movement program """

import arcade
import os
import random

#Set sprite sizes
SPRITE_SCALING_PLAYER = 0.25
SPRITE_SCALING_FIRE = 0.01
FIRE_COUNT = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 2


class Satellite(arcade.Sprite):

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

class Fire(arcade.Sprite):
    """
    This class represents the emergency on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def reset_pos(self):

        # Reset the fire to a random spot to the right of the screen
        self.center_y = random.randrange(0,SCREEN_HEIGHT )
        self.center_x = SCREEN_WIDTH + random.randrange(0,SCREEN_WIDTH/2) #


    def update(self):

        # Move the fire
        self.center_x -= 1

        # See if the fire has fallen off the bottom of the screen.
        # If so, reset it.
        if self.left < 0:
            self.reset_pos()

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self, width, height):
        """
        Initializer
        """

        # Call the parent class initializer
        super().__init__(width, height)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold the sprite lists
        self.player_list = None
        self.fire_sprite_list=None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Background image will be stored in this variable
        self.background = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.fire_sprite_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = Satellite("images/satellite.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)
        
        # Load the background image. Do this in the setup so we don't keep reloading it all the time.
        self.background = arcade.load_texture("images/fire.jpg")

        # Create the fires
        for i in range(FIRE_COUNT):

            # Create the fire instance
            fire = Fire("images/fire.png", SPRITE_SCALING_FIRE)

            # Position the fire
            fire.center_x = random.randrange(SCREEN_WIDTH)
            fire.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the coin to the lists
            self.fire_sprite_list.append(fire)
        
    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        
        # Draw the background texture
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw all the sprites.
        self.fire_sprite_list.draw()
        self.player_list.draw()

         # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on player and fire sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()
        self.fire_sprite_list.update()


        

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.SPACE:

            # Generate a list of all sprites that collided with the player.
            hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.fire_sprite_list)

            # Loop through each colliding sprite, remove it, and add to the score.
            for fire in hit_list:
                fire.reset_pos()
                self.score += 1



    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


def main():
    """ Main method """
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
