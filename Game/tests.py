import game
import arcade

import unittest

class TestSetupMethods(unittest.TestCase):

    def test_AddOneFire(self):
        window = init() 
        game.points = [("fire", (0,150))]
    
        window.setup()

        self.assertEqual(len(window.fire_list),1)
        arcade.window_commands.close_window()
 
    def test_AddManyFires(self):
        window = init() 
        game.points = [("fire", (0,150)),("fire", (5000,350)),("fire", (2000,550))]
    
        window.setup()

        self.assertEqual(len(window.fire_list),len(game.points))
        arcade.window_commands.close_window()

    def test_AddOneCloud(self):
        window = init() 
        game.points = [("cloud", (0,150))]
    
        window.setup()

        self.assertEqual(len(window.clouds_list),1)
        arcade.window_commands.close_window()
 
    def test_AddManyClouds(self):
        window = init() 
        game.points = [("cloud", (0,150)),("cloud", (5000,350)),("cloud", (2000,550))]
    
        window.setup()

        self.assertEqual(len(window.clouds_list),len(game.points))
        arcade.window_commands.close_window()


    def test_AddOneFireAndCloud(self):
        window = init() 
        game.points = [("cloud", (0,150)),("fire", (0,150))]
    
        window.setup()

        self.assertEqual((len(window.fire_list)+len(window.clouds_list)),2)
        arcade.window_commands.close_window()
 
    def test_AddManyFiresandClouds(self):
        window = init() 
        game.points = [("fire", (0,150)),("fire", (5000,350)),("fire", (2000,550)),("cloud", (0,150)),("cloud", (5000,350)),("cloud", (2000,550))]
    
        window.setup()

        self.assertEqual((len(window.fire_list)+len(window.clouds_list)),len(game.points))
        arcade.window_commands.close_window()


        

#Helper Functions
def init():
    return game.MyGame(game.SCREEN_WIDTH, game.SCREEN_HEIGHT)

if __name__ == '__main__':
    unittest.main()

