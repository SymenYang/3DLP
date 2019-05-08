import numpy as np
import cv2
import json
import math
from math import cos, sin


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

        self.paper = np.zeros((1, 1, 4))

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

        self.paper = np.zeros((self.width, self.height, 4))
        # calc R
        rx = self.eular[0] / 180 * math.pi
        Rx = np.asarray(
            [[1, 0, 0], [0, cos(rx), -sin(rx)], [0, sin(rx), cos(rx)]])
        ry = self.eular[1] / 180 * math.pi
        Ry = np.asarray(
            [[cos(ry), 0, sin(ry)], [0, 1, 0], [-sin(ry), 0, cos(ry)]])
        rz = self.eular[2] / 180 * math.pi
        Rz = np.asarray(
            [[cos(rz), -sin(rz), 0], [sin(rz), cos(rz), 0], [0, 0, 1]])
        self.rotation = Rx.dot(Ry).dot(Rz)

        # calc K
        self.K = np.asarray([[self.f,0,dx],[0,self.f,dy],[0,0,1]])

    def getP(self):
        T = np.asarray([[self.pos[0]],[self.pos[1]],[self.pos[2]])
        RT = np.append(R,T,axis=1)
        return self.K.dot(RT)