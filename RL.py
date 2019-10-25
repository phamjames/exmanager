class RLNode:
    def __init__(self,data):
        self.data = data
        self.next = None

class ReadyList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0


    def insert_front(self,PCB):
        new_node = RLNode(PCB)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

        if self.size == 1:
            self.tail = new_node


    def insert_end(self,PCB):
        new_node = RLNode(PCB)
        self.tail.next = new_node
        self.tail = new_node
        self.size += 1


    def get_head(self):
        return self.head

    def get_tail(self):
        return self.tail

    def get_size(self):
        return self.size

    def printList(self):
        temp = self.head
        while temp:
            print(temp.data)
            temp = temp.next
