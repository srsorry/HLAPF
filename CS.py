import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import math
from General import Location
from TPM import Pheromone
from UAV_new import UAV_1125
import os
write_file_flag = 0
target_search_mode = 1#此模式下，CS优先安排具有先验信息的目标

class Part:
    # l2       l3
    #
    #
    # l0       l1
    l0 = Location(0, 0)
    l1 = Location(0, 0)
    l2 = Location(0, 0)
    l3 = Location(0, 0)
    width = 0
    max_UAV = 0

    def __init__(self, width, x0, y0, max_uav):
        self.width = width
        self.l0 = Location(x0, y0)
        self.l1 = Location(x0 + width - 1, y0)
        self.l2 = Location(x0, y0 + width - 1)
        self.l3 = Location(x0 + width - 1, y0 + width - 1)
        self.max_UAV = max_uav

    def check(self, uav_loc):
        n = self.width - 1
        if (self.l0.x <= uav_loc.x and self.l0.x + n > uav_loc.x and self.l0.y <= uav_loc.y and self.l0.y + n > uav_loc.y):
            return 1
        else:
            return 0


class CS:
    location_list = 0
    UAV_num = 0
    part_list = []
    width = 0
    uav_list = []
    search_map = []
    threat_list_local = []
    pheromone = 0
    def __init__(self, P,w):

        self.UAV_num = P

        self.width = w
        self.part()
        self.search_map =np.zeros((w,w))
        self.threat_list_local = []
        self.pheromone = Pheromone(100,100,1)
    def update_ph(self):
        for i in self.uav_list:
            self.pheromone.update_auto(i.location)
    def target_sh(self,target_list):
        target_attack_know_num = 0
        for j in range(12):
            if target_list[j].type == 0:
                target_attack_know_num += 1
        if target_attack_know_num > 11:
            return 1
        uav_ready_num = 0
        for i in self.uav_list:
            if i.cs_flag == 1 or i.cs_countdown >0 :
                continue
            uav_ready_num +=1
        if uav_ready_num < 1:
            return 2
        min_l = [10000,0,Location(0,0)]

        for j in range(12):
            if target_list[j].type == 0:
                continue
            for i in self.uav_list:
                d = i.location.loc_length(target_list[j].location)
                if  d < min_l[0]:
                    min_l[0] = d
                    min_l[1] = i.num
                    min_l[2] = target_list[j].location

            self.uav_list[min_l[1]-1].cs_flag = 1
            self.uav_list[min_l[1]-1].next_location = min_l[2]

        return 0
    def update_search_map(self):
        for i in self.search_map:
            for j in range(100):
                if i[j] > 0 :
                    i[j] *= 0.9
                if i[j] >0 and i[j] < 0.1:
                    i[j] = 0.1
        for i in self.uav_list:
            if i.type > 0:
                continue
            x0 ,y0 = i.location.x,i.location.y
            for x_shift in range(7):
                for y_shift in range(7):
                    x1 = x0+x_shift -3
                    y1 = y0+y_shift -3
                    if x1 >= 0 and x1 <100 and y1 >=0 and y1 <100:
                        self.search_map[x1][y1] = 1
            if i.cs_flag == 1:
                x0, y0 = i.next_location.x, i.next_location.y
                for x_shift in range(7):
                    for y_shift in range(7):
                        x1 = x0 + x_shift - 3
                        y1 = y0 + y_shift - 3
                        if x1 >= 0 and x1 < 100 and y1 >= 0 and y1 < 100:
                            self.search_map[x1][y1] = 1
        for i in self.threat_list_local:
            x0,y0 = i.loc.x,i.loc.y
            for x_shift in range(i.r*2+1):
                for y_shift in range(i.r*2+1):
                    x1 = x0 +x_shift -i.r
                    y1 = y0 +y_shift -i.r
                    if x1 >= 0 and x1 <100 and y1 >=0 and y1 <100:
                        self.search_map[x1][y1] = 1

    def update_threat(self):
        for i in self.uav_list:
            for j in i.threat_list_local:
                if j not in self.threat_list_local:
                    self.threat_list_local.append(j)

    def get_part_center(self):
        n = 2
        w = 50
        rel = []
        for i in range(n):
            for j in range(n):
                sum_x = 0
                sum_y = 0
                sum = 0
                for i_x in range(w):
                    for i_y in range(w):
                        x = i_x +  j*w
                        y = i_y +  i*w
                        p = self.search_map[x][y]
                        sum += p
                        sum_x += p*x
                        sum_y += p*y
                meanx = sum_x// sum
                meany = sum_y// sum
                th_flag = 1
                while th_flag:
                    th_flag = 0
                    loc = Location(meanx,meany)
                    for i in self.threat_list_local:
                        if loc.loc_length(i.location)<i.r:
                            th_flag = 1
                            break
                    if th_flag == 1:
                        meanx +=1
                        meany +=1
                rel.append([meanx,meany])
        return rel
    def part(self):
        n = 2
        max_uav = 3
        layer_ticker = self.width / n
        L0 = Location(0,0)
        self.part_list = []
        for i in range(n):
            for j in range(n):
                p = Part(self.width, L0.x, L0.y, max_uav)
                self.part_list.append(p)
                L0.x += self.width
            L0.y += self.width
    def search_map_check(self):
        w = 10
        search_part = np.zeros(100)
        min = 10000
        uav_num_ready = 0
        for i in self.uav_list:
            if i.cs_flag == 1 or i.cs_countdown > 0 or i.type > 0:
                continue
            uav_num_ready +=1
        #print(uav_num_ready)
        if uav_num_ready < (self.UAV_num // 2 + 1):
        #if uav_num_ready <=0:
            return 0
        sum = 0
        rel_list = []
        min_val = 1000
        min_num = 0
        for i in range(w):
            for j in range(w):
                sum = 0
                for a in range(10):
                    for b in range(10):
                        x = i*10+a
                        y = j*10+b
                        sum += self.search_map[x][y]
                l_min = 10000
                min_uav_num = -1
                for uav_i in self.uav_list:
                    if uav_i.cs_flag == 1 or uav_i.cs_countdown > 0 or uav_i.type > 0:
                        continue
                    l = uav_i.location.loc_length(Location(i*10+5,j*10+5))
                    if l_min > l:
                        l_min = l
                        min_uav_num = uav_i.num
                rel_list.append([sum,l_min,min_uav_num])
                val = sum * 10 + l_min
                search_part[i*10+j] = val
                if min_val > val:

                    min_val = val
                    min_num = i*10+j
        target_uav = rel_list[min_num][2]-1
        #print(rel_list[min_num])
        #if target_uav >=20 or target_uav<0:
           # exit(0)
        self.uav_list[target_uav].cs_flag = 1
        x =(min_num//10) * 10 +5
        y =(min_num%10) * 10 +5
        self.uav_list[target_uav].next_location = Location(x,y)
        return [min_val,min_num]


    def uav_num_check(self):
        w = 50

        n = 2
        uav_part_list = []
        need_help_part = []
        for i in self.uav_list:
            if i.cs_flag == 1:
                a, b = i.next_location.x,i.next_location.y
            else:
                a, b = i.location.x, i.location.y
            a /= w
            b /= w
            a = math.floor(a)
            b = math.floor(b)
            uav_part_list.append(a+b*n)
        for i in range(n*n):
            x = uav_part_list.count(i)
            if x < 2:
                need_help_part.append(i)
        part_neighour= [(1,2,3),(0,3,2),(0,3,1),(1,2,0)]
        #part_center = [(25,25),(75,25),(25,75),(75,75)]
        if len(need_help_part) >0:
            part_center = self.get_part_center()
        for i in need_help_part:
            p0 = part_neighour[i][0]
            p1 = part_neighour[i][1]
            p0_n = uav_part_list.count(p0)
            p1_n = uav_part_list.count(p1)
            if p0_n == 0 and p1_n ==0 :
                continue
            else:
                if p0_n < p1_n:
                    p0,p0_n,p1,p1_n = p1,p1_n,p0,p0_n
                l_max = 0
                for j in self.uav_list:
                    if j.cs_flag == 1:
                        a, b = j.next_location.x, j.next_location.y
                    else:
                        a, b = j.location.x, j.location.y
                    a /= w
                    b /= w
                    a = math.floor(a)
                    b = math.floor(b)
                    if a + b*n == p0:
                        l = (a - part_center[i][0])**2 + (b - part_center[i][1])**2
                        weight = j.apf_before[0] **2 + j.apf_before[1] ** 2
                        if weight / l >=l_max:
                            l_max = weight / l
                            uav_j = j
                uav_j.cs_flag = 1
                #uav_j.next_location = Location(part_center[i][0],part_center[i][1])
                uav_num = uav_part_list.count(i)
                if uav_num == 0:
                    uav_j.next_location = Location(part_center[i][0], part_center[i][1])
                else:
                    index0 = uav_part_list.index(i)
                    l0 = self.uav_list[index0].location
                    x1,y1 = part_center[i][0]*2 - l0.x, part_center[i][1]*2 - l0.y
                    if x1 <0 :
                        x1 = 0
                    if x1 >=100:
                        x1 = 99
                    if y1 <0 :
                        y1 = 0
                    if y1 >= 100:
                        y1 = 99
                    uav_j.next_location = Location(x1,y1)
