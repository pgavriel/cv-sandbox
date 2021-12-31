import cv2 as cv
import numpy as np
import utils as ut
import time
import os, sys
from os.path import isfile, join

sys.path.append(".\\projects\\machina")
print (sys.path)
from clockanimator import ClockAnimator
from path import Path
from layer import Layer
from recording import record_on_img, record_on_video, extract_frame


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


if __name__ == "__main__":
    #CV Window and Trackbars
    cv.namedWindow("Layers",cv.WINDOW_AUTOSIZE)
    cv.setMouseCallback("Layers", click_event)

    im_file = "img/layer1.png"
    background = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    # background = ut.scale_image(background,25)
    print("Background Shape: ",background.shape)

    l_imgs = []
    i_select = 0
    im_file = "img/chest1.png"
    img1 = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    l_imgs.append([img1, im_file])
    im_file = "img/chest2.png"
    img2 = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    l_imgs.append([img2, im_file])
    

    (h, w) = background.shape[:2]
    layer_selection = 0

    im_file = "img/bench.png"
    img1 = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    # img1 = ut.scale_image(img1,25)
    bench = Layer(image=img1,im_file=im_file)
    bench.translation = [w//2, h//2]
    im_file = "img/components.png"
    img1 = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    # img1 = ut.scale_image(img1,25)
    components = Layer(image=img1,im_file=im_file)
    components.translation = [w//2, h//2]
    im_file = "img/bench_components.png"
    img1 = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    # img1 = ut.scale_image(img1,25)
    bench_components = Layer(image=img1,im_file=im_file)
    bench_components.translation = [w//2, h//2]
    im_file = "img/soul.png"
    img1 = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    # img1 = ut.scale_image(img1,25)
    soul = Layer(image=img1,im_file=im_file)
    soul.translation = [w//2, h//2]
    im_file = "img/soul_hand2.png"
    img1 = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    # img1 = ut.scale_image(img1,25)
    soul_hand = Layer(image=img1,im_file=im_file)
    soul_hand.translation = [w//2, h//2]
    im_file = "img/chest1.png"
    img1 = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    chest1 = Layer(image=img1,im_file=im_file)
    chest1.translation = [579*4, 405*4]
    chest1.scale = 0.27738957312183404*4
    chest1.set_rotation_hz(0.2)
    im_file = "img/chest2.png"
    img1 = cv.imread(im_file,cv.IMREAD_UNCHANGED)
    chest2 = Layer(image=img1,im_file=im_file)
    chest2.translation = [636*4, 387*4]
    chest2.scale = 0.2503440897424552*4

    # SOUL RENDER
    # import floor_path_def as fp
    # draw_list += [soul,chest1,fp.soul_paths[1],chest2,fp.soul_paths[0],soul_hand]

    # FULL RENDER SETUP
    import floor_path_def as fp
    import clock_def
    draw_list = clock_def.clocks_a + clock_def.clocks_b +clock_def.clocks_c + clock_def.clocks_d + clock_def.clocks_e
    for c in draw_list:
        c.layer.set_rotation_hz(1/(c.layer.scale*40))
    draw_list += fp.rear_chipset
    draw_list += fp.chip3
    draw_list.append(bench)
    draw_list += fp.chip1
    draw_list += fp.chip2
    draw_list += fp.chip3_extra

    draw_list += fp.random1 + fp.random2 + fp.random3 + fp.random4
    draw_list.append(components)
    draw_list.append(bench_components)

    draw_list += [soul,chest1,fp.soul_paths[1],chest2,fp.soul_paths[0],soul_hand]
    for d in draw_list:
        if type(d) is Path:
            d.scale(4)
            d.w_size = 8
        if type(d) is ClockAnimator:
            paths = []
            for p in d.paths:
                # x = p
                p.scale(4)
                # paths.append(x)
            # d.paths = paths
            d.layer.scale_layer(4)
    # draw_list = []

    running = True
    keep_updating = False
    redraw = True
    delay = 10 #ms (33=30fps)
    t_inc = 1
    while running:
        # bkg = background.copy()
        # print("select: ",layer_selection)
        if mouse_changed:
            draw_list[layer_selection].translation = mouse_xy
            mouse_changed = False

        if redraw:
            print("Redraw")
            bkg = background.copy()
            counter = 0
            types_list = []
            for x in draw_list:
                # if counter == layer_selection:
                #     counter += 1
                #     continue
                counter += 1
                if type(x) is Layer:
                    types_list.append("Layer")
                    # print("Drawing Layer")
                    x.draw_on(bkg)
                    if keep_updating: x.step()
                elif type(x) is Path:
                    types_list.append("Path")
                    # print("Drawing Path")
                    bkg = x.draw_on(bkg)
                    if keep_updating: x.step()
                elif type(x) is ClockAnimator:
                    types_list.append("ClockAnimator")
                    # print("Drawking ClockAnimator")
                    bkg = x.draw_on(bkg,c=(0,0,0,255))
                    if keep_updating: x.step()
                else:
                    types_list.append("Unknown")
                    print("Unknown draw object type")
                    print(type(x))
                    print(x)
                
            print(types_list)
            redraw = False
        
        # saved_bkg = bkg.copy()
        # if len(draw_list) > 0:
        #     if keep_updating: draw_list[layer_selection].step()
        #     saved_bkg = draw_list[layer_selection].draw_on(saved_bkg)

        show_overlay = True
        if show_overlay and len(draw_list) > 0:
            if type(draw_list[layer_selection]) is Layer:
                cv.circle(saved_bkg,draw_list[layer_selection].translation,3,(0,0,255,100),-1)
        
        # cv.imshow("Layers",saved_bkg)
        cv.imshow("Layers",bkg)

        k = cv.waitKey(delay) & 0xFF
        if k == ord('1'):
            layer_selection = (layer_selection - 1) % len(draw_list)
            redraw = True
            print("Layer",layer_selection+1)
        if k == ord('2'):
            layer_selection = (layer_selection + 1) % len(draw_list)
            redraw = True
            print("Layer",layer_selection+1)
        if k == ord('3'):
            layer = Layer(image=l_imgs[i_select][0],im_file=l_imgs[i_select][1])
            draw_list.append(layer)
            layer_selection = len(draw_list) - 1
            redraw = True
        if k == ord('w'): # Move Up 
            draw_list[layer_selection].translation[1] = draw_list[layer_selection].translation[1] - t_inc
        if k == ord('s'): # Move Down
            draw_list[layer_selection].translation[1] = draw_list[layer_selection].translation[1] + t_inc
        if k == ord('a'): # Move Left
            draw_list[layer_selection].translation[0] = draw_list[layer_selection].translation[0] - t_inc
        if k == ord('d'): # Move Right
            draw_list[layer_selection].translation[0] = draw_list[layer_selection].translation[0] + t_inc
        if k == ord('r'): # Increase Scale
            draw_list[layer_selection].scale = draw_list[layer_selection].scale + (draw_list[layer_selection].scale*0.05)
            draw_list[layer_selection].set_rotation_hz(1/draw_list[layer_selection].scale)
        if k == ord('f'): # Decrease Scale
            draw_list[layer_selection].scale = draw_list[layer_selection].scale - (draw_list[layer_selection].scale*0.05)
            draw_list[layer_selection].set_rotation_hz(1/draw_list[layer_selection].scale)
        if k == ord('t'):
            draw_list[layer_selection].rotation = draw_list[layer_selection].rotation + 45
        if k == ord('g'):
            draw_list[layer_selection].rotation = draw_list[layer_selection].rotation - 45
        if k == ord('e'):
            draw_list[layer_selection].set_rotation_hz(1/draw_list[layer_selection].scale)
        # if k == ord('z'):
        #     layers = import_layers("layers.csv")
        #     redraw = True
        # if k == ord('x'):
        #     export_layers(layers,"layers.csv")
        if k == ord('p'):
            cv.waitKey(0)
        if k == ord('l'): # Record animation
            # record_layers(background,layers,15)
            # record_clocks(background,clocks,60)
            record_on_img(background,draw_list,60,name="v4renderfinal")
            running = False
        if k == ord('k'): # Record animation
            # record(background,layers,5)
            # record_clocks_over_video("recording-12-5-21--23-43-55.avi",clocks)
            # record_layers_over_video("render0.avi",layers)
            video_file = "v2render_background.avi"
            record_on_video(video_file,draw_list,name=video_file[:-4])
            running = False
        if k == ord('j'):
            extract_frame(background,draw_list,250)
            extract_frame(background,draw_list,251)
            running = False
        if k == ord('o'):
            counter = 1
            print("LAYERS")
            for l in draw_list:
                print(counter,"-",l)
                counter = counter + 1
        if k == ord('q'):
            running = False
            counter = 1
            print("\nLAYERS")
            for l in draw_list:
                print(counter,"-",l)
                counter = counter + 1
        
