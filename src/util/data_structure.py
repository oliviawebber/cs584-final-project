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

    def __iter__(self):
        return iter(self.ds)

class Stack(SingleDataStructure):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.add = self.ds.appendleft

class Queue(SingleDataStructure):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.add = self.ds.append

class MultiDataStructure:
    def __init__(self, iterable):
        self.active_ds = deque(iterable)
        self.inactive_ds = deque()

    def remove(self, item):
        if item in self.active_ds:
            self.active_ds.remove(item)
        if item in self.inactive_ds:
            self.inactive_ds.remove(item)

    def get(self):
        try:
            return self.active_ds.popleft()
        except:
            self.active_ds, self.inactive_ds = self.inactive_ds, self.active_ds
            return self.get()

    def __str__(self):
        return self.active_ds.__str__() + self.inactive_ds.__str__()

    def length(self):
        return len(self.active_ds) + len(self.inactive_ds)

    def __iter__(self):
        return iter(self.active_ds + self.inactive_ds)



class MultiStack(MultiDataStructure):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.add = self.inactive_ds.appendleft

class MultiQueue(MultiDataStructure):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.add = self.inactive_ds.append

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
