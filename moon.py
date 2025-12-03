from physics_body import PhysicsBody

class Moon(PhysicsBody):

    def __init__(self, x: float, y: float, vX: float, vY: float, mass: float):
        super().__init__(x,y,mass)

        self.vX = vX
        self.vY = vY


    def get_vel(self):
        return (self.vX, self.vY)
    
    def pos_step(self, dt):
        self.x += self.vX*dt
        self.y += self.vY*dt

    def vel_step(self, dt, a: tuple()):
        self.vX += a[0]*dt
        self.vY += a[1]*dt