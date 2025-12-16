import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from physics_body import PhysicsBody
from star import Star
from planet import Planet
from asteroid import Asteroid
from moon import Moon
from math import pi

class SolarSystem():

    def __init__(self, stars_dict = dict(), planets_dict = dict(), asteroids_dict = dict()):
        # Dictionaries to hold physics bodies
        self.stars_dict = stars_dict
        self.planets_dict = planets_dict
        self.asteroids_dict = asteroids_dict

    # Method to display basic information of SS
    def info(self):
        if self.stars_dict.__len__() > 0:
            print("Stars:", *self.stars_dict.keys())    # Display stars
        if self.planets_dict.__len__() > 0:
            print("Planets:", *self.planets_dict.keys())    # Display Planets
            for planet_key in self.planets_dict.keys():
                planet = self.planets_dict[planet_key]
                if planet.get_moons() is not None:
                    print(f"{planet_key} Moons:", *planet.get_moons().keys())   # Display planetary moons
        if self.asteroids_dict.__len__() > 0:
            print("Asteroids:", *self.asteroids_dict.keys())    # Display asteroids

    
    # Method to perform derivative calculations (Velocity and Acceleration) of physics bodies
    def calc_derivs(self, dictionary, key): # Takes in: (dictionary for this body, key for this body)
        this_body = dictionary[key] # This body
        x,y = this_body.get_pos()   # This body's current position
        vX,vY = this_body.get_vel() # This body's current velocity
        aX = aY = 0                 # Initialize acceleration variable for this body


        if isinstance(this_body, (Planet, Asteroid)):       # "If this body is a planet or an asteroid, then..."
            for d in (self.stars_dict, self.planets_dict):  # Simulate gravity from stars and planets only
                if d.__len__() > 0: # "If dictionary is not empty, then..."
                    for k in d.keys():  # "For key in dictionary..."

                        body = d[k]             # Other body
                        x_,y_ = body.get_pos()  # Other body's current position
                        M = body.get_mass()     # Other body's mass

                        r = ((x - x_)**2 + (y - y_)**2)**0.5    # Distance between this body and other body

                        aX += -M*x/r**3 # Iteratively add acceleration from other body's gravity on this body
                        aY += -M*y/r**3 # Iteratively add acceleration from other body's gravity on this body
                        
                        if isinstance(this_body,Planet):    # "If this body is a planet, then..."
                            moons_dict = this_body.get_moons()  # Get moons for this planet
                            if moons_dict is not None:  # "If this planet has any moons, then..."
                                moon_derivs = None  # Initialize variable to hold moon derivative data

                                for moon_key in moons_dict.keys(): # "For key in dictionary..."
                                    moon = moons_dict[moon_key] # This moon
                                    moon_derivs = self.calc_derivs_moon(moon, this_body, x, y)  # Obtain moon derivatives
                                return (np.array([vX,vY,aX,aY]), moon_derivs)   # Return (this planet's derivatives, moon derivatives)

                        return np.array([vX,vY,aX,aY])  # Return this body's derivatives

        return np.array([vX,vY,aX,aY]) # Return this body's derivatives


    # Modified derivative calculator method for moons to account for their host planet's gravity only (greatly reducing computations per moon)
    def calc_derivs_moon(self, moon: Moon, planet: Planet, x_, y_): # Takes in: (this moon, host planet)
        x,y = moon.get_pos()    # This moon's current position
        vX, vY = moon.get_vel() # This moon's current velocity

        M = planet.get_mass()   # Mass of host planet

        r = ((x - x_)**2 + (y - y_)**2)**0.5    # Distance between this moon and host planet

        aX = -M*x/r**3 # Calculate acceleration of this moon due to host planet
        aY = -M*y/r**3 # Calculate acceleration of this moon due to host planet

        return np.array([vX,vY,aX,aY])  # Return this moon's derivatives


    # Euler-Cromer numerical method to advance orbits one step at a time
    def euler_cromer_step(self, dt, dictionary, key):   # Takes in: (magnitude of time step, dictionary for this body, key for this body)
        this_body = dictionary[key] # This body
        
        if isinstance(this_body,Planet) and this_body.get_moons() is not None:        # "If this body is a planet and has moons, then..."
            moons_dict = this_body.get_moons()  # Moon dictionary of this planet
            for moon_key in moons_dict.keys():  # "For key in moon dictionary..."
                moon = moons_dict[moon_key]     # This moon
            
            planet_derivs, moon_derivs = self.calc_derivs(dictionary, key)  # Obtain derivatives for this planet and moons
            vX,vY,aX,aY = planet_derivs                         # Unpackage derivatives for this planet
            moon_vX, moon_vY, moon_aX, moon_aY = moon_derivs    # unpackage derivatives for moons
            
            moon.update_pos_lists() # Update moon lists with current position
            moon.vel_step(dt,(moon_aX,moon_aY)) # Update moon velocity
            moon.pos_step(dt)                   # Update moon position

        else:   # "If not a planet OR if a planet with no moons, then..."
            vX,vY,aX,aY = self.calc_derivs(dictionary, key) # Obtain derivatives of this body

        this_body.update_pos_lists()    # Update this body's lists with current position
        this_body.vel_step(dt,(aX,aY))  # Update this body's velocity
        this_body.pos_step(dt)          # Update this body's position


    # Pass time in SS for orbits to develop
    def pass_time(self, time, dt):  # Takes in (amount of Earth years to pass, size of time steps)
        for step in np.arange(0,time,dt):   # "For each time step in time..."
            d = self.planets_dict   # Dictionary of planets in SS
            if d.__len__() > 0:     # "If dictionary is not empty, then..."
                for k in d.keys():  # "For key in planet dictionary..."
                    self.euler_cromer_step(dt, d, k)    # Perform one Euler-Cromer Step


    # Abstraction to add a star to SS
    def initialize_star(self, x, y, m, name):   # Takes in: (x0, y0, mass, name)
        new_star = Star(x,y,m)              # Instantiate Star object
        self.stars_dict[name] = new_star    # Add star to SS star dictionary

    # Abstraction to add a planet to SS
    def initialize_planet(self, x, y, m, name, vX=0, vY=0): # Takes in: (x0, y0, mass, name, v_x0, v_y0)
        if (vX and vY) == 0:    # "If initial velocities are not set (ie. equal to zero), then..."
            r = (x*x + y*y)**0.5    # Distance to origin (the Sun)
            T = r**1.5              # Period of this planet
            vX = -2*pi*y/T          # Set x-velocity for circular orbit
            vY = 2*pi*x/T           # Set y-velocity for circular orbit

        new_planet = Planet(x, y, vX, vY, m)    # Instantiate Planet object
        self.planets_dict[name] = new_planet    # Add planet to SS planet dictionary
    
    # Abstraction to add multiple planets to SS
    def inialize_planets(self, dictionary): # Takes in: (dictionary -> planet : (x, y, m, key, vX=0, vY=0))

        for key in dictionary.keys():
            values = dictionary[key].__len__()  # Use length of tuple to determine if velocity args are included
            if values < 3 or values == 4 or values > 5:
                print("3 values (x,y,m) or 5 values (x,y,m,vX,vY) needed.", values, " values given. Planet initialization skipped for", key, ".")
                pass
            elif values == 5:
                x,y,m,vX,vY = dictionary[key]
                self.initialize_planet(x, y, m, key, vX, vY)    # Initialize planet with preset velocities
            else:
                x,y,m = dictionary[key]
                self.initialize_planet(x, y, m, key)    # Initialize planet (calculate velocities for circular orbit)
    

    # Method to animate orbits over time
    def run_animation(self, speed=1, interval=20):  # Takes in: (Frames-skips per interval, ms per frame) -> to speed up animation: Increase [0] / Decrease [1]
        plt.rcParams["figure.figsize"] = (10, 10)   # Set figure size

        fig, ax = plt.subplots(1,1) # Create figure with one subplot
        line_dict = {}  # Initialize dictionary for line "artists"

        max_distance = 0    # Initialize variable for value largest radius

        for planet_key in self.planets_dict.keys(): # "For key in planet dictionary..."
            planet = self.planets_dict[planet_key]  # This planet

            # Create line (path) and dot (position) artists for this planet
            (new_line,) = ax.plot([],[], lw=2)  # Create empty line artist for this planet's path (X,Y)
            
            planet_mass = planet.get_mass() # This planet's mass
            dot_type = '.'  # Set default dot type for this planet's position
            if planet_mass >= 10*(4*pi**2)*(6e24/2e30): # If planet's mass is >= 10x Earth's mass (aka. a gas giant)
                dot_type = 'o'  # Set dot type to larger dot for gas giants
            (new_dot,) = ax.plot([],[], marker=dot_type)    # Create empty line artist for this planet's position (x,y)
                
            line_dict[planet_key] = (new_line,new_dot)  # Add (line, dot) artists tuple to line dictionary for this planet

            # Update maximum orbit radius in SS if necessary
            x_list,y_list = planet.get_pos_lists()  # This planet's orbit path
            # If planet's x or y radii exceed current max orbit, set as max orbit
            if (max(x_list)) > max_distance:
                max_distance = max(x_list)
            if (max(y_list)) > max_distance:
                max_distance = max(y_list)


            # Create moon position artists as necessary
            if planet.get_moons() is not None:  # Check if moons exist for this planet
                m_dict = planet.get_moons() # Host planet moon dictionary
                for moon_key in m_dict.keys():  # "For key in moon dictionary..."
                    moon = m_dict[moon_key]                          # This moon
                    (moon_dot,) = ax.plot([],[], marker='.')         # Create dot artist for moon possition
                    line_dict[moon] = moon_dot                       # Add moon artist to line dictionary

                    ## TEMPORARY HARD-CODE FIX FOR BROKEN MOON PHYSICS
                    planet.moon_orbit_quick_fix(moon_key, num_of_orbits=12) # Hard-code circular moon path around host-planet


        print(f"Maximum orbit radius in Solar System: {max_distance} AUs")

        for planet in self.planets_dict.keys(): # Obtain path list length via arbitrary planet's list
            frames = int(self.planets_dict[planet].get_list_length()/speed) # Set number of animation frames to number of position steps in path lists for all physics bodies
            print(f"Number of frames of animation: {frames}")
            break   # Break after one iteration

        # Set figure boundaries according to maximum orbit radius within SS
        ax.set_xlim(1.1*(-max_distance), 1.1*(max_distance))    # from -110% to 110% of maximum orbit value
        ax.set_ylim(1.1*(-max_distance), 1.1*(max_distance))    # from -110% to 110% of maximum orbit value

        def update_figure(frame):   # Inner update function for FuncAnimation. Takes in: (Current frame)
            nonlocal speed  # Use nonlocal speed argument from parent function params
            tail = 0        # Initialize list-tail value
            frame *= speed  # Increase speed of animation by skipping number of frames equal to `speed`

            # Update tail length as orbits progress
            if frame > 200:
                tail = frame - 200

            # for d in (self.planets_dict):
            d = self.planets_dict   # SS dictionary of planets
            if d.__len__() > 0: # "If planets exist in SS, then..."
                for k in d.keys():  # "For key in planet dictionary..."
                    X,Y = d[k].get_pos_lists(frame) # This planet's path
                    # X,Y = d[k].get_pos_lists(frame, tail) # Apply path-tails (optional)

                    if len(X) > 0:  # Ensure path exists before generating dot
                        x,y = X[-2:-1], Y[-2:-1]    # This planet's position
                    else:
                        x,y = [],[] # Leave empty lists until path exists

                    line_dict[k][0].set_data(X,Y)   # Update artist data for this planet's path (line)
                    line_dict[k][1].set_data(x,y)   # Update artist data for this planet's position (dot)

                    if d[k].get_moons() is not None: # "If this planet has moons, then..."
                        m_dict = d[k].get_moons()   # This planet's moon dictionary
                        for moon_key in m_dict.keys():  # "For key in moon dictionary..."
                            moon = m_dict[moon_key]              # This moon
                            m_X, m_Y = moon.get_pos_lists(frame) # This moon's path
                            m_x, m_y = m_X[-2:-1], m_Y[-2:-1]    # This moon's position
                            line_dict[moon].set_data(m_x,m_y)    # Update artist data for this moon's position (dot)


            ax.set_title(f"Frame {int(frame/speed)}")  # Set title of figure using current frame's number
            return

        # Use FuncAnimation to animate orbits
        anim = FuncAnimation(fig, update_figure, frames, interval=interval) # Takes in: (figure, pointer to update method, total number of frames of animation, Interval between frames in ms)
        plt.show()  # Show figure


    ## DEVELOPER METHODS –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # Method to plot orbits (for developer use only)
    def plot_system(self):
        plt.rcParams["figure.figsize"] = (13, 13)
        for d in (self.stars_dict, self.planets_dict):
            if d.__len__() > 0:
                for k in d.keys():
                    this_body = d[k]
                    if isinstance(this_body, Star):
                        X,Y = this_body.get_pos()
                        plt.plot(X,Y,'yo')
                    else:
                        X,Y = this_body.get_pos_lists()
                        plt.plot(X,Y)
        plt.axis('equal')
        plt.show()
    ## DEVELOPER METHODS –––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––



    ## NOT FINISHED ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
    # Abstraction to add a planetary moon to SS
    def initialize_moon(self,m,name,planet_key):    # Takes in: (moon mass, name of moon, name of home_planet)
        host_planet = self.planets_dict[planet_key] # Home planet
        x_,y_ = host_planet.get_pos()   # Host planet position
        vX_,vY_ = host_planet.get_vel() # Host planet velocity


        x = x_ - 0.00257    
        y = y_  
        r = (x*x + y*y)**0.5    

        # T = (4*pi**2/(host_planet.get_mass() + m)*r**3)**0.5
        # vX = -2*pi*y/T
        # vY = 2*pi*x/T

        vX = vX_
        vY = 0.966*vY_

        new_moon = Moon(x,y,vX,vY,m)
        host_planet.add_moon((name, new_moon))
    ## NOT FINISHED ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––