from sprites import *
import time


class Mixin:

    def startMenu_update(self):


        # If centered set boolean to 0
        if abs(self.joystick.y) < DEAD_ZONE:
            self.check = 0
            return
        
        #If joystick pushed up update selected button and pointer position
        if self.joystick.y < 0 and self.check == 0:
            if self.selected == self.about_button:
                self.pointer.center_y = self.inst_button.center_y
                self.pointer.center_x = self.inst_button.center_x - 100
                self.selected = self.inst_button
                self.selected_index = 1
                self.check = 1
                


            elif self.selected == self.inst_button:
                self.pointer.center_y = self.start_button.center_y
                self.pointer.center_x = self.start_button.center_x - 100
                self.selected = self.start_button
                self.selected_index = 0
                self.check = 1
                
        #Otherwise move pointer down and update selected button
        elif self.check == 0:
            if self.selected == self.start_button:
                self.pointer.center_y = self.inst_button.center_y
                self.pointer.center_x = self.inst_button.center_x - 100
                self.selected = self.inst_button
                self.selected_index = 1
                self.check = 1 
                
            
            else:
                self.pointer.center_y = self.about_button.center_y
                self.pointer.center_x = self.about_button.center_x - 100
                self.selected = self.about_button
                self.selected_index = 2
                self.check = 1
                


        self.pointer.update()
