from sprites import *
import pygame

class Mixin:
    #Change between game pages (e.g instructions and high score)

    def on_mouse_press(self, x, y, button, modifiers):
        self.change_state()

    def change_state(self):
        if self.current_state == MENU_PAGE:
            #Change state depending on menu button selected
            if self.selected == self.inst_button:
                self.current_state = INSTRUCT1
            elif self.selected == self.start_button:
                self.demo_setup()
                self.draw_demo()
                self.current_state = INS0
            elif self.selected == self.about_button:
                self.current_state = ABOUT
            elif self.selected == self.feedback_button:
                self.current_state = FEEDBACK_PAGE

        elif self.current_state == INSTRUCT1:
            self.current_state = INSTRUCT2

        elif self.current_state == INSTRUCT2:
                self.demo_setup()
                self.draw_demo()
                self.current_state = INS0

        elif self.current_state == ABOUT:
            self.menu_setup()
            self.current_state = MENU_PAGE

        elif self.current_state == END_PAGE:
            self.current_state = ENTER_NAME
            self.keyboard_setup()

        elif self.current_state == HIGH_SCORE_PAGE:
            self.current_state = FEEDBACK_PAGE

        elif self.current_state == FEEDBACK_PAGE:
            self.menu_setup()
            self.current_state = MENU_PAGE

        elif self.current_state >= 10:
            self.game_setup()
            self.current_state = GAME_PAGE
