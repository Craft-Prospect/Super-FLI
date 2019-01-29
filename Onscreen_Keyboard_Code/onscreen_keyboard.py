#Onscreen Keyboard
import arcade
import os
import random
import glob
import time

SPRITE_SCALING_POINTER = 1
SPRITE_SCALING_KEY = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MOVEMENT_SPEED = 3
DEAD_ZONE = 0.02




class Key(arcade.Sprite):
    character = ""
    y_coord = 0
    x_coord = 0
        

        
        
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

          

          

    def setup(self):

        # Create your sprites and sprite lists here
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

        #Setup Delete button
        self.key_sprite = Key('keyboard_images/icons8-enter-26.png',SPRITE_SCALING_KEY)
        self.key_sprite.center_x = 400
        self.key_sprite.center_y = 100
        self.key_sprite.character = ';'  # use ';' as identifier for backspace
        self.key_list.append(self.key_sprite)

        #String taking input
        self.name = []

        #Character list tracking variable
        self.key_position = 0

        #Check variable for joystick
        self.check = 0
        self.check_y = 0

        #Setup keys
        x = 0
        y = 0
        count = 0
        #for filename in os.listdir('keyboard_images/characters'):
        for filename in sorted(glob.glob('keyboard_images/characters/*.png')):
            if filename.endswith(".png"):
                #print(filename[7])
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
                self.key_sprite.x_coord = 50 + x 
                self.key_sprite.y_coord = 200 + y 

                count += 1
                
                #print(filename[29])
        
                

            
                x+=50
                self.key_list.append(self.key_sprite)

            

    def on_draw(self):
        """
        Render the screen.
        """

        # This command should happen before we start drawing. It will clear
        # the screen to the background color, and erase what we drew last frame.
        arcade.start_render()

        start_x = 200
        start_y = 300
        arcade.draw_text(''.join(self.name), start_x, start_y, arcade.color.BLACK, 30)

        # Call draw() on all your sprite lists below
        self.pointer_list.draw()
        self.key_list.draw()

    def update(self, deltatime):
        """
        All the logic to move, and the game logic goes here.
        Normally, you'll call update() on the sprite lists that
        need it.
        """
        
        

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

    def on_joybutton_press(self, joystick, button):
        print("Button {} down".format(button))

        # On button press generate/add to list of keys selected by the button
        character_hit_list = arcade.check_for_collision_with_list(self.pointer_sprite,self.key_list)

        for Key in character_hit_list:

            if Key.character == '-':
                self.name = self.name[0:-1]

            else:
                self.name.append(Key.character.upper())
            

            #print(''.join(self.name))


    def on_joybutton_release(self, joystick, button):
        print("Button {} up".format(button))

    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        print("Hat ({}, {})".format(hat_x, hat_y))    

       


def main():
    """ Main method """
    game = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()