"""Satellite game where user competes against CPU to capture events while avoid clouds"""
import os
import time
import sys

from sprites import *
from helper import *

import menu
import instructions
import runGame
import highscore
import demo
import keyboard
import keypress
import stateChange
import spriteFunc
import drawing
import updateGame
import updateIns
import updateKeyboard
import splash
import levels
import pygame

#Main window
class MyGame(drawing.Mixin, keypress.Mixin, stateChange.Mixin, spriteFunc.Mixin, levels.Mixin, splash.Mixin, updateGame.Mixin, updateIns.Mixin, updateKeyboard.Mixin, menu.Mixin, instructions.Mixin, demo.Mixin, runGame.Mixin,keyboard.Mixin,highscore.Mixin, arcade.Window):
    #Initalise game variables and window
    def __init__(self, width, height,test):

        # Call the parent class initialise to window
        super().__init__(width, height)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold the sprite lists
        self.fire_list=None
        self.clouds_list = None

        self.Test = test

        #Sprite co-ordinates (will be replaced by NN)
        self.init_fire_data = [("fire",(904,483))]
        self.init_cloud_data = [("cloud", (0,150)),("cloud", (420,300)),("cloud", (700,742)),("cloud", (1000,200)),("cloud", (1500,10)),("cloud", (1800,200)),("cloud", (2000,0)),("cloud", (1500,10)),("cloud", (1800,200)),("cloud", (2000,0)),("cloud", (1500,10)),("cloud", (1800,200)),("cloud", (2000,0))]

        self.fire_data = None
        self.cloud_data = None
        self.cloud_damage = CLOUD_DAMAGE

        # Set up the player info
        self.player_sprite = None

        #Set up CPU sprite
        self.cpu_sprite = None

        #Background sprites
        self.background_list = None
        self.background_even = None
        self.background_odd = None
        self.background_index = 0
        self.final_background = False
        self.background = None

        #For screenshot timings
        self.frame = 800
        self.frame_count = 0
        self.picture = 0

        #Game state
        self.current_state = STATE

        #Instruction pages
        self.instructions = []

        #Setup background textures
        texture = arcade.load_texture("images/menu.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/instruct_0.png")
        self.instructions.append(texture)

        texture = arcade.load_texture("images/instruct_1.png")
        self.instructions.append(texture)
        #Menu buttons
        self.buttons = None
        self.start_button = None
        self.inst_button = None

        #Currently selected buttons
        self.selected = None

        #Pointer into button list
        self.selected_index = None

        #Sprite to show which button is selected
        self.pointer_list = None
        self.pointer = None

        self.player_score = None

        #Keyboard values
        self.key_list = None

        self.source = SOURCE[0]
        self.NNDir = NNDir

        self.update_count = 0

        # Get a list of all the game controllers that are plugged in
        joysticks = arcade.get_joysticks()

        # If we have a game controller plugged in, grab it and
        # make an instance variable out of it.
        joysticks = arcade.get_joysticks()
        if joysticks:
            self.joystick = joysticks[0]
            self.joystick.open()
            self.joystick.on_joybutton_press = self.on_joybutton_press
            self.joystick.on_joybutton_release = self.on_joybutton_release
            self.joystick.on_joyhat_motion = self.on_joyhat_motion

        else:
            self.joystick = None


        self.setup_splash()

        if not self.Test:
            self.lvl_up =  pygame.mixer.Sound("Music/sounds/lvlup.wav")


    def update(self, delta_time):

        if self.current_state == GAME_PAGE:
            self.game_update()

        elif self.current_state == ENTER_NAME:
            self.keyboard_update()

        else:
            self.ins_update()
