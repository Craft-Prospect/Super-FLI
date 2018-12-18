import game
import arcade

#Helper Functions

def make():
    
    game.points = [("fire", (0,150))]

    window =game.MyGame(game.SCREEN_WIDTH, game.SCREEN_HEIGHT)
    window.setup()
    assert(len(window.fire_sprite_list)==1)
    arcade.window_commands.close_window()
make() 
