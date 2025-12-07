from physics_body import PhysicsBody

class Moon(PhysicsBody):    # Subclass of PhysicsBody

    def __init__(self, x: float, y: float, vX: float, vY: float, mass: float):  # Sub takes in: (..., vx_0, vy_0, ...)
        super().__init__(x,y,mass)

        self.vX = vX
        self.vY = vY


    def get_vel(self):
        return (self.vX, self.vY)
    
    # Apply numerical step to update position
    def pos_step(self, dt):
        self.x += self.vX*dt
        self.y += self.vY*dt

    # Apply numerical step to update velocity
    def vel_step(self, dt, a: tuple()):
        self.vX += a[0]*dt
        self.vY += a[1]*dt