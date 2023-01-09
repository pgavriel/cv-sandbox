from PIL import ImageFont, ImageDraw, Image
import cv2 as cv
import numpy as np

class TextAnimator:
    def __init__(self,txt="BLANK",font="aakar.TTF",font_size=64,im_size=None):
        if im_size is not None:
            self.size = im_size
        else:
            self.size = [int(len(txt)*font_size*2),int(font_size*1.5)]
        self.image = np.zeros([self.size[1],self.size[0]],dtype=np.float32)
        self.image = cv.cvtColor(self.image, cv.COLOR_GRAY2BGR)

        self.str = txt
        self.font_file = font
        self.font_size = font_size
        self.font = ImageFont.truetype(font, font_size)
        self.draw_transparent = True

    def set_font(self,font=None,size=None,change_draw_size=True):
        if font is None:
            f = self.font_file
        else:
            f = font
        if size is None:
            s = self.font_size
        else:
            s = size
        print("Setting Font: {}, Size: {}".format(f,s))
        self.font_file = f
        self.font_size = s
        self.font = ImageFont.truetype(f, s)

        if change_draw_size:
            self.size = [int(len(self.str)*s),int(s*1.5)]

    def set_text(self,txt,resize=True):
        self.str = txt
        if resize:
            self.size = [int(len(self.str)*self.font_size),int(self.font_size*1.5)]

    def draw(self):
        self.image = np.zeros([self.size[1],self.size[0]],dtype=np.float32)
        cv2_im_rgb = cv.cvtColor(self.image,cv.COLOR_GRAY2RGB)
        pil_im = Image.fromarray((cv2_im_rgb * 255).astype(np.uint8))

        draw = ImageDraw.Draw(pil_im)
        draw.text((5, 5), self.str, font=self.font)

        cv2_im_processed = cv.cvtColor(np.array(pil_im), cv.COLOR_RGB2BGR)

        gray = cv.cvtColor(cv2_im_processed, cv.COLOR_BGR2GRAY)

        # Crop right side of text image
        skip = 2
        for i in range(1,gray.shape[1],skip):
            # print(max(gray[:,-i]))
            if max(gray[:,-i]) > 5:
                i -= 10
                gray = gray[:,:-i]
                cv2_im_processed = cv2_im_processed[:,:-i]
                break
        if self.draw_transparent:

            _,alpha = cv.threshold(gray,0,255,cv.THRESH_BINARY)
            b, g, r = cv.split(cv2_im_processed)
            rgba = [b,g,r, alpha]
            cv2_im_processed = cv.merge(rgba,4)

        self.image = cv2_im_processed
        print(self.image.shape)
        return cv2_im_processed

if __name__ == "__main__":
    ta = TextAnimator()
    ta.set_text("SEE YOU SPACE COWBOY...")
    ta.draw()
    cv.imshow("Test",ta.image)
    cv.waitKey(0)
    ta.set_text("Test")
    ta.draw()
    cv.imshow("Test",ta.image)
    cv.waitKey(0)
