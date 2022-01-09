import cv2 as cv
from layer import Layer

im_file = "img/tail6.png"
layer_img = cv.imread(im_file,cv.IMREAD_UNCHANGED)
tail = Layer(layer_img,im_file)
tail.set_rotation_hz(0.25)
tail.scale(0.5)
tail.translation = [720,540]