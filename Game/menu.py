from sprites import *
import pygame 

class Mixin:
    def start_page_setup(self):
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
 
        self.buttons.append(self.start_button)
        self.buttons.append(self.inst_button)

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

        #Add text for title and buttons
        arcade.draw_text(("Working Title"),SCREEN_WIDTH//2 - 100 , (5*(SCREEN_HEIGHT//6)), arcade.color.RED, 30)
        arcade.draw_text(("Start Game"),SCREEN_WIDTH//2-55 , ((SCREEN_HEIGHT//2+50)), arcade.color.BLACK, 15)
        arcade.draw_text(("Instructions"),SCREEN_WIDTH//2-55 , ((SCREEN_HEIGHT//2-50)), arcade.color.BLACK, 15)


 
