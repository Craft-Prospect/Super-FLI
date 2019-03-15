from sprites import *

class Mixin:
    #Display top ten high scores
    def draw_highscore(self):
        page_texture = arcade.load_texture(IMG_HIGHSCORE)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

        arcade.draw_text(("HIGH SCORES"), SCREEN_WIDTH//2-200, 3*SCREEN_HEIGHT/4, arcade.color.RED, 40)

        #Get top ten high scores from file
        i = 1
        with open('scores.txt', 'r') as f:
            while i <11:
                line = f.readline()
                line = str(i) + ". " + line

                #Display highscores on screen
                arcade.draw_text((line),SCREEN_WIDTH//2-150 , (3*SCREEN_HEIGHT/4-(40*i)), arcade.color.WHITE, 30)
                i += 1

    #Displays QR feedback page
    def draw_feedback(self):
        page_texture = arcade.load_texture(IMG_FEEDBACK)
        arcade.draw_texture_rectangle(SCREEN_WIDTH//2, SCREEN_HEIGHT//2, page_texture.width, page_texture.height, page_texture, 0)

        arcade.draw_text(("Please leave some feedback"), SCREEN_WIDTH//2-380, 3*SCREEN_HEIGHT/4, arcade.color.RED, 40)

        arcade.draw_text((FEEDBACK_LINK),SCREEN_WIDTH//2-300, 40, arcade.color.RED, 25)
