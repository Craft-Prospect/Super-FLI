from sprites import *

class Mixin:
    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()

        #Draw different events dependant on stage

        if self.current_state == SPLASH:
            self.draw_splash()

        if self.current_state == START_PAGE:
            self.draw_start_page()

        elif self.current_state == INSTRUCT1:
            self.draw_page(1)

        elif self.current_state == INSTRUCT2:
            self.draw_page(2)

        elif self.current_state == ABOUT:
            self.draw_about()

        elif self.current_state == GAME_PAGE:
            self.draw_game()

        elif self.current_state == END_PAGE:
            self.draw_game()
            self.draw_game_over()

        elif self.current_state == ENTER_NAME:
            self.keyboard_on_draw()

        elif self.current_state == HIGH_SCORE_PAGE:
            self.draw_high_score()

        elif self.current_state == FEEDBACK_PAGE:
            self.draw_feedback()

        elif self.current_state >= 10:
            self.draw_demo()
            self.draw_ins_state()


        #Draw instruction on screen
    def draw_ins(self,text):
        arcade.draw_text((text),SCREEN_WIDTH//2-450,SCREEN_HEIGHT//2-100,arcade.color.ORANGE, 15)

    def draw_ins_state(self):
    #Draw different text depending on stage
            if self.current_state == INS0:
                self.draw_ins("You will be controlling the blue satellite. \nThe neural network will be controlling the red satellite.")

            elif self.current_state == INS1:
                self.draw_ins("The aim of the game is collect the most money. \nCapture fires to collect money")

            elif self.current_state == INS2:
                self.draw_ins("The Neural Network will detect fires\n It will add a sprite to help you capture the fires")

            elif self.current_state == INS4:
                self.draw_ins("Clouds will drain your power. \nIf you have no power left, your satellite will disapear")

            elif self.current_state == INS7:
                self.draw_ins("Capture a fire by pressing the [] button\n Your score will increase by £100")

            elif self.current_state == INS9:
                self.draw_ins("Press {} to start!")
