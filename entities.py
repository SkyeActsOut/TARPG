from datetime import datetime
import libtcodpy as tcod
from numpy import ndarray

class Entity:
    def __init__(self, pos_x, pos_y, cost_values, p=None):

        self.action_stack = []

        self.hp = 50
        self.max_hp = 100

        self.mana = 65
        self.max_mana = 100

        self.move_time = False
        self.move_speed = 200 # Tiles per x milliseconds

        self.cooldown_time = False
        self.cooldown_speed = 250 # Global cooldown of abilities per x milliseconds

        self.pos_x = 0
        self.pos_y = 0

        self.vision_r = 25

        if (p != None):
            self.player = p

            self.cost_values = cost_values
            self.astar = tcod.path.AStar(self.cost_values)
            self.path = self.astar.get_path(self.pos_y, self.pos_x, self.player.pos_y, self.player.pos_x)
    
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

    def add_to_stack(self, action):
        self.action_stack.append(action)

    # Moves the entity towards the player
    def move_to_player(self):
        # dx, dy = (p.pos_x - self.pos_x, p.pos_y - self.pos_y)
        if (self.move_cooldown()):
            # print (self.pos_y, self.pos_x, p.pos_y, p.pos_x)
            # if (self.pos_y + self.pos_x + p.pos_y + p.pos_x == 0):
            if (len(self.path) > 0):
                self.update_pos(self.path[0][0], self.path[0][1])
                print ((self.path[0][0], self.path[0][1]))
                self.path.pop(0)

            # if (abs(dx) + abs(dy) > 25):
                # step_x = 0
                # step_y = 0
                # if (dx < -2):
                #     step_x = 1
                # elif (dx > 2):
                #     step_x = -1
                # if (dy < -2):
                #     step_y = -1
                # if (dy > 2):
                #     step_y = 1

                # self.update_pos(self.pos_x + step_y, self.pos_y + step_x)
                # print (p.pos_x, p.pos_y, self.pos_x, self.pos_y)

    def update_astar(self, p):
        self.path = self.astar.get_path(self.pos_y, self.pos_x, p.pos_y, p.pos_x)
    
    def vision(self, x, y):
        pass

    def update(self):
        self.add_to_stack(self.move_to_player())

    def getHealth(self):
        return self.hp
    def getMaxHealth(self):
        return self.max_hp

    def getMana(self):
        return self.mana
    def getMaxMana(self):
        return self.max_mana

    def update_pos (self, x, y):
        self.pos_x = x
        self.pos_y = y

class Player(Entity):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y, None)

        self.active_abilities = []

    def add_active_ability (self, ability):
        self.active_abilities.append (ability)