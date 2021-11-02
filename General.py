import numpy as np
class Location:
    x = 0
    y = 0
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def update(self,x,y):
        self.x = self.x + x
        self.y = self.y + y
    def loc_print(self):
        print(self.x,self.y)
    def loc_length(self, m):
        v1 = np.array([self.x,self.y])
        v2 = np.array([m.x,m.y])
        return  np.linalg.norm(v1-v2)
    def __add__(self, other):
        return Location(self.x + other.x, self.y + other.y)

    def get_loc_mv(self,mv):

        if mv == 0:
            loc_next = Location(self.x, self.y + 1)
        elif mv == 1:
            loc_next = Location(self.x+1,self.y+1)
        elif mv == 2:
            loc_next = Location(self.x+1,self.y)
        elif mv == 3:
            loc_next = Location(self.x+1,self.y-1)
        elif mv == 4:
            loc_next = Location(self.x,self.y-1)
        elif mv == 5:
            loc_next = Location(self.x-1,self.y-1)
        elif mv == 6:
            loc_next = Location(self.x-1,self.y)
        elif mv == 7:
            loc_next = Location(self.x-1,self.y+1)
        else:
            loc_next = Location(-1,-1)
        return loc_next
class  Speed:
    x = 0
    y = 0
    def __init__(self,x,y):
        self.x = x
        self.y = y
class Threat:
    loc = Location(0,0)
    r = 0
    def __init__(self,loc,r):
        self.loc = loc
        self.r = r
    def check_loc(self,loc):
        l = self.loc.loc_length(loc)
        if l <= self.r:
            return 1 # in threat range
        else:
            return 0
class Search_Map:
    w = 0
    smap = []
    def __init__(self,w):
        self.w = w
        self.smap = np.zeros((w,w), dtype = np.int)
    def get_apf(self,loc,time):
        return  0
class Globalvar:
    uav_total = 0

    def __init__(self,uav_total):
        self.uav_total = uav_total