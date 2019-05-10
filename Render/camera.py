import numpy as np
import cv2
import json
import math
from math import cos, sin
import os, sys
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from Structures import line,point


class camera:
    def __init__(self):
        self.pos = (0.0, 0.0, 0.0)
        self.eular = (0.0, 0.0, 0.0)
        self.w = 1.0
        self.h = 1.0
        self.f = 1.0
        self.dx = 0.5
        self.dy = 0.5
        self.width = 1024  # px
        self.height = 1024  # px

        self.rotation = np.identity(3)
        self.K = np.identity(3)

        self.paper = np.zeros((1, 1, 3))
        self.filename = ''
        self.P = np.zeros((3,4))

    def readFromDict(self, data):
        if 'pos' in data:
            self.pos = tuple(data['pos'])
        if 'eular' in data:
            self.eular = tuple(data['eular'])
        if 'w' in data:
            self.w = float(data['w'])
        if 'h' in data:
            self.h = float(data['h'])
        if 'f' in data:
            self.f = float(data['f'])
        if 'dx' in data:
            self.dx = float(data['dx'])
        if 'dy' in data:
            self.dy = float(data['dy'])
        if 'width' in data:
            self.width = int(data['width'])
        if 'height' in data:
            self.height = int(data['height'])
        if 'filename' in data:
            self.filename = data['filename']

        self.paper = np.full((self.height, self.width, 3),255.0)
        # calc R
        self.rotation = self.getR(self.eular)

        # calc K
        self.K = np.asarray([[self.f,0,self.dx],[0,self.f,self.dy],[0,0,1]])

        self.P = self.getP()

    def getR(self,eular):
        rx = eular[0] / 180 * math.pi
        Rx = np.asarray(
            [[1, 0, 0], [0, cos(rx), -sin(rx)], [0, sin(rx), cos(rx)]])
        ry = eular[1] / 180 * math.pi
        Ry = np.asarray(
            [[cos(ry), 0, sin(ry)], [0, 1, 0], [-sin(ry), 0, cos(ry)]])
        rz = eular[2] / 180 * math.pi
        Rz = np.asarray(
            [[cos(rz), -sin(rz), 0], [sin(rz), cos(rz), 0], [0, 0, 1]])
        return Rx.dot(Ry).dot(Rz)

    def getP(self):
        C = np.asarray([[self.pos[0]],[self.pos[1]],[self.pos[2]]])
        T = -self.rotation.dot(C)
        RT = np.append(self.rotation,T,axis=1)
        return self.K.dot(RT)

    def addADim(self,array):
        t = np.asarray([1])
        return np.append(array,t,axis=0)

    def drawLine(self,aLine,trans):
        start = np.asarray(aLine.start)
        end = np.asarray(aLine.end)
        start = self.addADim(start)
        end = self.addADim(end)
        start = start.dot(trans)
        end = end.dot(trans)
        sp = self.P.dot(start)
        ep = self.P.dot(end)
        if sp[-1] != 0:
            sp = sp / sp[-1]
        else:
            print(sp)
        if ep[-1] != 0:
            ep = ep / ep[-1]
        else:
            print(ep)
        cv2.line(self.paper,(int(sp[0] / self.h * self.height),int(sp[1] / self.w * self.width)),(int(ep[0] / self.h * self.height),int(ep[1] / self.w * self.width)),aLine.color,int(aLine.width),lineType=cv2.LINE_AA)
    
    def drawPoint(self,aPoint,trans):
        pos = np.asarray(aPoint.pos)
        pos = self.addADim(pos)
        pos = pos.dot(trans)

        p = self.P.dot(pos)
        p = p / p[-1]
        cv2.circle(self.paper,(int(p[0] / self.h * self.height),int(p[1] / self.w * self.width)),int(aPoint.width),aPoint.color,-1)
    
    def write(self):
        cv2.imwrite(self.filename,self.paper)