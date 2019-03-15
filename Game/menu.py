from sprites import *
import pygame

class Mixin:
    def menu_setup(self):
        if not self.Test :
            pygame.mixer.stop()
            pygame.mixer.music.load(SND_MENU)
            pygame.mixer.music.play(-1)


        #Setup up lists for buttons
        self.buttons = arcade.SpriteList()
        self.pointer_list = arcade.SpriteList()

        #Setup button for launching game
        self.start_button = Button(IMG_BUTTON, SPRITE_SCALING_BUTTON)
        self.start_button.center_x = SCREEN_WIDTH//2
        self.start_button.center_y = SCREEN_HEIGHT//2 + 50

        #Setup button for displaying
        self.inst_button = Button(IMG_BUTTON, SPRITE_SCALING_BUTTON)
        self.inst_button.center_x = SCREEN_WIDTH//2
        self.inst_button.center_y = SCREEN_HEIGHT//2 - 50

        self.about_button = Button(IMG_BUTTON, SPRITE_SCALING_BUTTON)
        self.about_button.center_x = SCREEN_WIDTH//2
        self.about_button.center_y = SCREEN_HEIGHT//2 - 150

        self.feedback_button = Button(IMG_BUTTON, SPRITE_SCALING_BUTTON)
        self.feedback_button.center_x = SCREEN_WIDTH//2
        self.feedback_button.center_y = SCREEN_HEIGHT//2 - 250

        self.buttons.append(self.start_button)
        self.buttons.append(self.inst_button)
        self.buttons.append(self.about_button)
        self.buttons.append(self.feedback_button)

        #Set up indicator for selected button
        self.pointer = Button(IMG_POINTER, SPRITE_SCALING_BUTTON)
        self.pointer.center_y = self.start_button.center_y
        self.pointer.center_x = self.start_button.center_x - 100

        self.pointer_list.append(self.pointer)

        #Start off with the start game button being selected
        self.selected = self.start_button
        self.selected_index = 0

    #Draw main menu
    def draw_menu(self):

        #Load background image
        page_texture = self.textures[0]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

        #Draw buttons
        self.buttons.draw()
        self.pointer_list.draw()

        #Draw button text
        arcade.draw_text(("Start Game"),SCREEN_WIDTH//2-55 , ((SCREEN_HEIGHT//2+45)), arcade.color.WHITE, 15)
        arcade.draw_text(("Instructions"),SCREEN_WIDTH//2-55 , ((SCREEN_HEIGHT//2-55)), arcade.color.WHITE, 15)
        arcade.draw_text(("About"),SCREEN_WIDTH//2-25 , ((SCREEN_HEIGHT//2-155)), arcade.color.WHITE, 15)
        arcade.draw_text(("Feedback"),SCREEN_WIDTH//2-45 , ((SCREEN_HEIGHT//2-255)), arcade.color.WHITE, 15)

    #Draw about section
    def draw_about(self):
        page_texture = self.textures[3]
        arcade.draw_texture_rectangle(SCREEN_WIDTH //2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

        offset = 95 #Offset for text centering

        for line in ABOUT_TEXT:
            center = 23 - len(line)/2 # Figure out were to center line
            arcade.draw_text(line, SCREEN_WIDTH//2-240+center*8,(SCREEN_HEIGHT//2+offset),arcade.color.WHITE,15)
            offset -= 20 #Place next line 20 pixels down
