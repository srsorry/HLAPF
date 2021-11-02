
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import math
from Target import Target
from General import Location
from General import Threat
from General import Speed
from UAV_new import UAV_1125
from Environmance import EnV
from CS import Part
from CS import CS
#import tensorflow as tf
from TPM import TPM
# km
import csv
import datetime
from General import Globalvar
import os
env = EnV(100,100)
threat_init = [
    [1,10,40,3],
    [2,30,85,4],
    [3,60,30,6],
    [4,30,15,3],
    [5,70,85,3]
]
""""
target_init_ = [
    [1,80,70,1,3,0,0],
    [2,15,30,1,3,0,0],
    [3,45,50,1,2,0,0],
    [4,70,20,1,4,0,0],
    [5,30,40,2,3,0.03,0],
    [6,15,90,2,1,0.02,0],
    [7,40,10,2,3,0.04,0],
    [8,85,30,2,5,0.05,0],
    [9,8,15,3,2,0.01,1],
    [10,55,20,3,3,0.02,1.7],
    [11,60,85,3,4,0.025,4],
    [12,25,70,3,3,0.03,5],
    [13,65,60,4,1,0,0],
    [14,20,30,4,2,0,0],
    [15,40,80,4,1,0,0],
    [16,75,40,4,2,0,0],
    #add target
    [17, 5, 70, 5, 3, 0, 0],
    [18, 70, 5, 5, 3, 0, 0],
    [19, 40, 40, 5, 2, 0, 0],
    [20, 20, 20, 5, 4, 0, 0]
]
"""
target_init_ = [
    [1,80,70,1,3,0,0],
    [2,15,30,1,3,0,0],
    [3,45,50,1,2,0,0],
    [4,70,20,1,4,0,0],
    [5,30,40,2,3,0.03,0],
    [6,15,90,2,1,0.02,0],
    [7,40,10,2,3,0.04,0],
    [8,85,30,2,5,0.05,0],
    [9,8,15,3,2,0.01,1],
    [10,55,20,3,3,0.02,1.7],
    [11,60,85,3,4,0.025,4],
    [12,25,70,3,3,0.03,5],
    [13,65,60,4,1,0,0],
    [14,20,30,4,2,0,0],
    [15,40,80,4,1,0,0],
    [16,75,40,4,2,0,0],
    #add target
    [17, 5, 70, 5, 3, 0, 0],
    [18, 70, 5, 5, 3, 0, 0],
    [19, 40, 40, 5, 2, 0, 0],
    [20, 20, 20, 5, 4, 0, 0]
]


loop_max = 10   #循环次数
find_num = 0
uav_total = 10  #无人机总数
#attack_list_250 = np.zeros(250)
#coverage_all_250 = np.zeros(250)

attack_list_250 = np.zeros(10000)
coverage_all_250 = np.zeros(10000)

coverage_all = 0
file_data_out1 = open("uav_num_attack"+".txt","w")
file_data_out2 = open("coverage"+".txt","w")
disable_time = 150
file_data_out3 = open("target_95_time.txt","w")
for loop_num in range(loop_max):
    attack_num_now = 0
    coverage_now = 0
    time_start = datetime.datetime.now()
    coverage_matrix = np.zeros((100,100))

    #exit(0)
    target_list = []
    threat_list = []
    target_track_list = []
    target_attack_list_x = []
    target_attack_list_y = []
    target_attack_list_ =[]
    for i in target_init_:
        t = Target(i[0],i[3],i[4],Location(i[1],i[2]),i[5]*10,i[6])
        target_track_list.append([t.location.x])
        target_track_list.append([t.location.y])
        target_list.append(t)
    for i in threat_init:
        t = Threat(Location(i[1],i[2]),i[3])
        threat_list.append(t)
    UAV_init_ = [
        [1,10,10,0],
        [2,90,90,0],
        [3,30,30,0],
        [4,50,50,0],
        [5,70,70,0],
        [6,10,90,0],
        [7, 30, 70, 0],
        [8, 70, 30, 0],
        [9, 90, 10, 0],
        [10 , 20,20,0],
        [11, 80 ,80 ,0],
        [12, 20,80,0],
        [13,80,20,0],
        [14,20,20,0],
        [15,80,80,0],
        [16,40,60,0],
        [17,60,40,0],
        [18,35,80,0],
        [19,35,35,0],
        [20,80,35,0],
        [21,5,95,0],
        [22, 15, 85, 0],
        [23, 25, 75, 0],
        [24, 35, 65, 0],
        [25, 45, 55, 0],
        [26, 55, 45, 0],
        [27, 65, 35, 0],
        [28, 75, 25, 0],
        [29, 85, 15, 0],
        [30, 95, 5, 0]
    ]






    #
    '''
    for i in range(4):
        while(1):
            xx = math.floor(random.random()*100)
            yy = math.floor(random.random()*100)
            for m in threat_init:
                if (xx - m[1])**2 + (yy-m[2])**2 < m[3] **2:
                    continue
            break
        UAV_init_.append([i+6,xx,yy,0])
    '''
    #
    UAV_list = []
    UAV_track_list = []
    tpm_i = TPM(100,100,target_init_)
    sr_i = 0
    for i in UAV_init_:
        xx = math.floor(random.random() * 100)
        yy = math.floor(random.random() * 100)
        #u = UAV_1125(i[0],i[3],Location(xx,yy))
        u = UAV_1125(i[0],i[3],Location(i[1],i[2]))
        u.tpm = tpm_i
        UAV_list.append(u)
        UAV_track_list.append([u.location.x])
        UAV_track_list.append([u.location.y])
        for j in target_init_:
            if j[3] <3:
                s =0

            elif j[3] ==4 or j[3] == 5:
                continue
            else:
                s = j[5] * 10
            t = Target(j[0], j[3], j[4], Location(j[1], j[2]),s, j[6])
            u.target_list_local.append(t)
        sr_i +=1
        if sr_i >= uav_total:
            break

    cs = CS(uav_total,100)
    cs.uav_list = UAV_list
    #for i in range(250):
    for i in range(250):
        #print(i)
        #
        # 加入扰动

        if i == disable_time:
            #让1/3的无人机失效
            unable_uav_num = 0
            #while unable_uav_num <= len(UAV_list)//3:
            while unable_uav_num <= 2:
                random_uav = random.random() * uav_total
                random_uav = math.floor(random_uav)
                if UAV_list[random_uav].type == 0:
                    #print(UAV_list[random_uav].num,"unable")
                    UAV_list[random_uav].type =1
                    unable_uav_num +=1

        cs.update_search_map()
        target_attack_know_num = 0
        for j in range(9):
            if target_list[j].type ==0:
                target_attack_know_num += 1
        if target_attack_know_num >= 8:
            s_map_rel = cs.search_map_check()
        #if i %3 == 1:
           # cs.uav_num_check()

        for j in target_list:
            for k in UAV_list:
                if k.type >0 :
                    continue
                length = j.location.loc_length(k.location)
                #if length <= 3 & j.type > 0:
                if abs(j.location.x - k.location.x) <=3 and abs(j.location.y - k.location.y) <=3 and  j.type > 0 :
                    j.target_attack()
                    target_attack_list_x.append(j.location.x)
                    target_attack_list_y.append(j.location.y)
                    target_attack_list_.append([j,k,i])
                    for attack_i in range(250 - i):
                        attack_list_250 [249 - attack_i] +=1
                    attack_num_now += 1
        #update

        p = 0
        for j in UAV_list:
            if j.type >0:
                continue
            j.get_swarm_info(UAV_list)
            j.update_threat_list_local(threat_list)
            j.make_decision()

            #j.pheromone.update_auto(j.location)
            j.update_target_list_local()
            j.update_location_auto()
            UAV_track_list[2*p].append(j.location.x)
            UAV_track_list[2 * p + 1].append(j.location.y)
            p = p +1
            loc_uav_x = j.location.x
            loc_uav_y = j.location.y

            for x in range(7):
                for y in range(7):
                    a_x = loc_uav_x - x +3
                    a_y = loc_uav_y - y +3
                    if a_x >= 0 and a_x < 100 and a_y >= 0 and a_y < 100:
                        coverage_matrix[a_x,a_y] = 1

            # j.update_moving_direction_auto()
        p = 0
        for j in target_list:
            j.update_location_auto()
            target_track_list[2 * p].append (j.location.x)
            target_track_list[2 * p + 1].append(j.location.y)
            p = p + 1
        coverage_now = coverage_matrix.sum()
        coverage_all_250[i] += coverage_now
        write_str1 = str(attack_num_now) + " "
        write_str2 = str(coverage_now) + " "

        file_data_out1.write(write_str1)
        file_data_out2.write(write_str2)
        '''
        if attack_num_now >= 14:
            write_str3 = str(i) + " "
            file_data_out3.write(write_str3)
            break
        '''
    write_str1 = os.linesep
    write_str2 = os.linesep
    file_data_out1.write(write_str1)
    file_data_out2.write(write_str2)
    find_num += len(target_attack_list_x)
    coverage_all += coverage_matrix.sum()
    time_end = datetime.datetime.now()
    if loop_num % 5 == 0:
        print(loop_num)
        print((time_end - time_start).seconds)

    #print(coverage_matrix.sum())
print(find_num / loop_max)
print(attack_list_250)
print(coverage_all / 100 /100 / loop_max)
print(coverage_all_250)




plt.figure()
color_list = [
'#F0F8FF',
'#FAEBD7',
'#00FFFF',
'#7FFFD4',
'#F0FFFF',
'#F5F5DC',
'#FFE4C4',
'#000000',
'#FFEBCD',
'#0000FF',
'#8A2BE2',
'#A52A2A',
'#DEB887',
'#5F9EA0',
'#7FFF00',
'#D2691E',
'#FF7F50',
'#6495ED',
'#FFF8DC',
'#DC143C',
'#00FFFF',
'#00008B',
'#008B8B',
'#B8860B',
'#A9A9A9',
'#006400',
'#BDB76B',
'#8B008B',
'#556B2F',
'#FF8C00',
'#9932CC',
'#8B0000',
'#E9967A',
'#8FBC8F',
'#483D8B',
'#2F4F4F',
'#00CED1',
'#9400D3',
'#FF1493',
'#00BFFF',
'#696969',
'#1E90FF',
'#B22222',
'#FFFAF0',
'#228B22',
'#FF00FF',
'#DCDCDC',
'#F8F8FF',
'#FFD700',
'#DAA520',
'#808080',
'#008000',
'#ADFF2F',
'#F0FFF0',
'#FF69B4',
'#CD5C5C',
'#4B0082',
'#FFFFF0',
'#F0E68C',
'#E6E6FA',
'#FFF0F5',
'#7CFC00',
'#FFFACD',
'#ADD8E6',
'#F08080',
'#E0FFFF',
'#FAFAD2',
'#90EE90',
'#D3D3D3',
'#FFB6C1',
'#FFA07A',
'#20B2AA',
'#87CEFA',
'#778899',
'#B0C4DE',
'#FFFFE0',
'#00FF00',
'#32CD32',
'#FAF0E6',
'#FF00FF',
'#800000',
'#66CDAA',
'#0000CD',
'#BA55D3',
'#9370DB',
'#3CB371',
'#7B68EE',
'#00FA9A',
'#48D1CC',
'#C71585',
'#191970',
'#F5FFFA',
'#FFE4E1',
'#FFE4B5',
'#FFDEAD',
'#000080',
'#FDF5E6',
'#808000',
'#6B8E23',
'#FFA500',
'#FF4500',
'#DA70D6',
'#EEE8AA',
'#98FB98',
'#AFEEEE',
'#DB7093',
'#FFEFD5',
'#FFDAB9',
'#CD853F',
'#FFC0CB',
'#DDA0DD',
'#B0E0E6',
'#800080',
'#FF0000',
'#BC8F8F',
'#4169E1',
'#8B4513',
'#FA8072',
'#FAA460',
'#2E8B57',
'#FFF5EE',
'#A0522D',
'#C0C0C0',
'#87CEEB',
'#6A5ACD',
'#708090',
'#FFFAFA',
'#00FF7F',
'#4682B4',
'#D2B48C',
'#008080',
'#D8BFD8',
'#FF6347',
'#40E0D0',
'#EE82EE',
'#F5DEB3',
'#FFFFFF',
'#F5F5F5',
'#FFFF00'
]
for i in threat_list:
    r = i.r
    theta = np.arange(0,2*np.pi,0.01)
    x = i.loc.x+r*np.cos(theta)
    y = i.loc.y + r*np.sin(theta)
    plt.plot(x,y)
    plt.plot(x,-y)
for i in range(20):
    plt.plot(target_track_list[2*i], target_track_list[2*i+1],'b-')
for i in range(uav_total):

    plt.plot(UAV_track_list[2 * i], UAV_track_list[2 * i + 1],'k--', color=color_list[2*i+1])
if target_attack_list_x :
    plt.plot(target_attack_list_x,target_attack_list_y,'k+')
plt.axis("scaled")
plt.axis([0,100,0,100])

plt.savefig('1.png')
for i in target_attack_list_:
    print ('Target',i[0].num,'in run ',i[2],'attacked by UAV',i[1].num,'in location (',i[0].location.x,',',i[0].location.y,')')
print(UAV_track_list)

np.savetxt("search_map.txt",cs.search_map)


