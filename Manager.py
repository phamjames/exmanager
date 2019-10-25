from RL import *
from consts import *
import PCB

class Manager:
    def __init_(self):
        self.PCB_list = [PCB(state=READY,priority=LOW)] + [PCB() for x in range(15)]
        self.wait_list = []
        self.ready_list = ReadyList()

    def create(self):
        return

    def destroy(self):
        return

    def request(self):
        return

    def release(self):
        return

    def timeout(self):
        return

    def scheduler(self):
        return
