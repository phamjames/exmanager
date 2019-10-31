from consts import *
class RCB:
    def __init__(self):
        self.state = RCB_FREE
        self.waitlist = []

    def get_state(self):
        return self.state

    def set_state(self,newState):
        self.state = newState


