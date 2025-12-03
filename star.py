from physics_body import PhysicsBody

class Star(PhysicsBody):

    def __init__(self, x: float, y: float, mass: float):
        super().__init__(x,y,mass)