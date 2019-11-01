from RL import *
from consts import *
from PCB import PCB, PCB_List
from RCB import RCB


class Manager:
    def __init__(self):
        # do not modify PCB or RCB list
        self._PCB_list = PCB_List(DEFAULT_PCBL_SIZE)
        self._RCB_list = [RCB(0,1),RCB(1,1),RCB(2,2),RCB(3,3)]
        self.ready_list = ReadyList(self._PCB_list[0])
        self.current_running_pcb = self._PCB_list[0] # returns pcb, NOT INDEX!



    def __str__(self):
        str = "~~~~~ MANAGER INFO ~~~~~\n"
        str += "PCB List = {}\n".format(self._PCB_list)
        str += "RCB List = {}\n".format(self._RCB_list)
        str += "ready list = {}".format(self.ready_list)
        str += "\n"
        return str

    def _get_running_proc(self):
        return self.current_running_pcb

    def _get_running_ind(self):
        return self.current_running_pcb.num

    def _set_running_proc(self, pcb):
        self.current_running_pcb = pcb

    def _req_error_check(self,running_pcb,r,k):
        units_req = k
        units_held = running_pcb.get_resource(r).state
        init_inventory = self._RCB_list[r].inventory

        return units_req + units_held <= init_inventory

    def _rel_error_check(self,running_pcb,r,k):
        units_released = k
        units_held = running_pcb.get_resource(r).state
        return units_released <= units_held

    def _de_error_check(self,running_pcb, j:"index of child process"):
        return self._get_running_proc().get_child(j) != False

    def create(self,p: "p is priority"):
        if p > 3 or p < 0:
            print("-1")
            return

        new_PCB = PCB(state=READY,priority=p,num=self._PCB_list.size()+1)
        self._PCB_list.add(new_PCB)
        running_PCB = self._get_running_proc()
        running_PCB.insert_child(new_PCB)
        # use currently running proc's index to set new_PCB's parent field
        new_PCB.set_parent(running_PCB.num)
        self.ready_list.append(new_PCB)
        print("process j created")



    def destroy(self, j: "index child PCB"):
        # destroy child process j
        destroyed = 0
        running_PCB = self._get_running_proc()

        # run error check
        if not self._de_error_check(running_PCB, j):
            print("-1 destroy error")

        child_proc = running_PCB.get_child(j)



        for k in child_proc.children:
            self.destroy(k)
            destroyed += 1

        running_PCB.remove_child(j) # remove child from PCB children
        self.ready_list.remove(child_proc) # remove child from ready list

        # remove child from wait list
        for rcb in self._RCB_list:
            for item in rcb.waitlist.copy():
                wait_proc = item[0]
                if wait_proc.num == j:
                    rcb.waitlist.remove(item)



        # release resources of child and free PCB
        for resource in child_proc.resources().copy():
            self.release(resource.type,resource.state)

        self._PCB_list.free(child_proc)

        # return destroyed


    def request(self,r:"resource type", k:"number of units requested"):
        req_RCB = self._RCB_list[r]
        available_units = req_RCB.state
        running_PCB = self._get_running_proc()

        # error check here
        if not self._req_error_check(running_PCB,req_RCB,k):
            print("-1 request error")
            return

        if available_units >= k:
            available_units -= k
            running_PCB.append_resource(RCB(r,k))
            print("resource {} allocated".format(r))

        else:
            self.ready_list.remove(running_PCB)
            req_RCB.waitlist.append((running_PCB,k))
            print("process {} blocked".format(running_PCB.num))
            self.scheduler()

        return




    def release(self,r:"resource type",k:"number of units"):
        running_proc = self._get_running_proc()
        units_freed = running_proc.remove_resource(r,k)

        if not self._rel_error_check(running_proc,r,k):
            print("-1 release error")
            return



        # add freed units back to resource
        resource = self._RCB_list[r] # THIS RESOURCE IS THE MANAGER RESOURCE
        resource.state += units_freed
        print("resource {} released".format(r))


        # if item on wait list can be unblocked,
        # unblock it by adding to ready list,
        #      adding resource to process list
        #      and removing it from wait list
        if not resource.waitlist:
            waitlist_copy = resource.waitlist
            for item in waitlist_copy:
                available_units = resource.state
                process, units_requested = item[0], item[1]
                if available_units >= units_requested:
                    self.ready_list.append(process)
                    process.append(RCB(r,units_requested))
                    available_units -= units_requested
                    resource.waitlist.remove(item)











    def timeout(self):
        running_proc = self._get_running_proc()
        running_proc_list = self.ready_list.get_priority_list(running_proc)

        # swap first and last ind
        running_proc_list.append(running_proc_list.pop(running_proc))
        self.scheduler()







    def scheduler(self):
        # print("process {} running".format(self.ready_list.head.index))
        hp_proc = self.ready_list.get_highest_priority() # highest priority process "j"
        cur_proc = self._get_running_proc() # current running process "i"

        if hp_proc.priority > cur_proc.priority:
            print(hp_proc.num)
            self._set_running_proc(hp_proc)
        else:
            print(cur_proc.num)

