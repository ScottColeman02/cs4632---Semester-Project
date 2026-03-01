from DataStructures import FIFOqueue, PriorityQueue
class QueueManager:
    def __init__(self):
        #Triage queue to store patients based on ESI level,
        #implemented using a priority queue.
        self.triage_queue = FIFOqueue()

        #Waiting room queue also implemented as priority queue
        self.bed_queue = PriorityQueue()
        self.provider_queue = PriorityQueue()
        self.followup_queue = PriorityQueue()

        #lab and inpatient bed queues implemented as standard FIFO queues.
        self.lab_queue = FIFOqueue()
        self.inpatient_bed_queue = FIFOqueue()
        self.discharge_queue = FIFOqueue()