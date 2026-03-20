import random

base_2 = {'CARDIAC','RESP','TOXIC','TRAUMA','NEURO','PSYCH'}
base_2_inv = {'DIZZY', 'HEADACHE', 'ANXIETY'}
base_3 = {'GASTRO', 'MUSCULO', 'INFECT'}
class TriagePolicy:
    def __init__(self):
        self.standard = True
    
    #TODO: create method to get the next patient for triage
    #next_patient() -> Patient
    
    def standard_esi(self, patient):
        comp_cat = patient.comp_cat
        chief_comp = patient.chief_comp
        sev = patient.severity

        esi = None
        

        if comp_cat in base_2:
            patient.conscious = random.choice(True,False)
            if not patient.conscious:
                return 1, random.uniform(0,2)
            if chief_comp in base_2_inv and (sev >= 4 and sev <= 6):
                return 3, random.uniform(3,5)
            elif chief_comp in base_2_inv and (sev >= 0 and sev <=3):
                return 4, random.uniform(2,4)
        elif comp_cat in base_3:
            if sev >= 7:
                esi = 2
            elif sev <=3:
                esi = 4
            esi = 3

        return esi
    
