#Scaling for sprites(a multiplication factor i.e scaling*(sprite_image_size) )
SPRITE_SCALING_POINTER = 1
SPRITE_SCALING_KEY = 1
SPRITE_SCALING_PLAYER = 1
SPRITE_SCALING_FIRE = 1
SPRITE_SCALING_CLOUD = 1
SPRITE_SCALING_BUTTON = 1
BACKGROUND_SCALING = 1

#Window size
SCREEN_WIDTH = 1040
SCREEN_HEIGHT = 597

#Raspberry Pi speeds
RASP = 0
#RASP = 20

#Sprite Speeds
MOVEMENT_SPEED = 1.5 + RASP  #Player speeds
CPU_SPEED = 1.25 + RASP #Normal CPU speed
CPU_TRACK_SPEED = 0.5 + RASP #CPU speed when no emergency on screen and is tracking player movement
SCROLL_SPEED = 1 + RASP #Speed of background_sprite, clouds and fire sprites

#Variable for setting difficulty
CLOUD_DAMAGE = 0.1*(RASP +1)
HEALTH = 100

#Image sources
LVL1=["images/LVL1/lvl1.png", "images/LVL1/background1.png","images/LVL1/background2.png", "images/LVL1/background3.png", "images/LVL1/background4.png","images/sea.png"]
LVL2=["images/LVL2/lvl2.png", "images/LVL2/background1.png","images/LVL2/background2.png", "images/LVL2/background3.png", "images/LVL2/background4.png","images/sea.png"]
SOURCE = [LVL1,LVL2]
NNDir = "NNData/"
#PLayer's score for saving in Highscore file
Final_score = 0

#Game states
SPLASH = -1
START_PAGE = 0
INSTRUCT1 = 1
INSTRUCT2 = 2
ABOUT = 3
GAME_PAGE = 4
END_PAGE = 5
ENTER_NAME = 6
HIGH_SCORE_PAGE = 7
FEEDBACK_PAGE = 8

#Demo states
#Game states
INS0 = 10
INS1 = 11
INS2 = 12
INS3 = 13
INS4 = 14
INS5 = 15
INS6 = 16
INS7 = 17
INS8 = 18
INS9 = 19

#Initial game state
STATE = SPLASH

#Player co-ordinates
PLAYER_START_X = 50
PLAYER_START_Y = 50

#Demo co-ordinates
STARTX= 50
STARTY = 50

#CPU co-ordinates
CPU_START_X = 50
CPU_START_Y = SCREEN_HEIGHT - 50

#Variables used for joystick movement
DEAD_ZONE = 0.02

#Text for about page

ABOUT_TEXT = [
"Craft Prospect is a space engineering practice, founded",
"on the principal of bringing together NewSpace",
"professionals and experts in the latest technologies to",
"advance the NewSpace state of the art. Our focus is on",
"developing adaptive mission architectures, space",
"applications. Our goal is to bring autonomy and ",
"capability to the next generation of small satellites.",
]

#Local and Remote Neural Network Commands

COMMAND = ['../yolo_tiny/darknet', 'detector', 'test', '../yolo_tiny/cfg/obj.data', '../yolo_tiny/cfg/tiny-yolo.cfg', '../yolo_tiny/backup/tiny-yolo_2000.weights']

#COMMAND = ['ssh', 'andrew@10.42.0.1', 'cd', '/home/andrew/testing_tiny/darknet2/darknet', ';', './darknet', 'detector', 'test', 'cfg/obj.data', 'cfg/tiny-yolo.cfg', 'backup/tiny-yolo_2000.weights']
