import heapq
from collections import deque
class QueueManager:
    
    #Triage queue to store patients based on ESI level,
    #implemented using a priority queue.
    triage_queue = []

    #Waiting room queue also implemented as priority queue
    waiting_room_queue = []

    #Provider, lab, and inpatient bed queues implemented as standard FIFO queues.
    provider_queue = deque()
    lab_queue = deque()
    inpatient_bed_queue = deque()