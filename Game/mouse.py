from sprites import *

class Mixin:
    #Change between game pages (e.g instructions and high score)
    def on_mouse_press(self, x, y, button, modifiers):
        if self.current_state == START_PAGE:
            #Change state depending on button selected
            if self.selected == self.inst_button:
                self.current_state = INSTRUCT1
            else:
                self.demo_setup()
                self.draw_demo()
                self.current_state = INS0

        elif self.current_state == INSTRUCT1:
            self.current_state = INSTRUCT2

        elif self.current_state == INSTRUCT2:
                self.demo_setup()
                self.draw_demo()
                self.current_state = INS0

        elif self.current_state == END_PAGE:
            self.current_state = ENTER_NAME
            self.keyboard_setup()
        
        elif self.current_state == HIGH_SCORE_PAGE:
            self.current_state = FEEDBACK_PAGE
    
        elif self.current_state == FEEDBACK_PAGE:
            self.start_page_setup()
            self.current_state = START_PAGE

        elif self.current_state >= 10:
            global PLAYER_START_X
            PLAYER_START_X = self.player_sprite.center_x

            global PLAYER_START_Y 
            PLAYER_START_Y = self.player_sprite.center_y

            self.setup()
            self.current_state = GAME_PAGE


