from Patient import Patient
from QueueManager import QueueManager
class Event:
    def __init__(self,simulation):
        self.simulation = simulation
        self.time = simulation.clock
        self.patient_id = 0
    
    def execute():
        raise NotImplementedError


class Arrive(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self):
        patient = Patient(self.simulation)
        print("Patient "+str(patient.patient_id)+" has arrived")
        patient.status = "WAITING_TRIAGE"
        self.simulation.queues.triage_queue.enqueue(patient)
        
