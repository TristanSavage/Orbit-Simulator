from planet import Planet

class Asteroid(Planet): # Subclass of Planet (NOT STARTED)

    def __init__(self, x: float, y: float, vX: float, vY: float, mass: float):
        super().__init__(x,y,vX,vY,mass)