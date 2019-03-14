from sprites import *
from helper import *

class Mixin:
    #Handles keyboard controls
    def on_key_press(self, key, modifiers):

        if self.current_state == GAME_PAGE:
            if self.player_sprite.active:
                self.player_keyboard(key)

        elif self.current_state == MENU_PAGE:
            self.menu_keyboard(key)

        elif self.current_state == ENTER_NAME:
            self.enter_keyboard(key)

        elif self.current_state > 9:
            self.ins_skip(key)

    #Controls for capturing fires and moving the player sprites
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

    #Controls for cycling between buttons on start menu
    def menu_keyboard(self,key):
        if key == arcade.key.SPACE:
            self.selected_index = (self.selected_index+1)%len(self.buttons)

        if key == arcade.key.BACKSPACE:
            self.selected_index = (self.selected_index-1)

            if self.selected_index == -1:
                self.selected_index = len(self.buttons) -1

        self.selected = self.buttons[self.selected_index]
        self.pointer.center_y = self.selected.center_y

    #Moves pointer up or down, depending on joystick direction
    def menu_jopystick_update(self):
        # If centered set boolean to 0
        if abs(self.joystick.y) < DEAD_ZONE:
            self.check = 0
            return

        #If joystick pushed up update selected button and pointer position
        if self.joystick.y < 0 and self.check == 0:
            self.menu_keyboard(arcade.key.BACKSPACE)
            self.check = 1

        #Otherwise move pointer down and update selected button
        elif self.check == 0:
                self.menu_keyboard(arcade.key.SPACE)
                self.check = 1
    #Controls for entering name for highscore
    def enter_keyboard(self,key):
        # 65293 value for **ENTER**
        if key == 65293:
            add_highscore(self.name,self.player_score)
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


    #Handles pressing of joystick buttons
    def on_joybutton_press(self, joystick, button):

    # If there is a collision between a 'Key' object and the pointer. The Key is added to the hit list
        # Hit list is then iterated through and character value from Key object is added to string  thats printed to the screen

        # If red button is pressed
        if button == 1:
            if self.current_state == GAME_PAGE:
                self.check_fire_collison(self.player_sprite)


            elif self.current_state == ENTER_NAME:
                character_hit_list = arcade.check_for_collision_with_list(self.pointer_sprite,self.key_list)

                for Key in character_hit_list:
                    if Key.character == ';':
                        add_highscore(self.name,self.player_score)
                        self.current_state = HIGH_SCORE_PAGE

                    if Key.character == '-':
                        self.name = self.name[0:-1]

                    elif len(self.name) <= 3:self.name.append(Key.character.upper())

            elif self.current_state == MENU_PAGE:
                    self.menu_keyboard(arcade.key.SPACE)

            elif self.current_state >= 10:
                self.ins_skip(arcade.key.SPACE)

        #if BUTTON button pressed, try change state
        if button == 0:
            self.change_state() #see changeState.py

    #Skips current instruction in demo video
    def ins_skip(self,key):
        if key == arcade.key.SPACE:
                #If instruction left, skip current instruction
                if self.current_state <19:
                    self.current_state += 1
                else:
                    #Go to start game
                    self.game_setup()
                    self.current_state = GAME_PAGE

    # Arcade academy throws errors if these functions aren't implemented
    def on_joybutton_release(self, joystick, button):
        pass

    def on_joyhat_motion(self, joystick, hat_x, hat_y):
        pass
