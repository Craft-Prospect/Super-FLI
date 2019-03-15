from game import *
import pygame

#Run game
def main():
    #Start pygame for music(arcade library is broken)
    pygame.init()
    pygame.mixer.init()
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT,False)
    arcade.run()

if __name__ == "__main__":
    main()
