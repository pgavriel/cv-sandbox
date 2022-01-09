import cv2 as cv
import numpy as np
import math
import os
import time
from PIL import Image
from datetime import datetime

def generate_filename(label, filetype='.jpg'):
    dt = datetime.now()
    date_str = str(dt.month) + '-' + str(dt.day) + '-' + str(dt.year - 2000)
    time_str = str(dt.hour) + '-' + str(dt.minute) + '-' + str(dt.second)
    file = label + '-' + date_str + '--' + time_str + filetype
    print(file)
    return file

def constrain(n, minn, maxn):
    return max(min(maxn, n), minn)

def draw_textline(image,string,org=[5,30],scale=1.0,c=(0,0,0),c2=(255,255,255),t=2,border=True):
    font = cv.FONT_HERSHEY_PLAIN
    if border: image = cv.putText(image,string,org,font,scale,c2,t+1,cv.LINE_AA)
    image = cv.putText(image,string,org,font,scale,c,t,cv.LINE_AA)

def scale_image(image, percent,interp=cv.INTER_CUBIC):
    width = int(image.shape[1] * percent / 100)
    height = int(image.shape[0] * percent / 100)
    dim = (width, height)
    resized = cv.resize(image, dim, interpolation=interp)
    return resized

def add_border(image, width, mode=1, color=(255,255,255), adj=[0,0,0,0], fixed_img_size=True, interp=cv.INTER_CUBIC):
    """Adds a border to an image of specified width.   
    MODES:   
    0 - Solid Border (use color parameter to specify color)    
    1 - Reflect Border (gfedcb|abcdefgh|gfedcba)  
    2 - Extend Border (aaaaa|abcdefgh|hhhhh)   
    fixed_img_size will resize the image to it's original dimensions after adding border.  
    """
    (h, w) = image.shape[:2]
    if mode == 0: # SOLID COLOR
        bordered = cv.copyMakeBorder(image, width+adj[0], width+adj[1], width+adj[2], width+adj[3], cv.BORDER_CONSTANT, value=color)
    elif mode == 1: # REFLECT BORDER
        bordered = cv.copyMakeBorder(image, width+adj[0], width+adj[1], width+adj[2], width+adj[3], cv.BORDER_REFLECT101)
    elif mode == 2: # EXTEND BORDER
        bordered = cv.copyMakeBorder(image, width+adj[0], width+adj[1], width+adj[2], width+adj[3], cv.BORDER_REPLICATE)
    else:
        print("Unknown border mode.")
        return image
    
    if fixed_img_size:
        bordered = cv.resize(bordered, (w,h), interpolation=interp)

    return bordered

def calculateDistance(x1,y1,x2,y2,precision=1):
    dist = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    dist = round(dist,precision)
    return dist

def angle_between_points(p1, p2):
    dx = p2[0] - p1[0]
    dy = p1[1] - p2[1]

    # if dx == 0:
    #     if dy == 0:  # same points?
    #         return 0
    #     else:
    #         dx = 0.00001

    deg = math.degrees(math.atan2(dy,dx))
    if deg < 0: deg = 360+deg
    return deg

def colorFader(c1,c2,mix=0): #fade (linear interpolate) from color c1 (at mix=0) to c2 (mix=1)
    c1=np.array(c1)
    c2=np.array(c2)
    new_color = (1-mix)*c1 + mix*c2
    return new_color

def shift_color_space(image,amount,sat_boost=0,cvt_back=True):
    img = cv.cvtColor(image,cv.COLOR_BGR2HSV)
    h, s, v = cv.split(img)
    h[:] = (h[:] + amount) % 180
    s[:] = s[:]+sat_boost #if s[:]+sat_boost <= 255 else 255
    img = cv.merge((h,s,v))
    if cvt_back: img = cv.cvtColor(img,cv.COLOR_HSV2BGR)
    return img

def get_pixels(image,pos,h=1,w=1,verbose=True):
    roi = image[pos[0]-w:pos[0]+w,pos[1]-h:pos[1]+h]
    if verbose: print(roi)
    return roi


def rotate(origin, point, angle):
    '''
    Rotate a point counterclockwise by a given angle around a given origin. 
    The angle should be given in radians.'''
    ox, oy = origin
    px, py = point

    qx = ox + math.cos(angle) * (px - ox) - math.sin(angle) * (py - oy)
    qy = oy + math.sin(angle) * (px - ox) + math.cos(angle) * (py - oy)
    return qx, qy