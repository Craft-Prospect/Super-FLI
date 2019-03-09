from sprites import *
import pygame

class Mixin:
    def setup_splash(self):
        if not self.Test:
            pygame.mixer.music.load("Music/sounds/poweron.wav")
            pygame.mixer.music.play(1)

    def draw_splash(self):
        #Load background image
        page_texture =arcade.load_texture('images/splashscreen.png')
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
