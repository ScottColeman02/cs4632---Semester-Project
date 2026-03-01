class Resource:
    staff_id_count = 0
    bed_id_count = 0

    def __init__(self):
        self.name = ""
        self.available = True
class TriageNurse(Resource):
    def __init__(self):
        super().__init__()
        self.name = "TRIAGE_NURSE"
        Resource.staff_id_count += 1
        self.emp_id = "TN_"+str(Resource.staff_id_count)
class Nurse(Resource):
    def __init__(self):
        super().__init__()
        self.name = "NURSE"
        Resource.staff_id_count += 1
        self.emp_id = "N_"+str(Resource.staff_id_count)

class Provider(Resource):
    def __init__(self):
        super().__init__()
        self.name = "PROVIDER"
        Resource.staff_id_count += 1
        self.emp_id = "P_"+str(Resource.staff_id_count)

class LabTech(Resource):
    def __init__(self):
        super().__init__()
        self.name = "LAB_TECH"
        Resource.staff_id_count += 1
        self.emp_id = "LT_"+str(Resource.staff_id_count)

class Bed(Resource):
    def __init__(self):
        super().__init__()
        self.name = "BED"
        Resource.bed_id_count += 1
        self.bed_id = "B_"+str(Resource.bed_id_count)