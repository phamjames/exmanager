class PCB:
    def __init__(self,state=-1,priority=None,parent=None,children=[],resources=[]):
        self.state = state
        self.priority = priority
        self.parent = parent
        self.children = children
        self.resources = resources


    def get_state(self):
        return self.state

    def set_state(self,newState):
        # check for 0 or 1
        if newState != 0 or newState != 1:
            #raise error here
            print("error")
            return
        self.state = newState

    def get_parent(self,parent):
        return self.parent

    def get_children(self):
        return self.children

    def get_resources(self):
        return self.resources