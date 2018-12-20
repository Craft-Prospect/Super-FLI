import game
import arcade

import unittest

class TestSetupMethods(unittest.TestCase):

    def test_AddOneFire(self):
        window = init([("fire", (0,150))])

        self.assertEqual(len(window.fire_list),1)
        arcade.window_commands.close_window()
 
    def test_AddManyFires(self):
        window = init([("fire", (0,150)),("fire", (5000,350)),("fire", (2000,550))])
        self.assertEqual(len(window.fire_list),len(game.points))
        arcade.window_commands.close_window()
       
    def test_AddOneCloud(self):
        window = init([("cloud", (0,150))])
    
        self.assertEqual(len(window.clouds_list),1)
        arcade.window_commands.close_window()
 
    def test_AddManyClouds(self):
        window = init([("cloud", (0,150)),("cloud", (5000,350)),("cloud", (2000,550))])
    
        window.setup()

        self.assertEqual(len(window.clouds_list),len(game.points))
        arcade.window_commands.close_window()


    def test_AddOneFireAndCloud(self):
        window = init([("cloud", (0,150)),("fire", (0,150))])

        self.assertEqual((len(window.fire_list)+len(window.clouds_list)),2)
        arcade.window_commands.close_window()
 
    def test_AddManyFiresandClouds(self):
        window = init([("fire", (0,150)),("fire", (5000,350)),("fire", (2000,550)),("cloud", (0,150)),("cloud", (5000,350)),("cloud", (2000,550))])
    
        self.assertEqual((len(window.fire_list)+len(window.clouds_list)),len(game.points))
        arcade.window_commands.close_window()

class TestErrorHandlingSetupt(unittest.TestCase):
    def test_negative_coOrdinates(self):
        window = init([("fire", (0,-150)),("fire", (-500,350)),("fire", (-2000,-550))])
    
        self.assertEqual((len(window.fire_list)),0)
        arcade.window_commands.close_window()

    def test_topBigY(self):
        window = init([("fire", (50,(game.SCREEN_HEIGHT+10)))])
    
        self.assertEqual((len(window.fire_list)),0)
        arcade.window_commands.close_window()

    def test_topBigY_negative_normal(self):
        window = init([(("fire", (50,(game.SCREEN_HEIGHT+10)))),("fire", (5000,12)),("fire", (0,-150)),(("cloud", (200,50)))])

        self.assertEqual(((len(window.fire_list))+(len(window.clouds_list))),2)
        arcade.window_commands.close_window()



        

#Helper Functions
def init(points):
    window = game.MyGame(game.SCREEN_WIDTH, game.SCREEN_HEIGHT)
    game.points = points
    window.setup()
    return window

if __name__ == '__main__':
    unittest.main()

