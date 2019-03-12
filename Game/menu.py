from sprites import *
import pygame

class Mixin:
    def start_page_setup(self):
        if not self.Test :
            pygame.mixer.stop()
            pygame.mixer.music.load("Music/ResistorAnthemsII/menu.mp3")
            pygame.mixer.music.play(-1)


        #Setup up lists for buttons
        self.buttons = arcade.SpriteList()
        self.pointer_list = arcade.SpriteList()

        #Setup button for launching game
        self.start_button = Button("images/button(blank).png", SPRITE_SCALING_BUTTON)
        self.start_button.center_x = SCREEN_WIDTH//2
        self.start_button.center_y = SCREEN_HEIGHT//2 + 50

        #Setup button for displaying instructions
        self.inst_button = Button("images/button(blank).png", SPRITE_SCALING_BUTTON)
        self.inst_button.center_x = SCREEN_WIDTH//2
        self.inst_button.center_y = SCREEN_HEIGHT//2 - 50

        self.about_button = Button("images/button(blank).png", SPRITE_SCALING_BUTTON)
        self.about_button.center_x = SCREEN_WIDTH//2
        self.about_button.center_y = SCREEN_HEIGHT//2 - 150

        self.buttons.append(self.start_button)
        self.buttons.append(self.inst_button)
        self.buttons.append(self.about_button)

        #Set up indicator for selected button
        self.pointer = Button("images/arrow.png", SPRITE_SCALING_BUTTON)
        self.pointer.center_y = self.start_button.center_y
        self.pointer.center_x = self.start_button.center_x - 100

        self.pointer_list.append(self.pointer)

        #Start off with the start game button being selected
        self.selected = self.start_button
        self.selected_index = 0

    #Draw main menu
    def draw_start_page(self):

        #Load background image
        page_texture = self.instructions[0]
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

        #Draw buttons
        self.buttons.draw()
        self.pointer_list.draw()

        arcade.draw_text(("Start Game"),SCREEN_WIDTH//2-55 , ((SCREEN_HEIGHT//2+45)), arcade.color.BLACK, 15)
        arcade.draw_text(("Instructions"),SCREEN_WIDTH//2-55 , ((SCREEN_HEIGHT//2-55)), arcade.color.BLACK, 15)
        arcade.draw_text(("About"),SCREEN_WIDTH//2-25 , ((SCREEN_HEIGHT//2-155)), arcade.color.BLACK, 15)

    def draw_about(self):
        page_texture = self.instructions[3]
        arcade.draw_texture_rectangle(SCREEN_WIDTH //2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)

        arcade.draw_text(("Craft Prospect is a space engineering practice, founded"),SCREEN_WIDTH//2-280, ((SCREEN_HEIGHT//2+100)), arcade.color.WHITE, 15)
        arcade.draw_text(("on the principal of bringing together NewSpace"),SCREEN_WIDTH//2-280, ((SCREEN_HEIGHT//2+80)), arcade.color.WHITE, 15)
        arcade.draw_text(("professionals and experts inthe latest technologies to "),SCREEN_WIDTH//2-280, ((SCREEN_HEIGHT//2+60)), arcade.color.WHITE, 15)
        arcade.draw_text(("advance the NewSpace state of the art. Our focus is on "),SCREEN_WIDTH//2-280, ((SCREEN_HEIGHT//2+40)), arcade.color.WHITE, 15)
        arcade.draw_text(("developing adaptive mission architectures, space"),SCREEN_WIDTH//2-280, ((SCREEN_HEIGHT//2+20)), arcade.color.WHITE, 15)
        arcade.draw_text(("applications. Our goal is to bring autonomy and "),SCREEN_WIDTH//2-280, ((SCREEN_HEIGHT//2)), arcade.color.WHITE, 15)
        arcade.draw_text(("capability to the next generation of small satellites."),SCREEN_WIDTH//2-280, ((SCREEN_HEIGHT//2-20)), arcade.color.WHITE, 15)
