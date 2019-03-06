
from game import *
from network import *

#Run game
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    network()
    #window.set_update_rate(1/10)
    arcade.run()

if __name__ == "__main__":
    main()
  

