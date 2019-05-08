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
        
    def __str__(self):
        return vars(self).__str__()
    
    def __repr__(self):
        return vars(self).__str__()
