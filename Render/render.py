import numpy as np
import cv2
import json
import math
from math import cos, sin
import os, sys
lib_path = os.path.abspath(os.path.join('..'))
sys.path.append(lib_path)

from Structures.line import line
from Structures.point import point
from Structures.node import node
from Structures.scene import scene
from camera import camera

class render:
    def __init__(self,sceneFileName = None,cameraFileName = None):
        self.scene = scene()
        self.camera = camera()
        if sceneFileName != None:
            fp = open(sceneFileName,'r')
            jd = json.load(fp)
            self.scene.readFromDict(jd)
        if cameraFileName != None:
            fp = open(cameraFileName,'r')
            jd = json.load(fp)
            self.camera.readFromDict(jd)
    
    def getR(self,eular):
        rx = eular[0] / 180 * math.pi
        Rx = np.asarray(
            [[1, 0, 0], [0, cos(rx), sin(rx)], [0, -sin(rx), cos(rx)]])
        ry = eular[1] / 180 * math.pi
        Ry = np.asarray(
            [[cos(ry), 0, -sin(ry)], [0, 1, 0], [sin(ry), 0, cos(ry)]])
        rz = eular[2] / 180 * math.pi
        Rz = np.asarray(
            [[cos(rz), sin(rz), 0], [-sin(rz), cos(rz), 0], [0, 0, 1]])
        return Rx.dot(Ry).dot(Rz)
    
    def getTrans(self,eular,pos):
        R = self.getR(eular)
        t = np.asarray(pos)
        t.resize((1,3))
        T = np.append(R,t,axis=0)
        i = np.zeros((4,1))
        i[3] = 1
        T = np.append(T,i,axis=1)
        return T

    def render(self,aCamera):
        nowTrans = np.identity(4)
        self.renderANode(self.scene,nowTrans,aCamera)
        aCamera.write()

    def renderANode(self,aNode,trans,aCamera):
        for item in aNode.lines:
            aCamera.drawLine(item,trans)
        for item in aNode.points:
            aCamera.drawPoint(item,trans)
        for item in aNode.nodes:
            newTrans = self.getTrans(item.rotation,item.pos)
            self.renderANode(item,trans.dot(newTrans),aCamera)

if __name__ == '__main__':
    rd = render('./scene.json','./camera.json')
    rd.render(rd.camera)