import numpy as np
class StatsCollector:
    def __init__(self):
        self.event_log = "event_log.txt"
        self.triage_waits = []
        self.bed_waits = []
        self.eval_waits = []
        self.labs_waits = []
        self.followup_waits = []
        self.discharge_waits = []
        self.total_times = []

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

    #Method to fill wait time log for individual patients
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

    #Method to fill the simulation stats file
    def fill_sim_stats(self, simulation):
        try:
            with open(simulation.sim_stats,'w') as file:
                file.write("=====Core Simulation Statistics=====\n")
                file.write("# of patients: "+str(simulation.patient_count)+'\n')
                file.write("# of patients fully treated: "+str(simulation.patients_fully_treated)+'\n')
                file.write('% of patients discharged: '+str(round((simulation.num_discharge / simulation.patient_count)*100,2))+'%\n')
                file.write('% of patients admitted: '+str(round((simulation.num_admit / simulation.patient_count)*100,2))+'%\n')
                file.write("Completion rate: "+str(round((simulation.patients_fully_treated/simulation.patient_count)*100,2))+'%\n')

                file.write('\n% needing labs: '+str(round((simulation.num_labs / simulation.patient_count)*100, 2))+'\n')

                file.write('\nAverage total patient time in ER: '+str(round(np.mean(self.total_times),2))+'\n')
                file.write('Median total patient time in ER: '+str(round(np.median(self.total_times),2))+'\n')
                file.write('Min total patient time in ER: '+str(round(np.min(self.total_times),2))+'\n')
                file.write('Max total patient time in ER: '+str(round(np.max(self.total_times),2))+'\n')
                file.write("Total simulation time: "+str(round(simulation.final_time,2))+'\n')
                file.write('===============================\n')

                #Write the wait time statistics for each station
                file.write('\n=====Wait Time Statistics=====\n')

                file.write('Min Triage wait time: '+str(np.min(self.triage_waits))+'\n')
                file.write('Average Triage wait time: '+str(np.mean(self.triage_waits))+'\n')
                file.write('Max Triage wait time: '+str(np.max(self.triage_waits))+'\n')

                file.write('\nMin Bed wait time: '+str(np.min(self.bed_waits))+'\n')
                file.write('Average Bed wait time: '+str(np.mean(self.bed_waits))+'\n')
                file.write('Max Bed wait time: '+str(np.max(self.bed_waits))+'\n')

                file.write('\nMin Evaluation wait time: '+str(np.min(self.eval_waits))+'\n')
                file.write('Average Evaluation wait time: '+str(np.mean(self.eval_waits))+'\n')
                file.write('Max Evaluation wait time: '+str(np.max(self.eval_waits))+'\n')

                file.write('\nMin Labs wait time: '+str(np.min(self.labs_waits))+'\n')
                file.write('Average Labs wait time: '+str(np.mean(self.labs_waits))+'\n')
                file.write('Max Labs wait time: '+str(np.max(self.labs_waits))+'\n')

                file.write('\nMin Followup wait time: '+str(np.min(self.followup_waits))+'\n')
                file.write('Average Followup wait time: '+str(np.mean(self.followup_waits))+'\n')
                file.write('Max Followup wait time: '+str(np.max(self.followup_waits))+'\n')

                file.write('\nMin Discharge wait time: '+str(np.min(self.discharge_waits))+'\n')
                file.write('Average Discharge wait time: '+str(np.mean(self.discharge_waits))+'\n')
                file.write('Max Discharge wait time: '+str(np.max(self.discharge_waits))+'\n')

                file.write('================================')
        except FileNotFoundError:
            print("Error: No good writing "+str(simulation.sim_id)+" stats file.")