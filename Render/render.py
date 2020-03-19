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
from Render.camera import camera

class render:
    def __init__(self,sceneFileName = None,directDict = None):
        self.scene = scene()
        self.cameras = []
        if sceneFileName != None:
            fp = open(sceneFileName,'r')
            jd = json.load(fp)
            self.scene.readFromDict(jd)
        elif directDict != None:
            self.scene.readFromDict(directDict)
            jd = directDict
        if 'cameras' in jd:
            cameraJson = jd['cameras']
            for item in cameraJson:
                self.cameras.append(camera())
                self.cameras[-1].readFromDict(item)
        self.parts = []
    
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
    
    def getTrans(self,eular,pos,scale):
        R = self.getR(eular)
        t = np.asarray(pos)
        t.resize((1,3))
        T = np.append(R,t,axis=0)
        i = np.zeros((4,1))
        i[3] = 1
        T = np.append(T,i,axis=1)
        S = np.identity(4)
        S[0][0] = scale[0]
        S[1][1] = scale[1]
        S[2][2] = scale[2]
        return S.dot(T)

    def render(self,aCamera,method = "Normal"):
        nowTrans = np.identity(4)
        if method == "Normal":
            self.renderANode(self.scene,nowTrans,aCamera)
        else:
            self.getAllDistance(self.scene,nowTrans,aCamera)
        aCamera.write()

    def renderAll(self,method = "Normal"):
        for aCamera in self.cameras:
            nowTrans = np.identity(4)
            if method == "Normal":
                self.renderANode(self.scene,nowTrans,aCamera)
            else:
                self.getAllDistance(self.scene,nowTrans,aCamera)
                self.renderDistanceQueue(aCamera)
            aCamera.write()

    def renderANode(self,aNode,trans,aCamera):
        for item in aNode.nodes:
            newTrans = self.getTrans(item.rotation,item.pos,item.scale)
            self.renderANode(item,trans.dot(newTrans),aCamera)
        for item in aNode.lines:
            aCamera.drawLine(item,trans)
        for item in aNode.points:
            aCamera.drawPoint(item,trans)

    def getAllDistance(self, aNode,trans,aCamera):
        for item in aNode.nodes:
            newTrans = self.getTrans(item.rotation,item.pos,item.scale)
            self.renderANodeByDistance(item,trans.dot(newTrans),aCamera)
        for item in aNode.lines:
            dist = aCamera.getLineDistance(item,trans)
            self.parts.append((item,trans,"l",dist))
        for item in aNode.points:
            dist = aCamera.getPointDistance(item,trans)
            self.parts.append((item,trans,"p",dist))

    def renderDistanceQueue(self,aCamera):
        self.parts.sort(key=lambda x : -x[3])
        for item in self.parts:
            if item[2] == "l":
                aCamera.drawLine(item[0],item[1])
            elif item[2] == "p":
                aCamera.drawPointRealSize(item[0],item[1])

if __name__ == '__main__':
    rd = render('../ScenesAndCameras/scene2.json')
    rd.renderAll()