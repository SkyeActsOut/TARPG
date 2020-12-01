class Entity:
    def __init__(self):
        self.hp = 50
        self.max_hp = 100

        self.mana = 65
        self.max_mana = 100
    
    def getHealth(self):
        return self.hp
    def getMaxHealth(self):
        return self.max_hp

    def getMana(self):
        return self.mana
    def getMaxMana(self):
        return self.max_mana

class Player(Entity):
    def __init__(self):
        super().__init__()