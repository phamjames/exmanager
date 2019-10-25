from RL import *
from consts import *
from PCB import PCB
from RCB import RCB

class PCB_List:
    def __init__(self,size):
        self.list = [PCB(state=READY,priority=LOW)] + [FREE for x in range(size)]

    def _PCB_check(self,x):
        if not isinstance(x,PCB):
            print("add param must be PCB")
            return False
        return True

    def index(self,x:"Must be a PCB"):
        if not self._PCB_check(x):
            return
        return self.list.index(x)

    def add(self,x:"Must be a PCB"):
        if not self._PCB_check(x):
            return

        for i in self.list:
            if i == FREE:
                self.list[i] = x
        print("pcb list full")

    def remove(self,j: "index or PCB"):
        if type(j) == int:
            del self.list[j]

        if isinstance(j,PCB):
            self.list.remove(j)



class Manager:
    def __init_(self):
        self.PCB_list = PCB_List(DEFAULT_SIZE)
        self.RCB_list = [RCB() for x in range(4)]
        self.wait_list = []
        self.ready_list = ReadyList().insert_front(self.PCB_list[0])

    def create(self):
        new_PCB = PCB(state=READY)
        running_PCB = self._get_running_proc()
        running_PCB.insert_child(new_PCB)
        # use currently running proc's index to set new_PCB's parent field
        new_PCB.set_parent(self.PCB_list.index(running_PCB))
        self.ready_list.append(new_PCB)
        print("process j created")



    def destroy(self, j: "child PCB"):
        running_PCB = self._get_running_proc()

        for k in j.children:
            self.destroy(k)

        del running_PCB.get_children[j]
        del self.ready_list[j]

        # release resources of j



        return

    def request(self):
        return

    def release(self):
        return

    def timeout(self):
        return

    def scheduler(self):
        return

    def _get_running_proc(self):
        return self.ready_list.head