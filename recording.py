import time
import cv2 as cv
import utils as ut
from path import Path
from layer import Layer
from clockanimator import ClockAnimator

def frame_info(current,total,dt,t_sum):
    t_avg = round(t_sum / (current + 1),2)
    to_finish = int((total - current + 1) / t_avg)# // 100
    if to_finish > 120:
        to_finish = to_finish//60
        print("Frame {}/{} - T: {}s \tAvg: {}s \tRemaining: {} min".format(current,total,str(round(dt,2)),t_avg,to_finish))
    else:
        print("Frame {}/{} - T: {}s \tAvg: {}s \tRemaining: {} sec".format(current,total,str(round(dt,2)),t_avg,to_finish))


def extract_frame(background,draw_list,frames,name="frame",fps=30,window="Layers"):
    frame = 0

    while frame < frames:
        print("Frame",frame)
        frame += 1
        for x in draw_list:
            if type(x) is Layer:
                x.step()
            elif type(x) is Path:
                x.step()
            elif type(x) is ClockAnimator:
                x.step()
            else:
                print(type(x))
                print(x)
    
    bkg = background.copy()
    for x in draw_list:
            if type(x) is Layer:
                x.draw_on(bkg)
            elif type(x) is Path:
                bkg = x.draw_on(bkg)
            elif type(x) is ClockAnimator:
                bkg = x.draw_on(bkg,c=(0,0,0,255))
            else:
                # print("Unknown draw object type")
                print(type(x))
                print(x)
    file_name = ut.generate_filename(name)
    cv.imwrite(file_name,bkg)
    print("Frame extracted.")


def record_on_img(background,draw_list,seconds,name="recording",fps=30,window="Layers"):
    cv.namedWindow(window,cv.WINDOW_AUTOSIZE)
    (h, w) = background.shape[:2]
    recorder = cv.VideoWriter(ut.generate_filename(name, '.avi'), cv.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
    frame = 0
    end_frame = int(seconds * fps)

    t = time.time()
    t_sum = 0
    while frame < end_frame:
        bkg = background.copy()
        
        for x in draw_list:
            if type(x) is Layer:
                # print("Drawing Layer")
                x.draw_on(bkg)
                x.step()
            elif type(x) is Path:
                # print("Drawing Path")
                bkg = x.draw_on(bkg)
                x.step()
            elif type(x) is ClockAnimator:
                # print("Drawking ClockAnimator")
                bkg = x.draw_on(bkg,c=(0,0,0,255))
                x.step()
            else:
                # print("Unknown draw object type")
                print(type(x))
                print(x)
        cv.imshow(window,bkg)
        recorder.write(bkg[:,:,:-1])
        # if window is not None:
        

        frame = frame + 1  
        nt = time.time()
        dt = nt - t
        t = nt
        t_sum += dt
        frame_info(frame,end_frame,dt,t_sum)

    print("Done writing.")
    recorder.release()

def record_on_video(video_file,draw_list,name="recording",fps=30,window="Layers"):
    cv.namedWindow(window,cv.WINDOW_AUTOSIZE)
    print("Opening\n",video_file)
    reader = cv.VideoCapture(video_file) 
    # (h, w) = background.shape[:2]
    (h, w) = (int(reader.get(cv.CAP_PROP_FRAME_HEIGHT)),int(reader.get(cv.CAP_PROP_FRAME_WIDTH)))
    print(h,w)
    print("Saving as")
    recorder = cv.VideoWriter(ut.generate_filename(name, '.avi'), cv.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
    end_frame = int(reader.get(cv.CAP_PROP_FRAME_COUNT))
    print("Writing over {} frames".format(end_frame))
    
    
    recorder = cv.VideoWriter(ut.generate_filename(name, '.avi'), cv.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
    frame = 0

    t = time.time()
    t_sum = 0
    while frame < end_frame:
        _, bkg = reader.read()
        bkg = cv.cvtColor(bkg, cv.COLOR_RGB2RGBA)
        bkg[:, :, 3] = 255
        
        for x in draw_list:
            if type(x) is Layer:
                # print("Drawing Layer")
                x.draw_on(bkg)
                x.step()
            elif type(x) is Path:
                # print("Drawing Path")
                bkg = x.draw_on(bkg)
                x.step()
            elif type(x) is ClockAnimator:
                # print("Drawking ClockAnimator")
                bkg = x.draw_on(bkg,c=(0,0,0,255))
                x.step()
            else:
                print("Unknown draw object type")
                print(type(x))
                print(x)

        recorder.write(bkg[:,:,:-1])
        if window is not None:
            cv.imshow(window,bkg)

        frame = frame + 1  
        nt = time.time()
        dt = nt - t
        t = nt
        t_sum += dt
        frame_info(frame,end_frame,dt,t_sum)

    print("Done writing.")
    recorder.release()

# def record_layers(background_image,layers,seconds,name="recording",fps=30,window="Layers"):
#     video_files = [".avi"]
#     print("Given",background[-4:])
#     (h, w) = background_image.shape[:2]
#     recorder = cv.VideoWriter(ut.generate_filename(name, '.avi'), cv.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
#     frame = 0
#     end_frame = int(seconds * fps)

#     # Modify layers before animating
#     # im_file = "img/tail5.png"
#     # for l in layers:
#     #     l.load_image(im_file)
#     #     l.set_rotation_hz(1/(l.scale*20))

#     #Custom soul draw
#     p1 = Path([[578, 405], [596, 407], [614, 406], [625, 408], [641, 404], [654, 404], [668, 400], [682, 395], [688, 389], [703, 385], [712, 378], [712, 369], [714, 364], [711, 358]],hz=0.3,color=(255,255,255,255),w_size=2)
#     p1.deg_offset(180)
#     p1.speed = 5
#     p2 = Path([[582, 406], [601, 405], [614, 408], [625, 405], [639, 407], [656, 401], [671, 400], [681, 392], [692, 390], [702, 382], [714, 374], [712, 364], [715, 360], [711, 355]],hz=0.3,w_size=2)
#     p2.speed = 5

#     t = time.time()
#     t_sum = 0
#     while frame < end_frame:
#         bkg = background.copy()
#         # for l in layers:
#         #     l.draw_on(bkg)
#         #     l.step()

#         #Custom soul draw
#         layers[0].draw_on(bkg)
#         layers[0].step()
        
#         bkg = p2.draw_on(bkg)
#         p2.step()
#         layers[1].draw_on(bkg)
#         layers[1].step()
#         bkg = p1.draw_on(bkg)
#         p1.step()


#         recorder.write(bkg[:,:,:-1])
#         if window is not None:
#             cv.imshow(window,bkg)
#         frame = frame + 1  
#         nt = time.time()
#         dt = nt - t
#         t = nt
#         t_sum += dt
#         frame_info(frame,end_frame,dt,t_sum)
#         # if frame % 5 == 0:
#         # print("Frame {}/{} - {}s".format(frame,end_frame,str(round(dt,2))))

#     print("Done writing.")
#     recorder.release()

# def record_layers_over_video(video_file,layers,name="overlay",fps=30,window="Layers"):
#     print("Opening\n",video_file)
#     reader = cv.VideoCapture(video_file) 
#     print("Saving as")
#     recorder = cv.VideoWriter(ut.generate_filename(name, '.avi'), cv.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
#     frame_count = 0
#     end_frame = reader.get(cv.CAP_PROP_FRAME_COUNT)
#     print("Writing over {} frames".format(end_frame))
    
#     # Modify layers before animating
#     for l in layers:
#         if type(l) is Layer: print("YES")
#         pass

#     t = time.time()
#     t_sum = 0
#     while frame_count < end_frame:
#         ret, frame = reader.read()
#         print(frame.shape)
#         frame_count += 1

#         # bkg = background.copy()
#         frame = cv.cvtColor(frame, cv.COLOR_RGB2RGBA)
#         frame[:, :, 3] = 255
#         print(frame.shape)
#         for l in layers:
#             frame = l.draw_on(frame)
#             l.step()
#         recorder.write(frame[:,:,:-1]) 
#         if window is not None:
#             cv.imshow(window,frame)
#         nt = time.time()
#         dt = nt - t
#         t = nt
#         t_sum += dt
#         frame_info(frame_count,end_frame,dt,t_sum)
#         # if frame % 5 == 0:
#         # print("Frame {}/{} - {}s".format(frame_count,end_frame,str(round(dt,2))))

#     print("Done writing.")
#     recorder.release()


# def record_clocks(background_image,clocks,seconds,name="recording",fps=30,window="Layers"):
#     (h, w) = background_image.shape[:2]
#     recorder = cv.VideoWriter(ut.generate_filename(name, '.avi'), cv.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
#     frame = 0
#     end_frame = int(seconds * fps)

#     # Modify layers before animating
#     for c in clocks:
#         c.layer.set_rotation_hz(1/(c.layer.scale*20))
#     # clock.layer.set_rotation_hz(1)

#     t = time.time()
#     t_sum = 0
#     while frame < end_frame:
#         bkg = background.copy()
#         for c in clocks:
#             bkg = c.draw_on(bkg,c=(0,0,0,255))
#             c.step()
#         recorder.write(bkg[:,:,:-1])
#         if window is not None:
#             cv.imshow(window,bkg)
#         frame = frame + 1  
#         nt = time.time()
#         dt = nt - t
        
#         t = nt
#         t_sum += dt
#         frame_info(frame,end_frame,dt,t_sum)
        
#     print("Done writing.")
#     recorder.release()

# def record_clocks_over_video(video_file,clocks,name="overlay",fps=30,window="Layers"):
#     reader = cv.VideoCapture(video_file) 
#     recorder = cv.VideoWriter(ut.generate_filename(name, '.avi'), cv.VideoWriter_fourcc(*'MJPG'), fps, (w, h))
#     frame_count = 0
#     end_frame = reader.get(cv.CAP_PROP_FRAME_COUNT)
    
#     # Modify layers before animating
#     for c in clocks:
#         c.layer.set_rotation_hz(1/(c.layer.scale*20))
#     # clock.layer.set_rotation_hz(1)

#     t = time.time()
#     t_sum = 0
#     while frame_count < end_frame:
#         ret, frame = reader.read()
#         frame_count += 1

#         # bkg = background.copy()
#         frame = cv.cvtColor(frame, cv.COLOR_RGB2RGBA)
#         frame[:, :, 3] = 255
#         for c in clocks:
#             frame = c.draw_on(frame,c=(0,0,0,255))
#             c.step()
#         recorder.write(frame[:,:,:-1]) 
#         if window is not None:
#             cv.imshow(window,frame)
#         nt = time.time()
#         dt = nt - t
#         t = nt
#         t_sum += dt
#         frame_info(frame_count,end_frame,dt,t_sum)
#         # if frame % 5 == 0:
#         # print("Frame {}/{} - {}s".format(frame_count,end_frame,str(round(dt,2))))

#     print("Done writing.")
#     recorder.release()