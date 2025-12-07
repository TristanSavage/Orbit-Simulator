from physics_body import PhysicsBody
import numpy as np
from math import pi
import random

class Planet(PhysicsBody):  # Subclass of PhysicsBody

    def __init__(self, x: float, y: float, vX: float, vY: float, mass: float):  # Sub takes in: (..., vx_0, vy_0, ...)
        super().__init__(x,y,mass)

        self.vX = vX
        self.vY = vY
        
        self.moons_dict = dict()    # Dictionary to hold this planet's moons

    # Update position via one numerical step
    def pos_step(self, dt):
        self.x += self.vX*dt
        self.y += self.vY*dt

    # Update velocity via one numerical step
    def vel_step(self, dt, a: tuple()):
        self.vX += a[0]*dt
        self.vY += a[1]*dt

    def get_vel(self):
        return (self.vX, self.vY)


    ## Moon methods
    # Add Moon object to this planet's dictionary
    def add_moon(self, moon: tuple()):
        self.moons_dict[moon[0]] = moon[1]

    # Add list of moons to this planet's dictionary
    def add_moons(self, moons: list(tuple())):
        for moon in moons:
            self.moons_dict[moon[0]] = moon[1]

    # Return moons dictionary (returns None if empty)
    def get_moons(self):
        if self.moons_dict.__len__() == 0:
            return None
        else:
            return self.moons_dict

    # Temporary hard-code orbit path fix for this planet's moons (for use while gravity calculations are inaccurate)
    def moon_orbit_quick_fix(self, moon_key, num_of_orbits):   # Takes in: (this moon's key, number of orbits for moon to complete per Earth year)
        z = np.linspace(0, 2*pi*num_of_orbits, len(self.x_list))    # Line space with # of elements = # elements in this planet's positions lists -> One orbit per 2 pi
        x_plan_array = np.array(self.x_list)    # This planet's path (x)
        y_plan_array = np.array(self.y_list)    # This planet's path (y)
        x_array = 0.2*np.cos(z) # Initialize this moon's path (x) -> radius of orbit * cos(z)
        y_array = 0.2*np.sin(z) # Initialize this moon's path (y) -> radius of orbit * sin(z)

        # Random mechanism to determine orbit direction (CW or CCW)
        dice_roll = random.randint(a=0,b=1)
        if dice_roll > 0:
            place_holder = x_array.copy()
            x_array = y_array.copy()
            y_array = place_holder

        x_array += x_plan_array # Place this planet's path as the origin for this moon's orbit
        y_array += y_plan_array # Place this planet's path as the origin for this moon's orbit

        x_list = x_array.tolist()   # Convert arrays to lists (ensuring compatibility with this moon's position lists)
        y_list = y_array.tolist()   # Convert arrays to lists (ensuring compatibility with this moon's position lists)

        self.moons_dict[moon_key].x_list = x_list   # Overwrite this moon's position lists with hard-code paths
        self.moons_dict[moon_key].y_list = y_list   # Overwrite this moon's position lists with hard-code paths