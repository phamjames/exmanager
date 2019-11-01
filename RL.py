from consts import *

class ReadyList:
    def __init__(self,first_proc):
        self.high = []
        self.med = []
        self.low = [first_proc]


    def __str__(self):
        return str(self.high + self.med + self.low)

    def get_priority_list(self,pcb):
        # this function will return the list of
        # the given PCB
        if pcb.priority == HIGH:
            return self.high
        elif pcb.priority == MED:
            return self.med
        else:
            return self.low

    def append(self, pcb):
        pcb_list = self.get_priority_list(pcb)
        pcb_list.append(pcb)

    def get_highest_priority(self):
        all_lists = [self.high, self.med, self.low]
        for l in all_lists:
            if l != []:
                return l[0]


    def get_all(self):
        return self.high + self.med + self.low


    def remove(self, pcb):
        pcb_list = self.get_priority_list(pcb)
        pcb_list.remove(pcb)




    # def pop(self,i=-1):
    #     item = self.list[i]
    #     self.list.remove(item)
    #     return item

    # def items(self):
    #     return self.list