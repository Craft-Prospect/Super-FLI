import game
import arcade
import pygame
import unittest
import helper
import os

#Test the game generates sprites
class TestSetupMethods(unittest.TestCase):

    def test_add_sprite_fire(self):
        window = init([])
        window.add_sprite("fire", (1,1))
        self.assertEqual(len(window.fire_list), 1)
        finish()

    def test_add_sprite_cloud(self):
        window = init([])
        window.add_sprite("cloud")
        self.assertEqual(len(window.clouds_list),1)
        finish()

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
        window = init(fire = [("fire", (game.CPU_START_X, game.CPU_START_Y))] )
        window.draw_game()

        window.update(1)

        self.assertEqual(window.cpu_sprite.score, game.SCOREINC)
        finish()

    def test_tracking_fire_above_left(self):
        game.STATE = game.GAME_PAGE
        window = init(fire = [("fire", (game.CPU_START_X + 10, game.CPU_START_Y-10))])
        #Don't allow clouds to interfere
        window.clouds_limit = 0
        window.clouds_list = arcade.SpriteList()

        window.cpu_sprite.speed = 1

        for i in range(10):
            window.cpu_sprite.cpu_update(window.player_sprite, window.fire_list[0])

        self.assertEqual((window.cpu_sprite.center_x + window.cpu_sprite.center_y),(window.fire_list[0].center_x + window.fire_list[0].center_y))
        finish()


    def test_tracking_fire_below_right(self):
        game.STATE = game.GAME_PAGE
        window = init(fire = [("fire", (game.CPU_START_X - 10, game.CPU_START_Y +10))])
        #Don't allow clouds to interfere
        window.clouds_limit = 0
        window.clouds_list = arcade.SpriteList()

        window.cpu_sprite.speed = 1

        for i in range(10):
            window.cpu_sprite.cpu_update(window.player_sprite, window.fire_list[0])

        self.assertEqual((window.cpu_sprite.center_x + window.cpu_sprite.center_y),(window.fire_list[0].center_x + window.fire_list[0].center_y))
        finish()

    def test_tracking_player_below_right(self):
        game.STATE = game.GAME_PAGE
        window = init()
        #Don't allow clouds to interfere
        window.clouds_limit = 0
        window.clouds_list = arcade.SpriteList()

        window.cpu_sprite.center_x = game.STARTY - 20
        window.cpu_sprite.center_y = game.STARTX - 20
        window.cpu_sprite.track_speed = 1

        for i in range(21):
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
        self.assertEqual(window.player_sprite.score, game.SCOREINC)
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

    #buttons are a image holder. Ensure updating them does nothing
    def test_button_does_nothing(self):
        game.STATE = game.MENU_PAGE
        window = init()
        window.menu_setup()

        window.buttons[0].update()

        self.assertEqual(window.current_state,game.MENU_PAGE)
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
        finish()

    def test_neg_health_rounds(self):
        game.STATE = game.GAME_PAGE
        window = init()
        window.player_sprite.health = -100.75

        self.assertEqual(window.round_health(window.player_sprite), 0)

        finish()

    def test_Player_can_skip_on_death(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud",(game.CPU_START_X,game.CPU_START_Y)), ("cloud", (game.PLAYER_START_X,game.PLAYER_START_Y))])
        window.player_sprite.health = 0
        window.update(1)

        window.change_state()

        self.assertEqual(window.current_state, game.ENTER_NAME)
        finish()

#Test menu selection screen works
class TestMenuSystem(unittest.TestCase):

    def test_demo_launchs_on_click(self):
        game.STATE = game.MENU_PAGE
        window = init([])
        window.menu_setup()
        window.draw_menu()
        window.on_mouse_press(0.0,0.0,1,0)
        self.assertEqual(window.current_state, game.INS0)
        finish()

    def test_demo_skips_on_click(self):
        game.STATE = game.MENU_PAGE
        window = init([])
        window.menu_setup()
        window.draw_menu()
        window.on_mouse_press(0.0,0.0,1,0)
        window.on_mouse_press(0.0,0.0,1,0)
        self.assertEqual(window.current_state, game.GAME_PAGE)
        finish()

    def test_button_changes_state(self):
        game.STATE = game.MENU_PAGE
        window = init([])
        window.menu_setup()
        window.draw_menu()
        window.on_key_press(arcade.key.SPACE, 0)
        window.on_mouse_press(0.0,0.0,1,0)
        self.assertEqual(window.current_state, game.INSTRUCT1)
        finish()

    def test_game_menu_rolls(self):
        game.STATE = game.MENU_PAGE
        window = init([])
        window.menu_setup()
        window.draw_menu()
        for i in range(len(window.buttons)):
            window.on_key_press(arcade.key.SPACE,0)
        self.assertEqual(window.selected,window.start_button)
        finish()


class TestHelpers(unittest.TestCase):
    def test_get_numer(self):
        self.assertEqual(helper.get_number(game.SYMBOL + "100"),"100")

    def test_add_highscore(self):
        clear_scores()
        helper.add_highscore("Test1", 100)
        helper.add_highscore("Test2", 500)
        helper.add_highscore("Test", 200)

        with open('scores.txt', 'r') as f:
            lines = f.readlines()
            self.assertEqual(lines[0].strip(), "Test2 : "+ game.SYMBOL + "500")
            self.assertEqual(lines[1].strip(), "Test : "+ game.SYMBOL + "200")
            self.assertEqual(lines[2].strip(), "Test1 : "+ game.SYMBOL + "100")

    def test_empty_name_high_score(self):
        clear_scores()
        helper.add_highscore("","100")
        self.assertEqual(os.stat("scores.txt").st_size, 0)

    def test_empty_score_high_score(self):
        clear_scores()
        helper.add_highscore("Test",None)
        self.assertEqual(os.stat("scores.txt").st_size, 0)

class TestLevelingUp(unittest.TestCase):
    def test_level_up_even(self):
        game.SOURCE = [["images/LVL1/background2.png","images/LVL1/background2.png"],["images/LVL1/background3.png","images/LVL1/background3.png"]]
        window = game.MyGame(game.SCREEN_WIDTH, game.SCREEN_HEIGHT,True)
        window.current_state = game.GAME_PAGE
        window.NNDir = 'TestDir/'
        window.SOURCE = [["images/LVL1/background2.png","images/LVL1/background2.png"],["images/LVL1/background3.png","images/LVL1/background3.png"]]
        window.game_setup()

        window.background_even.speed = 500
        window.background_odd.speed = 500
        for i in range(10):
            update = window.background_even.update()
            update -= window.background_odd.update()
            window.game_background_update(update)

        self.assertEqual(window.level, 2)
        finish()

    def test_level_up_odd(self):
        game.SOURCE = [["images/LVL1/background2.png","images/LVL1/background2.png","images/LVL1/background2.png"],["images/LVL1/background3.png","images/LVL1/background3.png"]]
        window = game.MyGame(game.SCREEN_WIDTH, game.SCREEN_HEIGHT,True)
        window.current_state = game.GAME_PAGE
        window.SOURCE = [["images/LVL1/background2.png","images/LVL1/background2.png"],["images/LVL1/background3.png","images/LVL1/background3.png"]]
        window.game_setup()

        window.background_even.speed = 500
        window.background_odd.speed = 500
        window.NNDir = "TestDir/"
        for i in range(20):
            update = window.background_even.update()
            update -= window.background_odd.update()
            window.game_background_update(update)
            if update == -1:
                window.background_odd.speed = 500

        self.assertEqual(window.level, 2)
        finish()

    def test_game_over_lvl(self):
        game.SOURCE = [["images/LVL1/background2.png","images/LVL1/background2.png"],["images/LVL1/background3.png","images/LVL1/background3.png"]]
        window = game.MyGame(game.SCREEN_WIDTH, game.SCREEN_HEIGHT,True)
        window.current_state = game.GAME_PAGE
        window.SOURCE = [["images/LVL1/background2.png","images/LVL1/background2.png"],["images/LVL1/background3.png","images/LVL1/background3.png"]]
        window.game_setup()

        window.level_up()
        window.level_up()

        self.assertEqual(window.current_state, game.END_PAGE)
        finish()

class TestSpriteMovementHandling(unittest.TestCase):

    def test_check_cloud_death(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud", (0,0))])
        window.clouds_list[0].right = 0
        window.clouds_list[0].update()
        self.assertEqual(len(window.clouds_list), 0)
        finish()
    def test_left_border_Satelite(self):
        game.STATE = game.GAME_PAGE
        window = init()
        window.player_sprite.left = 0
        window.player_sprite.change_x = -1
        window.player_sprite.update()
        self.assertEqual(window.player_sprite.left, 0)
        finish()
    def test_right_border_Satelite(self):
        game.STATE = game.GAME_PAGE
        window = init()
        window.player_sprite.right = game.SCREEN_WIDTH
        window.player_sprite.change_x = 1
        window.player_sprite.update()
        self.assertEqual(window.player_sprite.right, (game.SCREEN_WIDTH-1))
        finish()

    def test_bottom_border_Satelite(self):
        game.STATE = game.GAME_PAGE
        window = init()
        window.player_sprite.bottom = 0
        window.player_sprite.change_y = -1
        window.player_sprite.update()
        self.assertEqual(window.player_sprite.bottom, 0)
        finish()

    def test_top_border_Satelite(self):
        game.STATE = game.GAME_PAGE
        window = init()
        window.player_sprite.top = game.SCREEN_HEIGHT
        window.player_sprite.change_y = 1
        window.player_sprite.update()
        self.assertEqual(window.player_sprite.top, (game.SCREEN_HEIGHT-1))
        finish()

    def test_CPU_avoids_cloud_right_below(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud", (0,0))])
        window.cpu_sprite.center_x = 300
        window.cpu_sprite.center_y = 300
        window.clouds_list[0].center_x = window.cpu_sprite.center_x + 10
        window.clouds_list[0].center_y = window.cpu_sprite.center_y - 10

        window.cloud_damages(window.cpu_sprite)
        window.cpu_sprite.cpu_update(window.player_sprite)
        self.assertEqual(window.cpu_sprite.avoid, ["left", "up"])
        self.assertEqual(window.cpu_sprite.center_x, 300-2*game.CPU_SPEED)
        self.assertEqual(window.cpu_sprite.center_y, 300+2*game.CPU_SPEED)

        finish()

    def test_CPU_avoids_cloud_left_above(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud", (0,0))])
        window.clouds_list[0].center_x = window.cpu_sprite.center_x - 10
        window.clouds_list[0].center_y = window.cpu_sprite.center_y + 10

        window.cloud_damages(window.cpu_sprite)
        window.cpu_sprite.cpu_update(window.player_sprite)
        self.assertEqual(window.cpu_sprite.avoid, ["right", "down"])
        self.assertEqual(window.cpu_sprite.center_x, game.CPU_START_X+2*game.CPU_SPEED)
        self.assertEqual(window.cpu_sprite.center_y, game.CPU_START_Y-2*game.CPU_SPEED)

        finish()

    def test_CPU_avoids_cloud_near_border_left_above(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud", (0,0))])
        window.cpu_sprite.center_x = 30
        window.cpu_sprite.center_y = 30
        window.clouds_list[0].center_x = window.cpu_sprite.center_x + 10
        window.clouds_list[0].center_y = window.cpu_sprite.center_y - 10

        window.cloud_damages(window.cpu_sprite)
        window.cpu_sprite.cpu_update(window.player_sprite)
        self.assertEqual(window.cpu_sprite.avoid, ["left", "up"])
        self.assertEqual(window.cpu_sprite.center_x, 30 +2*game.CPU_SPEED)
        self.assertEqual(window.cpu_sprite.center_y, 30 +2*game.CPU_SPEED)

        finish()

    def test_CPU_avoids_cloud_near_border_right_down(self):
        game.STATE = game.GAME_PAGE
        window = init(clouds = [("cloud", (0,0))])
        window.cpu_sprite.center_x = game.SCREEN_WIDTH-30
        window.cpu_sprite.center_y = game.SCREEN_HEIGHT-30
        window.clouds_list[0].center_x = window.cpu_sprite.center_x - 10
        window.clouds_list[0].center_y = window.cpu_sprite.center_y + 10

        window.cloud_damages(window.cpu_sprite)
        window.cpu_sprite.cpu_update(window.player_sprite)
        self.assertEqual(window.cpu_sprite.avoid, ["right", "down"])
        self.assertEqual(window.cpu_sprite.center_x,  game.SCREEN_WIDTH-30 -2*game.CPU_SPEED)
        self.assertEqual(window.cpu_sprite.center_y, game.SCREEN_HEIGHT-30 -2*game.CPU_SPEED)

        finish()
class TestDemoVideo(unittest.TestCase):
    def test_helper_counting(self):
        window = init()
        window.current_state = 3
        window.counting(2)
        window.counting(2)
        window.counting(2)
        self.assertEqual(window.current_state,4)
        finish()


class TestOnscreenKeyboard(unittest.TestCase):
    def test_input(self):
        window = init()
        window.current_state = game.ENTER_NAME
        window.change_state()
        window.keyboard_setup()
        window.on_key_press(arcade.key.T, 0)
        self.assertEqual(window.name, ['t'])
        finish()

    def test_caps(self):
        window = init()
        window.current_state = game.ENTER_NAME
        window.change_state()
        window.keyboard_setup()
        window.on_key_press(arcade.key.CAPSLOCK,0)
        window.on_key_press(arcade.key.T,0)
        window.on_key_press(arcade.key.E,0)
        window.on_key_press(arcade.key.CAPSLOCK,0)
        window.on_key_press(arcade.key.S,0)
        self.assertEqual(window.name,['T','E','s'])
        finish()

    def test_max_input_length(self):
        window = init()
        window.current_state = game.ENTER_NAME
        window.change_state()
        window.keyboard_setup()
        for i in range(10):
            window.on_key_press(arcade.key.T,0)
        self.assertEqual(len(window.name),4)
        finish()

    def test_enter_key_works(self):
        window = init()
        window.current_state = game.ENTER_NAME
        window.change_state()
        window.keyboard_setup()
        window.on_key_press(arcade.key.ENTER,0)
        self.assertEqual(window.current_state,game.HIGH_SCORE_PAGE)
        finish()
#Helper Functions

#Set up game
def init(clouds=[],fire=[],source=["images/LVL1/background1.png","images/LVL1/background1.png"]):
    pygame.init()  #Uncomment for code coverage tests
    pygame.mixer.init() #Uncomment for code coverage tests
    window = game.MyGame(game.SCREEN_WIDTH, game.SCREEN_HEIGHT,False) #Change true to false for code coverage tests
    window.source = source
    window.NNDir = "TestDir/"
    window.clouds_limit = 0
    window.game_setup()
    change_game_sprites(window,clouds)
    change_game_sprites(window,fire)
    return window

def clear_scores():
    open('scores.txt', 'w').close()

def finish():
    arcade.window_commands.close_window()

def change_game_sprites(game,sprites):
    for sprite in sprites:
        game.add_sprite(sprite[0],sprite[1])

if __name__ == '__main__':
    unittest.main()
