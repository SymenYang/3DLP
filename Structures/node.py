import numpy as np
from Structures.line import line
from Structures.point import point

import json

class node:
    def __init__(self):
        self.name = ''
        self.refNode = {}
        self.pos = (0,0,0)
        self.rotation = (0,0,0)

        self.lines = []
        self.points = []
        self.nodes = []
        
        self.lineDatas = []
        self.pointDatas = []
        self.nodeDatas = []

        self.lineStyle = {}
        self.pointStyle = {}
        self.scale = (1.0,1.0,1.0)
    
    def giveRefNode(self,data):
        self.refNode = data

    def readFromDict(self,data):
        if 'name' in data:
            self.name = data['name']
        if 'pos' in data:
            self.pos = tuple(data['pos'])
        if 'rotation' in data:
            self.rotation = tuple(data['rotation'])
        
        if 'lineStyle' in data:
            self.lineStyle = data['lineStyle']
        if 'pointStyle' in data:
            self.pointStyle = data['pointStyle']

        if 'lines' in data:
            self.lineDatas = list(data['lines'])
        if 'points' in data:
            self.pointDatas = list(data['points'])
        if 'nodes' in data:
            self.nodeDatas = list(data['nodes'])

        if 'scale' in data:
            self.scale = tuple(data['scale'])
        
        self.initAtomS(self.lineDatas,self.lines,self.lineStyle,line)
        self.initAtomS(self.pointDatas,self.points,self.pointStyle,point)
        self.initNodes(self.nodeDatas,self.nodes,self.refNode)

    def initAtomS(self,datas,targets,style,ttype):
        for item in datas:
            itemDict = item.copy()
            for key in style:
                if not key in itemDict:
                    itemDict[key] = style[key]
            atom = ttype()
            atom.readFromDict(itemDict)
            added = atom.refine()
            targets.extend(added)
            #targets.append(atom)
        print(targets)

    def initNodes(self,datas,targets,ref):
        for item in datas:
            itemDict = item.copy()
            name = ''
            if 'name' in itemDict:
                name = itemDict['name']
            if name in ref:
                for key in ref[name]:
                    if not key in itemDict:
                        itemDict[key] = ref[name][key]
            anode = node()
            anode.giveRefNode(ref)
            anode.readFromDict(itemDict)
            targets.append(anode)

    def __str__(self):
        return vars(self).__str__()
    
    def __repr__(self):
        return vars(self).__str__()


if __name__ == '__main__':
    testjson = 'test.json'
    testnode = node()
    fp = open(testjson,'r')
    datas = json.load(fp)
    testnode.readFromDict(datas)
    print(testnode.lines)
    print(testnode.points)
    print(testnode.nodes)