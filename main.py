from solar_system import SolarSystem
from math import pi, sin, cos
import matplotlib.pyplot as plt

# Sun mass
M = 4*pi**2

# Earth mass and radius
m = M*6e24/2e30
r = 1
angle = 0
x = r*cos(angle)
y = r*sin(angle)

planets = {
    "Earth" : (x, y, m),
    "Mercury" : (0.39*r, 0*r, .055*m),
    "Venus" : (0.72*r, 0*r, .815*m),
    "Mars" : (1.52*r, 0*r, 0.107*m),
    # "Jupiter" : (5.2*r, 0*r, 317.8*m),
    # "Saturn" : (9.54*r, 0*r, 95.2*m),
    # "Uranus" : (19.19*r, 0*r, 14.5*m),
    # "Neptune" : (30.06*r, 0*r, 17.1*m),
    # "Pluto" : (39.53*r, 0*r, .00218*m),
}

SS = SolarSystem()

SS.initialize_star(0, 0, M, "Sun")
SS.inialize_planets(planets)
SS.initialize_moon(.0123*m,"Moon","Earth")
# SS.initialize_moon(.0123*m,"Moon","Mercury")
# SS.initialize_moon(.0123*m,"Moon","Venus")
# SS.initialize_moon(.0123*m,"Moon","Mars")
# SS.initialize_moon(.0123*m,"Moon","Jupiter")
# SS.initialize_moon(.0123*m,"Titan","Saturn")

SS.info()

SS.pass_time(1, 0.0001)

# SS.plot_system()
SS.run_animation(20,20)


# print(dir(plt))

# print(planets["Earth"].__len__())