from consts import *
class RCB:
    def __init__(self,type,units):
        self.type = type
        self.inventory = units
        self.state = units # total units available
        self.waitlist = [] # contains process index AND number of units

    def get_state(self):
        return self.state

    # def set_state(self,newState):
    #     self.state = newState


