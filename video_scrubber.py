import cv2 as cv
import utils as ut

class ImageViewport:
    def __init__(self,scale=1.0,offset=[0,0]):
        self.scale = max(min(scale,1.0),0.05)
        self.offset = offset
        self.size = None
        # self.size = (1000,1000)
        # self.interpolation = cv.INTER_NEAREST
        self.interpolation = cv.INTER_CUBIC

    def set_scale(self,scale=1.0):
        self.scale = max(min(scale,1.0),0.05)
        return self.scale

    def view(self,image):
        (h, w) = image.shape[:2]
        vph = int(h * self.scale)
        vpw = int(w * self.scale)
        x_off = int(self.offset[0])
        y_off = int(self.offset[1])
        if x_off+vpw >= w:
            x_off = x_off - (x_off+vpw - w)
        if x_off < 0:
            x_off = 0
        if y_off+vph >= h:
            y_off = y_off - (y_off+vph - h)
        if y_off < 0:
            y_off = 0
        
        self.offset = [x_off,y_off]
        crop = image[y_off:vph+y_off,x_off:vpw+x_off,:]

        if self.size is None:
            scaled = cv.resize(crop, (w,h), interpolation=self.interpolation)
        else:
            scaled = cv.resize(crop, self.size, interpolation=self.interpolation)

        return scaled

mouse_xy = [0,0]
mouse_changed = False
def click_event(event,x,y,flags,param):
    global mouse_xy,mouse_changed
    if event == cv.EVENT_LBUTTONUP:
        mouse_xy = [x,y]
        mouse_changed = True


if __name__ == "__main__":
    #CV Window and Trackbars
    cv.namedWindow("Video Scrubber",cv.WINDOW_AUTOSIZE)
    cv.setMouseCallback("Video Scrubber", click_event)

    video_file = 'projects/projector/recording-12-31-21--16-32-47.avi'
    reader = cv.VideoCapture(video_file) 
    
    (h, w) = (int(reader.get(cv.CAP_PROP_FRAME_HEIGHT)),int(reader.get(cv.CAP_PROP_FRAME_WIDTH)))
    end_frame = int(reader.get(cv.CAP_PROP_FRAME_COUNT))
    print(h,w)
    frame_counter = 0
    frame_skip = 1

    scale = 1
    # scale = 1.0
    scale_inc = 0.05
    offset = [0,0]
    # offset = [0,0]
    offset_inc = 100
    viewer = ImageViewport(scale,offset)

    running = True
    playing = True
    delay = 33 #ms (33=30fps)
    while running:
        reader.set(cv.CAP_PROP_POS_FRAMES, frame_counter)
        _, img = reader.read()
        (h, w) = img.shape[:2]
        if playing:
            frame_counter = (frame_counter + frame_skip) % end_frame
        
        if mouse_changed:
            old = offset
            offset = [old[0]-(w//2-mouse_xy[0]),old[1]-(h//2-mouse_xy[1])]
            offset = [max(offset[0],0),max(offset[1],0)]
            offset = [min(offset[0],w-(w*scale)),min(offset[1],h-(h*scale))]
            print("Old: {} \t New: {} \t Mousexy: {}".format(old,offset,mouse_xy))
            viewer = ImageViewport(scale,offset)
            mouse_changed = False


        img = viewer.view(img)

        cv.imshow("Video Scrubber",img)
        # print("Frame Skip: {} \tCurrent:{}/{}".format(frame_skip,frame_counter,end_frame))
        k = cv.waitKey(delay) & 0xFF
        if k == ord('1'): # Decrease Frame Skip 
            frame_skip = max(frame_skip-1,1)
        if k == ord('2'): # Increase Frame Skip
            frame_skip = min(frame_skip+1,end_frame//2)
        if k == ord('3'): # Decrease scale
            scale = max(scale-scale_inc,0.05)
            viewer = ImageViewport(scale,offset)
        if k == ord('4'): # Increase scale
            scale = min(scale+scale_inc,1.0)
            viewer = ImageViewport(scale,offset)
        if k == ord('w'): # Move Up 
            playing = not playing
        if k == ord('a'): # Move Down
            frame_counter = (frame_counter - frame_skip) % end_frame
        if k == ord('d'): # Move Left
            frame_counter = (frame_counter + frame_skip) % end_frame
        if k == ord('s'): # Save
            save_dir = "projects/projector/"
            file_name = ut.generate_filename("cap",".png")
            cv.imwrite(save_dir+file_name,img)
        if k == ord('i'): # Move Up view
            offset = [offset[0],offset[1]-offset_inc]
            viewer = ImageViewport(scale,offset)
        if k == ord('j'): # Move left view
            offset = [offset[0]-offset_inc,offset[1]]
            viewer = ImageViewport(scale,offset)
        if k == ord('k'): # Move Down view
            offset = [offset[0],offset[1]+offset_inc]
            viewer = ImageViewport(scale,offset)
        if k == ord('l'): # Move right view
            offset = [offset[0]+offset_inc,offset[1]]
            viewer = ImageViewport(scale,offset)
        if k == ord('q'): # Move Right
            running = False
            