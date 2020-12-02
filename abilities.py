from datetime import datetime

class Ability ():
    def __init__(self, stx, sty, tx, ty):
        
        self.start_x = stx
        self.start_y = sty

        self.target_x = tx
        self.target_y = ty

        self.projectiles_count = 0
        self.projectiles = []

class Projectile ():
    def __init__(self, speed, damage, r, start_x, start_y, buff_x, buff_y, tx, ty, dir_x, dir_y):
        self.speed = speed # Projectile travel every x milliseconds
        self.damage = damage
        self.range = r
        self.buffer_x = buff_x # the buffer in terms of spaces from the player and the projectile
        self.buffer_y = buff_y 

        self.target_x = tx
        self.target_y = ty

        self.traveled = 0

        self.dir_x = dir_x
        self.dir_y = dir_y

        self.curr_x = start_x + buff_x
        self.curr_y = start_y + buff_y
        self.time = False

    def update(self):
        # start elapsed time
        if (not self.time):
            self.time = datetime.now()
        # Checks to see if it should go this frame or not
        else:
            curr_time = datetime.now()
            ms_elapsed  = abs(int((self.time - curr_time).total_seconds()*1000))
            if (ms_elapsed / self.speed >= 1):
                self.time = datetime.now()
            else:
                return False
    
        if (self.traveled > self.range):
            return True # Returns true when the projectile should be destroyed
        self.curr_x += self.dir_x
        self.curr_y += self.dir_y
        self.traveled += 1
        return False

class KnifeThrow(Ability):
    def __init__(self, stx, sty, tx, ty, dir_x, dir_y):
        super().__init__(stx, sty, tx, ty)

        # Equations for the direction of the KnifeThrow
        # (1-i)*2*-1*dir_y, (1-i)*2*dir_x

        self.projectiles_count = 2
        for i in range(self.projectiles_count):
            self.projectiles.append(
                Projectile(33, 5, 12, self.start_x, self.start_y, 
                (int(self.projectiles_count/2)-i)*2*-1*dir_y, 
                (int(self.projectiles_count/2)-i)*2*dir_x, 
                tx, ty, dir_x, dir_y)
            )

class TriRifle(Ability):
    def __init__(self, stx, sty, tx, ty, dir_x, dir_y):
        super().__init__(stx, sty, tx, ty)

        self.projectiles_count = 3
        for i in range(self.projectiles_count):
            self.projectiles.append(
                Projectile(38, 4, 10, self.start_x, self.start_y, (1-i)*2*dir_x, (1-i)*2*dir_y, tx, ty, dir_x, dir_y)
            )