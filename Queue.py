from collections import deque
import heapq
class Queue:
    def enqueue(self):
        raise NotImplementedError
    
    def dequeue(self):
        raise NotImplementedError

class FIFOqueue(Queue):
    def __init__(self):
        super().__init__()
        self.queue = deque()

    def enqueue(self,item):
        self.queue.appendleft(item)

    def dequeue(self):
        return self.queue.pop()
    
class PriorityQueue(Queue):
    def __init__(self):
        super().__init__()
        self.queue = []

    def enqueue(self, patient):
        heapq.heappush(self.queue, (patient.esi, patient.arrival, patient.id))

    def dequeue(self):
        return heapq.heappop(self.queue)