from sprites import *
import glob

class Mixin:
    def keyboard_setup(self):
        
        arcade.set_background_color(arcade.color.AMAZON)
        #String taking input
        self.name = []

        #Boolean for CapsLock toggle
        self.caps_on = False

        #Character list tracking variable
        self.key_position = 0

        #Check variable for joystick
        self.check = 0
        self.check_y = 0


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

        #Setup enter button
        self.key_sprite = Key('keyboard_images/icons8-enter-26.png',SPRITE_SCALING_KEY)
        self.key_sprite.center_x = 400
        self.key_sprite.center_y = 100
        self.key_sprite.character = ';'  # use ';' as identifier for enter
        self.key_list.append(self.key_sprite)

        #Setup keys
        x = 0
        y = 0
        count = 0
        #for filename in os.listdir('keyboard_images/characters'):
        #Loops through file containing characters and adds creates a 'Key' object for each character
        for filename in sorted(glob.glob('keyboard_images/characters/*.png')):
            if filename.endswith(".png"):
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


                count += 1

                x+=50
                self.key_list.append(self.key_sprite)


    def keyboard_on_draw(self):

        arcade.start_render()

        #Print question:
        arcade.draw_text("Enter player name?",50,500,arcade.color.BLACK,20)

        #Prints input text
        arcade.draw_text(''.join(self.name),350,350, arcade.color.BLACK, 40)

        
        
        # Call draw() on all your sprite lists below
        self.pointer_list.draw()
        self.key_list.draw()




