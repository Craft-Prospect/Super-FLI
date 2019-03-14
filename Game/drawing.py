from sprites import *

class Mixin:
    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        #Draw different events dependant on stage
        if self.current_state == SPLASH:
            self.draw_splash()#See splash.py

        if self.current_state == MENU_PAGE:
            self.draw_menu() #See menu.py

        elif self.current_state == INSTRUCT1:
            self.draw_page(1)#See instructions.py

        elif self.current_state == INSTRUCT2:
            self.draw_page(2)#See instructions.py

        elif self.current_state == ABOUT:
            self.draw_about()#See menu.py

        elif self.current_state == GAME_PAGE:
            self.draw_game() #See runGame.py

        elif self.current_state == END_PAGE:
            self.draw_game() #See runGame.py
            self.draw_game_over() #See runGame.py

        elif self.current_state == ENTER_NAME:
            self.keyboard_on_draw() #See keyboard.py

        elif self.current_state == HIGH_SCORE_PAGE:
            self.draw_highscore() # See highscore.py

        elif self.current_state == FEEDBACK_PAGE:
            self.draw_feedback() #See highscore.py

        elif self.current_state >= 10: #See demo.py
            self.draw_demo()
            self.draw_ins_state()
