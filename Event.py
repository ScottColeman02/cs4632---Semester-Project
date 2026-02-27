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

class Start_Triage(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self):
        patient = self.simulation.queues.triage_queue.dequeue()
        patient.status = "IN_TRIAGE"

        if(patient.severity >= 9 or patient.chief_complaint == "CHEST_PAIN"):
            patient.esi = 1
        elif(patient.severity >= 7 and patient.severity <= 8):
            patient.esi = 2
        elif(patient.severity >= 5 and patient.severity <= 6):
            patient.esi = 3
        elif(patient.severity >= 3 and patient.severity <= 4):
            patient.esi = 4
        elif(patient.severity >= 1 and patient.severity <= 2):
            patient.esi = 5 

        return End_Triage(), patient    

        

class End_Triage(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self, patient):
        print("Patient "+str(patient.patient_id)+" has been triaged, ESI = "+str(patient.esi))
        self.simulation.queues.bed_queue.enqueue(patient)
        patient.status = "WAITING_BED"

        return Transfer_to_bed()

class Transfer_to_bed(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self,patient):
        patient = self.simulation.queues.bed_queue.dequeue()
        patient.status = "TRANSFERING_TO_BED"

        nurse = self.simulation.resources.seize("nurse")
        nurse.available = False
        return Get_to_bed(), patient, nurse   

class Get_to_bed(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self, patient, nurse):
        bed = self.simulation.resources.seize("bed")
        bed.available = False
        pass    

