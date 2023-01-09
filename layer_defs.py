import cv2 as cv
from layer import Layer
from random import randint
import oscillator as osc
from oscillator import Oscillator
import math

origin = [400,200]

wlkrz_file = "img/wlkrz2.png"
wlkrz_img = cv.imread(wlkrz_file,cv.IMREAD_UNCHANGED)
wlkrz = Layer(image=wlkrz_img,im_file=wlkrz_file)
wlkrz.translation = origin
wlkrz.scale = 0.8
wlkrz.name = "1"
# wlkrz.dt = [randint(-5,5),randint(-5,5)]
# wlkrz.scale = 1.0

wlkrz_file = "img/wlkrz.png"
wlkrz_img = cv.imread(wlkrz_file,cv.IMREAD_UNCHANGED)
wlkrz2 = Layer(image=wlkrz_img,im_file=wlkrz_file)
wlkrz2.translation = origin
wlkrz2.scale = 1.2
wlkrz2.name = "2"
# wlkrz2.dt = [randint(-5,5),randint(-5,5)]

# wlkrz_set = dict()
# wlkrz_set["1"] = wlkrz
# wlkrz_set["2"] = wlkrz2
wlkrz_set = [wlkrz, wlkrz2]

lobby_file = "img/lobby2.jpg"
lobby_img = cv.imread(lobby_file,cv.IMREAD_UNCHANGED)
lobby = Layer(image=lobby_img,im_file=lobby_file)
lobby.translation = [800,500]
lobby.name = "lobby"

lobby_set = [lobby]


#Meeting XY oscillators
osc_origin = [str(origin[0]),str(origin[1])]
osc_range = ["600","600"]
# x_osc = Oscillator([math.sin,"+1","/2","*"+osc_range[0],"+"+osc_origin[0]],4,270,2)
# print(x_osc.points)
# y_osc = Oscillator([math.sin,"+1","/2","*"+osc_range[1],"+"+osc_origin[1]],4,270,2)
# print(y_osc.points)


print("\n\n\n\n\n\n\n")

x_osc1, y_osc1 = osc.create_XY_oscillators([400,200],[1000,200])
x_osc2, y_osc2 = osc.create_XY_oscillators([400,200],[400,800])

# Add sets of layers to this list, access this list in streamer
layer_sets = [lobby_set, wlkrz_set]

def pick_location(xbound=[400,1000],ybound=[200,800]):
    xcoord = randint(xbound[0],xbound[1])
    ycoord = randint(ybound[0],ybound[1])
    print("Location chosen",[xcoord,ycoord])
    return [xcoord,ycoord]
