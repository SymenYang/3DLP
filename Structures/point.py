import numpy as np

class point():
    def __init__(self,pos=(0,0,0),width=1,color=(0,0,0)):
        self.pos = pos
        self.width = width
        self.color = color

    def readFromDict(self,data):
        if 'pos' in data:
            self.pos = tuple(data['pos'])
        if 'width' in data:
            self.width = float(data['width'])
        if 'color' in data:
            self.color = tuple(data['color'])
        
    def refine(self):
        return [self]

    def __str__(self):
        return vars(self).__str__()
    
    def __repr__(self):
        return vars(self).__str__()