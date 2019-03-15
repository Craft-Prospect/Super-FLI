import arcade
from constants import *

#PLayer and CPU sprite class
class Satellite(arcade.Sprite):

    health = HEALTH
    score = 0
    active = True
    speed = MOVEMENT_SPEED
    track_speed = CPU_TRACK_SPEED
    avoid = None
    last_avoid = None

    #Normal update called when screen is refreshed
    def update(self):
        #Change satellite position to new x and y(see |keypress.py player_keyboard| and |updateGame.py joystick_update|)
        self.center_x += self.change_x
        self.center_y += self.change_y

        #Ensure satellite doesn't run off screen
        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1
        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1

    #Addtional update called for CPU player. Moves CPU towards Fire or Player
    def cpu_update(self, Player, Fire = None):
        #if cpu has hit cloud and decided to avoid it
        if self.avoid != None:
            self.avoid_clouds(Player,Fire)

        #else try and track fire or player if no fire there
        else:
            self.track_player_or_fire(Player,Fire)

        self.last_avoid = self.avoid

    #updateGame cloud_damages sets wether CPU will be trying to avoid cloud or not
    def avoid_clouds(self,Player,Fire):
        #If trying to avoid two or more clouds, go straight
        if self.last_avoid != None and self.last_avoid != self.avoid:
            self.center_x += 2*self.speed

        else:
            #If fire is close by and CPU has enough spare power, get fire
            if Fire and (self.center_x - Fire.center_x < 50 and self.center_y - Fire.center_y < 50) and self.health > 40:
                self.track_player_or_fire(Player,Fire)

            #Else follow avoid instructions.
            #The < 50 refers to cases when the CPU is near the border and so should try to the opposite avoid command
            #e.g cloud is near bottom of screen but the CPU below cloud's center. Thefore it can't go down much before meeting border, so instead it should go up to try and avoid cloud
            else:
                if self.avoid[0] == "left":
                    if self.left < 50:
                        self.center_x += 2*self.speed
                    else:
                        self.center_x -=2*self.speed
                else:
                    if self.right > SCREEN_WIDTH - 50:
                        self.center_x -= 2*self.speed
                    else:
                        self.center_x += 2*self.speed

                if self.avoid[1] == "up":
                    if self.top > SCREEN_HEIGHT - 50:
                        self.center_y -= 2*self.speed
                    else:
                        self.center_y += 2*self.speed
                else:
                    if self.bottom < 50:
                        self.center_y += 2*self.speed
                    else:
                        self.center_y -= 2*self.speed

    #The CPU will try and track fire and if no fire, the player
    def track_player_or_fire(self,Player,Fire):

        if (Fire and self.center_x <Fire.center_x and Fire.center_x < (SCREEN_WIDTH-10)):
            self.center_x += self.speed
                #Else if there's a fire on the screen and the CPU is to the right of it
        elif (Fire and self.center_x > Fire.center_x and Fire.center_x < (SCREEN_WIDTH-10)):
            self.center_x -= self.speed

                #Else if the fire is off-screen, follow the player
        else:
            if (self.center_x <Player.center_x):
                self.center_x += self.track_speed
            elif(self.center_x > Player.center_x):
                self.center_x -= 2*self.track_speed

        #Same as above except for Y co-ordinates
        if (Fire and self.center_y <Fire.center_y and Fire.center_x < (SCREEN_WIDTH-10)):
            self.center_y +=self.speed
        elif (Fire and self.center_y > Fire.center_y and Fire.center_x < (SCREEN_WIDTH-10)):
            self.center_y -= self.speed
        else:
            if (self.center_y <Player.center_y):
                self.center_y += self.track_speed
            elif(self.center_y > Player.center_y):
                    self.center_y -= self.track_speed

#Class for scrolling background image
class Background(arcade.Sprite):

    speed = SCROLL_SPEED
    def update(self):

        # Move the fire
        self.center_x -= self.speed

        #If background has finsished scrolling(No image left to show), end the game
        if self.right <0:
            self.kill()
            return 1

        return 0

#Fire sprite for satellites to capture
class Fire(arcade.Sprite):

    #Refresh the sprite movement
    def update(self):
        # Move the fire
        self.center_x -= SCROLL_SPEED

        # See if the fire has moved off the left side of the screen.If it is off screen remove it from the sprite list
        if self.right < 0:
            self.kill()

#Clouds which the satellites should avoid
class Cloud(arcade.Sprite):
    damage = CLOUD_DAMAGE
    #Scroll the clouds to the left
    def update(self):
        # Move the cloud
        self.center_x -= SCROLL_SPEED

        # See if the cloud has fallen off the left of the screen, if so, remove it from the sprite list.
        if self.right < 0:
            self.kill()

#Buttons for main menu, (they do nothin, just a graphical representation)
class Button(arcade.Sprite):
    #arcade requires every sprite to have an update
    def update(self):
        pass

#Class for each Key contains it's 'Character'
class Key(arcade.Sprite):
    character = ""
