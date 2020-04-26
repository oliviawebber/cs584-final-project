from collections import deque
from util.enums import Storage

class SingleDataStructure:
    def __init__(self, iterable):
        self.ds = deque(iterable)
        self.remove = self.ds.remove
        self.get = self.ds.popleft

    def __getitem__(self, item):
        return self.ds[item]

    def __str__(self):
        return self.ds.__str__()

    def length(self):
        return len(self.ds)

class Stack(SingleDataStructure):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.add = self.ds.appendleft

class Queue(SingleDataStructure):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.add = self.ds.append

class MultiDataStructure:
    def __init__(self):
        pass

class MultiStack(MultiDataStructure):
    pass

class MultiQueue(MultiDataStructure):
    pass

class DataStructure:
    def __new__(self, storage_type=Storage.queue, iterable=[]):
        if storage_type == Storage.stack:
            return Stack(iterable)
        elif storage_type == Storage.queue:
            return Queue(iterable)
        elif storage_type == Storage.multi_stack:
            return MultiStack(iterable)
        else:
            return MultiQueue(iterable)
