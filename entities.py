class Entity:
    def __init__(self):
        self.hp = 100
        self.max_hp = 100
    
    def getHealth(self):
        return self.hp
    def getMaxHealth(self):
        return self.max_hp

class Player(Entity):
    def __init__(self):
        super().__init__()