from game import *
from network import *
import pygame

#Run game
def main():
    pygame.init()
    pygame.mixer.init()
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    #network()
    #window.set_update_rate(1/10)
    arcade.run()

if __name__ == "__main__":
    main()
  

