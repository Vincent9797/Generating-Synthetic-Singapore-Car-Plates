#coding=utf-8
#coding=utf-8
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import random
import cv2
import numpy as np
import os
from math import *
from plate_generator import generate_random_plate
from aug import AddSmudginess, rot, rotRandrom, tfactor, random_envirment, AddGauss, r, AddNoiseSingleChannel, addNoise
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import argparse

WORD_WIDTH = 24
SPACE_MULTI = 0 # spacing for multi-line car plates
SPACE = 1 # spacing for single-line car plates

def GenCh1(f,val):
    img=Image.new("RGB", (WORD_WIDTH,70),(255,255,255))
    draw = ImageDraw.Draw(img)

    if val == "1":
        draw.text((7, 20), val.encode('utf-8').decode(encoding="utf-8"), (0, 0, 0), font=f)
    else:
        draw.text((-3, 20),val.encode('utf-8').decode(encoding="utf-8"),(0,0,0),font=f)
    A = np.array(img)
    return A

def MultiGenCh1(f,val):
    img = Image.new("RGB", (WORD_WIDTH, 30), (255, 255, 255))
    draw = ImageDraw.Draw(img)

    if val == "1":
        draw.text((7, 2), val.encode('utf-8').decode(encoding="utf-8"), (0, 0, 0), font=f)
    else:
        draw.text((0, 1),val.encode('utf-8').decode(encoding="utf-8"),(0,0,0),font=f)
    A = np.array(img)
    return A

class GenPlate:
    def __init__(self,font,NoPlates):
        self.fontMulti =  ImageFont.truetype(font,38,0)
        self.fontSingle =  ImageFont.truetype(font,45,0) # Single line uses larger font size
        self.smu = cv2.imread("./images/smu.jpg")
        self.noplates_path = []
        for parent,parent_folder,filenames in os.walk(NoPlates):
            for filename in filenames:
                path = parent+"/"+filename
                self.noplates_path.append(path)


    def draw(self,val):
        self.img = np.array(Image.new("RGB", (226, 70), (255, 255, 255)))
        if val[2].isdigit(): # 2 alphabets
            offset = 20
            length = 7
        else:
            offset = 20
            length = 8

        for i in range(length):
            self.img[0:70, offset+i*(WORD_WIDTH+SPACE): offset + (i+1)*WORD_WIDTH + i*SPACE] = GenCh1(self.fontSingle, val[i])
        return self.img

    def draw_multi(self,val):
        self.img = np.array(Image.new("RGB", (226, 70), (255, 255, 255)))
        if val[2].isdigit(): # 2 alphabets in front
            offset = 85
            self.img[5:35,offset:offset+WORD_WIDTH] = MultiGenCh1(self.fontMulti,val[0])
            self.img[5:35,offset+WORD_WIDTH+SPACE_MULTI:offset+2*WORD_WIDTH+SPACE_MULTI]= MultiGenCh1(self.fontMulti,val[1])
            word_offset = 2
            length = 7
        else:
            offset= 77
            self.img[5:35,offset:offset+WORD_WIDTH]= MultiGenCh1(self.fontMulti,val[0])
            self.img[5:35,offset+WORD_WIDTH+SPACE_MULTI:offset+2*WORD_WIDTH+SPACE_MULTI]= MultiGenCh1(self.fontMulti,val[1])
            self.img[5:35,offset+2*(WORD_WIDTH+SPACE_MULTI):offset+3*WORD_WIDTH+2*SPACE_MULTI]= MultiGenCh1(self.fontMulti,val[2])
            word_offset = 3
            length = 8

        offset = 5
        for i in range(length-word_offset):
            base = offset+WORD_WIDTH+WORD_WIDTH + i*WORD_WIDTH + (i+1)*SPACE_MULTI - 8
            self.img[35:65, base  : base+WORD_WIDTH]= MultiGenCh1(self.fontMulti,val[i+word_offset])
        return self.img

    def generate(self,text, lines):
        if lines == 'single':
            fg = self.draw(text.encode('utf-8').decode(encoding="utf-8"))
            self.bg = cv2.resize(cv2.imread("./images/bw_template.bmp"), (226, 70))
        else:
            fg = self.draw_multi(text.encode('utf-8').decode(encoding="utf-8"))
            self.bg = cv2.resize(cv2.imread("./images/bw_template_multi.bmp"), (226, 70))
        fg = cv2.bitwise_not(fg)
        com = cv2.bitwise_or(fg,self.bg)

        tl = (4, 4)
        tr = (222,4)
        bl = (4, 68)
        br = (222, 68)
        points = [tl, tr, bl, br]

        com, points = rot(com,r(60)-30,com.shape,30, points)
        com, points = rotRandrom(com,random.randint(2,4),(com.shape[1],com.shape[0]), points)
        com = random_envirment(com, self.noplates_path, points)
        com = AddGauss(com, random.randint(1,3))
        return com

    def genBatch(self, batchSize, outputPath, size):
        if (not os.path.exists(outputPath)):
            os.mkdir(outputPath)
        for i in range(batchSize):
            plateStr = generate_random_plate() # generates a plate string
            if random.randint(0,1) == 0:
                img =  G.generate(plateStr, 'single') # single line
            else:
                img = G.generate(plateStr, 'multi')
            img = cv2.resize(img,size)
            filename = os.path.join(outputPath, str(i).zfill(4) + '.' + plateStr + ".jpg")
            # img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite(filename, img)

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("--num_plates", default=10, help="Number of plates generated")
    parser.add_argument("--dir", default='plates', help="Output directory of plates")
    args = parser.parse_args()

    if not os.path.exists(args.dir):
        os.mkdir(args.dir)

    random.seed(42)
    G = GenPlate("./font/UKNumberPlate.ttf","./NoPlates")
    G.genBatch(int(args.num_plates), args.dir, (272, 72))

