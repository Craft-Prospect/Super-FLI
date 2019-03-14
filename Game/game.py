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

        #Variable for running tests in headless display(C.I) (controls whether NN is run and if sounds are played)
        self.Test = test

        # Variables that will hold the sprite lists
        self.fire_list=None
        self.clouds_list = None

        #Used to set damage caused by a clouds sprite (only used in cloud generation)
        self.cloud_damage = CLOUD_DAMAGE

        #Controls maximum number of clouds onscreen
        self.clouds_limit = 3

        # Set up the player sprite
        self.player_sprite = None

        #Set up CPU sprite
        self.cpu_sprite = None

        #Background sprites
        self.background_list = None
        self.background_odd = None
        self.background_even = None
        self.background_index = 0
        self.final_background_even = False
        self.final_background_odd = False
        self.background = None

        #Currrent Game state
        self.current_state = STATE

        #Game page textures pages
        self.textures = []

        #Setup background textures
        texture = arcade.load_texture(IMG_MAIN_MENU)
        self.textures.append(texture)

        texture = arcade.load_texture(IMG_INS0)
        self.textures.append(texture)

        texture = arcade.load_texture(IMG_INS1)
        self.textures.append(texture)

        texture = arcade.load_texture(IMG_ABOUT)
        self.textures.append(texture)
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

        #Variable for storing final highscore(if player dies)
        self.player_score = None

        #Keyboard values
        self.key_list = None

        #Image file locations for game levels (see constants.py)
        self.SOURCE = SOURCE
        self.source = self.SOURCE[0]
        self.NNDir = NNDir

        #Controls when demo.py instruction refreshes (see updateIns.py)
        self.update_count = 0

        # Get a list of all the game controllers that are plugged in
        self.joysticks = arcade.get_joysticks()

        # If we have a game controller plugged in, use it make an instance variable out of it.
        if self.joysticks:
            self.joystick = self.joysticks[0]
            self.joystick.open()
            self.joystick.on_joybutton_press = self.on_joybutton_press
            self.joystick.on_joybutton_release = self.on_joybutton_release
            self.joystick.on_joyhat_motion = self.on_joyhat_motion

        else:
            self.joystick = None

        #If not running headless display test (on Continous Intergrator), load sounds for pygame to play later(see level.py and spriteFunc.py)
        if not self.Test:
            self.lvl_up =  pygame.mixer.Sound(SND_LVL)
            self.player_sound = pygame.mixer.Sound(SND_PLAYER)
            self.cpu_sound =  pygame.mixer.Sound(SND_CPU)
        else:
            self.player_sound = None
            self.cpu_sound = None

        #Initialises game level
        self.level = 1

        #Setups game to begin
        self.setup_splash() #See splash.py


    #Handles updating the game
    def update(self, delta_time):

        if self.current_state == MENU_PAGE:
            #Menu state change uses handled by keyboard presses but if joystick is connnected, polls (see updateMenu.py)
            if self.joysticks:
                self.menu_jopystick_update()#see updateMenu.py

        elif self.current_state == GAME_PAGE:
            self.game_update() #see updateGame.py

        elif self.current_state == ENTER_NAME:
            self.keyboard_update()#see updateKeyboard.py

        else:
            self.ins_update() # see updateIns.py
