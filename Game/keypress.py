from sprites import *
from helper import *

class Mixin:
    #Player controls
    def on_key_press(self, key, modifiers):
        if self.current_state == GAME_PAGE:
            if self.player_sprite.active:
                self.player_keyboard(key)

        elif self.current_state == START_PAGE:
            self.menu_keyboard(key)

        elif self.current_state == ENTER_NAME:
            self.enter_keyboard(key)

        elif self.current_state > 9:
            self.ins_skip(key)

    def player_keyboard(self,key):
        """Pressing arrow keys """
        if key == arcade.key.UP:
            self.player_sprite.change_y = self.player_sprite.speed
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -self.player_sprite.speed
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -self.player_sprite.speed
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = self.player_sprite.speed

        #PLayer attempts to capture
        elif key == arcade.key.SPACE:
            self.check_fire_collison(self.player_sprite)


    def menu_keyboard(self,key):
        if key == arcade.key.SPACE:
            self.selected_index = (self.selected_index+1)%len(self.buttons)
            self.selected = self.buttons[self.selected_index]
            self.pointer.center_y = self.selected.center_y

    def enter_keyboard(self,key):
        # 65293 value for **ENTER**
        if key == 65293:
            add_high_score(self.name,self.player_score)
            self.current_state = HIGH_SCORE_PAGE

        #If value over 2^16 is selected as it causes a crash
        if key> 65536:
            return

        #Value for shift instead of printing value return
        elif key == 65506:
            return

        #Value for caps key, boolean turned on and off if selected
        elif key == 65509:
            self.caps_on = not self.caps_on
            return

        #Value for delete key
        elif key == 65288:
            self.name = self.name[0:-1]

        #If caps is on append in upper case otherwise in lowercase z
        elif len(self.name) <= 3:

            if self.caps_on:
                self.name.append(chr(key).upper())

            else:
                self.name.append(chr(key))


    #Allows for continouse update
    def on_key_release(self, key, modifiers):
        if self.current_state == GAME_PAGE:
            if key == arcade.key.UP or key == arcade.key.DOWN:
                self.player_sprite.change_y = 0
            elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
                self.player_sprite.change_x = 0



    def on_joybutton_press(self, joystick, button):

    # If there is a collision between a 'Key' object and the pointer. The Key is added to the hit list
        # Hit list is then iterated through and character value from Key object is added to string  thats printed to the screen

        # If red button is pressed
        if button == 1:
            if self.current_state == ENTER_NAME:
                character_hit_list = arcade.check_for_collision_with_list(self.pointer_sprite,self.key_list)

                for Key in character_hit_list:
                    if Key.character == ';':
                        add_high_score(self.name,self.player_score)
                        self.current_state = HIGH_SCORE_PAGE

                    if Key.character == '-':
                        self.name = self.name[0:-1]

                    elif len(self.name) <= 3:self.name.append(Key.character.upper())

            if self.current_state == GAME_PAGE:
                self.check_fire_collison(self.player_sprite)

            if self.current_state >= 10:
                self.ins_skip(arcade.key.SPACE)

        if button == 0:
            self.change_state()

    # Arcade academy throws errors if these functions aren't implemented
    def on_joybutton_release(self, joystick, button):
        print("Button {} up".format(button))

    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        print("Hat ({}, {})".format(hat_x, hat_y))

    def ins_skip(self,key):
        if key == arcade.key.SPACE:
                if self.current_state <19:
                    self.current_state += 1
                else:
                    self.game_setup()
                    self.current_state = GAME_PAGE
