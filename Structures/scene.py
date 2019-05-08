import numpy as np
from line import line
from point import point
from node import node
import json

class scene(node):
    def __init__(self):
        super(scene,self).__init__()
        self.refPath = {}
    
    def readFromDict(self,data):
        Path = './'
        if 'path' in data:
            Path = data['path']
        if 'import' in data:
            importList = data['import']
            for key in importList:
                self.refPath[key] = Path + importList[key]
        
        for key in self.refPath:
            fp = open(self.refPath[key])
            self.refNode[key] = json.load(fp)
            fp.close()
        
        super().readFromDict(data)


if __name__ == '__main__':
    testjson = 'scene.json'
    testnode = scene()
    fp = open(testjson,'r')
    datas = json.load(fp)
    testnode.readFromDict(datas)
    print(testnode.lines)
    print(testnode.points)
    print(testnode.nodes)