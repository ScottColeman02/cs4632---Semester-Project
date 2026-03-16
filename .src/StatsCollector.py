class StatsCollector:
    def __init__(self):
        self.event_log = "event_log.txt"

    #TODO: create method to record statistics
    #record()

    #TODO: create method to get the final time for a patient
    #finalize_time(p_id, time) -> float

    #TODO: create method to investigate simulation statistics
    #get_report() -> statistics

    def fill_log(self, events):
        try:
            with open(self.event_log,"w") as file:
                for event in events:
                    file.write(str(event))
                    file.write("\n")
        except FileNotFoundError:
            print("Error: No good writing event log.")            

    def fill_wait_log(self, patient):
        try:
            with open(patient.wait_time_log,"w") as file:
                file.write("=====Patient Time Log=====\n")
                file.write("Triage wait time: "+str(patient.triage_wait_time)+'\n')
                file.write("Bed wait time: "+str(patient.bed_wait_time)+'\n')
                file.write("Provider eval wait time: "+str(patient.eval_wait_time)+'\n')
                file.write("Labs wait time: ")
                if patient.labs_wait_time is None:
                    file.write("N/A\n")
                else:
                    file.write(str(patient.labs_wait_time)+'\n')
                file.write("Provider followup wait time: ")
                if patient.followup_wait_time is None:
                    file.write("N/A\n")
                else:
                    file.write(str(patient.followup_wait_time)+'\n')
                file.write("Discharge wait time: "+str(patient.discharge_wait_time)+'\n')
                file.write('===============\n')
                file.write(str(patient.total_time))
        except FileNotFoundError:
            print("Error: No good writing "+str(patient.patient_id)+" time log.")           

    def fill_sim_stats(self, simulation):
        try:
            with open(simulation.sim_stats,'w') as file:
                file.write("=====Simulation Statistics=====\n")
                file.write("# of patients: "+str(simulation.patient_count)+'\n')
                file.write("# of patients fully treated: "+str(simulation.patients_fully_treated)+'\n')
                file.write("Completion rate: "+str((simulation.patients_fully_treated/simulation.patient_count)*100)+'%\n')
                file.write("Total simulation time: "+str(simulation.final_time)+'\n')
                file.write('===============\n')
        except FileNotFoundError:
            print("Error: No good writing "+str(simulation.sim_id)+" stats file.")