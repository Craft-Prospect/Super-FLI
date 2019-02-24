from sprites import *

class Mixin:
    def on_draw(self):
        # This command has to happen before we start drawing
        arcade.start_render()
        
        #Draw different events dependant on stage

        if self.current_state == START_PAGE:
            self.draw_start_page()

        elif self.current_state == INSTRUCT1:
            self.draw_page(1)

        elif self.current_state == INSTRUCT2:
            self.draw_page(2)

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
    def on_joybutton_press(self, joystick, button):
        print("Button {} down".format(button))

        # If there is a collision between a 'Key' object and the pointer. The Key is added to the hit list
        # Hit list is then iterated through and character value from Key object is added to string  thats printed to the screen 
        if self.current_state == ENTER_NAME:
            character_hit_list = arcade.check_for_collision_with_list(self.pointer_sprite,self.key_list)

            for Key in character_hit_list:
                if Key.character == ';':
                    add_high_score(self.name)
                    self.current_state = HIGH_SCORE_PAGE

                if Key.character == '-':
                    self.name = self.name[0:-1]

                elif len(self.name) <= 3:self.name.append(Key.character.upper())

        if self.current_state == GAME_PAGE:
            # Generate a list of all sprites that collided with the player.
                    hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.fire_list)
                    # Loop through each colliding sprite, remove it, and add to the player_score.
                    for fire in hit_list:
                        fire.kill()
                        self.player_sprite.score += 100
