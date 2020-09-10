class Carry:
    def __init__(self):
        self.carry = 0

    def Get (self):
        return self.carry
    def Set (self, val):
        self.carry = val
    def Add (self, val):
        self.carry += val