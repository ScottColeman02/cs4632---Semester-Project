import random

complaints = ["HEADACHE", "CHEST_PAIN", "NAUSEA", "TRAUMA", "FEVER"]
class Patient:
   id_count = 0
   def __init__(self,simulation):
      Patient.id_count += 1
      self.patient_id = Patient.id_count
      self.arrival_time = simulation.clock
      self.status = "WAITING_TRIAGE"
      self.chief_complaint = complaints[random.randint(0,4)]
      self.severity = random.randint(1,10)
      self.esi = 0

   def __str__(self):
      return f"Patient {self.patient_id}, status= {self.status}"   
   
   def __repr__(self):
      return f"Patient {self.patient_id}, status= {self.status}"

   
