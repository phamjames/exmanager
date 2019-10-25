from consts import *

class PCB:
    def __init__(self,state,priority=None,parent=None,children=[],resources=[]):
        self.state = state
        self.priority = priority
        self.parent = parent
        self.children = children
        self.resources = resources


    def get_state(self):
        return self.state

    def set_state(self,newState):
        # check for 0 or 1
        if newState != READY or newState != BLOCKED:
            #raise error here
            print("error")
            return
        self.state = newState

    def get_parent(self):
        return self.parent

    def set_parent(self,parent):
        self.parent = parent

    def get_children(self):
        return self.children


    def insert_child(self,child):
        self.children.append(child)

    def get_resources(self):
        return self.resources