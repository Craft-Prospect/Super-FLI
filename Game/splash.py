from sprites import *
import pygame

class Mixin:
    #Play power up sound
    def setup_splash(self):
        if not self.Test:
            s = pygame.mixer.Sound(SND_SPLASH)
            s.play()

    #Draw loading screen
    def draw_splash(self):
        #Load background image
        page_texture =arcade.load_texture(IMG_SPLASH)
        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      page_texture.width,
                                      page_texture.height, page_texture, 0)
