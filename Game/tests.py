import game
import arcade
import pygame
import unittest

#Test the game generates sprites
class TestSetupMethods(unittest.TestCase):

    def test_AddOneFire(self):
        window = init(fire=[("fire", (0,150))])
        self.assertEqual(len(window.fire_list),1)
        finish()

    def test_AddManyFires(self):
        window = init(fire=[("fire", (0,150)),("fire", (5000,350)),("fire", (2000,550))])
        self.assertEqual(len(window.fire_list),3)
        finish()

    def test_AddOneCloud(self):
        window = init(clouds=[("cloud", (0,150))])
        self.assertEqual(len(window.clouds_list),1)
        finish()

    def test_AddManyClouds(self):
        window = init(clouds=[("cloud", (0,150)),("cloud", (5000,350)),("cloud", (2000,550))])
        self.assertEqual(len(window.clouds_list),3)
        finish()

    def test_AddOneFireAndCloud(self):
        window = init(clouds=[("cloud", (0,150))], fire =[("fire", (0,150))])
        self.assertEqual((len(window.fire_list)+len(window.clouds_list)),2)
        finish()

    def test_AddManyFiresandClouds(self):
        window = init(fire =[("fire", (0,150)),("fire", (5000,350)),("fire", (2000,550))], clouds = [("cloud", (0,150)),("cloud", (5000,350)),("cloud", (2000,550))])
        self.assertEqual((len(window.fire_list)+len(window.clouds_list)),6)
        finish()

    def test_add_sprite_fire(self):
        window = init([])
        window.add_sprite("fire", (0,0))
        self.assertEqual(len(window.fire_list), 1)
        finish()

    def test_add_sprite_cloud(self):
        window = init([])
        window.add_sprite("cloud", (100,100))
        self.assertEqual(len(window.clouds_list),1)
        finish()

#Test the game won't generate sprites outside game bounds
class TestErrorHandlingSetupt(unittest.TestCase):

    def test_negative_coOrdinates(self):
        window = init(fire = [("fire", (0,-150)),("fire", (-500,350)),("fire", (-2000,-550))])
        self.assertEqual((len(window.fire_list)),0)
        finish()

    def test_topBigY(self):
        window = init(fire = [("fire", (50,(game.SCREEN_HEIGHT+10)))])
        self.assertEqual((len(window.fire_list)),0)
        finish()

    def test_topBigY_negative_normal(self):
        window = init(fire = [(("fire", (50,(game.SCREEN_HEIGHT+10)))),("fire", (5000,12)),("fire", (0,-150))],clouds =[(("cloud", (200,50)))])
        self.assertEqual(((len(window.fire_list))+(len(window.clouds_list))),2)
        finish()

#Test CPU Satelite behaviour
class TestEventsCPU(unittest.TestCase):

    #Update game to check the CPU tracks and captures the sprite
    def test_fireCapture(self):
        game.STATE = game.GAME_PAGE
        window = init(fire = [("fire", (game.CPU_START_X + 30,game.CPU_START_Y-30))])
        window.draw_game()

        for i in range(100):
            window.update(1)

        self.assertEqual(window.cpu_sprite.score, 100)
        finish()

    #Update CPU to see if it follows the player
    def test_tracking(self):
        window = init()

        for i in range(game.SCREEN_HEIGHT+400):
            window.cpu_sprite.cpu_update(window.player_sprite)

        self.assertEqual((round((window.cpu_sprite.center_x)+ window.cpu_sprite.center_y)), (window.player_sprite.center_x + window.player_sprite.center_y))
        finish()


    #Keeping the cloud stationary, check to see if the cloud damages it
    def test_cloudDamage(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds=[("cloud",(game.CPU_START_X,game.CPU_START_Y))])
        window.cpu_sprite.track_speed = 0 #Keep CPU stationary to cause damage
        window.draw_game()

        for i in range(100):
                window.update(1)
        self.assertNotEqual(window.cpu_sprite.health, game.HEALTH)
        finish()

#Test player actions
class TestPlayerEvents(unittest.TestCase):

    #Update the game to make sure the player doesn't automatically capture the fire
    def test_DoesntPassivelyCollectFire(self):
        game.STATE = game.GAME_PAGE
        window = init(fire = [("fire", (game.PLAYER_START_X, game.PLAYER_START_Y))])
        window.draw_game()

        for i in range(100):
            window.update(1)
        self.assertEqual(window.player_sprite.score, 0)
        finish()


    #Update the game and press the button to see if the player captures the fire
    def test_CollectsFireOnButtonPress(self):
        game.STATE = game.GAME_PAGE
        window = init(fire = [("fire", (game.PLAYER_START_X +40, game.PLAYER_START_Y))])
        window.draw_game()

        for i in range(100):
            window.update(1)
            window.on_key_press(arcade.key.SPACE, 0)
        self.assertEqual(window.player_sprite.score, 100)
        finish()


    #Press the buttons to see if the player moves
    def test_Movement(self):
        game.STATE = game.GAME_PAGE
        window = init()
        window.draw_game()

        for i in range(100):
                window.update(1)
                window.on_key_press(arcade.key.UP,0)
                window.on_key_press(arcade.key.RIGHT, 0)

        self.assertNotEqual(window.player_sprite.center_x, game.PLAYER_START_X)
        self.assertNotEqual(window.player_sprite.center_y, game.PLAYER_START_Y)
        finish()


    #Update the game and see if the player gets cloud damage
    def test_PlayerDamage(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud",(game.PLAYER_START_X,game.PLAYER_START_Y))])
        window.draw_game()

        for i in range(100):
                window.update(1)
        self.assertNotEqual(window.player_sprite.health, game.HEALTH)
        finish()

#Test PLayer and Satellite Deaths
class TestDeaths(unittest.TestCase):

    #Increase clouds damage and check it kills the player
    def test_Player_death(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud",(game.PLAYER_START_X,game.PLAYER_START_Y))])
        window.clouds_list[0].damage = 100
        window.draw_game()

        for i in range(100):
                window.update(1)
        self.assertFalse(window.player_sprite.active)
        finish()

    #Check if player doesn't move when dead
    def test_Player_death_no_movement(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud",(game.PLAYER_START_X,game.PLAYER_START_Y))])
        window.draw_game()
        window.player_sprite.health = 0
        window.update(1)

        for i in range(10):
                window.update(1)
                window.on_key_press(arcade.key.UP, 0)
        self.assertEqual(window.player_sprite.center_x, game.PLAYER_START_X)
        finish()

    #Increase cloud damage and check it kills CPU
    def test_CPU_death(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud",(game.CPU_START_X,game.CPU_START_Y))])
        window.cpu_sprite.track_speed = 0
        window.clouds_list[0].damage = 100
        window.draw_game()

        for i in range(100):
                window.update(1)
        self.assertFalse(window.cpu_sprite.active)
        finish()

    #Check dead CPU doesn't move
    def test_CPU_death_no_moment(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud",(game.CPU_START_X,game.CPU_START_Y))])
        window.draw_game()
        window.cpu_sprite.health = 0
        window.update(1)
        window.add_sprite("fire",(game.CPU_START_X + 40, game.CPU_START_Y-30))

        for i in range(100):
                window.update(1)
        self.assertEqual(window.cpu_sprite.center_x, game.CPU_START_X)
        finish()

    #Check if both are dead, the game ends
    def test_Player_CPU_death_ends_game(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud",(game.CPU_START_X,game.CPU_START_Y)), ("cloud", (game.PLAYER_START_X,game.PLAYER_START_Y))])
        window.player_sprite.health = 0
        window.cpu_sprite.health = 0
        window.update(1)

        self.assertEqual(window.current_state, game.END_PAGE)


#Test menu selection screen works
class TestMenuSystem(unittest.TestCase):

    def test_demo_launchs_on_click(self):
        game.STATE = game.START_PAGE
        window = init([])
        window.draw_start_page()
        window.on_mouse_press(0.0,0.0,1,0)
        self.assertEqual(window.current_state, game.INS0)
        finish()

    def test_demo_skips_on_click(self):
        game.STATE = game.START_PAGE
        window = init([])
        window.draw_start_page()
        window.on_mouse_press(0.0,0.0,1,0)
        window.on_mouse_press(0.0,0.0,1,0)
        self.assertEqual(window.current_state, game.GAME_PAGE)
        finish()


    def test_button_changes_state(self):
        game.STATE = game.START_PAGE
        window = init([])
        window.draw_start_page()
        window.on_key_press(arcade.key.SPACE, 0)
        window.on_mouse_press(0.0,0.0,1,0)
        self.assertEqual(window.current_state, game.INSTRUCT1)
        finish()

    def test_game_menu_rolls(self):
        game.STATE = game.START_PAGE
        window = init([])
        window.draw_start_page()
        for i in range(game.BUTTON):
            window.on_key_press(arcade.key.SPACE,0)
        self.assertEqual(window.selected,window.start_button)
        finish()


#Helper Functions

#Set up game
def init(clouds=[],fire=[],source=["images/fire.jpg","images/forest.png"]):
    pygame.init()
    window = game.MyGame(game.SCREEN_WIDTH, game.SCREEN_HEIGHT)
    window.init_cloud_data = clouds
    window.init_fire_data = fire
    window.source = source
    window.NNDir = "TestDir/"
    window.setup()
    return window

def finish():
    arcade.window_commands.close_window()

if __name__ == '__main__':
    unittest.main()
