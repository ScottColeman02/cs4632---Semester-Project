class Resource:
    staff_id_count = 0
    bed_id_count = 0

    def __init__(self):
        self.name = ""
        self.available = True

    def set_available(self):
        self.available = True

    def set_unavailable(self):
        self.available = False

class Nurse(Resource):
    def __init__(self):
        super().__init__()
        self.name = "NURSE"
        Resource.staff_id_count += 1
        self.emp_id = "N_"+Resource.staff_id_count

class Provider(Resource):
    def __init__(self):
        super().__init__()
        self.name = "PROVIDER"
        Resource.staff_id_count += 1
        self.emp_id = "P_"+Resource.staff_id_count

class LabTech(Resource):
    def __init__(self):
        super().__init__()
        self.name = "LAB_TECH"
        Resource.staff_id_count += 1
        self.emp_id = "LT_"+Resource.staff_id_count

class Bed(Resource):
    def __init__(self):
        super().__init__()
        self.name = "BED"
        Resource.bed_id_count += 1
        self.bed_id = "B_"+Resource.bed_id_count