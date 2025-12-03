

class PhysicsBody():
    

    def __init__(self, x: float, y: float, mass: float):
        self.x = x
        self.y = y

        self.x_list = []
        self.y_list = []

        self.mass = mass

    def update_pos_lists(self):
        self.x_list.append(self.x)
        self.y_list.append(self.y)

    def get_list_length(self):
        return len(self.x_list)

    def get_pos_lists(self, head=-1, tail=0) -> tuple():
        return (self.x_list[tail:head], self.y_list[tail:head])

    def get_pos(self):
        return (self.x, self.y)
    
    def get_mass(self):
        return self.mass