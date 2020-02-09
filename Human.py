from Player import Player

class Human(Player):

    def __init__(self, name, stack):
        Player.__init__(self, name)
        self.stack = stack

    def show_stack(self):
        print("Il possède {} jeton(s) au total.\n".format(self.stack))
      
    def is_out(self):
        return self.stack <= 0