from sprites import *

class Mixin:
    #Will be used by NN to generate newly identified events
    def add_sprite(self,event,coOrds):

     if coOrds[0] >= 0 and coOrds[1] >=0 and coOrds[1] < SCREEN_HEIGHT:

                if  event == "fire":
                    # Create the fire instance
                    detected = Fire("images/fire_sprite.png", SPRITE_SCALING_FIRE)

                else:
                    #Create cloud instance
                    detected=Cloud("images/clouds.png", SPRITE_SCALING_CLOUD)

                # Position the fire
                detected.center_x = coOrds[0]
                detected.center_y = coOrds[1]

                if event == "fire":
                    self.fire_list.append(detected)
                else:
                    self.clouds_list.append(detected)

    def add_new_data(self):
        fileName = self.NNDir + "background" + str(self.background_index-1) + "-fire.txt"

        with open(fileName) as f:
            lines = f.readlines()

            for line in lines:
                line[-1].strip()
                line = eval(line, {"__builtins__": {}})
                self.add_sprite("fire",(line[0] + SCREEN_WIDTH, line[1]))
