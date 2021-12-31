import cv2 as cv
import numpy as np
from layer import Layer
import math


class Oscillator:
    '''
    General purpose oscillator class.
    Offset Modes:
    0 - Absolute position within self.points
    1 - Fractional/relative position (0.0-1.0)
    2 - Degree position (0-360)
    3 - Radian Position (0-2pi)

    '''
    def __str__(self):
        s = "Oscillator:\n" + str(self.draw_layer) + "\nCurrent Value:" + str(self.points[self.position])
        return s

    def __init__(self,operations=[],step=1,offset=0,mode=2,resolution=64,dtype=np.float16,verbose=False):
        print("Constructing Oscillator...")
        print("Resolution: ",resolution)
        self.verbose = verbose
        self.resolution = resolution
        
        self.points =  np.zeros((resolution),dtype=dtype)
        
        self.position = self.get_position(offset,mode,verbose=True)
        self.offset = offset
        self.mode = mode
        self.step_size = step
        print("Step Size:", step)

        self.draw_layer = Layer()
        self.draw_w = 400
        self.draw_h = 200
        self.draw_mode = 1
        self.draw_skip = 1
        self.draw_color = (255,255,255)
        self.draw_size = 3
        self.draw_thick = 2
        self.draw_transparent = True

        print("Operations: ",operations)
        for i in range(len(self.points)):
            val = 0
            out_str = ""
            for o in operations:
                # print(o.__class__)
                if type(o) == str:
                    if o[0] == '+': # Add
                        val += float(o[1:])
                        out_str += "Add ({}) - ".format(float(o[1:]))
                    if o[0] == '-': # Subtract
                        val -= float(o[1:])
                        out_str += "Sub ({}) - ".format(float(o[1:]))
                    if o[0] == '*': # Mult
                        val *= float(o[1:])
                        out_str += "Mult ({}) - ".format(float(o[1:]))
                    if o[0] == '/': # Div
                        val /= float(o[1:])
                        out_str += "Div ({}) - ".format(float(o[1:]))

                elif o.__class__.__module__ == 'builtins':
                    # if self.mode == 0:
                    #     out_str += "Builtin ("+str(round(o(i),2))+") - "
                    #     val += o(i)
                    # else:
                    x = o((i/len(self.points))*(2*math.pi))
                    out_str += "Builtin ("+str(round(x,2))+") - "
                    val += x
            out_str += "VAL: "+str(val)
            if verbose: print(out_str)
            self.points[i] = val
        if verbose: print(self.points)
        if verbose: print("Points Length: ",len(self.points))
        print("Current Position: {}/{}, Value: {}".format(self.position,len(self.points),self.points[self.position]))

    def get_position(self,offset,mode=None,verbose=None):
        if mode is None: mode = self.mode
        if verbose is None: verbose = self.verbose
        pos = 0
        if mode == 0: # Absolute Position
            pos = offset % len(self.points)
            if verbose: print("Mode: ABSOLUTE, Val: {}, Pos: {}/{}".format(offset,pos,len(self.points)))
        elif mode == 1: # Relative Position
            pos = int((offset % 1)*len(self.points))
            if verbose: print("Mode: RELATIVE, Val: {}, Pos: {}/{}".format(offset,pos,len(self.points)))
        elif mode == 2: # Degree Position
            pos = int(((offset % 360) / 360)*len(self.points))
            if verbose: print("Mode: DEGREE, Val: {}, Pos: {}/{}".format(offset,pos,len(self.points)))
        elif mode == 3: # Radian Position
            pi2 = math.pi * 2
            pos = int(((offset % pi2) / pi2)*len(self.points))
            if verbose: print("Mode: RADIAN, Val: {}, Pos: {}/{}".format(offset,pos,len(self.points)))
        else:
            print("Unknown mode, returning position 0.")

        return pos

    def set_range(self,rng=1):
        if self.verbose: print("Setting Range:", rng)
        minv = self.points.min()
        maxv = self.points.max()
        current_range = maxv - minv
        for i in range(len(self.points)):
            self.points[i] = ((self.points[i]-minv)/current_range)*rng

    def shift(self,amount):
        if self.verbose: print("Shifting:", amount)
        for i in range(len(self.points)):
            self.points[i] = self.points[i] + amount

    def cat(self,osc,n=1):
        '''Concatenate current points with Oscillator/ndarray (osc) (n) times.'''
        
        for i in range(n):
            print(type(osc))
            if type(osc) is Oscillator:
                self.points = np.concatenate((self.points,osc.points),axis=0)
            if type(osc) is np.ndarray:
                self.points = np.concatenate((self.points,osc),axis=0)
        
        return self

    def step(self,amount=None):
        if amount is None:
            self.offset += self.step_size
            self.position = self.get_position(self.offset,self.mode)
        else:
            self.offset += amount
            self.position = self.get_position(self.offset,self.mode)

    def read(self):
        return self.points[self.position]

    # def draw(self,height=200,width=None,mode=0,ds=3,dt=1,pt_skip=1,transparent=False):
    def draw(self):
        '''
        Return an image of the oscillator at current position
        Draw Modes:
        0 - Pixel points
        1 - Connected Lines
        2 - Circles
        '''

        height = self.draw_h
        width = self.draw_w
        mode = self.draw_mode
        ds = self.draw_size
        dt = self.draw_thick
        c = self.draw_color
        ratio = width / len(self.points)
        img = np.zeros((height,width),dtype=np.float32)

        if self.draw_transparent:
            img = cv.cvtColor(img,cv.COLOR_GRAY2BGRA)
            img[:, :, 3] = 0
            color = (c[0],c[1],c[2],255)
        else:
            img = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
            color = (c[0],c[1],c[2])

        minv = self.points.min()
        maxv = self.points.max()
        abs_range = max(abs(minv),abs(maxv))
        scale = (height-((ds+abs(dt))*2))/2
        last_pt = None
        for i in range(0,len(self.points),self.draw_skip):
            idx = (self.position + i) % len(self.points)
            point = ((abs_range-self.points[idx])/abs_range)*scale
            point = min(height-1,point+ds)
            # point = int(max(0,point))
            point = int(point)

            xpos = int(i*ratio)
            if mode == 0: #Pixel Points
                img[point,xpos] = color
            if mode == 1: #Lines
                if last_pt is not None:
                    img = cv.line(img,last_pt,[xpos,point],color,dt)
                last_pt = [xpos,point]
            if mode == 2: #Circles
                img = cv.circle(img,[xpos,point],ds,color,dt)
        
        if mode == 1: # Draw final line segment
            point = ((abs_range-self.points[self.position])/abs_range)*scale
            point = [width,int(min(height-1,point+ds))]
            img = cv.line(img,last_pt,point,color,dt)

        
        # if width is not None:
        #     img = cv.resize(img,(width,height))
        # img = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
        self.draw_layer.im = img
        return img



if __name__ == "__main__":
    
    operations = [math.sin, math.cos,"/2"]
    operations = [math.sin]
    operations = [math.cosh,"/100",math.sin]
    osc = Oscillator(operations=operations,step=2,offset=90,mode=2,resolution=360,dtype=np.float16)
    # img = osc.draw(height=400,width=400)
    # osc.cat(osc.points)

    running = True
    while(running):
        osc.step()
        img = osc.draw()
        cv.imshow("Osc",img)
        k = cv.waitKey(33) & 0xFF
        if k == ord('w'):
            cv.waitKey(0)
        if k == ord('q'):
            running = not running
    # for i in range(40):
    #     osc.step()
    #     print("{}. Off:{} Pos:{}/{} Val:{}".format(i+1,osc.offset,osc.position,osc.resolution,osc.read()))
