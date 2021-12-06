import cv2
import numpy as np
import os
import time
from PIL import Image
from datetime import datetime


def scale_image(image, percent):
    width = int(image.shape[1] * percent / 100)
    height = int(image.shape[0] * percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized


def generate_filename(label, filetype='.jpg'):
    dt = datetime.now()
    date_str = str(dt.month) + '-' + str(dt.day) + '-' + str(dt.year - 2000)
    time_str = str(dt.hour) + '-' + str(dt.minute) + '-' + str(dt.second)
    file = label + '-' + date_str + '--' + time_str + filetype
    print(file)
    return file


def write_sequence(seq, step_size=0.1, loop=3, label="sequence", fps=30):
    w, h = seq[0].shape[1], seq[0].shape[0]
    recorder = cv2.VideoWriter(generate_filename(label, '.avi'), cv2.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
    frame = np.zeros((w, h, 3))

    for img in seq:
        print(img.shape)
    steps = int(1 / step_size)
    num_frames = loop * len(seq) * steps
    for l in range(0, loop):
        for i in range(0, len(seq)):
            pos = 0
            for s in range(0, steps):
                if i == 0:
                    frame = cv2.addWeighted(seq[-1], 1 - pos, seq[i], pos, 0)
                else:
                    frame = cv2.addWeighted(seq[i - 1], 1 - pos, seq[i], pos, 0)
                pos = pos + step_size
                recorder.write(frame)
                print("Frame written {}-{}-{} / {}".format(l + 1, i + 1, s + 1, num_frames))

    print("Done writing.")
    recorder.release()


def write_thresh_seq(image, step=5, type=cv2.THRESH_BINARY, loop=2, reverse=True, label="thresh", fps=30):
    w, h = image.shape[1], image.shape[0]
    recorder = cv2.VideoWriter(generate_filename(label, '.avi'), cv2.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
    frame = image.copy()
    steps = int(255 / step)
    pos = 0
    for l in range(0, loop):
        for i in range(0, steps):
            print(i, pos)
            ret, frame = cv2.threshold(image, pos, 255, type)
            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
            pos = pos + step
            recorder.write(frame)
        if reverse:
            pos = 255
            for i in range(0, steps):
                print(i, pos)
                ret, frame = cv2.threshold(image, pos, 255, type)
                frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
                pos = pos - step
                recorder.write(frame)

    print("Done writing.")
    recorder.release()

def color_space(image):
    #Assumes image is BGR
    # BGR is default image
    BGR = image
    b, g, r = cv2.split(BGR)
    BRG = cv2.merge((b, r, g))
    RBG = cv2.merge((r, b, g))
    RGB = cv2.merge((r, g, b))
    GRB = cv2.merge((g, r, b))
    GBR = cv2.merge((g, b, r))

    seq = [BGR,BRG,RBG,RGB,GRB,GBR,BGR]

    write_sequence(seq, step_size=0.02, loop=1, fps=15, label="colorspace")
    pass


def nightmare(img_name):
    d = cv2.imread('{}.jpg'.format(img_name))
    d0 = cv2.imread('{}_vgg-conv_0_000000.jpg'.format(img_name))
    d1 = cv2.imread('{}_vgg-conv_1_000000.jpg'.format(img_name))
    d2 = cv2.imread('{}_vgg-conv_2_000000.jpg'.format(img_name))
    d3 = cv2.imread('{}_vgg-conv_3_000000.jpg'.format(img_name))
    d4 = cv2.imread('{}_vgg-conv_4_000000.jpg'.format(img_name))
    d5 = cv2.imread('{}_vgg-conv_5_000000.jpg'.format(img_name))
    d6 = cv2.imread('{}_vgg-conv_6_000000.jpg'.format(img_name))
    d7 = cv2.imread('{}_vgg-conv_7_000000.jpg'.format(img_name))
    d8 = cv2.imread('{}_vgg-conv_8_000000.jpg'.format(img_name))
    d9 = cv2.imread('{}_vgg-conv_9_000000.jpg'.format(img_name))
    d10 = cv2.imread('{}_vgg-conv_10_000000.jpg'.format(img_name))
    d11 = cv2.imread('{}_vgg-conv_11_000000.jpg'.format(img_name))
    d12 = cv2.imread('{}_vgg-conv_12_000000.jpg'.format(img_name))
    d13 = cv2.imread('{}_vgg-conv_13_000000.jpg'.format(img_name))
    d14 = cv2.imread('{}_vgg-conv_14_000000.jpg'.format(img_name))
    d15 = cv2.imread('{}_vgg-conv_15_000000.jpg'.format(img_name))
    d16 = cv2.imread('{}_vgg-conv_16_000000.jpg'.format(img_name))
    d17 = cv2.imread('{}_vgg-conv_17_000000.jpg'.format(img_name))

    # All frames
    # seq = [d0, d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, d13, d14, d15, d16, d17, d]
    # seq = [d,d,d4,d6,d7,d8,d9,d10,d11,d17,d]
    seq = [d11, d]

    # FAST
    write_sequence(seq, step_size=0.1, loop=5, fps=60, label=img_name)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    os.chdir('M:/Pictures/cv-sandbox')
    label = "test"

    frame = cv2.imread('panther.jpeg')
    # w, h = frame.shape[1], frame.shape[0]

    #color_space(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img = Image.fromarray(frame)
    img.save('panth.png')

    # cv2.imshow('frame', frame)

    key = cv2.waitKey(0) & 0xFF
    if key == ord('q'):
        print('Quitting...')
    cv2.destroyAllWindows()
