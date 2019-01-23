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

class TestEventsCPU(unittest.TestCase):
    def test_fireCapture(self):
        game.STATE = game.GAME_PAGE
        window = init([("fire", (80,game.SCREEN_HEIGHT-80))])
        window.draw_game()
        for i in range(100):
            window.update(1)
        self.assertEqual(window.cpu_sprite.score, 100)

    def test_tracking(self):
        window = init([])
        game.CPU_TRACK_SPEED = 1 
        for i in range(game.SCREEN_HEIGHT+100):
            window.cpu_sprite.cpu_update(window.player_sprite)
        self.assertEqual((round((window.cpu_sprite.center_x)+ window.cpu_sprite.center_y)), (window.player_sprite.center_x + window.player_sprite.center_y))

    def test_cloudDamage(self):
        game.STATE = game.GAME_PAGE
        window = init([("cloud",(50,game.SCREEN_HEIGHT-50))])
        game.CPU_TRACK_SPEED = 0 #Keep CPU stationary to cause damage
        window.draw_game()
        for i in range(100):
                window.update(1)
        self.assertNotEqual(window.cpu_sprite.health, game.HEALTH)

#Helper Functions
def init(points,source="images/fire.jpg"): 
    window = game.MyGame(game.SCREEN_WIDTH, game.SCREEN_HEIGHT)
    game.points = points
    game.SOURCE = source
    window.setup()
    return window

if __name__ == '__main__':
    unittest.main()

