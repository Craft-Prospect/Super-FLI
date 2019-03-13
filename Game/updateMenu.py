from sprites import *
import time


class Mixin:

    def update_pointer(self,button,index):
        self.pointer.center_y = button.center_y
        self.pointer.center_x = button.center_x - 100
        self.selected = button
        self.selected_index = index
        self.check = 1

    def startMenu_update(self):
        # If centered set boolean to 0
        if abs(self.joystick.y) < DEAD_ZONE:
            self.check = 0
            return
        
        #If joystick pushed up update selected button and pointer position
        if self.joystick.y < 0 and self.check == 0:
            if self.selected == self.about_button:
                Mixin.update_pointer(self,self.inst_button,1)

            
            elif self.selected == self.inst_button:
                Mixin.update_pointer(self,self.start_button,0)

            
                
        #Otherwise move pointer down and update selected button
        elif self.check == 0:
            if self.selected == self.start_button:
                Mixin.update_pointer(self,self.inst_button,1)
                
            
            else:
                Mixin.update_pointer(self,self.about_button,2)
                
            

        self.pointer.update()
