import cv2 as cv
import utils as ut
import numpy as np
import math
from layer import Layer
from path import Path

#Custom animator class for machina vivit drawing
class ClockAnimator:
    def __init__(self,layer,paths=None):
        self.layer = layer

        if paths is None:
            self.paths = []
        else:
            self.paths = paths

    def step(self):
        self.layer.update()
        r = self.layer.rotation
        pad = self.layer.dr / 2
        for p in self.paths:
            p.step()
            # print("R-PAD",r-pad,"TRIGGER",p.trigger,"R+PAD",r+pad)
            if r-pad <= p.trigger < r+pad:
                p.spawn_walker()
        pass

    def draw_on(self,image,c=(0,0,255,255)):
        img = image.copy()

        # Draw Layer
        self.layer.draw_on(img)

        # Draw Paths
        for p in self.paths:
            img = p.draw_on(img,c)
        
        return img

    def export(self):
        pass