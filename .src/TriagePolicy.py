base_2 = {'CARDIAC','RESP','TOXIC','TRAUMA','NEURO','PSYCH'}
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
        

        if chief_comp == 'OD':
            esi = 1



        

        return esi
    
