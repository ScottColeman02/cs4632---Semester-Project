import heapq
from collections import deque
class QueueManager:
    def __init__(self):
        #Triage queue to store patients based on ESI level,
        #implemented using a priority queue.
        self.triage_queue = []

        #Waiting room queue also implemented as priority queue
        self.waiting_room_queue = []

        #Provider, lab, and inpatient bed queues implemented as standard FIFO queues.
        self.provider_queue = deque()
        self.lab_queue = deque()
        self.inpatient_bed_queue = deque()