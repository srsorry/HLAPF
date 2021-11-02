from General import Speed
from General import Location
import random
import math

class Target:
    num = 0
    type = 0
    #  0:Target has been attacked
    #  1:Target has unknown speed and unknown direction
    #  2:Target has known speed and unknown direction
    #  3:Target has known speed and known direction
    #  4:Target is still
    #  5:Target has unknown speed and unknown direction and unknown start
    value = 0
    location = Location(0, 0)
    speed = 0
    # km/s
    moving_direction = 0

    # rad
    def hello(self):
        print(self.location, self.num, self.type)

    def __init__(self, num, type_, value, location, speed, moving_direction):
        self.type = type_
        self.num = num
        self.value = value
        self.location = location
        self.speed = speed
        self.moving_direction = moving_direction

    def update_location(self, x, y):
        self.location.update(x, y)

    def update_location_auto(self):
        if self.type == 0 or self.type == 4:
            s = Speed(0, 0)
        elif self.type == 1 or self.type == 5:
            # get_speed
            a = random.random() * 0.80 - 0.40
            b = random.random() * 0.80 - 0.40
            s = Speed(a, b)
        elif self.type == 2:
            a = random.random() * 6.283
            b = math.sin(a) * self.speed  # x
            a = math.cos(a) * self.speed  # y
            s = Speed(a, b)
        else:
            a = math.sin(self.moving_direction) * self.speed
            b = math.cos(self.moving_direction) * self.speed
            s = Speed(b, a)
        self.location.update(s.x, s.y)

    def target_attack(self):
        self.type = 0

'''
x = Target(1, 2, 3, Location(10, 10))
x.update_location(1, 1)
print(x.location.x, x.location.y)
'''