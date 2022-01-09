import cv2 as cv
import os, sys, time
import math
import utils as ut
from playsound import playsound
from video_scrubber import ImageViewport
from layer import Layer
from oscillator import Oscillator
from textanimator import TextAnimator
from threading import Thread

# TODO
# Easy Layer Edit Mode (Move, Scale, Rotate, Export, Import, Add, Remove)
# Add border control mode (Change individual side widths)
# Viewport Control Options (Separate VPs for still and camera + controls)
# Add GIF support?
# Class for drawing patterns/grids/dots?

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


def filter_image(image,mode=0):
    if mode==0:
        filtered = cv.Canny(image,100,200)
        filtered = cv.cvtColor(filtered,cv.COLOR_GRAY2BGR)
    
    return filtered

if __name__ == "__main__":
    # CREATE VIDEO STREAMER OBJECT
    ip = "192.168.2.17"
    port = "4040"
    video_source = "tcp://"+ip+":"+port
    streamer = VideoStreamer(video_source)
    # streamer = VideoStreamer(1)
    streamer.start()
    cv.namedWindow("PiCam",cv.WINDOW_GUI_EXPANDED)
    # cv.namedWindow("PiCam",cv.WINDOW_AUTOSIZE)
    cv.setMouseCallback("PiCam", click_event)

    

    interlace = False
    interlace_skip = 60
    interlace_duration = 15
    interlace_color = (255,255,255)

    show_solid = False
    solid_start = 0
    solid_duration = 5
    solid_color = (255,255,255)

    shift_color = False
    shift_amount = 90

    # Gain / brightness? 

    noise_filtering = False
    # filter_selection = 0
    #Create filter list and controls to switch between them

    #Create Layer list/ import layer def file and controls
    draw_layers = True
    animate_layers = True
    layer_selection = 0
    im_file = "img/pneuma03-2.png"
    layer_img = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    im_layer = Layer(image=layer_img,im_file=im_file)
    im_layer.scale = 0.75
    # im_layer.set_rotation_hz(0.1/tail.scale)
    im_layer.translation = [266, 282]
    
    osc = Oscillator([math.sin],step=4,offset=0,resolution=360)
    osc.draw_mode = 1
    osc.draw_skip  = 12
    osc.draw_color = (0,0,240)
    osc.draw_thick = 5
    osc.draw_size = 5
    osc.draw_w = 1080
    osc.draw_h = 150
    # osc.cat(osc)
    osc2 = Oscillator([math.sin],step=8,offset=0,resolution=360)
    osc2.draw_mode = 1
    osc2.draw_skip  = 12
    osc2.draw_color = (180,0,0)
    osc2.draw_thick = 5
    osc2.draw_size = 5
    osc2.draw_w = 1080
    osc2.draw_h = 150
    osc2.position = osc2.get_position(30)
    osc2.cat(osc2)
    osc3 = Oscillator([math.sin],step=20,offset=0,resolution=90)
    osc3.draw_mode = 1
    osc3.draw_skip  = 12
    osc3.draw_color = (0,240,0)
    osc3.draw_thick = 5
    osc3.draw_size = 5
    osc3.draw_w = 1080
    osc3.draw_h = 150
    osc3.position = osc3.get_position(60)
    osc3.cat(osc3,3)

    
    osc.draw_layer.translation = [540, 750]
    osc2.draw_layer.translation = [540, 750]
    osc3.draw_layer.translation = [540, 900]

    ta_q = TextAnimator("?",font_size=128)
    ta_q.draw()
    t_layer = Layer(image = ta_q.image)
    t_layer.translation = [878, 676]
    t_layer.rotation = 45
    t_layer.scale = 2
    
    ta_i = TextAnimator("you",font_size=128)
    ta_i.draw()
    tl2 = Layer(image = ta_i.image)
    tl2.translation = [912, 754]
    tl2.rotation = -30
    tl2.scale = 1

    ta_am = TextAnimator("are",font_size=128)
    ta_am.draw()
    tl3 = Layer(image = ta_am.image)
    tl3.translation = [339, 780]
    tl3.rotation = 15
    tl3.scale = 1

    ta_who = TextAnimator("who",font_size=128)
    ta_who.draw()
    tl4 = Layer(image = ta_who.image)
    tl4.translation = [1009, 647]
    tl4.rotation = -20
    tl4.scale = 1

    # draw_list = [t_layer,tl2,tl3,tl4,osc2,osc]
    draw_list = [im_layer]

    #Add patterns? 

    #Border Attributes
    add_border = True
    border_edit_mode = False
    toggle_border_top = False
    toggle_border_bot = False
    toggle_border_left = False
    toggle_border_right = False
    # border_width = 40
    border_mode = 0
    border_color = (255,255,255)
    dtop = 46
    dbot = 38
    # dl = 0
    # dr = 0
    borders = [40,40,40,40]
    border_inc = 10

    #Implement ImageViewport
    use_viewport = False
    vp_zoom = 1.0
    vp_zoom_inc = 0.05
    vp_off = [0,0]
    vp = ImageViewport(vp_zoom,vp_off)

    # Freeze Frame
    frozen = False
    freeze_frame = None

    running = True
    sound = True
    recording = False
    recorder = None
    delay = 200 # adapt waitkey value based on processing time for smoother framerate
    frame_num = 0
    alpha = 0.5
    beta = 1.0 - alpha
    gamma = -20
    adj_bc = True
    brightness = 0
    contrast = 0.65

    # Fix Aspect Ratio
    aspect_ratio = 1# 4/3 #16/9 #1
    print("A/R: ",aspect_ratio)
    # ret, frame = cap.read() 
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
    (h, w) = frame.shape[:2]
    # MIGHT HAVE SOME WEIRD EFFECT
    # if frame.shape[0] < 1080:
        # print("Resizing")
    frame = cv.resize(frame,(int(1080*(w/h)),1080))
    (h, w) = frame.shape[:2]
    print("Before A/R: ",frame.shape)
    if aspect_ratio >= 1.0:
        new_w = min(int(h * aspect_ratio),w)
        new_h = h
        slice_w = (w//2)-(new_w//2)
        slice_h = (h//2)-(new_h//2)
    else:
        new_h = min(int(w * aspect_ratio),h)
        new_w = w
        slice_w = (w//2)-(new_w//2)
        slice_h = (h//2)-(new_h//2)
    frame = frame[slice_h:slice_h+new_h,slice_w:slice_w+new_w]
    
    (h, w) = frame.shape[:2]
    recorder_dim = (w,h)
    black_pad = (1920-w)//2
    white_frame = frame.copy()
    white_frame[:,:] = (255,255,255)
    white_frame = cv.copyMakeBorder(white_frame,0,0,black_pad,black_pad, cv.BORDER_CONSTANT, value=(0,0,0))
    black_frame = frame.copy()
    black_frame[:,:] = (0,0,0)
    black_frame = cv.copyMakeBorder(black_frame,0,0,black_pad,black_pad, cv.BORDER_CONSTANT, value=(0,0,0))
    print("After A/R: ",frame.shape)  
               
    while(running): 
        start_time = time.time()
        # ret, frame = cap.read() 
        frame = streamer.frame.copy()
        if frame.shape[0] < 1080:
            frame = cv.resize(frame,(int(1080*(w/h)),1080))
            (h, w) = frame.shape[:2]
        # Apply Aspect Ratio
        
        frame = frame[slice_h:slice_h+new_h,slice_w:slice_w+new_w]
        
        if mouse_changed:
            ut.get_pixels(frame,mouse_xy)
            mouse_xy = [mouse_xy[0]-black_pad,mouse_xy[1]]
            # if add_border:
            #     mouse_xy = [mouse_xy[0]-dl,mouse_xy[1]-dt]
            if draw_layers:
                if type(draw_list[layer_selection]) is Layer:
                    draw_list[layer_selection].translation = mouse_xy
                if type(draw_list[layer_selection]) is Oscillator:
                    draw_list[layer_selection].draw_layer.translation = mouse_xy
                print("Moved Layer to ",mouse_xy)
            else:
                vp_x = int(vp_off[0]+vp_zoom*(mouse_xy[0]-(w/2)))
                vp_y = int(vp_off[1]+vp_zoom*(mouse_xy[1]-(h/2)))
                vp_off = [vp_x,vp_y]
                vp.offset = vp_off
            mouse_changed = False

        if noise_filtering:
            frame = cv.fastNlMeansDenoisingColored(frame,None,10,10,7,7)

        if use_viewport:
            frame = vp.view(frame)
            vp_off = vp.offset
        
        if frozen:
            frame = cv.addWeighted(frame, alpha, freeze_frame, beta, gamma)

        if shift_color:
            frame = ut.shift_color_space(frame,shift_amount,0)
    
        # if use_viewport:
        #     frame = vp.view(frame)
        #     vp_off = vp.offset

        if draw_layers:
            if len(draw_list) > 0:
                        a_frame = cv.cvtColor(frame, cv.COLOR_RGB2RGBA)
                        a_frame[:, :, 3] = 255
            for x in draw_list:
                if type(x) is Layer:
                    frame = x.draw_on(a_frame)
                    if animate_layers:
                        x.step() 
                if type(x) is Oscillator:
                    x.draw()
                    x.draw_layer.draw_on(a_frame)
                    if animate_layers:
                        x.step()


               
        

        if add_border:
            adj = []
            adj.append((0 if toggle_border_top else borders[0])+dtop)
            adj.append((0 if toggle_border_bot else borders[1])+dbot)
            adj.append(0 if toggle_border_left else borders[2])
            adj.append(0 if toggle_border_right else borders[3])
            frame = ut.add_border(frame,0,border_mode,border_color,adj=adj)
        
        if interlace and frame_num % interlace_skip <= interlace_duration:
            frame[:,:] = interlace_color

        if show_solid:
            if solid_start + solid_duration > frame_num:
                frame[:,:] = solid_color
            else:
                show_solid = False

        # Adjust Brightness & Contrast
        if adj_bc:
            frame = cv.convertScaleAbs(frame,alpha=contrast,beta=brightness)


        frame_num += 1

        

        # Pad Frame
        # black_pad = (1920-w)//2
        frame = cv.copyMakeBorder(frame,0,0,black_pad,black_pad, cv.BORDER_CONSTANT, value=(0,0,0))


        cv.imshow('PiCam', frame) 

        if recording and recorder is not None:
            if frame.shape[2] == 4:
                frame = frame[:,:,:-1]
            frame = frame[dtop:-dbot,black_pad:black_pad+w]
            frame = cv.resize(frame,recorder_dim)
            # print("writing frame size ", frame.shape)
            recorder.write(frame)
        
        # LOOP TIMER -----------------------------------------------------------
        loop_time = int((time.time() - start_time)*1000)
        if loop_time > delay:
            print("WARNING Frame Time: {}ms - Desired Delay: {}ms".format(loop_time,delay))
        real_delay = max(1,delay-loop_time)



        # KEYBOARD CONTROLS -----------------------------------------------------
        # k = cv.waitKey(delay) & 0xFF
        k = cv.waitKey(real_delay) & 0xFF
        if k != 255: print(k)
        if k == ord('i'): # Freeze Frame NO FLASH
            if not frozen:
                freeze_frame = streamer.frame.copy()
                freeze_frame = freeze_frame[slice_h:slice_h+new_h,slice_w:slice_w+new_w]
            frozen = not frozen
        if k == ord('o'): # Freeze Frame WITH FLASH
            if not frozen:
                cv.imshow('PiCam',white_frame)
                for i in range(5):
                    print("Grabbing frame")
                    cv.waitKey(200)
                    freeze_frame = streamer.frame.copy()
                freeze_frame = freeze_frame[slice_h:slice_h+new_h,slice_w:slice_w+new_w]
            frozen = not frozen
        if k == ord('['): # Decrease Freeze Blend Alpha   
            alpha = max(0.0, alpha - 0.05)
            beta = 1.0 - alpha
        if k == ord(']'): # Increase Freeze Blend Alpha
            alpha = min(1.0, alpha + 0.05)
            beta = 1.0 - alpha
        if k == ord('7'): # Decrease Freeze Blend Gamma   
            gamma -= 2
        if k == ord('8'): # Increase Freeze Blend Gamma
            gamma += 2
        if k == ord('p'): # TOGGLE COLOR SHIFT
            shift_color = not shift_color
            print("Color Shift "+("ENABLED"if shift_color else "DISABLED"))
        if k == ord('9'): # Decrease color shift
            shift_amount -= 5
        if k == ord('0'): # Increase color shift
            shift_amount += 5

        # LAYER CONTROLS
        if k == ord('t'): # TOGGLE LAYERS
            draw_layers = not draw_layers
            print("Layers "+("ENABLED"if draw_layers else "DISABLED"))
            if draw_layers:
                for l in draw_list:
                    print(l)
        if k == ord('y'): # TOGGLE LAYER ANIMATE
            animate_layers = not animate_layers
            print("Layer Animate "+("ENABLED"if animate_layers else "DISABLED"))
        if k == ord('3'): # LAST LAYER
            layer_selection = (layer_selection-1) % len(draw_list)
            print("Layer Selection:",layer_selection)
        if k == ord('4'): # NEXT LAYER
            layer_selection = (layer_selection+1) % len(draw_list)
            print("Layer Selection:",layer_selection)

        # BORDER CONTROLS
        if k == ord('b'): # TOGGLE BORDER
            add_border = not add_border
            print("Border "+("ENABLED"if add_border else "DISABLED"))
        if k == ord('n'): # DECREASE BORDER WIDTH
            for i in range(len(borders)):
                borders[i] = max(0, borders[i] - border_inc)
        if k == ord('m'): # INCREASE BORDER WIDTH
            for i in range(len(borders)):
                borders[i] = borders[i] + border_inc
        if k == ord(','): # CHANGE BORDER MODE
            border_mode = (border_mode + 1) % 2 
        if k == ord('.'): # TOGGLE BORDER EDIT MODE
            border_edit_mode = not border_edit_mode
            print("Border Edit Mode "+("ENABLED"if border_edit_mode else "DISABLED"))

        # BRIGHTNESS/CONTRAST CONTROLS
        if k == ord('g'): # TOGGLE B/C
            adj_bc = not adj_bc
            print("Brightness/Contrast "+("ENABLED"if adj_bc else "DISABLED"))
            if adj_bc:
                print("Brightness: {}, Contrast:{}".format(brightness,contrast))
        if k == ord('h'): # BRIGHTNESS DOWN
            brightness = ut.constrain(brightness-2,0,100)
        if k == ord('j'): # BRIGHTNESS UP
            brightness = ut.constrain(brightness+2,0,100)
        if k == ord('k'): # CONTRAST DOWN
            contrast = ut.constrain(contrast-0.05,0,3.0)
        if k == ord('l'): # CONTRAST UP
            contrast = ut.constrain(contrast+0.05,0,3.0)

        # FILTER CONTROLS
        if k == ord('f'): # TOGGLE FILTER
            noise_filtering = not noise_filtering
            print("Noise Filtering "+("ENABLED"if noise_filtering else "DISABLED"))

        # VIEWPORT CONTROLS
        if k == ord('v'): # TOGGLE VIEWPORT
            use_viewport = not use_viewport
            print("Viewport "+("ENABLED"if use_viewport else "DISABLED"))
        if k == ord('x'): # VIEWPORT ZOOM OUT
            vp_zoom += vp_zoom_inc
            vp_zoom = vp.set_scale(vp_zoom)
            print("Zoom: ",round(vp_zoom,2))
        if k == ord('c'): # VIEWPORT ZOOM IN
            vp_zoom -= vp_zoom_inc
            vp_zoom = vp.set_scale(vp_zoom)
            print("Zoom: ",round(vp_zoom,2))
        dvp = 25
        if k == ord('w'): # TOGGLE TOP BORDER / MOVE VP UP
            if border_edit_mode:
                toggle_border_top = not toggle_border_top
            else:
                vp.offset[1] = vp.offset[1] - max(1,dvp*vp_zoom)
        if k == ord('s'): # TOGGLE BOTTOM BORDER / MOVE VP DOWN
            if border_edit_mode:
                toggle_border_bot = not toggle_border_bot
            else:
                vp.offset[1] = vp.offset[1] + max(1,dvp*vp_zoom)
        if k == ord('a'): # TOGGLE LEFT BORDER / MOVE VP LEFT
            if border_edit_mode:
                toggle_border_left = not toggle_border_left
            else:
                vp.offset[0] = vp.offset[0] - max(1,dvp*vp_zoom)
        if k == ord('d'): # TOGGLE RIGHT BORDER / MOVE VP RIGHT
            if border_edit_mode:
                toggle_border_right = not toggle_border_right
            else:
                vp.offset[0] = vp.offset[0] + max(1,dvp*vp_zoom)
        
        # MEDIA OUTPUT
        if k == ord('1'): # SAVE IMAGE
            label = "projector"
            if sound: playsound("sound/low.mp3", block = False)
            filename = ut.generate_filename(label)
            x2 = black_pad + w # -( 2*border_width)
            frame = frame[dtop:-dbot,black_pad:x2]
            cv.imwrite("projects/projector/"+filename,frame)
            print("Saved "+filename)
            print("SHAPE:",frame.shape)
        if k == ord('2'): # TOGGLE VIDEO RECORDING
            recording = not recording
            print("Recording "+("STARTED"if recording else "STOPPED"))
            if recording:
                if sound: playsound("sound/high.mp3", block = False)
                record_start_time = time.time()
                video_file = "projects/projector/"+ut.generate_filename("recording", '.avi')
                recorder = cv.VideoWriter(video_file, cv.VideoWriter_fourcc(*'MJPG'), 30, (w, h))
                recorder_dim = (w,h)
                print("Recorder created, ",h,w)
            else:
                if sound: playsound("sound/mid.mp3", block = False)
                total_time = time.time() - record_start_time
                print("Time: ",round(total_time,2))
                recorder.release()
            
        # QUIT
        if k == ord('q'): 
            streamer.stop()
            running = False

# cap.release() 
cv.destroyAllWindows() 
print("Finished.")