from sprites import *
import time

class Mixin:
    def keyboard_update(self):
        if self.joystick:
            # Set a "dead zone" to prevent drive from a centered joystick
            if abs(self.joystick.x) < DEAD_ZONE:
                self.pointer_sprite.change_x = 0
                self.check = 0

            elif self.check == 0:
                #Joystick movement to the right update position
                if self.joystick.x == 1:
                    self.pointer_sprite.change_x +=50
                #Joystick movement to the left update postion
                else:
                    self.pointer_sprite.change_x -= 50
                self.check = 1
                time.sleep(0.2)

                #if statements to ensure pointer always on the keyboard
            if self.pointer_sprite._position[0] >500:
                self.pointer_sprite._position[0] = 50

            if self.pointer_sprite._position[0] <50:
                self.pointer_sprite._position[0] = 500

            if self.pointer_sprite._position[0] > 400 and self.pointer_sprite._position[1] == 100:
                self.pointer_sprite._position[0] = 50

            if self.pointer_sprite._position[0] <50 and self.pointer_sprite._position[1] == 100:
                self.pointer_sprite._position[0] = 400

            # Set a "dead zone" to prevent drive from a centered joystick
            # Movement value must be greater than dead zone for movement to be registered by the joystick
            if abs(self.joystick.y) < DEAD_ZONE:
                self.pointer_sprite.change_y = 0
                self.check_y = 0

            elif self.check_y == 0:
                if self.joystick.y == -1:
                    self.pointer_sprite.change_y +=50
                else:
                    self.pointer_sprite.change_y -= 50
                self.check_y = 1
                time.sleep(0.2)

            #Scroll back if sprite is moving off the keyboard
            if self.pointer_sprite._position[1] > 200:
                self.pointer_sprite._position[1] = 100

            if self.pointer_sprite._position[1] <100:
                self.pointer_sprite._position[1] = 200

            self.pointer_sprite.update()
