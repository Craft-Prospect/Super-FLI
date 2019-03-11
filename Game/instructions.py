from sprites import *

class Mixin:
    def draw_page(self, page_number):

        #Load background image
        page_texture = self.instructions[page_number] 
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
        #Load test for insturction pages
        if page_number == 1:
            arcade.draw_text(("Control your satellite \nwith the joystick"),SCREEN_WIDTH - 500 , (5*(SCREEN_HEIGHT//6)), arcade.color.BLACK, 25)
            arcade.draw_text(("Capture fire by \npressing the button"),SCREEN_WIDTH - 500 , (13*(SCREEN_HEIGHT//24)), arcade.color.BLACK, 25)
            arcade.draw_text(("Avoid clouds which \ndrain your power"),SCREEN_WIDTH - 500 , (6*(SCREEN_HEIGHT//24)), arcade.color.BLACK, 25)

        elif page_number == 2:
            arcade.draw_text(("You will be competing \nagainst a computer, acting \nas a satellite powered  \nby a Neural Network."),SCREEN_WIDTH - 600 , (2*(SCREEN_HEIGHT//3)), arcade.color.BLACK, 30)


