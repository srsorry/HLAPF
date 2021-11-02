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
import os
dir_list = [1.5707963,0.78539815,0,-0.78539815,-1.5707963,-2.35619445,3.1415926,2.35619445]
md_dict = {0:[0,1],1:[0.707,0.707],2:[1,0],3:[0.707,-0.707],4:[-1,0],5:[-0.707,-0.707],6:[-1,0],7:[-0.707,0.707]}
env_perception_factor = 0.1
write_file_flag = 0
cs_INC = 1
s_mode = 0
test_mode = 0
borad_mode =0# 1 ：边界有人工场
HAPF_ACO = 0
def conv3x3( a, b):
    sum_ = 0
    for i in range(3):
        for j in range(3):
            sum_ += (a[i][j] * b[i][j])
    return sum_
class UAV_1125:
    type = 0
    num = 0
    moving_direction = 0
    location = Location(0,0)
    search_l = []
    swarm_info = []
    traversed_distance = 0
    start_location = Location(0,0)
    pheromone = []
    turn_num = 0
    #apf_list =[]
    target_list_local = []
    search_list_swarm = []
    swarm_kownn = []
    threat_list_local = []
    search_list_local = []
    type0_l0 =3
    type0_l1 =20
    type0_index0 =20
    type0_k_apf = type0_index0 * type0_l0**2
    type1_l0 =3
    type1_l1 =0
    type1_index0 =0
    type1_k_apf = 1000
    type2_l0 =0
    type2_l1 =0
    type2_index0 =0
    type2_k_apf = 0
    type3_l0 =3
    type3_l1 =30
    type3_index0 =5
    type3_k_apf = type3_index0 * type3_l0 ** 2

    type4_l0 =1
    type4_l1 =20
    type4_index0 =10
    type4_k_apf = type4_index0 * type4_l0**2



    file_data_out = 0
    basic_q = math.pi /18


    apf_before = 0
    #
    next_location = 0
    cs_flag = 0
    cs_countdown = 0

    def __init__(self,num,moving_direction,location):
        self.apf_before = np.zeros(2)
        self.num = num
        self.moving_direction = moving_direction
        self.location = Location(0,0)
        self.start_location = Location(0,0)
        self.location.x = location.x
        self.location.y = location.y
        self.start_location.x = location.x
        self.start_location.y = location.y
        if num %2 == 1:
            self.auto_index = 1
        else:
            self.auto_index = -1
        self.auto_i = 0
        self.search_map = np.zeros((100,100))
        self.pheromone = Pheromone(100,100,1)
        self.turn_num = 0
        self.target_list_local = []
        self.threat_list_local = []
        self.search_list_local = []
        self.search_list_swarm = []
        self.swarm_kownn = []
        self.basic_q = math.pi/9
        self.swarm_info = []
        if write_file_flag == 1:
            self.file_data_out = open("uav"+str(self.num)+".txt","w")
        self.next_location = Location(0,0)
        self.cs_flag = 0
        self.type = 0
    def update_location(self, x, y):
        self.location.update(x, y)
    def update_threat_list_local(self,threat_list):
        for i in threat_list:
            if self.location.loc_length(i.loc) <= 3+i.r :
                if i.loc not in self.threat_list_local:
                    self.threat_list_local.append(i)
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

    def get_swarm_info(self,uav_list:list):
        communication_distance = 50
        self.swarm_info = []
        for i in uav_list:
            if self.location.loc_length(i.location) <= communication_distance and i.num != self.num:
                #self.swarm_info.append([i.num,i.moving_direction,i.location.x,i.location.y])
                self.swarm_info.append(i)
                for j in range (len(self.target_list_local)):
                    if i.target_list_local[j].type == 0:
                        self.target_list_local[j].type = 0
                #self.search_list_swarm = i.search_list_local
                if i.num not in self.swarm_kownn:
                    self.swarm_kownn.append(i.num)
                    self.search_list_swarm.append(i.search_list_local)
    def update_target_list_local(self):
        for i in self.target_list_local:
            if abs(i.location.x - self.location.x) <=3 and abs(i.location.y - self.location.y) <=3 and  i.type > 0:
                i.target_attack()
            i.update_location_auto()
    def normal_apf(self):
        a = 1
        b = 1

        for i in self.target_list_local:
            fatt = a
    def make_decision(self):



        if self.traversed_distance ==1 :
            test = 1
        write_str = ""
        write_str += "num"+str(self.traversed_distance)+"  "
        write_str += "location:(" + str(self.location.x) + "," + str(self.location.y) + ")  "
        if self.cs_flag == 1 and cs_INC == 1:
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
            write_str += "cs_mode  "
            write_str += "md" + str(self.moving_direction)
            write_str += "next:(" + str(self.next_location.x) + " , " + str(self.next_location.y) + ") "
        elif self.turn_num !=0 and borad_mode == 0:
            self.turn_md()
            if self.num == 2:
                # print("o")
                self.num = self.num

            write_str += "type0  "
            write_str += "turn_num:"+str(self.turn_num) + "  "
            write_str += "md" + str(self.moving_direction) + "  "
        elif self.check_board() ==0 and borad_mode == 0:
            #self.cs_flag = 0
            if self.num == 2:
                # print("o")
                self.num = self.num
            if self.traversed_distance >= 1000 / 2:
                # max_range = 330
                l = 330 - self.traversed_distance
                min_d = l
                for i in range(3):
                    md_next = self.moving_direction + i - 1
                    if md_next < 0:
                        md_next = 7
                    if md_next >= 8:
                        md_next = 0
                    loc_next = Location(self.location.x,self.location.y)
                    if md_next == 0:
                        loc_next.update(0, 1)
                    elif md_next == 1:
                        loc_next.update(1, 1)
                    elif md_next == 2:
                        loc_next.update(1, 0)
                    elif md_next == 3:
                        loc_next.update(1, -1)
                    elif md_next == 4:
                        loc_next.update(0, -1)
                    elif md_next == 5:
                        loc_next.update(-1, -1)
                    elif md_next == 6:
                        loc_next.update(-1, 0)
                    elif md_next == 7:
                        loc_next.update(-1, 1)
                    if loc_next.x < 0 or loc_next.x >= 100 or loc_next.y < 0 or loc_next.y > 100:
                        continue
                    # a error may happen such as loc:(0,0),dir = 5
                    ll = self.start_location.loc_length(loc_next)
                    if abs(l - ll) < min_d:
                        min_d = abs(l - ll)
                        self.moving_direction = md_next

            else:
                apf_l = []
                apl_len = 3
                apf_lx = np.zeros(apl_len * apl_len)
                apf_ly = np.zeros(apl_len * apl_len)
                apf_now = []
                apf_abs_max = 0.0001
                apf_l_angle = np.zeros(apl_len * apl_len)
                apf_max = []
                threat_flag = 0
                for i in range(apl_len):
                    for j in range(apl_len):
                        apf = np.zeros(2)
                        for tar in self.target_list_local :
                            if tar.type >0:
                                apf -= self.type0_getapf(tar.location,i-(apl_len-1)/2,j-(apl_len-1)/2)

                        if test_mode == 1:
                            srtest = [self.num, self.traversed_distance, i, j]
                            print(srtest)
                            print(apf)

                        b = 0
                        sum_x =0
                        sum_y =0
                        if HAPF_ACO == 1:
                            for a in self.threat_list_local:
                                f_t = self.type1_getapf(a.loc, i - (apl_len - 1) / 2, j - (apl_len - 1) / 2, a.r)
                                apf += f_t
                                if abs(f_t[0]) + abs(f_t[1]) > 0 and i == (apl_len - 1) / 2 and j == (apl_len - 1) / 2:
                                    threat_flag = 1
                            for a in self.swarm_info:
                                apf += self.type4_getapf(a.location, i - (apl_len - 1) / 2,
                                                         j - (apl_len - 1) / 2)
                        else:
                            for a in self.search_list_local:
                                sum_x += a[0]
                                sum_y += a[1]
                                if s_mode == 1:
                                    apf += self.type3_getapf(Location(a[0], a[1]), i - (apl_len - 1) / 2,j - (apl_len - 1) / 2, b // 10)
                                elif b %10 == 9:
                                    #apf += self.type3_getapf(Location(sum_x/10,sum_y/10),i-(apl_len-1)/2,j-(apl_len-1)/2,b//10)
                                    sum_x = 0
                                    sum_y = 0
                                b +=1
                            if test_mode == 1:
                                print(apf)
                            b = 0
                            sum_x = 0
                            sum_y = 0
                            for a in self.swarm_info:
                                b = 0
                                sum_x = 0
                                sum_y = 0
                                d = []
                                if a.cs_flag == 1:
                                    apf += self.type4_getapf(a.next_location, i - (apl_len - 1) / 2,
                                                             j - (apl_len - 1) / 2)
                                for c in a.search_list_local:

                                    sum_x += c[0]
                                    sum_y += c[1]

                                    if s_mode == 1:
                                        apf += self.type3_getapf(Location(c[0],c[1]), i - (apl_len - 1) / 2,j - (apl_len - 1) / 2, b // 10)

                                    elif b % 10 == 9:
                                        apf += self.type3_getapf(Location(sum_x / 10, sum_y / 10), i - (apl_len-1)/2, j - (apl_len-1)/2, b // 10)
                                        sum_x = 0
                                        sum_y = 0
                                    b += 1
                                    if b == len(a.search_list_local):
                                        apf += self.type4_getapf(Location(c[0], c[1]), i - (apl_len - 1) / 2,j - (apl_len - 1) / 2)
                                if s_mode == 0:
                                    apf += self.type3_getapf(Location(sum_x / 10, sum_y / 10), i - (apl_len - 1) / 2, j - (apl_len - 1) / 2, b // 10)
                            if test_mode == 1:
                                print(apf)
                            for a in self.threat_list_local:
                                f_t = self.type1_getapf(a.loc,i-(apl_len-1)/2,j-(apl_len-1)/2,a.r)
                                apf  +=f_t
                                if  abs(f_t[0]) + abs(f_t[1]) >0 and i ==(apl_len-1)/2 and j ==(apl_len-1)/2:
                                    threat_flag =1
                        if borad_mode == 1:
                            uav_x0 ,uav_y0 = self.location.x,self.location.y
                            if uav_x0 < 5 and uav_y0 < 5:
                                apf += np.asarray([5,5])
                            elif uav_x0 <5 and uav_y0 >95 :
                                apf += np.asarray([5,-5])
                            elif uav_x0 <5:
                                apf += np.asarray([5,0])
                            elif uav_y0 <5 and uav_x0 >95:
                                apf += np.asarray([-5,5])
                            elif uav_y0 <5:
                                apf += np.asarray( [0,5])
                            elif uav_x0 >95 and uav_y0 >95:
                                apf += np.asarray([-5,-5])
                            elif uav_x0 > 95:
                                apf += np.asarray([-5,0])
                            elif uav_y0 >95 :
                                apf += np.asarray([0,-5])
                            else:
                                apf = apf
                        if test_mode == 1:
                            print(apf)
                        apf_absxx2 = apf[0] * apf[0] + apf[1] * apf[1]
                        if apf_absxx2 > apf_abs_max:
                            apf_max = apf
                            apf_abs_max = apf_absxx2
                        apf_lx[i*apl_len + j] = apf[0]
                        apf_ly[i*apl_len + j] = apf[1]
                        if apf[1] == 0 and apf [0] == 0:
                            apf_l_angle[i*apl_len + j] = 0
                        else:
                            if apf[0] == 0:
                                if apf[1] >0:
                                    apf_l_angle[i * apl_len + j] = math.pi / 2
                                else:
                                    apf_l_angle[i * apl_len + j] = -math.pi / 2
                            else:
                                if apf[1] < 0:

                                    apf_l_angle[i * apl_len + j] = math.atan(apf[1] / apf[0])- math.pi
                                else:
                                    apf_l_angle[i * apl_len + j] = math.atan(apf[1] / apf[0])
                        apf_l.append(apf)
                        if i ==(apl_len-1)/2 and j ==(apl_len-1)/2:
                            apf_now = apf
                q0 = random.random()*9
                #q0 = random.random() * math.pi/36
                #print(q0,apf_ly.std()**2 + apf_lx.std()**2)
                q2 = apf_ly.std()**2 + apf_lx.std()**2
                q1 = 0
                apf_l_a_mean = apf_l_angle.mean()
                for apf_a in apf_l_angle:
                    abs_a = abs(apf_a - apf_l_a_mean)
                    if abs_a >= math.pi:
                        abs_a -= math.pi
                    q1 = q1 + abs_a**2
                q1 = (q1 / apl_len / apl_len) **0.5
                apf_nowxx2 = apf_now[0]**2 + apf_now[1]**2
               # if 0 :
                #if q0 > q2 or threat_flag >0 or q1 < math.pi / 8:
                if(HAPF_ACO==1 and   apf_nowxx2 /apf_abs_max > random.random()) or  ( HAPF_ACO==0 and ( q1 < math.pi / 8) and apf_nowxx2 > 1) or threat_flag > 0 :
                #if q0 > q1 :
                    #print("ok")
                    #apf_now = apf_max
                    #if threat_flag >0:
                      #  print("ok")
                    angle_f = 0
                    if apf_now[0] == 0 and apf_now[1] == 0:
                        a = 0
                    else:
                        if apf_now[0] == 0:
                            if apf_now[1] >0:

                                angle_f = math.pi / 2
                            else:
                                angle_f = -math.pi / 2
                        else:
                            angle_f = math.atan(apf_now[1] / apf_now[0])
                            if apf_now[0] <0:
                                angle_f = angle_f - math.pi
                        a = dir_list [self.moving_direction] - angle_f

                    while a > 3.1415926:
                        a -= 3.1415926*2
                    while a < -3.1415926:
                        a += 3.1415926*2

                    #a = 0

                    if a < -0.392699075:
                        self.moving_direction -= 1
                        self.basic_q *= 0.9

                    elif a > 0.392699075:
                        self.moving_direction += 1
                        self.basic_q *= 0.9
                    else:
                        self.basic_q *= 1.1



                    if self.basic_q < math.pi / 72:
                        self.basic_q = math.pi / 72
                    elif  self.basic_q > math.pi / 18:
                        self.basic_q = math.pi / 18
                    self.check_moving_direction()

                    self.apf_before = apf_now
                    write_str += "type2  "
                    write_str += "apf_list:  "
                    for i in range(apl_len*apl_len):
                        write_str += "("+str(apf_lx[i])+","+str(apf_ly[i])+")  "
                    write_str += "md" + str(self.moving_direction) + "  "
                    write_str += "angle_f:" + str(angle_f) + "  "
                    write_str += "a:" + str(a) + " "
                    write_str += "q0:"+ str(q0) + " " + "q1:"+ str(q1) + " " + "q2:"+ str(q2) + " "
                    write_str += "threat_flag "
                    write_str += str(threat_flag)
                elif HAPF_ACO == 1:
                    write_str += "type3  "
                    write_str += "md" + str(self.moving_direction) + "  "
                    ph_list = []

                    for i in range (3):
                        md_next = self.moving_direction + i - 1
                        if md_next < 0:
                            md_next = 7
                        if md_next >= 8:
                            md_next = 0
                        loc_next = Location(self.location.x,self.location.y)
                        if md_next == 0:
                            loc_next.update(0, 1)
                        elif md_next == 1:
                            loc_next.update(1, 1)
                        elif md_next == 2:
                            loc_next.update(1, 0)
                        elif md_next == 3:
                            loc_next.update(1, -1)
                        elif md_next == 4:
                            loc_next.update(0, -1)
                        elif md_next == 5:
                            loc_next.update(-1, -1)
                        elif md_next == 6:
                            loc_next.update(-1, 0)
                        elif md_next == 7:
                            loc_next.update(-1, 1)
                        if loc_next.x < 0 or loc_next.x >= 100 or loc_next.y < 0 or loc_next.y >= 100:
                            continue
                        ph_list.append(self.pheromone.pheromone[loc_next.y][loc_next.x] * (-(i-1)**2 +1.5))
                    q = random.random()
                    ph_np = np.array(ph_list)
                    sum_p = sum(ph_list)
                    # if len(ph_list) >0 and ph_np.mean()!=0:
                    #     print(ph_np.std() / ph_np.mean())
                    if len(ph_list) >0 :
                        pd  = 0
                        for i in range(len(ph_list)):
                            pd += ph_list[i]/sum_p
                            if pd >= q:
                                break
                        md_next = self.moving_direction + i - 1
                        if md_next < 0:
                            md_next = 7
                        if md_next >= 8:
                            md_next = 0
                    self.moving_direction =md_next

        #
        else:
            write_str += "type1  "
            write_str += "md" + str(self.moving_direction) + "  "
        self.traversed_distance += 1

        self.search_list_local.append([self.location.x,self.location.y])
        if self.cs_countdown >0 :
            #self.cs_countdown -=1
            self.cs_countdown = 0
        if write_file_flag == 1:
            write_str += os.linesep
            self.file_data_out.write(write_str)
            if self.traversed_distance == 250:
                self.file_data_out.close()
    def check_board(self):
        flag = 0
        if (self.moving_direction == 0 or self.moving_direction ==1 or self.moving_direction ==7) and self.location.y > 95:
            flag = 1
            if self.location.x <50:
                self.moving_direction +=1
                self.turn_num = -6
            else:
                self.moving_direction -=1
                self.turn_num =6
        elif (self.moving_direction == 1 or self.moving_direction ==2 or self.moving_direction ==3) and self.location.x > 95:
            flag = 1
            if self.location.y <50:
                self.moving_direction -= 1
                self.turn_num = 6
            else:
                self.moving_direction += 1
                self.turn_num = -6
        elif (self.moving_direction == 3 or self.moving_direction ==4 or self.moving_direction ==5) and self.location.y < 5:
            flag = 1
            if self.location.x > 50:
                self.moving_direction += 1
                self.turn_num = -6
            else:
                self.moving_direction -= 1
                self.turn_num = 6
        elif (self.moving_direction == 5 or self.moving_direction ==6 or self.moving_direction ==7) and self.location.x < 5:
            flag = 1
            if self.location.y > 50:
                self.moving_direction -= 1
                self.turn_num = 6
            else:
                self.moving_direction += 1
                self.turn_num = -6
        self.check_moving_direction()
        return flag
    def turn_md(self):
        if self.turn_num == 6 or self.turn_num == 1 or self.turn_num == 2:
            self.moving_direction -=1
        if self.turn_num == -6 or self.turn_num == -1 or self.turn_num == -2:
            self.moving_direction +=1
        if self.turn_num >0:
            self.turn_num-=1
        if self.turn_num <0:
            self.turn_num+=1
        self.check_moving_direction()
    def check_moving_direction(self):
        if self.moving_direction > 7:
            self.moving_direction = 0
        if self.moving_direction < 0:
            self.moving_direction = 7
    def type0_getapf(self,location_target,shift_x,shift_y):
        x0 = self.location.x - shift_x
        y0 = self.location.y - shift_y
        l = location_target.loc_length(Location(x0,y0))
        rel = np.zeros(2)
        if l < self.type0_l0:
            rel[0] = md_dict[self.moving_direction][0] * self.type0_index0
            rel[1] = md_dict[self.moving_direction][1] * self.type0_index0
        elif l < self.type0_l1:
            rel[0] = (x0 - location_target.x) * self.type0_k_apf / (l ** 2.5)
            rel[1] = (y0 - location_target.y) * self.type0_k_apf / (l ** 2.5)
        return rel
    def type3_getapf(self,location_target,shift_x,shift_y,num):
        x0 = self.location.x - shift_x
        y0 = self.location.y - shift_y
        l = location_target.loc_length(Location(x0,y0))

        rel = np.zeros(2)
        td = self.traversed_distance // 10 + 1
        # if num >= td:
        #     return rel
        if l < self.type3_l0:
            rel[0] = md_dict[self.moving_direction][0] * self.type3_index0
            rel[1] = md_dict[self.moving_direction][1] * self.type3_index0
        elif l < self.type3_l1:
            rel[0] = (x0- location_target.x) * self.type3_k_apf / (l ** 3.5)
            rel[1] = (y0 - location_target.y) * self.type3_k_apf / (l ** 3.5)
        rel[0] =rel[0]*math.exp(num / td-1)
        rel[0] = rel[1] * math.exp(num / td-1)
        return rel
    def type1_getapf(self,location_threat,shift_x,shift_y,r):
        x0 = self.location.x - shift_x
        y0 = self.location.y - shift_y
        l = location_threat.loc_length(Location(x0, y0))
        if l == 0:
            x0 = md_dict[self.moving_direction][0] * self.type1_index0
            y0 = md_dict[self.moving_direction][1] * self.type1_index0
            return (-x0, -y0)
        rel = np.zeros(2)
        if l < self.type1_l0+r:
            rel[0] = (x0-location_threat.x)/(l**0.5) * (1/(l**2)-1/(self.type1_l0**2)) * self.type1_k_apf
            rel[1] = (y0 - location_threat.y) / (l ** 0.5) * (1 / (l ** 2) - 1 / (self.type1_l0 ** 2)) * self.type1_k_apf
        return -rel
    def type4_getapf(self,location_threat,shift_x,shift_y):
        x0 = self.location.x - shift_x
        y0 = self.location.y - shift_y
        l = location_threat.loc_length(Location(x0, y0))
        if l == 0:
            x0 = md_dict[self.moving_direction][0] * self.type4_index0
            y0 = md_dict[self.moving_direction][1] * self.type4_index0
            return (-x0,-y0)
        rel = np.zeros(2)
        if l < self.type4_l1:
            rel[0] = (x0-location_threat.x)/(l**0.5) * (1/(l**2)-1/(self.type4_l0**2)) * self.type4_k_apf
            rel[1] = (y0 - location_threat.y) / (l ** 0.5) * (1 / (l ** 2) - 1 / (self.type4_l0 ** 2)) * self.type4_k_apf
        return -rel
        #return  0