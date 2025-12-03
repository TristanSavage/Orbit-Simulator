from physics_body import PhysicsBody
import numpy as np
from math import pi
import random

class Planet(PhysicsBody):

    def __init__(self, x: float, y: float, vX: float, vY: float, mass: float):
        super().__init__(x,y,mass)

        self.vX = vX
        self.vY = vY

        # self.x_list = []
        # self.y_list = []
        
        self.moons_dict = dict()

    # def update_pos_lists(self):
    #     self.x_list.append(self.x)
    #     self.y_list.append(self.y)

    # def get_list_length(self):
    #     return len(self.x_list)

    # def get_pos_lists(self, head=-1, tail=0) -> tuple():
    #     return (self.x_list[tail:head], self.y_list[tail:head])

    def pos_step(self, dt):
        self.x += self.vX*dt
        self.y += self.vY*dt

    def vel_step(self, dt, a: tuple()):
        self.vX += a[0]*dt
        self.vY += a[1]*dt

    def get_vel(self):
        return (self.vX, self.vY)



    def add_moon(self, moon: tuple()):
        self.moons_dict[moon[0]] = moon[1]

    def add_moons(self, moons: list(tuple())):
        for moon in moons:
            self.moons_dict[moon[0]] = moon[1]

    def get_moons(self):
        if self.moons_dict.__len__() == 0:
            return None
        else:
            return self.moons_dict

    def moon_orbit_quick_fix(self, moon_key, orbits):
        z = np.linspace(0, 2*pi*orbits, len(self.x_list))
        x_plan_array = np.array(self.x_list)
        y_plan_array = np.array(self.y_list)
        x_array = 0.2*np.cos(z)
        y_array = 0.2*np.sin(z)

        dice_roll = random.randint(a=0,b=1)
        if dice_roll > 0:
            place_holder = x_array.copy()
            x_array = y_array.copy()
            y_array = place_holder

        x_array += x_plan_array
        y_array += y_plan_array

        x_list = x_array.tolist()
        y_list = y_array.tolist()

        self.moons_dict[moon_key].x_list = x_list
        self.moons_dict[moon_key].y_list = y_list