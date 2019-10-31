from consts import *

class PCB_List:
    def __init__(self,capacity):
        self.list = [PCB(state=READY,priority=LOW,num=0)] + [PCB_FREE for x in range(capacity)]
        self.capacity = capacity
    def __getitem__(self,index):
        return self.list[index]

    def __str__(self):
        return str(self.list)

    def _PCB_check(self,x):
        if not isinstance(x,PCB):
            print("add param must be PCB")
            return False
        return True

    def size(self):
        """" Returns the number of PCB's in this list """
        total_size = 0
        for item in self.list:
            total_size += 1 if item != PCB_FREE else 0
        return total_size



    def capacity(self):
        """ Returns the overall capacity of the list """
        return len(self.list)


    def index(self,x:"Must be a PCB"):
        if not self._PCB_check(x):
            return
        return self.list.index(x)

    def add(self,x:"Must be a PCB"):
        if not self._PCB_check(x):
            return

        for i in self.list:
            if i == PCB_FREE:
                self.list[i] = x

        print("pcb list full")

    def remove(self,j: "index or PCB"):
        if type(j) == int:
            del self.list[j]

        if isinstance(j,PCB):
            self.list.remove(j)

    def items(self):
        return self.list

class PCB:
    def __init__(self,state,priority,num,parent=None):
        self.state = state
        self.priority = priority
        self.num = num
        self.parent = parent
        self.children = []
        self.resources = []

    def __str__(self):
        return "PCB[{}]".format(self.num)
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