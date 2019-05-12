import numpy as np


class line:
    __line_types = ['solid','dash']
    def __init__(self,start = (0,0,0),end = (0,0,0),width = 1.0,color=(0,0,0),type = 'solid'):
        self.start = start
        self.end = end
        self.width = width;
        self.color = color;
        self.type = type;
        if not self.type in self.__line_types:
            self.type = self.__line_types[0]

    def readFromDict(self,data):
        if 'start' in data:
            self.start = tuple(data['start'])
        if 'end' in data:
            self.end = tuple(data['end'])
        if 'width' in data:
            self.width = float(data['width'])
        if 'type' in data:
            self.type = data['type']
        if 'color' in data:
            self.color = tuple(data['color'])
            
        if not self.type in self.__line_types:
            self.type = self.__line_types[0]
        
    def refine(self):
        if self.type == 'solid':
            return [self]
        elif self.type == 'dash':
            ret = []
            s = np.asarray(self.start)
            e = np.asarray(self.end)
            d = e - s
            ld = np.linalg.norm(d)
            ds = d / ld * 0.15
            de = d / ld * 0.1
            for i in range(int(ld / 0.15)):
                ret.append(line(s + ds * i,s + ds * i + de,self.width,self.color))
            ret.append(line(s + ds * int(ld / 0.15),self.end,self.width,self.color))
            return ret


    def __str__(self):
        return vars(self).__str__()

    def __repr__(self):
        return vars(self).__str__()
