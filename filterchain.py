# import cv2 as cv


class FilterChain:
    def __init__(self):
        self.input = None
        self.chain = []
        self.output = None
        self.mode = 0
        pass

    #
    def add(self,layer,position=None):
        if position is None:
            self.chain.append(layer)
        else:
            self.chain.insert(position,layer)
        pass

    def setInput(self,input):
        self.input = input

    def process(self,image=None):
        self.input = image
        if self.input is None:
            print("No input to process")
            return
        img = self.input.copy()

        for f in self.chain:
            img = f.apply(img)

        self.output = img

    def __str__(self):
        print("Filter chain object")
        for f in self.chain:
            print(f)

        pass
