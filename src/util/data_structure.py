from collections import deque
from util.enums import Storage
# This file defines wrapper classes around deque's for each of the possible
# data structure types the Boykov-Kolmogorov algorithm can use

# This serves as a base class for the data structures which only use one
# underlying deque
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

# Wrapper so behavior is like a stack
class Stack(SingleDataStructure):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.add = self.ds.appendleft

# Wrapper so behavior is like a queue
class Queue(SingleDataStructure):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.add = self.ds.append

# This serves as a base call for the data structures which have two underlying
# deque's. These deque's are switched whenever one of them becomes full
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

# Wrapper so both deques behave like stacks
class MultiStack(MultiDataStructure):
    def __init__(self, iterable):
        super().__init__(iterable)
        self.add = self.inactive_ds.appendleft

# Wrapper so both deques behave like queues
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
