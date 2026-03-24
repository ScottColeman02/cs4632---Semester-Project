from Patient import Patient
from QueueManager import QueueManager
import random

events_log = []

high_sev = {"CHEST_PAIN", "ARRYTHMIA","SHORT_BREATH","DIFF_BREATH", "CHEST_TIGHT", "WHEEZING","SEIZURE",
             "CONFUSION","DIZZY",'AB_PAIN', 'CUTS', 'HEAD_INJ','OD', 'ALC_INTOX', 'HEATSTROKE', 'POISON'}
med_sev = {'FEVER','COUGH', 'CHILL', 'FATIGUE', 'BODY_ACHE','NAUSEA', 'DIARR','BROKE_BONE'}
low_sev = {'JOINT_PAIN', 'BACK_PAIN', 'SPRAIN'}

lab_time_range = {'CARDIAC': (45, 90), "RESP": (30, 75), "NEURO": (45, 90), "GASTRO": (40, 80),
    "TRAUMA": (30, 75), "INFECT": (45, 120), "MUSCULO": (25, 60), "TOXIC": (45, 100),"PSYCH": (35, 80)}
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
        self.simulation.patient_count += 1

        events_log.append("\nPatient "+str(patient.patient_id)+" has arrived , time = "+str(self.simulation.clock))
        
        patient.status = "WAITING_TRIAGE"
        self.simulation.queues.triage_queue.enqueue(patient)
        #Record triage queue length
        self.simulation.triage_queue_len.append(len(self.simulation.queues.triage_queue))

        self.simulation.schedule(Start_Triage(self.simulation),self.simulation.clock)
        

        self.simulation.schedule(Arrive(self.simulation),self.simulation.clock+self.simulation.next_patient_arrival())

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
        self.simulation.triage_queue_len.append(len(self.simulation.queues.triage_queue))

        patient.status = "IN_TRIAGE"
       
        #calculate the wait time and store into triage wait times list
        patient.wait_calc('triage',self.simulation.clock)
        self.simulation.stats.triage_waits.append(patient.triage_wait_time)


        events_log.append("\nPatient "+str(patient.patient_id)+" is being triaged by "+str(triage_nurse.emp_id)+", time = "+str(self.simulation.clock))
        

        self.triage_stats = self.simulation.triage_policy.standard_esi(patient)
        patient.esi = self.triage_stats[0]
        self.triage_time = self.triage_stats[1]

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
        patient.bed_wait_enter = self.simulation.clock
        self.simulation.queues.bed_queue.enqueue(patient)

        self.simulation.bed_queue_len.append(len(self.simulation.queues.bed_queue))

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

        self.simulation.bed_queue_len.append(len(self.simulation.queues.bed_queue))

        #calculate the wait time and store to bed wait time list
        patient.wait_calc('bed',self.simulation.clock)
        self.simulation.stats.bed_waits.append(patient.bed_wait_time)

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
        self.simulation.queues.eval_queue.enqueue(patient)
        patient.status = "WAITING_PROVIDER"
        patient.eval_wait_enter = self.simulation.clock

        self.simulation.eval_queue_len.append(len(self.simulation.queues.eval_queue))

        events_log.append("\nPatient "+str(patient.patient_id)+" is waiting evaluation, time = "+str(self.simulation.clock))

        self.simulation.schedule(Provider_Eval(self.simulation),self.simulation.clock)

        
class Provider_Eval(Event):
    def __init__(self, simulation):
        super().__init__(simulation)

    def execute(self):
        if self.simulation.resources.provider_stack.is_empty():
            return None
        
        if self.simulation.queues.eval_queue.is_empty():
            return None
        #get the next patient
        patient = self.simulation.queues.eval_queue.dequeue()
        self.simulation.eval_queue_len.append(len(self.simulation.queues.eval_queue))

        #seize provider 
        provider = self.simulation.resources.seize("provider")

        #update patient status
        patient.status = "EVAL"

        #calculate the wait time
        patient.wait_calc('eval',self.simulation.clock)
        self.simulation.stats.eval_waits.append(patient.eval_wait_time)

        events_log.append("\nPatient "+str(patient.patient_id)+" is being evaluated by "+str(provider.emp_id)+", time = "+str(self.simulation.clock))

        match patient.esi:
            case 1:
                eval_time = random.uniform(2,5)
            case 2:
                eval_time = random.uniform(5,12)
            case 3:
                eval_time = random.uniform(13,17)
            case 4:
                eval_time = random.uniform(7,15)
            case 5:
                eval_time = random.uniform(5,8)

        self.simulation.schedule(EndEval(self.simulation, patient, provider),self.simulation.clock+eval_time)

        

class EndEval(Event):
    def __init__(self, simulation, patient, provider):
        super().__init__(simulation)
        self.patient = patient
        self.provider = provider

    def execute(self):
        patient = self.patient
        provider = self.provider

        #Establish a baseline probability for if a patient needs labs based on chief complaint
        labs_prob = 0.0
        if patient.chief_comp in high_sev:
            labs_prob = 0.5
        elif patient.chief_comp in med_sev:
            labs_prob = 0.35
        elif patient.chief_comp in low_sev:
            labs_prob = 0.20

        #Adjust based on ESI level
        if patient.esi <= 2:
            labs_prob += 0.35
        
        if patient.severity >= 6:
            labs_prob += 0.15

        patient.needs_labs = random.random() < labs_prob


        self.simulation.resources.release("provider",provider)

        self.simulation.schedule(Provider_Eval(self.simulation),self.simulation.clock)
        

        if patient.needs_labs:
            patient.status = "WAITING_LABS"
            patient.labs_wait_enter = self.simulation.clock

            self.simulation.num_labs += 1

            self.simulation.queues.lab_queue.enqueue(patient)
            self.simulation.labs_queue_len.append(len(self.simulation.queues.lab_queue))

            events_log.append("\nPatient "+str(patient.patient_id)+" is waiting for labs, time = "+str(self.simulation.clock))

            self.simulation.schedule(Going_to_Labs(self.simulation), self.simulation.clock)
    
        else:
            patient.status = "WAITING_DISCHARGE"
            patient.discharge_wait_enter = self.simulation.clock

            self.simulation.queues.discharge_queue.enqueue(patient)
            self.simulation.discharge_queue_len.append(len(self.simulation.queues.discharge_queue))


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
        self.simulation.labs_queue_len.append(len(self.simulation.queues.lab_queue))
        #seize a lab tech resource
        tech = self.simulation.resources.seize("tech")

        #update patient status
        patient.status = "GOING_TO_LAB"
        patient.wait_calc('labs',self.simulation.clock)
        self.simulation.stats.labs_waits.append(patient.labs_wait_time)

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

        a, b = lab_time_range[patient.comp_cat]
        time_in_lab = random.uniform(a,b)

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
        patient.followup_wait_enter = self.simulation.clock
        self.simulation.queues.followup_queue.enqueue(patient)
        self.simulation.followup_queue_len.append(len(self.simulation.queues.followup_queue))

        events_log.append("\nPatient "+str(patient.patient_id)+" is waiting for followup, time = "+str(self.simulation.clock))


        self.simulation.schedule(Followup(self.simulation),self.simulation.clock)

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
        self.simulation.followup_queue_len.append(len(self.simulation.queues.followup_queue))

        #seize provider
        provider = self.simulation.resources.seize("provider")

        #update patient status
        patient.status = "FOLLOWUP"
        patient.wait_calc('followup',self.simulation.clock)
        self.simulation.stats.followup_waits.append(patient.followup_wait_time)

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

        
        match patient.esi:
            case 1:
                admit_prob = 0.9
            case 2:
                admit_prob = 0.70
            case 3:
                admit_prob = 0.45
            case 4:
                admit_prob = 0.20
            case 5:
                admit_prob = 0.05

        admit = random.random() < admit_prob

        self.simulation.resources.release("provider",provider)

        self.simulation.schedule(Provider_Eval(self.simulation),self.simulation.clock)
        self.simulation.schedule(Followup(self.simulation),self.simulation.clock)

        if admit:
            self.simulation.resources.release("bed", patient.bed_num)
            self.simulation.schedule(Transfer_to_bed(self.simulation),self.simulation.clock)

            
            self.simulation.queues.inpatient_bed_queue.enqueue(patient)
            patient.status = "ADMITTED"

            self.simulation.patients_fully_treated += 1
            self.simulation.num_admit += 1
            events_log.append("\nPatient "+str(patient.patient_id)+" is waiting to be admitted, time = "+str(self.simulation.clock))

            
        else:
            self.simulation.queues.discharge_queue.enqueue(patient)
            patient.status = "WAITING_DISCHARGE"
            patient.discharge_wait_enter = self.simulation.clock

            self.simulation.discharge_queue_len.append(len(self.simulation.queues.discharge_queue))

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
        self.simulation.discharge_queue_len.append(len(self.simulation.queues.discharge_queue))


        #seize the nurse for discharge
        nurse = self.simulation.resources.seize("nurse")

        events_log.append("\nPatient "+str(patient.patient_id)+" is being discharged by "+str(nurse.emp_id)+", time = "+str(self.simulation.clock))
        patient.wait_calc('discharge', self.simulation.clock)
        self.simulation.stats.discharge_waits.append(patient.discharge_wait_time)

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
        patient.total_time = self.simulation.clock - patient.arrival_time
        self.simulation.stats.total_times.append(patient.total_time)

        #Create patient time log containing wait times at each station and total time in ER
        #self.simulation.stats.fill_wait_log(patient)

        #release the nurse and bed resources
        self.simulation.resources.release("nurse", nurse)
        self.simulation.resources.release("bed", patient.bed_num)

        events_log.append("\nPatient "+str(patient.patient_id)+" has been discharged, time = "+str(self.simulation.clock))

        self.simulation.patients_fully_treated += 1
        self.simulation.num_discharge += 1

        self.simulation.schedule(Transfer_to_bed(self.simulation),self.simulation.clock)
        self.simulation.schedule(Discharge(self.simulation),self.simulation.clock)

        

