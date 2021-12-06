import cv2 as cv
import numpy as np
import utils as ut
import time
import os
from os.path import isfile, join
from clockanimator import ClockAnimator
from path import Path
from layer import Layer



def check(lbl=None):
    show_checks = False
    if show_checks:
        if lbl is None: print(" > > > Check.")
        else: print(" > > > Check. - {}".format(lbl))


mouse_xy = [0,0]
mouse_changed = False
def click_event(event,x,y,flags,param):
    global mouse_xy,mouse_changed
    if event == cv.EVENT_LBUTTONUP:
        mouse_xy = [x,y]
        mouse_changed = True
    pass

def import_layers(layer_file):
    layers = []
    print("Importing "+str(layer_file)+" ...")
    try:
        f = open(layer_file,"r")
        lines = f.readlines()
        # lines = lines[1:]
        for line in lines:
            d = line.split(',')
            img = cv.imread(d[0],cv.IMREAD_UNCHANGED)
            layer = Layer(image=img,im_file=d[0])
            layer.origin = [int(d[1]),int(d[2])]
            layer.translation = [int(d[3]),int(d[4])]
            layer.dt = [int(d[5]),int(d[6])]
            layer.rotation = float(d[7])
            layer.dr = float(d[8])
            layer.scale = float(d[9])
            layer.ds = float(d[10])
            layer.padding_scale = float(d[11])

            layers.append(layer)
        print("Imported Layers: ",len(layers))
    except:
        print("LAYER IMPORT FAILED")
    return layers


# im_file, ox, oy, tx, ty, dtx, dty, r, dr, scale, ds, pad_scale
def export_layers(layers,out_file):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    export_file = os.path.join(dir_path,out_file)
    print("Export File: ",export_file)
    
    f = open(export_file,"w+")
    # f.write(self.im_file[:-4]+"\n")
    for l in layers:
        write_str = l.im_file+","+str(l.origin[0])+","+str(l.origin[1])+","+str(l.translation[0])+","+str(l.translation[1])
        write_str = write_str+","+str(l.dt[0])+","+str(l.dt[1])+","+str(l.rotation)+","+str(l.dr)+","+str(l.scale)+","+str(l.ds)
        write_str = write_str+","+str(l.padding_scale)+"\n"
        f.write(write_str)
    f.close()
    print("LAYERS EXPORTED TO " + out_file)

def record(background_image,layers,seconds,name="recording",fps=30):
    (h, w) = background_image.shape[:2]
    recorder = cv.VideoWriter(ut.generate_filename(name, '.avi'), cv.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
    frame = 0
    end_frame = int(seconds * fps)

    # Modify layers before animating
    im_file = "img/tail5.png"
    for l in layers:
        l.load_image(im_file)
        l.set_rotation_hz(1/(l.scale*20))

    t = time.time()
    while frame < end_frame:
        bkg = background.copy()
        for l in layers:
            l.draw_on(bkg)
            l.update()
        recorder.write(bkg[:,:,:-1])
        frame = frame + 1  
        nt = time.time()
        dt = nt - t
        t = nt
        # if frame % 5 == 0:
        print("Frame {}/{} - {}s".format(frame,end_frame,str(round(dt,2))))

    print("Done writing.")
    recorder.release()

def record_clocks(background_image,clocks,seconds,name="recording",fps=30):
    (h, w) = background_image.shape[:2]
    recorder = cv.VideoWriter(ut.generate_filename(name, '.avi'), cv.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
    frame = 0
    end_frame = int(seconds * fps)

    # Modify layers before animating
    for c in clocks:
        c.layer.set_rotation_hz(1/(c.layer.scale*20))
    # clock.layer.set_rotation_hz(1)

    t = time.time()
    while frame < end_frame:
        bkg = background.copy()
        for c in clocks:
            bkg = c.draw_on(bkg,c=(0,0,0,255))
            c.step()
        recorder.write(bkg[:,:,:-1])
        frame = frame + 1  
        nt = time.time()
        dt = nt - t
        t = nt
        # if frame % 5 == 0:
        print("Frame {}/{} - {}s".format(frame,end_frame,str(round(dt,2))))

    print("Done writing.")
    recorder.release()

def record_clocks_over_video(video_file,clocks,name="overlay",fps=30):
    reader = cv.VideoCapture(video_file) 
    
    
    recorder = cv.VideoWriter(ut.generate_filename(name, '.avi'), cv.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
    frame_count = 0
    end_frame = reader.get(cv.CAP_PROP_FRAME_COUNT)
    
    # Modify layers before animating
    for c in clocks:
        c.layer.set_rotation_hz(1/(c.layer.scale*20))
    # clock.layer.set_rotation_hz(1)

    t = time.time()
    while frame_count < end_frame:
        ret, frame = reader.read()
        frame_count += 1

        # bkg = background.copy()
        frame = cv.cvtColor(frame, cv.COLOR_RGB2RGBA)
        frame[:, :, 3] = 255
        for c in clocks:
            frame = c.draw_on(frame,c=(0,0,0,255))
            c.step()
        recorder.write(frame[:,:,:-1]) 
        nt = time.time()
        dt = nt - t
        t = nt
        # if frame % 5 == 0:
        print("Frame {}/{} - {}s".format(frame_count,end_frame,str(round(dt,2))))

    print("Done writing.")
    recorder.release()


if __name__ == "__main__":
    #CV Window and Trackbars
    cv.namedWindow("Layers",cv.WINDOW_AUTOSIZE)
    cv.setMouseCallback("Layers", click_event)

    # background = cv.imread("img/cleanup3.png",cv.IMREAD_UNCHANGED)
    background = cv.imread("clock_ref.png",cv.IMREAD_UNCHANGED)
    background = ut.scale_image(background,25)
    print("Background Shape: ",background.shape)

    l_imgs = []
    im_file = "img/tail5.png"
    spinner = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    # spinner = ut.scale_image(spinner,25)
    
    l_imgs.append([spinner, im_file])
    i_select = 0

    (h, w) = background.shape[:2]
    l1 = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
    l1.set_rotation_hz(1.0)
    l1.scale = 0.5
    l1.translation = [w//2, h//2]
    layers = [l1]
    layers = []
    layer_selection = 0

    clocks = []
    
    import clock_def
    clocks = clock_def.clocks_a

    running = True
    keep_updating = False
    redraw = True
    delay = 10 #ms (33=30fps)
    t_inc = 1
    while running:
        # bkg = background.copy()
        # print("select: ",layer_selection)
        if mouse_changed:
            layers[layer_selection].translation = mouse_xy
            mouse_changed = False

        if redraw:
            bkg = background.copy()
            counter = 0
            for l in layers:
                if counter != layer_selection:
                    if keep_updating: l.update()
                    l.draw_on(bkg)
                counter = counter + 1
            for c in clocks:
                bkg = c.draw_on(bkg)
                c.step()
            redraw = False
        
        saved_bkg = bkg.copy()
        if len(layers) > 0:
            if keep_updating: layers[layer_selection].update()
            layers[layer_selection].draw_on(saved_bkg)

        show_overlay = True
        if show_overlay and len(layers) > 0:
            cv.circle(saved_bkg,layers[layer_selection].translation,3,(0,0,255,100),-1)
        cv.imshow("Layers",saved_bkg)

        k = cv.waitKey(delay) & 0xFF
        if k == ord('1'):
            layer_selection = (layer_selection - 1) % len(layers)
            redraw = True
            print("Layer",layer_selection+1)
        if k == ord('2'):
            layer_selection = (layer_selection + 1) % len(layers)
            redraw = True
            print("Layer",layer_selection+1)
        if k == ord('3'):
            layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
            layers.append(layer)
            layer_selection = len(layers) - 1
            redraw = True
        if k == ord('w'): # Move Up 
            layers[layer_selection].translation[1] = layers[layer_selection].translation[1] - t_inc
        if k == ord('s'): # Move Down
            layers[layer_selection].translation[1] = layers[layer_selection].translation[1] + t_inc
        if k == ord('a'): # Move Left
            layers[layer_selection].translation[0] = layers[layer_selection].translation[0] - t_inc
        if k == ord('d'): # Move Right
            layers[layer_selection].translation[0] = layers[layer_selection].translation[0] + t_inc
        if k == ord('r'): # Increase Scale
            layers[layer_selection].scale = layers[layer_selection].scale + (layers[layer_selection].scale*0.05)
            layers[layer_selection].set_rotation_hz(1/layers[layer_selection].scale)
        if k == ord('f'): # Decrease Scale
            layers[layer_selection].scale = layers[layer_selection].scale - (layers[layer_selection].scale*0.05)
            layers[layer_selection].set_rotation_hz(1/layers[layer_selection].scale)
        if k == ord('t'):
            layers[layer_selection].rotation = layers[layer_selection].rotation + 45
        if k == ord('g'):
            layers[layer_selection].rotation = layers[layer_selection].rotation - 45
        if k == ord('e'):
            layers[layer_selection].set_rotation_hz(1/layers[layer_selection].scale)
        # if k == ord('z'):
        #     layers = import_layers("layers.csv")
        #     redraw = True
        # if k == ord('x'):
        #     export_layers(layers,"layers.csv")
        if k == ord('p'):
            cv.waitKey(0)
        if k == ord('l'): # Record animation
            # record(background,layers,2)
            record_clocks(background,clocks,5)
        if k == ord('k'): # Record animation
            # record(background,layers,5)
            record_clocks_over_video("recording-12-5-21--23-43-55.avi",clocks)
        if k == ord('o'):
            counter = 1
            print("LAYERS")
            for l in layers:
                print(counter,"-",l)
                counter = counter + 1
        if k == ord('q'):
            running = False
            counter = 1
            print("\nLAYERS")
            for l in layers:
                print(counter,"-",l)
                counter = counter + 1
        
