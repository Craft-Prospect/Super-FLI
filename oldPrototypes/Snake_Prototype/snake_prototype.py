"""
Sprite Move With Keyboard

Simple program to show basic sprite usage.

Artwork from http://kenney.nl

If Python and Arcade are installed, this example can be run from the command line with:
python -m arcade.examples.sprite_move_keyboard
"""

import arcade
import os
import random

SPRITE_SCALING = 0.5
SPRITE_SCALING_FIRE = 0.01
#SPRITE_SCALING_TAIL = 0.2
FIRE_COUNT = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

MOVEMENT_SPEED = 5

class Fire(arcade.Sprite):
    """
    This class represents the coins on our screen. It is a child class of
    the arcade library's "Sprite" class.
    """

    def reset_pos(self):

        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(SCREEN_HEIGHT + 20,
                                         SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

    def update(self):

        # Move the coin
        

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            self.reset_pos()

#class Tail(arcade.Sprite):
#    def update(self):
#        self.center_x += self.change_x
#        self.center_y += self.change_y

#        if self.left < 0:
#            self.left = 0
#        elif self.right > SCREEN_WIDTH - 1:
#            self.right = SCREEN_WIDTH - 1

#        if self.bottom < 0:
#            self.bottom = 0
#        elif self.top > SCREEN_HEIGHT - 1:
#            self.top = SCREEN_HEIGHT - 1



    




class Player(arcade.Sprite):

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


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
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.fire_sprite_list = None
#        self.tail_sprite_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

#       self.tail_sprite = None

        # Set the background color
        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.fire_sprite_list = arcade.SpriteList()
#        self.tail_sprite_list = arcade.SpriteList()

        # Set up the player
        self.score = 0
        self.player_sprite = Player("images/satellite.png", SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

        #Set up the fire
        for i in range(FIRE_COUNT):

            # Create the fire instance
            # Coin image from kenney.nl
            fire = Fire("images/fire.png", SPRITE_SCALING_FIRE)

            # Position the fire randomly
            fire.center_x = random.randrange(SCREEN_WIDTH)
            fire.center_y = random.randrange(SCREEN_HEIGHT)

            # Add the fire to the list
            self.fire_sprite_list.append(fire)

        #Set up tail
 #       tail_sprite = Tail("images/star.png", SPRITE_SCALING_TAIL)
 #       tail_sprite.center_x = self.player_sprite.center_x +1
 #       tail_sprite.center_y = self.player_sprite.center_y -2    
 #       self.tail_sprite_list.append(tail_sprite)

    def on_draw(self):
        """
        Render the screen.
        """

        # This command has to happen before we start drawing
        arcade.start_render()
        

        # Draw all the sprites.
        self.player_list.draw()
        self.fire_sprite_list.draw()
#       self.tail_sprite_list.draw()

    def update(self, delta_time):
        """ Movement and game logic """

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.player_list.update()
        self.fire_sprite_list.update()
#        self.tail_sprite_list.update()
        

        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.fire_sprite_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for fire in hit_list:
            fire.center_x = random.randrange(SCREEN_WIDTH)
            fire.center_y = random.randrange(SCREEN_HEIGHT)
            self.score += 1


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
#            self.tail_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
#            self.tail_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
#            self.tail_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
 #           self.tail_sprite.change_x = MOVEMENT_SPEED

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