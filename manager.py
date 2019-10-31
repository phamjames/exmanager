from RL import *
from consts import *
from PCB import PCB, PCB_List
from RCB import RCB


class Manager:
    def __init__(self):
        self.PCB_list = PCB_List(DEFAULT_PCBL_SIZE)
        self.RCB_list = [RCB() for x in range(4)]
        self.wait_list = []
        self.ready_list = ReadyList(self.PCB_list[0])



    def __str__(self):
        str = "~~~~~ MANAGER INFO ~~~~~\n"
        str += "PCB List = {}\n".format(self.PCB_list)
        str += "RCB List = {}\n".format(self.RCB_list)
        str += "wait list = {}\n".format(self.wait_list)
        str += "ready list = {}".format(self.ready_list)
        str += "\n"
        return str


    def create(self):
        new_PCB = PCB(state=READY,priority=LOW,num=self.PCB_list.size()+1)
        self.PCB_list.add(new_PCB)
        running_PCB = self._get_running_proc()
        running_PCB.insert_child(new_PCB)
        # use currently running proc's index to set new_PCB's parent field
        new_PCB.set_parent(self.PCB_list.index(running_PCB))
        self.ready_list.append(new_PCB)
        print("process j created")



    def destroy(self, j: "index child PCB"):
        destroyed = 0
        running_PCB = self._get_running_proc()
        j = running_PCB[j]

        for k in j.children:
            self.destroy(k)
            destroyed += 1

        del running_PCB.get_children[j]
        del self.ready_list[j]

        for i in range(len(j.resources)):
            self.release(i,j)
            j = PCB_FREE
            print("{} processes destroyed".format(destroyed))

        return destroyed


    def request(self,r: "index of resource"):
        req_RCB = self.RCB_list[r]
        running_PCB = self._get_running_proc()

        if req_RCB.state == RCB_FREE:
            req_RCB.state = ALLOCATED
            running_PCB.get_resources().append(req_RCB)
            print("resource r allocated")

        else:
            running_PCB.state = BLOCKED
            self.ready_list.remove(running_PCB)
            self.wait_list.append(running_PCB)
            print("process i blocked")
            self.scheduler()


        return



    def release(self,r:"index resource of process i",
                    i:"PCB to release r from" = None):
        PCB = self._get_running_proc() if i == None else i
        resource = PCB.resources[r]
        PCB.resources.remove(resource)

        if len(resource.waitlist) == 0:
            resource.state = RCB_FREE
        else:
            # next waiting proc is aka process j (head of Waitlist)
            next_waiting_proc = resource.waitlist[0]
            resource.waitlist.remove(next_waiting_proc)
            next_waiting_proc.state = READY
            next_waiting_proc.resources.append(resource)

        print("resource r released")

        return



    def timeout(self):
        # running proc is the PCB,
        # i is the index of running_proc
        rl = self.ready_list
        running_proc = self._get_running_proc()
        i = rl.index(running_proc)

        rl.items.append(rl.pop(i)) # swap first and last ind

        self.scheduler()



    def scheduler(self):
        print("process {} running".format(self.ready_list.head.index))


    def _get_running_proc(self):
        return self.ready_list.head