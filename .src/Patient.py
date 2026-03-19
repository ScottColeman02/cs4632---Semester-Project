import random

symptom_dict = {'CARDIAC':["CHEST_PAIN", "ARRYTHMIA","SHORT_BREATH"], 'RESP':["DIFF_BREATH", "CHEST_TIGHT", "COUGH"],
                'NEURO':["SEIZURE", "CONFUSION","DIZZY","HEADACHE"], 'GASTRO': ['AB_PAIN', 'NAUSEA', 'DIAR'],
                'TRAUMA': ['BROKE_BONE', 'CUTS', 'HEAD_INJ', 'BURNS'], 'INFECT': ['FEVER', 'CHILL', 'FATIGUE', 'BODY_ACHE'],
                'MUSCULO': ['JOINT_PAIN', 'BACK_PAIN', 'SPRAIN'], 'TOXIC': ['OD', 'ALC_INTOX', 'HEATSTROKE', 'POISON'],
                'PSYCH': ['SUICIDE_IDEA', 'PSYCHOSIS','ANXIETY']}
symp_keys = symptom_dict.keys()

class Patient:
   id_count = 0
   def __init__(self,simulation):
      Patient.id_count += 1
      self.patient_id = Patient.id_count
      self.arrival_time = simulation.clock
      self.total_time = 0.0
      
      self.status = "ARRIVED"
      
      #Assign patient chief complaint category and symptom as well as severity level
      self.stats = self.get_symptoms()
      self.comp_cat = self.stats[0]
      self.chief_comp = self.stats[1]
      self.severity = self.stats[2]

      self.esi = 0
      self.bed_num = None

      #Patient stat files
      self.wait_time_log = "PAT-"+str(self.patient_id)+'_wait_time_log.txt'

      #Time attributes for entering each station queue
      self.bed_wait_enter = 0.0
      self.eval_wait_enter = 0.0
      self.labs_wait_enter = 0.0
      self.followup_wait_enter = 0.0
      self.discharge_wait_enter = 0.0

      #Wait time attributes for each station
      self.triage_wait_time = 0.0
      self.bed_wait_time = 0.0
      self.eval_wait_time = 0.0
      self.labs_wait_time = None
      self.followup_wait_time = None
      self.discharge_wait_time = 0.0

      #Time attributes for time spent at each station
      self.time_in_triage = 0.0
      self.time_to_bed = 0.0
      self.time_in_eval = 0.0
      self.time_in_labs = 0.0
      self.time_in_followup = 0.0
      self.time_in_discharge = 0.0

   #Method for getting patient complaint
   def get_symptoms(self):
      symp_cat = random.randint(0,9)
      chief_comp = symptom_dict[symp_cat[random.randint(0,len(symp_cat[symp_cat]))]]
      severity = random.randint(0,10)
      
      return symp_cat, chief_comp, severity

   def __str__(self):
      return f"Patient {self.patient_id}, status= {self.status}"   
   
   def __repr__(self):
      return f"Patient {self.patient_id}, status= {self.status}"
   
   def wait_calc(self,type,curr_time):
      match type:
         case 'triage':
            self.triage_wait_time = curr_time - self.arrival_time

         case 'bed':
            self.bed_wait_time = curr_time - self.bed_wait_enter

         case 'eval':
            self.eval_wait_time = curr_time - self.eval_wait_enter

         case 'labs':
            self.labs_wait_time = curr_time - self.labs_wait_enter

         case 'followup':
            self.followup_wait_time = curr_time - self.followup_wait_enter

         case 'discharge':
            self.discharge_wait_time = curr_time - self.discharge_wait_enter      
   
