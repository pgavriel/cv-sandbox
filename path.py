import cv2 as cv
import utils as ut
import numpy as np
import math

class Path:
    def __init__(self,points=None,trigger=0,hz=0.0,color=(0,0,0,255),w_size=10):
        if points is not None:
            self.points = points
        else:
            self.points = []

        self.frame = 0
        self.fps = 30
        self.freq = hz
        self.rot = 0
        self.dr = 0
        self.set_rotation_hz(hz)
        
        # self.speed = 5
        self.speed = 4
        self.color = color
        self.walkers = []
        self.w_size = w_size
        self.trigger = trigger
        self.update_path()

    def scale(self,factor):
        new_points = []
        for p in self.points:
            new_points.append([p[0]*factor,p[1]*factor])
        self.points = new_points
        self.update_path()


    def clear(self):
        self.points = []
        self.walkers = []
        self.update_path()

    def deg_offset(self,deg_off):
        self.rot = (self.rot + deg_off) % 360
        # spawn_freq = (self.fps/self.freq)
        # frame_off = deg_off * (spawn_freq/360)
        
        # self.frame += int(frame_off)

    def set_rotation_hz(self, hz):
        self.dr = hz * (360 / self.fps)

    def add_point(self,point):
        self.points.append(point)
        print("pts",self.points)
        self.update_path()

    def move_point(self,x,y,pos=None):
        if pos is None:
            pos = len(self.points)-1
        p = self.points[pos]
        self.points[pos] = [p[0]+x, p[1]+y]

    def set_points(self,points_list):
        self.points = points_list
        print("pts",self.points)
        self.update_path()

    def update_path(self):
        self.seg_len = []
        self.seg_angle = []
        if len(self.points) <= 1:
            pass
        else:
            p1 = self.points[0]
            for p in self.points:
                if p == p1: continue
                dist = ut.calculateDistance(p1[0],p1[1],p[0],p[1],2)
                ang = ut.angle_between_points(p1,p)
                self.seg_len.append(round(dist,2))
                self.seg_angle.append(ang)
                p1 = p
        # print("LEN",self.seg_len)
        # print("ANG",self.seg_angle)

    def spawn_walker(self):
        if len(self.points) < 2:
            print("Not enough points to spawn walker.")
        else:
            self.walkers.append([self.points[0][0],self.points[0][1],0,0])

    def step(self):
        total_len = sum(self.seg_len)
        # print(self.seg_len)
        # print("Total len:",total_len)
        # print(self.seg_angle)
        # print("\n\n")

        new_walkers = []
        for w in self.walkers:
            # Update all walkers positions
            # print("W",w)
            w[2] = w[2] + self.speed
            #Find position on path
            to_travel = w[2]
            counter = 0
            for seg in self.seg_len:
                if to_travel - seg > 0:
                    to_travel -= seg
                    # print("Seg {} passed, to travel: {}".format(seg,to_travel))
                else:
                    w[3] = counter # Segment walker is currently on
                    ang = self.seg_angle[counter] 
                    origin = self.points[counter]
                    w[0] = int(origin[0] + (to_travel * math.cos(math.radians(ang))))
                    w[1] = int(origin[1] + (to_travel * -math.sin(math.radians(ang))))
                    break
                counter += 1

            if w[2] < total_len: 
                new_walkers.append(w)
            else:
                pass
                # print("Path length exceeded, removing walker\n")
        self.walkers = new_walkers

        last_rot = self.rot
        self.rot = (self.rot + self.dr) % 360
        # print("last",last_rot,"  rot",self.rot,"  dr",self.dr)
        if self.dr > 0 and self.rot < last_rot:
            self.spawn_walker()
        if self.dr < 0 and self.rot > last_rot:
            self.spawn_walker()
        # add_walker = int(self.fps/self.freq)
        # print("add at ",add_walker,"  mod ",self.frame % add_walker)
        # if self.frame % add_walker == 0 and len(self.points) > 1:
            # self.walkers.append([self.points[0][0],self.points[0][1],0,0])
        
        # print("frame",self.frame,"   walkers ",self.walkers)
        self.frame += 1


    def draw_on(self,image,c=None,render_line=True,width=1):
        if len(self.points) == 0:
            return image

        if c is None:
            c = self.color
        img = image.copy()
        # print(self.points)
        if len(self.points) == 1:
            cv.circle(img,self.points[0],2,c,-1)
        else:
            p1 = self.points[0]
            for p in self.points:
                if render_line:
                    cv.line(img,p1,p,c,width)
                p1 = p
            for w in self.walkers:
                cv.circle(img,[w[0],w[1]],self.w_size,c,-1,cv.LINE_AA)
        return img
        
    

mouse_xy = [0,0]
mouse_changed = False
def click_event(event,x,y,flags,param):
    global mouse_xy,mouse_changed
    if event == cv.EVENT_LBUTTONUP:
        mouse_xy = [x,y]
        mouse_changed = True


def print_path_list(path_list):
    print_str = "["
    c = 1
    for p in path_list:
        print_str += str(p.points)
        if c < len(path_list):
            print_str += ","
        c += 1
    print_str += "]"
    print("Copy String:")
    print(print_str)
    return print_str

if __name__ == "__main__":
    #CV Window and Trackbars
    cv.namedWindow("Path Test",cv.WINDOW_AUTOSIZE)
    cv.setMouseCallback("Path Test", click_event)

    video_file = 'render2.avi'
    cap = cv.VideoCapture(video_file) 
    frame_counter = 0

    image_file = "img/layer1.png"
    background = cv.imread(image_file,cv.IMREAD_UNCHANGED)
    background = ut.scale_image(background,25)
    print("Background Shape: ",background.shape)

    # path1 = Path([[237, 522], [236, 577], [269, 600], [240, 611], [254, 622]],180)
    # path1.freq = 1/(0.119999999999999*20)
    # path1.deg_offset(-20)
    # path2 = Path([[281, 517], [287, 534], [287, 560], [298, 569], [284, 575], [298, 587]],157.5)
    # path2.freq = 1/(0.119999999999999*20)
    # path2.deg_offset(90)
    # paths = [path1, path2]
    p1 = Path([[237, 522], [236, 577], [269, 600], [240, 611], [254, 622]],hz=0.8)
    paths = [p1]

    import floor_path_def as fp
    paths = fp.chip3

    # paths = [Path()]
    video = False
    running = True
    keep_updating = False
    redraw = True
    delay = 100 #ms (33=30fps)
    # bkg = background.copy()
    path_select = 0
    while running:
        if video:
            _, frame = cap.read()
            frame_counter += 1
            if frame_counter == cap.get(cv.CAP_PROP_FRAME_COUNT):
                frame_counter = 0 # Or whatever as long as it is the same as next line
                cap.set(cv.CAP_PROP_POS_FRAMES, 0)

        

        if mouse_changed:
            print("Add point",mouse_xy)
            paths[path_select].add_point(mouse_xy)
            mouse_changed = False
            redraw = True

        redraw = True
        if redraw:
            if video:
                bkg = frame
            else:
                bkg = background.copy()
            # bkg = background.copy()
            c = 0
            for p in paths:
                if path_select == c:
                    bkg = p.draw_on(bkg,c=(0,255,0,255),width=1)
                else:
                    bkg = p.draw_on(bkg,c=(0,0,255,255))
                p.step()
                c += 1
            redraw = False
        
        print("\nPATHS")
        c = 1
        for p in paths:
            print("p{} = Path({})".format(c,p.points))
            c += 1

        if len(paths[path_select].seg_angle) > 0:
            ang = paths[path_select].seg_angle[len(paths[path_select].seg_angle)-1]
            ang = round(360 - ((ang - 90) % 360),2)
        else:
            ang = "--"
        s = "Path {}/{}   {}deg".format(path_select+1,len(paths),ang)
        ut.draw_textline(bkg,s,scale=2.0,c=(255,255,255),c2=(50,50,50))

        cv.imshow("Path Test",bkg)

        # CV CONTROLS ==============================================
        k = cv.waitKey(delay) & 0xFF

        # Cycle through paths
        if k == ord('1'):
            path_select = (path_select - 1) % len(paths)
            print("Layer",path_select+1)
        if k == ord('2'):
            path_select = (path_select + 1) % len(paths)
            print("Path",path_select+1)

        # Add / remove paths
        if k == ord('3'):
            path = Path()
            paths.append(path)
            path_select = len(paths) - 1
        if k == ord('4'):
            l = len(paths)
            if l > 1:
                if path_select == l-1:
                    path_select -= 1
                paths.pop()
        
        # Remove last point, clear path
        if k == ord('e'):
            if len(paths[path_select].points) > 0:
                paths[path_select].points.pop()
                paths[path_select].update_path()
                redraw = True
        if k == ord('r'):
            paths[path_select].clear()
            redraw = True

        # Move last point
        if k == ord('w'):
            paths[path_select].move_point(0,-1)
        if k == ord('s'):
            paths[path_select].move_point(0,1)
        if k == ord('a'):
            paths[path_select].move_point(-1,0)
        if k == ord('d'):
            paths[path_select].move_point(1,0)

        # Pause and Quit
        if k == ord('p') or k == ord('z'):
            print_path_list(paths)
            cv.waitKey(0)
        if k == ord('q'):
            print("\n")
            print_path_list(paths)
            running = False
