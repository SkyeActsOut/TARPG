from datetime import datetime

class Entity:
    def __init__(self):
        self.hp = 50
        self.max_hp = 100

        self.mana = 65
        self.max_mana = 100

        self.move_time = False
        self.move_speed = 125 # Tiles per x milliseconds

        self.cooldown_time = False
        self.cooldown_speed = 250 # Global cooldown of abilities per x milliseconds
    
    def move_cooldown(self):
        if (not self.move_time):
            self.move_time = datetime.now()
            return True
        # Checks to see if it should go this frame or not
        else:
            curr_time = datetime.now()
            ms_elapsed  = abs(int((self.move_time - curr_time).total_seconds()*1000))
            if (ms_elapsed / self.move_speed >= 1):
                self.move_time = datetime.now()
                return True
            else:
                return False
    def global_cooldown(self):
        if (not self.cooldown_time):
            self.cooldown_time = datetime.now()
            return True
        # Checks to see if it should go this frame or not
        else:
            curr_time = datetime.now()
            ms_elapsed  = abs(int((self.cooldown_time - curr_time).total_seconds()*1000))
            if (ms_elapsed / self.cooldown_speed >= 1):
                self.cooldown_time = datetime.now()
                return True
            else:
                return False

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

        self.active_abilities = []

    def add_active_ability (self, ability):
        self.active_abilities.append (ability)