import cv2 as cv
from layer import Layer
from random import randint
import oscillator as osc
from oscillator import Oscillator
import math

origin = [400,200]

# WLKRZ ------------------------------------------------------------------------
wlkrz_file = "img/wlkrz2.png"
wlkrz_img = cv.imread(wlkrz_file,cv.IMREAD_UNCHANGED)
wlkrz = Layer(image=wlkrz_img,im_file=wlkrz_file)
wlkrz.translation = origin
wlkrz.name = "1"

wlkrz_file = "img/wlkrz.png"
wlkrz_img = cv.imread(wlkrz_file,cv.IMREAD_UNCHANGED)
wlkrz2 = Layer(image=wlkrz_img,im_file=wlkrz_file)
wlkrz2.translation = origin
wlkrz2.name = "2"

wlkrz_set = [wlkrz2, wlkrz]

# BAG --------------------------------------------------------------------------
bag_file = "img/bag1.png"
bag_img = cv.imread(bag_file,cv.IMREAD_UNCHANGED)
bag1 = Layer(image=bag_img,im_file=bag_file)
bag1.translation = origin
bag1.name = "1"

bag_file = "img/bag2.png"
bag_img = cv.imread(bag_file,cv.IMREAD_UNCHANGED)
bag2 = Layer(image=bag_img,im_file=bag_file)
bag2.translation = origin
bag2.name = "2"

bag_set = [bag2, bag1]

# ALREADY DEAD -----------------------------------------------------------------
ad_file = "img/already_dead1.png"
ad_img = cv.imread(ad_file,cv.IMREAD_UNCHANGED)
ad1 = Layer(image=ad_img,im_file=ad_file)
ad1.translation = origin
ad1.name = "1"

ad_file = "img/already_dead2.png"
ad_img = cv.imread(ad_file,cv.IMREAD_UNCHANGED)
ad2 = Layer(image=ad_img,im_file=ad_file)
ad2.translation = origin
ad2.name = "2"

ad_set = [ad2, ad1]

# LOBBY ------------------------------------------------------------------------
lobby_file = "img/lobby2.jpg"
lobby_img = cv.imread(lobby_file,cv.IMREAD_UNCHANGED)
lobby = Layer(image=lobby_img,im_file=lobby_file)
lobby.translation = [800,500]
lobby.name = "lobby"

lobby_set = [lobby]




# Add sets of layers to this list, access this list in streamer
layer_sets = [wlkrz_set, bag_set, ad_set]
