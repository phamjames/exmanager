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


    def index(self,pcb:"Must be a PCB"):
        if not self._PCB_check(pcb):
            return
        return self.list.index(pcb)

    def add(self,pcb:"Must be a PCB"):
        if not self._PCB_check(pcb):
            return

        for i in self.list:
            if i == PCB_FREE:
                self.list[i] = pcb

        print("-1 pcb list full")

    def free(self,pcb:"Must be a pcb"):
        self.list[self.list.index(pcb)] = -1


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

    def get_child(self,j:"index of child"):
        for child in self.children:
            if child.num == j:
                return child

        return False

    def remove_child(self,j:"index of child"):
        children_copy = self.children

        for child in children_copy:
            if child.num == j:
                self.children.remove(child)

    def insert_child(self,child):
        self.children.append(child)

    def get_resource(self,r:"resource type"):
        if not self.resources:
            print("resource don't exist buddy in this PCB -1")
            return None

        for res in self.resources:
            if res.type == r:
                return res

        return None


    def append_resource(self,rcb):
        if not self.resources:
            self.resources.append(rcb)
            return


        for res in self.resources:
            if res.type == rcb.type:
                res.state += rcb.state
                return

        self.resources.append(rcb)

    def remove_resource(self,r:"resource type",k:"units to remove"):
        ''' This function will remove k units from the resource type
            and return the number of k units removed. 0 if None'''

        units_removed = 0

        if not self.resources:
            print("resource don't exist buddy in this PCB -1")
            return units_removed

        for res in self.resources.copy():
            if res.type == r:
                res.state -= k # remove k units from resource
                units_removed += k
                if res.state == 0: # if there are no units of this resource
                    self.resources.remove(res) # remove from resource list
                else:
                    return -1

        return units_removed