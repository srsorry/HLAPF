import math
from General import Location
#from UAV import UAV
class TPM:
    L = 0
    W = 0
    tpm = []
    #km
    def __init__(self , l , w , target_list):
        self.L = l
        self.W = w
        self.tpm =[]
        if l*w >0 :
            for i in range(l):
                self.tpm.append([4/l/w]*w)


            for i in target_list:
                if i[3] == 1:
                    self.type1_init(5,2,50,i[1],i[2])
                if i[3] == 2:
                    self.type2_init(5,2,i[5],50,i[1],i[2])
                if i[3] == 3:
                    self.type3_init(5,2,i[5],50,i[6],i[1],i[2])

            #normalization
            sum_tpm = sum(sum(i) for i in self.tpm)
            for i in range(l):
                for j in range(w):
                    self.tpm [i][j] /= sum_tpm


        #[1,80,70,1,3,0,0],
    #  1:Target has unknown speed and unknown direction
    #  2:Target has known speed and unknown direction
    #  3:Target has known speed and known direction
    #  4:Target is still
    def type1_init(self,a0,ae,t0,target_x,target_y):
        m = a0 * a0 + ae * ae * t0
        m = m *2
        for i in range (self.L):
            for j in range (self.W):
                # 5x5
                sum = 0
                for p in range(5):
                    for q in range (5):

                        pdf = math.exp(- (i - target_x + p/4) **2 / m + (j - target_y + q/4) **2 / m) / m / math.pi
                        sum = sum + pdf
                sum = sum /25
                self.tpm[i][j] = self.tpm[i][j] + sum
    def type2_init(self,a0,ae,v,t0,target_x,target_y):
        #select 0,1/4,1/2...
        angle_list = [0,1/4* math.pi,1/2* math.pi, math.pi,5/4* math.pi,3/2* math.pi,7/4* math.pi]
        for i in range (self.L):
            for j in range (self.W):
                # 5x5
                sum = 0
                for p in range(5):
                    for q in range (5):
                        #pdf
                        pdf = 0
                        x = i + p/4
                        y = j + q/4
                        for angle in angle_list:
                            pdf = pdf + math.exp(-((-target_x+v*t0*math.cos(angle)+x) ** 2   + (-target_y+v*t0*math.sin(angle)+y) ** 2 )/2/(a0*a0))
                        pdf = pdf / 8 /((2*math.pi*a0)**2)
                        sum = sum + pdf
                sum = sum / 25
                self.tpm[i][j] = self.tpm[i][j] + sum
    def type3_init(self,a0,ae,v,t0,angle,target_x,target_y):
        m = 2 * a0 * a0
        for i in range (self.L):
            for j in range (self.W):
                # 5x5
                sum = 0
                for p in range(5):
                    for q in range (5):
                        pdf = math.exp(- (i - target_x + p/4 - v*t0*math.cos(angle)) **2 / m + (j - target_y + q/4 - v*t0*math.sin(angle)) **2 / m) / m / math.pi
                        sum = sum + pdf
                sum = sum / 25
                self.tpm[i][j] = self.tpm[i][j] + sum




class Pheromone:
    L = 0
    W = 0
    pheromone = []
    index = 0
    def __init__(self,l,w,i):
        self.L = l
        self.W = w
        self.index = i
        self.pheromone = []
        for i in range(w):
            self.pheromone.append([1]*l)
        #self.pheromone = [[1]*l]*w
    def chips(self,max_,min_):
        for i in range(self.W):
            for j in range(self.L):
                if self.pheromone[j][i] > max_:
                    self.pheromone[j][i] = max_
                if self.pheromone[j][i] < min_:
                    self.pheromone[j][i] = min_
    def update_auto(self,location:Location):
        R = 3
        x = location.x
        y = location.y

        for i in range(self.W):
            for j in range(self.L):
                d = location.loc_length(Location(i, j))
                if d <= R:
                    self.pheromone[i][j] = self.pheromone[i][j] - self.index * (81 - d**4)/81
        self.chips(200,-200)


