class ReadyList:
    def __init__(self,first_proc):
        self.list = [first_proc]

    def __str__(self):
        return str(self.list)

    def append(self, PCB):
        self.list.append(PCB)

    def remove(self, PCB):
        self.list.remove(PCB)

    def pop(self,i=-1):
        item = self.list[i]
        self.list.remove(item)
        return item

    def items(self):
        return self.list