
# Super class for all bodies undergoing physical simulation
class PhysicsBody():
    

    def __init__(self, x: float, y: float, mass: float):    # Currently, takes in: (x0, y0, mass)
        self.x = x
        self.y = y
        self.mass = mass

        self.x_list = []    # position lists
        self.y_list = []    # position lists


    # Appends current position components to position lists
    def update_pos_lists(self):
        self.x_list.append(self.x)
        self.y_list.append(self.y)

    def get_list_length(self):
        return len(self.x_list)

    # Returns position lists
    def get_pos_lists(self, head=-1, tail=0) -> tuple(): # Takes in: (list head, list tail) -> list[tail:head]
        return (self.x_list[tail:head], self.y_list[tail:head])

    def get_pos(self):
        return (self.x, self.y)
    
    def get_mass(self):
        return self.mass