SCREEN_HEIGHT = 54

class Menu:
    def __init__(self):
        pass

class LogsMenu (Menu):
    def __init__(self):
        super().__init__()
        
        self.height = 10
        self.width = 50

        self.x = 0
        self.y = SCREEN_HEIGHT - self.height

        self.logs = ""

    def add (self, line):
        self.logs += "\n " + line