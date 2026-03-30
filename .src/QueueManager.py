from DataStructures import FIFOqueue, PriorityQueue
class QueueManager:
    def __init__(self):
        #Triage queue to store patients based on ESI level,
        #implemented using a FIFO queue
        self.triage_queue = FIFOqueue()

        #Waiting room, eval, and followup queues also implemented as priority queues
        self.bed_queue = PriorityQueue()
        self.eval_queue = PriorityQueue()
        self.followup_queue = PriorityQueue()

        #lab and discharge implemented as standard FIFO queues.
        self.lab_queue = FIFOqueue()
        self.discharge_queue = FIFOqueue()

    
