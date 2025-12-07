from solar_system import SolarSystem
from math import pi, sin, cos

## Constants, initial values, and planets and moons to include in simulation
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
## Constants
# Sun constants
M = 4*pi**2 # Sun mass

# Earth constants
Earth_mass = M*6e24/2e30    # Earth mass
radius = 1                  # Earth Orbit

# Moon constants
Moon_mass = 0.0123*Earth_mass   # Earth mass

# Earth variables (initial)
angle = 0               # Initial angle of orbit
x = radius*cos(angle)   # initial x-position of orbit
y = radius*sin(angle)   # initial y-position of orbit

# HERE: planets dictionary : initial(x,y,mass)
planets = {
    "Earth" : (x, y, Earth_mass),
 
    "Mercury" : (0.39*radius, 0*radius, .055*Earth_mass),
    "Venus" : (0.72*radius, 0*radius, .815*Earth_mass),
    "Mars" : (1.52*radius, 0*radius, 0.107*Earth_mass),
    "Jupiter" : (5.2*radius, 0*radius, 317.8*Earth_mass),
    # "Saturn" : (9.54*radius, 0*radius, 95.2*Earth_mass),
    # "Uranus" : (19.19*radius, 0*radius, 14.5*Earth_mass),
    # "Neptune" : (30.06*radius, 0*radius, 17.1*Earth_mass),
    # "Pluto" : (39.53*radius, 0*radius, .00218*Earth_mass),
}

# HERE: moons dictionary : (mass, this moon's name, host planet)
moons = {
    "Earth_1" : (Moon_mass,"Moon","Earth"),
    "Merc_1" : (Moon_mass,"Moon","Mercury"),
    "Venus_1" : (Moon_mass,"Moon","Venus"),
    "Mars_1" : (Moon_mass,"Moon","Mars"),
    "Jup_1" : (Moon_mass,"Moon","Jupiter"),
    # "Sat_1" : (Moon_mass,"Titan","Saturn"),
}

## Initialize and run Orbit Simulation
# ––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––

SS = SolarSystem()                  # Initialize Solar System
SS.initialize_star(0, 0, M, "Sun")  # Add the Sun to SS
SS.inialize_planets(planets)        # Add planets to SS

for key in moons.keys():            # Add planetary moons to SS
    args = moons[key]
    SS.initialize_moon(args[0], args[1], args[2])



SS.info()                               # Display Solar System info (stars, planets, moons, etc.)
SS.pass_time(1, 0.0001)                 # Pass time in Earth years, and select delta t
SS.run_animation(speed=50,interval=20)  # Run animation of orbits