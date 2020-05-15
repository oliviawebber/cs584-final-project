from enum import Enum
# Defines an enumertor for use in selecting the data structure used by the
# Boykov-Kolmogorov algorithm"
class Storage(Enum):
    stack = 1
    queue = 2
    multi_stack = 3
    multi_queue = 4
