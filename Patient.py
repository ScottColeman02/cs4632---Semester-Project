import random

complaints = ("HEADACHE", "CHEST_PAIN", "NAUSEA", "TRAUMA", "FEVER")
class Patient:
   id_count = 0
   def __init__(self,simulation):
      Patient.id_count += 1
      self.patient_id = Patient.id_count
      self.arrival_time = simulation.clock
      self.status = "WAITING_TRIAGE"
      self.chief_complaint = complaints(random.randint(0,4))
      self.esi = 0

   
