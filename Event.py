from Patient import Patient
class Event:
    def __init__(self,simulation):
        self.time = simulation.clock
        self.patient_id = 0
    
    def execute():
        raise NotImplementedError


class Arrive(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute():
        patient = Patient()
        print("Patient "+patient.patient_id+" has arrived")
        patient.status = "WAITING_TRIAGE"