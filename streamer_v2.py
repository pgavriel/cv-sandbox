import cv2 as cv
import os, sys, time, traceback
from threading import Thread
from filterchain import FilterChain

class VideoStreamer:
    '''
    Handles an OpenCV VideoCapture object opened from (source), running in a separate thread.
    '''
    def __init__(self, source=1, frame=None):
        self.capture = cv.VideoCapture(source)
        if not self.capture.isOpened():
            print("Cannot open camera")
            exit()
        self.frame = frame
        self.status = None
        self.stopped = False
        self.start_time = None
        pass

    def read(self):
        while not self.stopped:
            self.status, self.frame = self.capture.read()
            # print(self.frame.shape)
            if self.frame is None:
                self.stop()
                print("Video Streamer stopped, no frame.")
        self.capture.release()

    def start(self):
        Thread(target = self.read, args=()).start()
        self.start_time = time.time()

    def stop(self):
        self.stopped = True


mouse_xy = [0,0]
mouse_changed = False
def click_event(event,x,y,flags,param):
    global mouse_xy,mouse_changed
    if event == cv.EVENT_LBUTTONUP:
        mouse_xy = [x,y]
        print("Mouse Clicked: ",mouse_xy)
        mouse_changed = True


if __name__ == "__main__":
    # Start video streamer and wait for frames
    streamer = VideoStreamer(0)
    streamer.start()
    frame = streamer.frame
    while frame is None:
        try:
            frame = streamer.frame.copy()
        except:
            pass
        cv.waitKey(25)
        if time.time() - streamer.start_time > 5:
            print("Timed out.")
            sys.exit()
            break

    # Setup cv window and mouse callback
    cv.namedWindow("Streamer",cv.WINDOW_GUI_EXPANDED)
    # cv.namedWindow("PiCam",cv.WINDOW_AUTOSIZE)
    cv.setMouseCallback("Streamer", click_event)


    chain = FilterChain()

    delay = 250 #ms
    running = True
    mode = 1
    try:
        while(running):
            start_time = time.time()

            # AQUIRE FRAME ---------------------------------------------------------
            frame = streamer.frame.copy()

            # PROCESS FRAME --------------------------------------------------------
            chain.process(frame)
            cv.imshow("Streamer",chain.output)

            # LOOP TIMER -----------------------------------------------------------
            loop_time = int((time.time() - start_time)*1000)
            if loop_time > delay:
                print("WARNING Frame Time: {}ms - Desired Delay: {}ms".format(loop_time,delay))
            real_delay = max(1,delay-loop_time)

            # HANLE CONTROLS -------------------------------------------------------
            k = cv.waitKey(real_delay) & 0xFF
            k = chr(k)
            print(k)
            # QUIT -------------------------------------------------------
            if k == ord('q') or k == 'q':
                streamer.stop()
                running = False
            if k.isnumeric():
                mode = int(k)
                print("Mode: {}".format(mode))


    except BaseException as e:
        print("Something went wrong.")
        print(traceback.format_exc())

    finally:
        streamer.stop()
        cv.destroyAllWindows()
        print("Finished.")
