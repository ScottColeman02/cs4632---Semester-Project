from Patient import Patient
from QueueManager import QueueManager
import random

events_log = []
class Event:
    def __init__(self,simulation):
        self.simulation = simulation
        self.patient_id = 0
    
    def execute(self):
        raise NotImplementedError


class Arrive(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self):
        patient = Patient(self.simulation)

        events_log.append("\nPatient "+str(patient.patient_id)+" has arrived , time = "+str(self.simulation.clock))
        
        patient.status = "WAITING_TRIAGE"
        self.simulation.queues.triage_queue.enqueue(patient)

        self.simulation.schedule(Start_Triage(self.simulation),self.simulation.clock)

        self.simulation.schedule(Arrive(self.simulation),self.simulation.clock+random.uniform(0.0,10.0))

class Start_Triage(Event):
    def __init__(self, simulation):
        super().__init__(simulation)
        self.triage_time = 0.0

    def execute(self):
        if self.simulation.resources.triage_nurse_stack.is_empty():
            return None
        if self.simulation.queues.triage_queue.is_empty():
            return None
        
        triage_nurse = self.simulation.resources.triage_nurse_stack.pop()

        patient = self.simulation.queues.triage_queue.dequeue()
        patient.status = "IN_TRIAGE"

        events_log.append("\nPatient "+str(patient.patient_id)+" is being triaged by "+str(triage_nurse.emp_id)+", time = "+str(self.simulation.clock))
        
        ####TODO: convert this to a match statement###

        if(patient.severity >= 9 or patient.chief_complaint == "CHEST_PAIN"):
            patient.esi = 1
            self.triage_time = random.uniform(8.0,10.0)
        elif(patient.severity >= 7 and patient.severity <= 8):
            patient.esi = 2
            self.triage_time = random.uniform(6.0,8.0)

        elif(patient.severity >= 5 and patient.severity <= 6):
            patient.esi = 3
            self.triage_time = random.uniform(4.0,6.0)

        elif(patient.severity >= 3 and patient.severity <= 4):
            patient.esi = 4
            self.triage_time = random.uniform(2.0,6.0)

        elif(patient.severity >= 1 and patient.severity <= 2):
            patient.esi = 5
            self.triage_time = random.uniform(0.0,2.0)
 
        self.simulation.schedule(End_Triage(self.simulation,patient, triage_nurse),self.simulation.clock+self.triage_time)
           

        

class End_Triage(Event):
    def __init__(self, simulation, patient, triage_nurse):
        super().__init__(simulation)
        self.patient = patient
        self.triage_nurse = triage_nurse

    def execute(self):
        patient = self.patient
        triage_nurse = self.triage_nurse

        events_log.append("\nPatient "+str(patient.patient_id)+" has been triaged by "+str(triage_nurse.emp_id)+", ESI = "+str(patient.esi)+", time = "+str(self.simulation.clock))
        

        self.simulation.resources.release("triage", triage_nurse)
        self.simulation.schedule(Start_Triage(self.simulation), self.simulation.clock)


        patient.status = "WAITING_BED"
        self.simulation.queues.bed_queue.enqueue(patient)

        events_log.append("\nPatient "+str(patient.patient_id)+" is waiting for a bed, time = "+str(self.simulation.clock))

        self.simulation.schedule(Transfer_to_bed(self.simulation), self.simulation.clock)


class Transfer_to_bed(Event):
    def __init__(self, simulation):
        super().__init__(simulation)
        self.transfer_time = 0.0

    def execute(self):
        if self.simulation.resources.nurse_stack.is_empty() or self.simulation.resources.bed_stack.is_empty():
            return None
        if self.simulation.queues.bed_queue.is_empty():
            return None
        patient = self.simulation.queues.bed_queue.dequeue()
        patient.status = "TRANSFERING_TO_BED"

        nurse = self.simulation.resources.seize("nurse")

        #seize bed for patient
        bed = self.simulation.resources.seize("bed")
        patient.bed_num = bed

        events_log.append("\nPatient "+str(patient.patient_id)+" is being transferred to a bed by "+str(nurse.emp_id)+", time = "+str(self.simulation.clock))


        self.transfer_time = random.uniform(0.0,5.0)

        self.simulation.schedule(Get_to_bed(self.simulation,patient,nurse),self.simulation.clock+self.transfer_time)

class Get_to_bed(Event):
    def __init__(self, simulation, patient, nurse):
        super().__init__(simulation)
        self.patient = patient
        self.nurse = nurse

    def execute(self):
        patient = self.patient
        nurse = self.nurse
        
        #release the nurse
        self.simulation.resources.release("nurse",nurse)

        events_log.append("\nPatient "+str(patient.patient_id)+" is in bed "+str(patient.bed_num.bed_id)+", time = "+str(self.simulation.clock))

        self.simulation.schedule(Transfer_to_bed(self.simulation),self.simulation.clock)
        self.simulation.schedule(Discharge(self.simulation),self.simulation.clock)

        
        #update patient status
        self.simulation.queues.provider_queue.enqueue(patient)
        patient.status = "WAITING_PROVIDER"

        events_log.append("\nPatient "+str(patient.patient_id)+" is waiting evaluation, time = "+str(self.simulation.clock))

        self.simulation.schedule(Provider_Eval(self.simulation),self.simulation.clock)

        
class Provider_Eval(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self):
        if self.simulation.resources.provider_stack.is_empty():
            return None
        
        if self.simulation.queues.provider_queue.is_empty():
            return None
        #get the next patient
        patient = self.simulation.queues.provider_queue.dequeue()

        #seize provider 
        provider = self.simulation.resources.seize("provider")

        #update patient status
        patient.status = "EVAL"

        events_log.append("\nPatient "+str(patient.patient_id)+" is being evaluated by "+str(provider.emp_id)+", time = "+str(self.simulation.clock))

        eval_time = random.uniform(0.0,8.0)

        self.simulation.schedule(EndEval(self.simulation, patient, provider),self.simulation.clock+eval_time)

        

class EndEval(Event):
    def __init__(self, simulation, patient, provider):
        super().__init__(simulation)
        self.patient = patient
        self.provider = provider

    def execute(self):
        patient = self.patient
        provider = self.provider
        #for now whether a patient needs labs is decided by coin toss
        needs_labs = random.randint(0,1)

        self.simulation.resources.release("provider",provider)

        self.simulation.schedule(Provider_Eval(self.simulation),self.simulation.clock)
        self.simulation.schedule(Followup(self.simulation),self.simulation.clock)

        if needs_labs == 1:
            patient.status = "WAITING_LABS"

            self.simulation.queues.lab_queue.enqueue(patient)

            events_log.append("\nPatient "+str(patient.patient_id)+" is waiting for labs, time = "+str(self.simulation.clock))

            self.simulation.schedule(Going_to_Labs(self.simulation), self.simulation.clock)
    
        else:
            patient.status = "WAITING_DISCHARGE"

            self.simulation.queues.discharge_queue.enqueue(patient)

            events_log.append("\nPatient "+str(patient.patient_id)+" is waiting for discharge, time = "+str(self.simulation.clock))

            self.simulation.schedule(Discharge(self.simulation),self.simulation.clock)      

class Going_to_Labs(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self):
        if self.simulation.resources.tech_stack.is_empty():
            return None
        
        if self.simulation.queues.lab_queue.is_empty():
            return None
        
        #get the next patient for labs
        patient = self.simulation.queues.lab_queue.dequeue()
        #seize a lab tech resource
        tech = self.simulation.resources.seize("tech")

        #update patient status
        patient.status = "GOING_TO_LAB"

        events_log.append("\nPatient "+str(patient.patient_id)+" is being transferred to labs by "+str(tech.emp_id)+", time = "+str(self.simulation.clock))

        time_to_lab = random.uniform(0.0,5.0)

        self.simulation.schedule(Labs(self.simulation,patient,tech, time_to_lab),self.simulation.clock+time_to_lab)
    
class Labs(Event):
    def __init__(self, simulation, patient, tech, time_to_lab):
        super().__init__(simulation)
        self.patient = patient
        self.tech = tech
        self.time_to_lab = time_to_lab

    def execute(self):
        patient = self.patient
        tech = self.tech
        time_to_lab = self.time_to_lab

        #update patient status
        patient.status = "IN_LABS"

        events_log.append("\nPatient "+str(patient.patient_id)+" is in labs, time = "+str(self.simulation.clock))


        time_in_lab = random.uniform(0.0,10.0)

        self.simulation.schedule(Leave_Lab(self.simulation,patient,tech,time_to_lab),self.simulation.clock+time_in_lab)
        
class Leave_Lab(Event):
    def __init__(self, simulation, patient, tech, time_to_lab):
        super().__init__(simulation)
        self.patient = patient
        self.tech = tech
        self.time_to_lab = time_to_lab

    def execute(self):
        patient = self.patient
        tech = self.tech
        time_to_lab = self.time_to_lab
        #update patient status
        patient.status = "RETURNING_TO_BED"

        events_log.append("\nPatient "+str(patient.patient_id)+" is being transferred back to bed "+str(patient.bed_num.bed_id)+" by "+str(tech.emp_id)+", time = "+str(self.simulation.clock))

        

        #release the lab tech 
        self.simulation.resources.release("tech", tech)
        
        self.simulation.schedule(Going_to_Labs(self.simulation),self.simulation.clock)

        #update patient status
        patient.status = "WAITING_FOLLOWUP"
        self.simulation.queues.followup_queue.enqueue(patient)

        events_log.append("\nPatient "+str(patient.patient_id)+" is waiting for followup, time = "+str(self.simulation.clock))


        self.simulation.schedule(Followup(self.simulation),self.simulation.clock+time_to_lab)

class Followup(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self):
        if self.simulation.resources.provider_stack.is_empty():
            return None
        
        if self.simulation.queues.followup_queue.is_empty():
            return None
        
        #get the next patient for followup
        patient = self.simulation.queues.followup_queue.dequeue()

        #seize provider
        provider = self.simulation.resources.seize("provider")

        #update patient status
        patient.status = "FOLLOWUP"

        events_log.append("\nPatient "+str(patient.patient_id)+" is receiving followup from "+str(provider.emp_id)+", time = "+str(self.simulation.clock))


        eval_time = random.uniform(0.0,8.0)

        self.simulation.schedule(EndFollowup(self.simulation,patient,provider),self.simulation.clock+eval_time)
        

class EndFollowup(Event):
    def __init__(self, simulation, patient, provider):
        super().__init__(simulation)
        self.patient = patient
        self.provider = provider

    def execute(self):
        patient = self.patient
        provider = self.provider

        admit = random.randint(0,1)

        self.simulation.resources.release("provider",provider)

        self.simulation.schedule(Provider_Eval(self.simulation),self.simulation.clock)
        self.simulation.schedule(Followup(self.simulation),self.simulation.clock)

        if admit == 1:
            self.simulation.resources.release("bed", patient.bed_num)
            self.simulation.schedule(Transfer_to_bed(self.simulation),self.simulation.clock)

            patient.status = "ADMITTED"

            self.simulation.queues.inpatient_bed_queue.enqueue(patient)

            events_log.append("\nPatient "+str(patient.patient_id)+" is waiting to be admitted, time = "+str(self.simulation.clock))

            
        else:
            self.simulation.queues.discharge_queue.enqueue(patient)
            patient.status = "WAITING_DISCHARGE"

            events_log.append("\nPatient "+str(patient.patient_id)+" is waiting for discharge, time = "+str(self.simulation.clock))
            

            self.simulation.schedule(Discharge(self.simulation),self.simulation.clock)
        
class Discharge(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self):
        if self.simulation.resources.nurse_stack.is_empty():
            return None
        
        if self.simulation.queues.discharge_queue.is_empty():
            return None
        
        #get the next patient for discharge
        patient = self.simulation.queues.discharge_queue.dequeue()

        #seize the nurse for discharge
        nurse = self.simulation.resources.seize("nurse")

        events_log.append("\nPatient "+str(patient.patient_id)+" is being discharged by "+str(nurse.emp_id)+", time = "+str(self.simulation.clock))

        

        discharge_time = 5.0

        self.simulation.schedule(EndDischarge(self.simulation, patient, nurse),self.simulation.clock+discharge_time)

class EndDischarge(Event):
    def __init__(self, simulation,patient,nurse):
        super().__init__(simulation)
        self.patient = patient
        self.nurse = nurse

    def execute(self):
        patient = self.patient
        nurse = self.nurse
        #update patient status
        patient.status = "DISCHARGED"


        #release the nurse and bed resources
        self.simulation.resources.release("nurse", nurse)
        self.simulation.resources.release("bed", patient.bed_num)

        events_log.append("\nPatient "+str(patient.patient_id)+" has been discharged, time = "+str(self.simulation.clock))

        self.simulation.schedule(Transfer_to_bed(self.simulation),self.simulation.clock)
        self.simulation.schedule(Discharge(self.simulation),self.simulation.clock)

        

