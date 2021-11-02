from General import Location
from Target import Target
import math
import random
from TPM import TPM
from TPM import Pheromone
from General import Threat
from APF import APF
import csv
#import tensorflow as tf
import numpy as np
dir_list = [1.5707963,0.78539815,0,-0.78539815,-1.5707963,-2.35619445,3.1415926,2.35619445]
md_dict = {0:[0,1],1:[0.707,0.707],2:[1,0],3:[0.707,-0.707],4:[-1,0],5:[-0.707,-0.707],6:[-1,0],7:[-0.707,0.707]}
search_auto_random_flag = 0#  1： 开启赌轮盘,0 :选择最大值
class UAV_part:
    num = 0
    moving_direction = 0
    location = Location(0,0)
    next_location = Location(0,0)
    cs_flag = 0
    cs_countdown = 0
    threat_list_local = []
    pheromone = 0
    p_index0 = 0
    p_index1 = 0
    def __init__(self,num,mv,loc_):
        self.num = num
        self.moving_direction= mv
        self.cs_flag = 0
        self.cs_countdown = 0
        self.location = loc_
        self.next_location = 0
        self.pheromone =Pheromone(100,100,1)
        self.threat_list_local = []
        self.p_index0 = 1
        self.p_index1 = 3
    def search_(self,CS0):
        #self.update_pheromone(CS0.uav_list)
        if self.cs_countdown > 0:
            self.cs_countdown -= 1
        if self.cs_flag:
            self.search_byCS()
        else:
            self.search_auto(CS0)
        self.update_location_auto()
    def search_auto(self,CS0):
        grid_list =  self.get_grid_reachable()
        p_list = []
        for i in grid_list:
            loc_next = i[0]
            afa = CS0.pheromone.pheromone[loc_next.x][loc_next.y]
            gma = 0
            loc_n1 = loc_next.get_loc_mv(i[1])
            loc_n2 = loc_n1.get_loc_mv(i[1])
            for x_shift in range(5):
                for y_shift in range(5):
                    xx = loc_n2.x - 2 + x_shift
                    yy = loc_n2.y - 2 + y_shift
                    if xx >=100 or xx <0 or yy >= 100 or yy <0:
                        continue
                    gma += (1- CS0.search_map[xx][yy])

            p0 = afa ** self.p_index0 + gma** self.p_index1
            p_list.append([p0,i[1]])

        #赌轮盘
        if search_auto_random_flag :
            p_sum = 0
            p_list_len = len(p_list)
            for i in range(p_list_len):
                p_sum += p_list[i][0]
            q = random.random() *p_sum

            for i in range(p_list_len):
                if i == 0:
                    pq = p_list[0][0]
                else:
                    pq += p_list[i][0]
                if pq >= q :
                    self.moving_direction = p_list[i][1]
                    break
        else :
            p_list_len = len(p_list)
            for i in range(p_list_len):
                if i == 0:
                    p_max = p_list[0][0]
                    self.moving_direction = p_list[0][1]
                else:
                    if p_max < p_list[i][0]:
                        p_max = p_list[i][0]
                        self.moving_direction = p_list[i][1]
            self.check_moving_direction()
    def search_byCS(self):
        x0, y0 = self.location.x, self.location.y
        x1, y1 = self.next_location.x, self.next_location.y

        if self.moving_direction == 0:
            l0 = self.location + Location(0, 1)
            l1 = self.location + Location(-1, 1)
            l2 = self.location + Location(1, 1)

        elif self.moving_direction == 1:
            l0 = self.location + Location(1, 1)
            l1 = self.location + Location(0, 1)
            l2 = self.location + Location(1, 0)
        elif self.moving_direction == 2:
            l0 = self.location + Location(1, 0)
            l1 = self.location + Location(1, 1)
            l2 = self.location + Location(1, -1)
        elif self.moving_direction == 3:
            l0 = self.location + Location(1, -1)
            l1 = self.location + Location(1, 0)
            l2 = self.location + Location(0, -1)
        elif self.moving_direction == 4:
            l0 = self.location + Location(0, -1)
            l1 = self.location + Location(1, -1)
            l2 = self.location + Location(-1, -1)
        elif self.moving_direction == 5:
            l0 = self.location + Location(-1, -1)
            l1 = self.location + Location(0, -1)
            l2 = self.location + Location(-1, 0)
        elif self.moving_direction == 6:
            l0 = self.location + Location(-1, 0)
            l1 = self.location + Location(-1, -1)
            l2 = self.location + Location(-1, 1)
        else:
            l0 = self.location + Location(-1, 1)
            l1 = self.location + Location(-1, 0)
            l2 = self.location + Location(0, 1)
        list_loc = [l0, l1, l2]
        m_loc = [self.moving_direction, self.moving_direction - 1, self.moving_direction + 1]
        min_l = 10000000
        for i in range(3):
            flag = 0
            for j in self.threat_list_local:

                if list_loc[i].loc_length(j.loc) < j.r:
                    flag = 1
                    break
            if flag == 1:
                continue
            else:
                l = list_loc[i].loc_length(self.next_location)
                if l < min_l:
                    self.moving_direction = m_loc[i]
                    min_l = l
        self.check_moving_direction()
        if self.location.x == self.next_location.x and self.location.y == self.next_location.y:
            self.cs_flag = 0
            self.cs_countdown = 10
        for i in self.threat_list_local:
            ll = i.loc.loc_length(self.next_location)
            if ll <= i.r + 1:
                self.cs_flag = 0
                self.cs_countdown = 10
    def get_grid_reachable(self):
        grid_list = []
        for i in range(3):
            mv = self.moving_direction -1 + i
            if mv > 7:
                mv = 0
            if mv < 0:
                mv = 7
            grid_next = self.location.get_loc_mv(mv)
            threat_flag = 0
            borad_flag = 0
            for threat_i in self.threat_list_local:
                if threat_i.check_loc(grid_next) :
                    threat_flag = 1
                    break
            if grid_next.x >=100 or grid_next.x <0 or grid_next.y >= 100 or grid_next.y <0:
                borad_flag = 1
            if threat_flag or borad_flag:
                continue
            else:
                grid_list.append([grid_next,mv])
        return grid_list
    def update_pheromone(self,uav_list):
        for i in uav_list:
            self.pheromone.update_auto(i.location)
    def check_moving_direction(self):
        if self.moving_direction > 7:
            self.moving_direction = 0
        if self.moving_direction < 0:
            self.moving_direction = 7
    def update_location_auto(self):
        if self.moving_direction == 0:
            self.location.update(0,1)
        elif self.moving_direction == 1:
            self.location.update(1,1)
        elif self.moving_direction == 2:
            self.location.update(1,0)
        elif self.moving_direction == 3:
            self.location.update(1,-1)
        elif self.moving_direction == 4:
            self.location.update(0,-1)
        elif self.moving_direction == 5:
            self.location.update(-1,-1)
        elif self.moving_direction == 6:
            self.location.update(-1,0)
        elif self.moving_direction == 7:
            self.location.update(-1,1)
    def update_threat_list_local(self,threat_list):
        for i in threat_list:
            if self.location.loc_length(i.loc) <= 3+i.r :
                if i.loc not in self.threat_list_local:
                    self.threat_list_local.append(i)