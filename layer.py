import cv2 as cv
import numpy as np
import utils as ut
import time
import os
from os.path import isfile, join

class Layer:
    def __init__(self,size=[500,500],image=None,im_file=None):
        pass
        if image is None:
            self.im = np.zeros((size[0],size[1],4))
        else:
            self.im = image
        self.im_file = im_file
        self.origin = [0,0]
        self.translation = [200,200]
        self.dt = [0,0]
        self.rotation = 0
        self.dr = 0
        self.scale = 1.0
        self.ds = 0
        self.add_padding = True
        self.padding_scale = 1.05
        self.fps = 30
    
    def __str__(self):
        s = "Im_file: "+self.im_file+"  Shape: "+str(self.im.shape)+"\n"
        s = s + "Origin: "+str(self.origin)+"  Translate: "+str(self.translation)+"  DT: "+str(self.dt)+"\n"
        s = s + "Rotation: "+str(self.rotation)+"  DR: "+str(self.dr)+" ||  Scale: "+str(self.scale)+"  DS: "+str(self.ds)+"\n" 
        return s

    def update(self):
        self.translation = [self.translation[0]+self.dt[0],self.translation[1]+self.dt[1]]
        self.rotation = (self.rotation + self.dr) % 360
        self.scale = self.scale + self.ds

    def load_image(self,im_file):
        self.im = cv.imread(im_file,cv.IMREAD_UNCHANGED)
        self.im_file = im_file

    def set_rotation_hz(self, hz):
        self.dr = hz * (360 / self.fps)

    def draw_on(self,image):
        debug = False
        if debug: print("Drawing...")
        current_layer = self.im.copy()
        if debug: print("Original H,W: ",current_layer.shape[:2])
        
        # Pad Border
        if self.add_padding: 
            top = int((self.padding_scale  * self.scale * 0.25 * self.im.shape[0]))  # shape[0] = rows
            bottom = top
            left = int((self.padding_scale * self.scale * 0.25 * self.im.shape[1]))  # shape[1] = cols
            right = left
            borderType = cv.BORDER_CONSTANT
            value = [0,0,0,0]
            current_layer = cv.copyMakeBorder(current_layer, top, bottom, left, right, borderType, None, value)
            if debug: print("Padded H,W: ",current_layer.shape[:2])
     
        #Get layer image properties
        (h, w) = current_layer.shape[:2]
        if debug: print("H,W: ",current_layer.shape[:2])
        (cX, cY) = (w // 2, h // 2)
        if debug: print("cx, cy: ",cX, cY)

        #Apply Rotation/Scale transform on layer image
        rot_mat = cv.getRotationMatrix2D((cX, cY), -self.rotation, self.scale)
        current_layer = cv.warpAffine(current_layer, rot_mat, current_layer.shape[1::-1], flags=cv.INTER_LINEAR)
          
        #Draw Center
        draw_center = [self.origin[0]+self.translation[0], self.origin[1]+self.translation[1]]
        
        # Handle X border conditions
        x1 = draw_center[0]-cX # X Left Border
        if x1 < 0: 
            self.check("x1 < 0")
            off = 0 - x1
            current_layer = current_layer[:,off:,:]
            x1 = x1 + off
        x2 = draw_center[0]+cX # X Right Border
        if w % 2 != 0: x2 = x2 + 1; self.check("w %2 != 0")
        if x2 > image.shape[1]: 
            self.check("x2 > shape 1")
            off = image.shape[1] - x2
            current_layer = current_layer[:,:off,:]
            x2 = x2 + off
        
        # Handle Y border conditions
        y1 = draw_center[1]-cY # Y Top Border
        if y1 < 0: 
            self.check("y1 < 0")
            off = 0 - y1
            current_layer = current_layer[off:,:,:]
            y1 = y1 + off
        y2 = draw_center[1]+cY # Y Bottom Border
        if h % 2 != 0: y2 = y2 + 1; self.check("h %2 != 0")
        if y2 > image.shape[0]: 
            self.check("y2 > shape 1")
            off = image.shape[0] - y2
            current_layer = current_layer[:off,:,:]
            y2 = y2 + off
       
        if debug: print("x1:",x1,"  x2:",x2,"  y1:",y1,"  y2:",y2)
        if debug: print("x:",x2-x1,"  y:",y2-y1)
        
        # Place layer onto image
        image_crop = image[y1:y2, x1:x2,:]
        # normalize alpha channels from 0-255 to 0-1
        alpha_bg = image_crop[:,:,3] / 255.0
        alpha_fg = current_layer[:,:,3] / 255.0

        if debug: print("\ncurrent_layer", current_layer.shape)
        if debug: print("image_crop", image_crop.shape)
        # set adjusted colors
        for color in range(0, 3):
            image_crop[:,:,color] = alpha_fg * current_layer[:,:,color] + \
                alpha_bg * image_crop[:,:,color] * (1 - alpha_fg)

        # set adjusted alpha and denormalize back to 0-255
        image_crop[:,:,3] = (1 - (1 - alpha_fg) * (1 - alpha_bg)) * 255

        image[y1:y2,x1:x2,:] = image_crop

    def check(self,lbl=None):
        show_checks = False
        if show_checks:
            if lbl is None: print(" > > > Check.")
            else: print(" > > > Check. - {}".format(lbl))


