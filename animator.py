import cv2 as cv
from layer import Layer
from random import randint
import oscillator as osc
from oscillator import Oscillator
from oscillator import create_XY_oscillators
import math
import traceback
import utils as ut
#Take layer list as input, mode variable determines what to do to it, return the new draw list

# x_osc1, y_osc1 = osc.create_XY_oscillators([400,200],[1000,200])
# x_osc2, y_osc2 = osc.create_XY_oscillators([400,200],[400,800])
#

class Animator:
    def __init__(self, mode=0, speed=6, paused=False):
        '''
        Mode 0: Split & Converge (Layer "1" and "2")
        Mode 1: Vertical Line
        Mode 2: Vertical Cycle
        Mode 3: Horizontal Line
        Mode 4: Horizontal Cycle
        '''
        self.possible_speeds = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30] #Factors of 360
        self.set_speed(speed)
        self.set_mode(mode)
        self.paused = paused
        self.reversed = False

    def playpause(self):
        self.paused = not self.paused

    def reverse(self):
        self.reversed = not self.reversed
        self.set_mode(self.mode)

    def speed_up(self):
        for c, x in enumerate(self.possible_speeds):
            if self.speed == x and c+1 != len(self.possible_speeds):
                self.speed = self.possible_speeds[c+1]
                break
        print("Speed set: {}".format(self.speed))

    def speed_down(self):
        for c, x in enumerate(self.possible_speeds):
            if self.speed == x and c-1 >= 0:
                self.speed = self.possible_speeds[c-1]
        print("Speed set: {}".format(self.speed))

    def set_speed(self,speed):
        try:
            s = int(speed)
            min_diff = 100
            to_set = 1

            for x in self.possible_speeds:
                if x == s:
                    self.speed = s
                    print("Animator speed set to {}".format(self.speed))
                    return
                diff = abs(x-s)
                if diff < min_diff:
                    min_diff = diff
                    to_set = x

            self.speed = to_set
            print("Weird speed received ({}), set to {} instead".format(speed,self.speed))
        except BaseException as e:
            print(traceback.format_exc())

    def set_mode(self,mode):

        #TODO: Check for valid mode here
        self.mode = mode
        print("ANIMATOR MODE SET: {}".format(self.mode))

        # Setup
        if self.mode == 0: # SPLIT AND CONVERGE
            self.x_osc1, self.y_osc1 = osc.create_XY_oscillators([400,200],[1000,200],step=self.speed)
            self.x_osc2, self.y_osc2 = osc.create_XY_oscillators([400,200],[400,800],step=self.speed)
        elif self.mode == 1 or self.mode == 2: # Vertical Line/Cycle
            xpos = randint(400,1000)
            if self.reversed:
                self.x_oscv, self.y_oscv = osc.create_XY_oscillators([xpos,850],[xpos,200],step=self.speed)
            else:
                self.x_oscv, self.y_oscv = osc.create_XY_oscillators([xpos,200],[xpos,850],step=self.speed)
        elif self.mode == 3 or self.mode == 4: # Horizontal Line/Cycle
            ypos = randint(200,850)
            if self.reversed:
                self.x_osch, self.y_osch = osc.create_XY_oscillators([1000,ypos],[400,ypos],step=self.speed)
            else:
                self.x_osch, self.y_osch = osc.create_XY_oscillators([400,ypos],[1000,ypos],step=self.speed)

    def animate(self, layer_list, mode=None):
        if self.paused:
            # Do nothing, just return list
            return layer_list

        if mode is None:
            mode = self.mode
        try:
            if mode == 0: #SPLIT & CONVERGE
                x1 = int(self.x_osc1.read())
                self.x_osc1.step()
                y1 = int(self.y_osc1.read())
                self.y_osc1.step()
                x2 = int(self.x_osc2.read())
                self.x_osc2.step()
                y2 = int(self.y_osc2.read())
                self.y_osc2.step()

                for c, l in enumerate(layer_list):
                    if l.name == "1": l.translation = [x1,y1]
                    if l.name == "2": l.translation = [x2,y2]

                if self.y_osc1.position >= len(self.y_osc1.points)//2: # New oscillator
                    #Decide to split or converge
                    t1 = [0,0]
                    t2 = [0,0]
                    for c, l in enumerate(layer_list):
                        if l.name == "1": t2 = l.translation
                        if l.name == "2": t1 = l.translation

                    tol = 50
                    try:
                        if abs(t1[0]-t2[0]) < tol and abs(t1[1]-t2[1]) < tol:
                            print("Split")
                            p1 = ut.pick_location()
                            p2 = ut.pick_location()
                            self.x_osc1, self.y_osc1 = create_XY_oscillators(t1,p1,step=self.speed)
                            self.x_osc2, self.y_osc2 = create_XY_oscillators(t2,p2,step=self.speed)
                        else:
                            print("Converge")
                            p1 = ut.pick_location()
                            self.x_osc1, self.y_osc1 = create_XY_oscillators(t2,p1,step=self.speed)
                            self.x_osc2, self.y_osc2 = create_XY_oscillators(t1,p1,step=self.speed)
                    except BaseException as e:
                        print(traceback.format_exc())
            elif self.mode == 1 or self.mode == 2: # Vertical Line/Cycle
                x = int(self.x_oscv.read())
                y = int(self.y_oscv.read())
                self.x_oscv.step()
                self.y_oscv.step()

                for l in layer_list:
                    if l.name == "1": l.translation = [x,y]
                    if l.name == "2": l.translation = [x-10,y-10]

                if self.mode == 1:
                    if self.x_oscv.position >= len(self.x_oscv.points)//2:
                        self.x_oscv.set_offset(0)
                        self.y_oscv.set_offset(0)
            elif self.mode == 3 or self.mode == 4: # Hoorizontal Line/Cycle
                x = int(self.x_osch.read())
                y = int(self.y_osch.read())
                self.x_osch.step()
                self.y_osch.step()

                for l in layer_list:
                    if l.name == "1": l.translation = [x,y]
                    if l.name == "2": l.translation = [x-10,y-10]

                if self.mode == 3:
                    if self.x_osch.position >= len(self.x_osch.points)//2:
                        self.x_osch.set_offset(0)
                        self.y_osch.set_offset(0)

            return layer_list

        except BaseException as e:
            print("Something went wrong. Did you call set_mode before animate?")
            print(traceback.format_exc())
