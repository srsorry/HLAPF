from General import Location
import numpy as np
class APF:
    # x is 0 ,  y is 1
    #taf = 0
    #Target Attraction Field
    #trf = 1
    #Threat Repulsive Field
    #rfb = 2
    #Repulsive Field Between the UAVs
    #srf = 3
    #search Repulsive Field
    #unuse = 4
    type = 0
    l0 = 0
    l1 = 0
    index0 = 0
    k_apf = 0
    location = Location(0,0)
    def __init__(self,type_,l0,l1,index0,k_apf,location_):
        self.type = type_
        self.l1 = l1
        self.l0 = l0
        self.index0 = index0
        self.k_apf = k_apf
        self.location = location_
    def get_apf(self,location_uav:Location,md_uav):
        if self.type ==0:
            return self.type0_getapf(location_uav,self.location,md_uav)
        elif self.type == 1:
            return self.type1_getapf(location_uav, self.location)
        elif self.type == 2:
            return self.type2_getapf(location_uav, self.location)
        elif self.type == 3:

            return self.type3_getapf(location_uav, self.location, md_uav)
        else:
            return np.zeros(2)
    def type0_getapf(self,location_uav:Location,location_target:Location,md_uav):
        l = location_target.loc_length(location_uav)
        rel = np.zeros(2)
        if l < self.l0:
            rel[0] = md_uav[0] * self.index0
            rel[1] = md_uav[1] * self.index0
        elif l < self.l1:
            rel[0] = (location_uav.x - location_target.x) * self.k_apf / (l ** 2.5)
            rel[1] = (location_uav.y - location_target.y) * self.k_apf / (l ** 2.5)
        return rel
    def type1_getapf(self,location_uav:Location,location_target:Location):
        l = location_target.loc_length(location_uav)
        rel = np.zeros(2)
        if l < self.l1:
            rel[0] = (-location_uav.x + location_target.x) * self.k_apf / (l ** 2.5)
            rel[1] = (-location_uav.y + location_target.y) * self.k_apf / (l ** 2.5)
        return rel
    def type2_getapf(self,location_uav:Location,location_target:Location):
        l = location_target.loc_length(location_uav)
        rel = np.zeros(2)
        if l < self.l1:
            rel[0] = (-location_uav.x + location_target.x) * self.k_apf / (l ** 2.5)
            rel[1] = (-location_uav.y + location_target.y) * self.k_apf / (l ** 2.5)
        return rel
    def type3_getapf(self,location_uav:Location,location_target:Location,md_uav):
        l = location_target.loc_length(location_uav)
        rel = np.zeros(2)
        if l < self.l0:
            rel[0] = -md_uav[0] * self.index0
            rel[1] = -md_uav[1] * self.index0
        elif l < self.l1:
            rel[0] = (location_target.x - location_uav.x) * self.k_apf / (l ** 2.5)
            rel[1] = (location_target.y - location_uav.y) * self.k_apf / (l ** 2.5)
        return rel