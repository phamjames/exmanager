from RL import *
from consts import *
from PCB import PCB, PCB_List
from RCB import RCB

_debug = False


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

    def display_current_running(self):
        if _debug:
            print("current running -> {}".format(self.current_running_pcb.num))
        else:
            print(self.current_running_pcb.num, end=' ')

    def _get_running_proc(self):
        return self.current_running_pcb

    def _get_running_ind(self):
        return self.current_running_pcb.num

    def _set_running_proc(self, pcb):
        self.current_running_pcb = pcb

    def _req_error_check(self,running_pcb,r,k):
        if running_pcb.num == 0: return False
        units_req = k
        resource = running_pcb.get_resource(r)
        # if resource == None: return False
        units_held = 0 if resource is None else running_pcb.get_resource(r).state
        init_inventory = self._RCB_list[r].inventory

        return units_req + units_held <= init_inventory

    def _rel_error_check(self,running_pcb,r,k):
        resource = running_pcb.get_resource(r)
        if resource == None:
            return False
        units_released = k
        units_held = resource.state
        return units_released <= units_held

    def _de_error_check(self,running_pcb, j:"index of child process"):
        return self._get_running_proc().get_child(j) != False

    def create(self,p: "p is priority"):
        #print("cr called")

        if p > 3 or p < 1:
            print("-1", end=' ')
            return False


        new_PCB = PCB(state=READY,priority=p,num=self._PCB_list.size())
        self._PCB_list.add(new_PCB)
        running_PCB = self._get_running_proc()
        running_PCB.insert_child(new_PCB)
        # use currently running proc's index to set new_PCB's parent field
        new_PCB.set_parent(running_PCB.num)
        self.ready_list.append(new_PCB)



        self.scheduler()



    def destroy(self, j: "index child PCB",op:"j if recursive call"=None):

        proc = self._PCB_list.get(j)
        if not proc:
            print("-1",end=' ')
            return proc

        for resource in proc.resources.copy():
            type = resource.type
            freed_units = resource.state
            self._RCB_list[type].state += freed_units
            # self.release(resource.type,resource.state,proc)

        for k in proc.children.copy():
            self.destroy(k.num)



        # remove j from i /parent
        proc_parent = self._PCB_list.get(proc.parent)
        proc_parent.children.remove(proc)

        #remove j from RL or WAITLIST
        try:
            self.ready_list.remove(proc)

        except ValueError:
            for rcb in proc.resources:
                for item in rcb.waitlist.copy():
                    wait_proc = item[0]
                    if wait_proc == j:
                        rcb.waitlist.remove(item)




        self._PCB_list.free(proc)
        # self.scheduler()

    def request(self,r:"resource type", k:"number of units requested"):
        #print("req called {} {}".format(r,k))
        if r < 0 or r > 3:
            print("-1", end=' ')
            return False

        req_RCB = self._RCB_list[r]
        available_units = req_RCB.state
        running_PCB = self._get_running_proc()

        # error check here
        if not self._req_error_check(running_PCB,r,k):
            print("-1", end=' ')
            return False

        if available_units >= k:
            req_RCB.state = available_units - k
            running_PCB.append_resource(RCB(r,k))
            # print("resource {} allocated".format(r))

        else:
            self.ready_list.remove(running_PCB)
            self._set_running_proc(self.ready_list.get_all()[0])
            req_RCB.waitlist.append((running_PCB,k))
            # print("process {} blocked".format(running_PCB.num))
            self.scheduler()

        return


    def release(self,r:"resource type",k:"number of units",op:"replace running proc if not None"= None):
        #print("rel called {} {}".format(r,k))

        running_proc = self._get_running_proc() if op is None else op

        if not self._rel_error_check(running_proc, r, k):
            print("-1", end='')
            return False

        units_freed = running_proc.remove_resource(r,k)
        if units_freed == False: return False





        # add freed units back to resource
        resource = self._RCB_list[r] # THIS RESOURCE IS THE MANAGER RESOURCE
        resource.state += units_freed
        #print("resource {} released".format(r))


        # if item on wait list can be unblocked,
        # unblock it by adding to ready list,
        #      adding resource to process list
        #      and removing it from wait list
        if resource.waitlist != []:
            for item in resource.waitlist.copy():
                available_units = resource.state
                process, units_requested = item[0], item[1]
                if available_units >= units_requested:
                    self.ready_list.append(process)
                    process.append_resource(RCB(r,units_requested))
                    resource.state -= units_requested
                    resource.waitlist.remove(item)
        self.scheduler()





    def timeout(self):
        #print("to called")
        running_proc = self._get_running_proc()
        running_proc_list = self.ready_list.get_priority_list(running_proc)
        running_proc_list.append(running_proc_list.pop(0))


        self.scheduler()






    def scheduler(self):

        # print("process {} running".format(self.ready_list.head.index))
        hp_proc = self.ready_list.get_highest_priority() # highest priority process "j"
        self._set_running_proc(hp_proc)


