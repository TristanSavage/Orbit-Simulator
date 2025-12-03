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
        self.stars_dict = stars_dict
        self.planets_dict = planets_dict
        self.asteroids_dict = asteroids_dict

    def info(self):
        if self.stars_dict.__len__() > 0:
            print("Stars:", *self.stars_dict.keys())
        if self.planets_dict.__len__() > 0:
            print("Planets:", *self.planets_dict.keys())
            for planet_key in self.planets_dict.keys():
                planet = self.planets_dict[planet_key]
                if planet.get_moons() is not None:
                    print(f"{planet_key} Moons:", *planet.get_moons().keys())
        if self.asteroids_dict.__len__() > 0:
            print("Asteroids:", *self.asteroids_dict.keys())

    

    def calc_derivs(self, dictionary, key):
        this_body = dictionary[key]
        x,y = this_body.get_pos()
        vX,vY = this_body.get_vel()
        aX = aY = 0


        if isinstance(this_body, (Planet, Asteroid)):
            for d in (self.stars_dict, self.planets_dict):
                if d.__len__() > 0:
                    for k in d.keys():

                        body = d[k]
                        x_,y_ = body.get_pos()
                        M = body.get_mass()
                        r = ((x - x_)**2 + (y - y_)**2)**0.5

                        aX += -M*x/r**3
                        aY += -M*y/r**3
                        
                        if isinstance(this_body,Planet):
                            moons_dict = this_body.get_moons()
                            if moons_dict is not None:
                                moon_derivs = None
                                if moons_dict.__len__() > 0:
                                    for moon_key in moons_dict.keys():
                                        moon = moons_dict[moon_key]
                                        moon_derivs = self.calc_derivs_moon(moon, this_body, x, y)
                                return (np.array([vX,vY,aX,aY]), moon_derivs)


                        return np.array([vX,vY,aX,aY])

        return np.array([vX,vY,aX,aY])

    def calc_derivs_moon(self, moon: Moon, planet: Planet, x_, y_):
        x,y = moon.get_pos()
        vX, vY = moon.get_vel()
        aX = aY = 0

        M = planet.get_mass()

        r = ((x - x_)**2 + (y - y_)**2)**0.5

        aX += -M*x/r**3
        aY += -M*y/r**3

        # if aX != 0:
        #     print("aX = ", aX)
        # if aY != 0:
        #     print("aY = ", aY)

        return np.array([vX,vY,aX,aY])



    def euler_cromer_step(self, dt, dictionary, key):
        this_body = dictionary[key]
        
        if isinstance(this_body,Planet):
            moons_dict = this_body.get_moons()
            
        if isinstance(this_body,Planet) and moons_dict is not None:
            for moon_key in moons_dict.keys():
                moon = moons_dict[moon_key]
            
            planet_derivs, moon_derivs = self.calc_derivs(dictionary, key)
            vX,vY,aX,aY = planet_derivs
            moon_vX, moon_vY, moon_aX, moon_aY = moon_derivs
            
            moon.update_pos_lists()
            moon.vel_step(dt,(moon_aX,moon_aY))
            moon.pos_step(dt)

        else:
            vX,vY,aX,aY = self.calc_derivs(dictionary, key)

        this_body.update_pos_lists()
        this_body.vel_step(dt,(aX,aY))
        this_body.pos_step(dt)


    def run_RK4(self):
        pass

    def pass_time(self, time, dt):
        for step in np.arange(0,time,dt):
            d = self.planets_dict
            if d.__len__() > 0:
                for k in d.keys():
                    self.euler_cromer_step(dt, d, k)

    def initialize_star(self, x, y, m, name):
        new_star = Star(x,y,m)
        self.stars_dict[name] = new_star

    def initialize_planet(self, x, y, m, name, vX=0, vY=0):
        if (vX and vY) == 0:
            r = (x*x + y*y)**0.5
            T = r**1.5
            vX = -2*pi*y/T
            vY = 2*pi*x/T

        new_planet = Planet(x, y, vX, vY, m)
        self.planets_dict[name] = new_planet
    
    def inialize_planets(self, dictionary):

        for key in dictionary.keys():
            values = dictionary[key].__len__()
            if values < 3 or values == 4 or values > 5:
                print("3 values (x,y,m) or 5 values (x,y,m,vX,vY) needed.", values, " values given. Planet initialization skipped for", key, ".")
                pass
            elif values == 5:
                x,y,m,vX,vY = dictionary[key]
                self.initialize_planet(x, y, m, key, vX, vY)
            else:
                x,y,m = dictionary[key]
                self.initialize_planet(x, y, m, key)
    
    def initialize_moon(self,m,name,planet_key):
        host_planet = self.planets_dict[planet_key]
        x_,y_ = host_planet.get_pos()
        vX_,vY_ = host_planet.get_vel()


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


    def run_animation(self, speed=1, interval=20):
        plt.rcParams["figure.figsize"] = (10, 10)
        # plt.axis('equal')
        fig, ax = plt.subplots(1,1)
        line_dict = {}

        max_distance = 0

        for planet_key in self.planets_dict.keys():
            planet = self.planets_dict[planet_key]
            
            (new_line,) = ax.plot([],[], lw=2)
            
            planet_mass = planet.get_mass()
            dot_type = '.'
            if planet_mass >= 10*(4*pi**2)*(6e24/2e30): # 10x Earth's mass
                dot_type = 'o'
            (new_dot,) = ax.plot([],[], marker=dot_type)
            line_dict[planet_key] = (new_line,new_dot)

            x_list,y_list = planet.get_pos_lists()
            if (max(x_list)) > max_distance:
                max_distance = max(x_list)
            if (max(y_list)) > max_distance:
                max_distance = max(y_list)

            if planet.get_moons() is not None:
                m_dict = planet.get_moons()
                for moon_key in m_dict.keys():
                    moon = m_dict[moon_key]
                    (moon_dot,) = ax.plot([],[], marker='.')
                    line_dict[moon] = moon_dot
                    planet.moon_orbit_quick_fix(moon_key, orbits=12)

        print(max_distance)

        for planet in self.planets_dict.keys():
            frames = int(self.planets_dict[planet].get_list_length()/speed)
            print(frames)
            break


        ax.set_xlim(1.1*(-max_distance), 1.1*(max_distance))
        ax.set_ylim(1.1*(-max_distance), 1.1*(max_distance))

        def update_figure(frame):
            # ax.cla()
            nonlocal speed
            tail = 0
            frame *= speed

            if frame > 200:
                tail = frame - 200

            # for d in (self.planets_dict):
            d = self.planets_dict
            if d.__len__() > 0:
                for k in d.keys():
                    X,Y = d[k].get_pos_lists(frame)
                    # X,Y = d[k].get_pos_lists(frame, tail)

                    if len(X) > 0:
                        x,y = X[-2:-1], Y[-2:-1]
                    else:
                        x,y = [],[]

                    line_dict[k][0].set_data(X,Y)
                    line_dict[k][1].set_data(x,y)

                    if d[k].get_moons() is not None:
                        m_dict = d[k].get_moons()
                        for moon_key in m_dict.keys():
                            moon = m_dict[moon_key]
                            m_X, m_Y = moon.get_pos_lists(frame)
                            m_x, m_y = m_X[-2:-1], m_Y[-2:-1]
                            line_dict[moon].set_data(m_x,m_y)


            ax.set_title(f"Frame {frame*speed}")
            return

        anim = FuncAnimation(fig, update_figure, frames, interval=interval)
        plt.show()
