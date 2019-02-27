from sprites import *

class Mixin:
    #Refresh the screen
    def update(self, delta_time):

        if self.current_state == GAME_PAGE:

            # Update the position according to the game controller
            if self.joystick:

                # Set a "dead zone" to prevent drive from a centered joystick
                if abs(self.joystick.x) < DEAD_ZONE:
                    self.player_sprite.change_x = 0
                else:
                    self.player_sprite.change_x = self.joystick.x * self.player_sprite.speed

            # Set a "dead zone" to prevent drive from a centered joystick
                if abs(self.joystick.y) < DEAD_ZONE:
                    self.player_sprite.change_y = 0
                else:
                    self.player_sprite.change_y = -self.joystick.y * self.player_sprite.speed

            self.player_sprite.update()



            #If player is alive, update
            if self.player_sprite.active:
                self.player_list.update()

            #Update sprites and clouds
            self.fire_list.update()

            self.clouds_list.update()

            update = self.background_even.update()
            update -= self.background_odd.update()

            #If the even background sprite have reached the end of the screen
            if(update == 1):

                #If there's no more backgrounds, don't make another
                if(self.final_background):
                    pass


                else:
                    #Else create a new even background, off screen, to scroll after the next odd one
                    self.background_even = Background(self.source[self.background_index], BACKGROUND_SCALING)
                    self.background_index += 1
                    self.background_even.center_x = SCREEN_WIDTH + SCREEN_WIDTH/2
                    self.background_even.center_y = SCREEN_HEIGHT/2
                    self.background_list.append(self.background_even)
                    self.add_new_data()

                #If there is no more backgrounds left
                if (self.background_index == len(self.source)):
                    self.final_background = True

            #If the odd background has reached the end of the screen
            elif(update == -1):

                #If it's the final background, end the game (This code may need to be added to the even side, if an even number of bacgkrounds is used)
                if(self.final_background):
                    self.current_state = END_PAGE

                else:
                    #Create a new odd background, opff screen, ready to scroll in after the next even one
                    self.background_odd = Background(self.source[self.background_index], BACKGROUND_SCALING)
                    self.background_index += 1
                    self.background_odd.center_x = SCREEN_WIDTH + SCREEN_WIDTH/2
                    self.background_odd.center_y = SCREEN_HEIGHT/2

                    self.background_list.append(self.background_odd)
                    self.add_new_data()

                    #If there's no backgrounds left
                    if (self.background_index == len(self.source)):
                        self.final_background = True

            #Update CPU satellite
            if self.cpu_sprite.active:
                if len(self.fire_list)> 0:
                    self.cpu_sprite.cpu_update(self.player_sprite,self.fire_list[0])
                else:
                    self.cpu_sprite.cpu_update(self.player_sprite)
                self.cpu_list.update()

                # Generate a list of all emergencies that collided with the satellite.
                hit_list = arcade.check_for_collision_with_list(self.cpu_sprite,self.fire_list)
                # Loop through each colliding fire, remove it, and add to the cpu_score.
                for fire in hit_list:
                    fire.kill()
                    self.cpu_sprite.score += 100


                # Generate a list of all clouds that collided with the CPU.
                hit_list = arcade.check_for_collision_with_list(self.cpu_sprite,self.clouds_list)

                # Loop through each colliding cloud, decrease CPU health.
                for cloud in hit_list:
                    self.cpu_sprite.health -= cloud.damage

                    if self.cpu_sprite.health <= 0:
                        self.cpu_sprite.active = False
                        self.cpu_sprite.kill()

                        if not self.player_sprite.active:
                            self.current_state = END_PAGE

            #If the player is there
            if self.player_sprite.active:
                # Generate a list of all clouds that collided with the player.
                hit_list = arcade.check_for_collision_with_list(self.player_sprite,self.clouds_list)

                # Loop through each colliding sprite, remove it, and add to the player_score.
                for cloud in hit_list:
                    self.player_sprite.health -= cloud.damage

                    if self.player_sprite.health <=0:
                        self.player_sprite.active = False
                        self.player_score = self.player_sprite.score
                        self.player_sprite.kill()

                        if not self.cpu_sprite.active:
                            self.current_state=END_PAGE

            if len(self.fire_list) <3 and len(self.fire_data) > 0:
                item = self.fire_data.pop(0)
                self.add_sprite(item[0], item[1])
            if len(self.clouds_list) <3 and len(self.cloud_data) > 0:
                item = self.cloud_data.pop(0)
                self.add_sprite(item[0], item[1])

        #If the game is in a text instruction, pause for ~5 secs
        elif self.current_state == INS0 or self.current_state == INS1 or self.current_state == INS4 or self.current_state == INS7:
            if self.update_count == 400:
                self.update_count = 0
                self.current_state += 1
            else:
                self.update_count += 1

        #Generate the sprite for the fire after ~2 secs and display text for ~5 secs
        elif self.current_state == INS2:
            if self.update_count == 400:
                self.update_count = 0
                self.current_state += 1

            elif self.update_count == 200:
                self.add_sprite("fire",(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
                self.add_sprite("fire",(2700,200))
            self.update_count += 1

        #Move the clouds close the player
        elif self.current_state == INS3:
            self.clouds_list.update()

            self.update_count += 1

            if self.update_count == 80:
                self.update_count = 0
                self.current_state += 1

        #Do cloud damage to the player
        elif self.current_state == INS5:
            self.clouds_list.update()

            players = [self.cpu_sprite, self.player_sprite]
            for sat in players:
                # Generate a list of all clouds that collided with the CPU.
                hit_list = arcade.check_for_collision_with_list(sat,self.clouds_list)

                # Loop through each colliding cloud, decrease CPU health.
                for cloud in hit_list:
                    sat.health -= cloud.damage
            self.update_count += 1

            if self.update_count == 400:
                self.update_count = 0
                self.current_state += 1

        #Move player close to fire
        elif self.current_state == INS6:
            self.player_sprite.cpu_update(self.cpu_sprite, self.fire_list[0])
            self.update_count += 1

            if self.update_count == 340:
                self.update_count = 0
                self.current_state += 1

        #Capture fire and add to player score
        elif self.current_state == INS8:
            self.fire_list[0].kill()
            self.player_sprite.score += 100
            self.current_state += 1

        elif self.current_state == ENTER_NAME:
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

                #if statements to ensure pointer always on the keyboard // Replace with case statement?
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
