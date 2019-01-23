#Onscreen Keyboard
import arcade
import os
import random

SPRITE_SCALING_POINTER = 1
SPRITE_SCALING_KEY = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 3
DEAD_ZONE = 0.02

class Key(arcade.Sprite):
    character = ""
        

        
        
class MyGame(arcade.Window):
    """
    Main application class.

    NOTE: Go ahead and delete the methods you don't need.
    If you do need a method, delete the 'pass' and replace it
    with your own code. Don't leave 'pass' in this program.
    """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.AMAZON)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # If you have sprite lists, you should create them here,
        # Variables that will hold sprite lists
        self.pointer_list = None
        self.key_list = None
        # and set them to None

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
            print("There are no Joysticks")
            self.joystick = None

    def on_joybutton_press(self, joystick, button):
        print("Button {} down".format(button))

    def on_joybutton_release(self, joystick, button):
        print("Button {} up".format(button))

    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        print("Hat ({}, {})".format(hat_x, hat_y))        

          

    def setup(self):
        # Create your sprites and sprite lists here
        #Sprite lists
        self.pointer_list = arcade.SpriteList()
        self.key_list = arcade.SpriteList()
        
        #Set up pointer
        # Set up the player
        self.pointer_sprite = arcade.Sprite("images/icons8-cursor-filled-24.png", SPRITE_SCALING_POINTER)
        self.pointer_sprite.center_x = 50
        self.pointer_sprite.center_y = 50
        self.pointer_list.append(self.pointer_sprite)

        #Setup keys
        x = 0
        y = 0
        for filename in os.listdir('images/keyboard_images'):
            if filename.endswith(".png"):
                #print(filename[7])
                self.key_sprite = Key('images/keyboard_images/'+ filename, SPRITE_SCALING_KEY)
                self.key_sprite.center_x = 50 + x
                self.key_sprite.center_y = 200
                self.key_sprite.character = filename[7]
        
                

            
                x+=50
                self.key_list.append(self.key_sprite)

            

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        # Call draw() on all your sprite lists below
        self.pointer_list.draw()
        self.key_list.draw()

    def update(self, delta_time):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        if self.joystick:

            # Set a "dead zone" to prevent drive from a centered joystick
            if abs(self.joystick.x) < DEAD_ZONE:
                self.pointer_sprite.change_x = 0
            else:
                self.pointer_sprite.change_x = self.joystick.x * MOVEMENT_SPEED

            # Set a "dead zone" to prevent drive from a centered joystick
            if abs(self.pointer_sprite.center_y) < DEAD_ZONE:
                self.pointer_sprite.change_y = 0
            else:
                self.pointer_sprite.change_y = -self.joystick.y * MOVEMENT_SPEED

        self.pointer_sprite.update()



    def on_key_press(self, key, key_modifiers):
        """
        Called whenever a key on the keyboard is pressed.

        For a full list of keys, see:
        http://arcade.academy/arcade.key.html
        """
        pass

    def on_key_release(self, key, key_modifiers):
        """
        Called whenever the user lets off a previously pressed key.
        """
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        """
        Called whenever the mouse moves.
        """
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        """
        Called when the user presses a mouse button.
        """
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        """
        Called when a user releases a mouse button.
        """
        pass


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()