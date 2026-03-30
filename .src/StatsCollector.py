import numpy as np
import csv
import json
import datetime

class StatsCollector:
    def __init__(self):
        #Lists to store wait times 
        self.triage_waits = []
        self.bed_waits = []
        self.eval_waits = []
        self.labs_waits = []
        self.followup_waits = []
        self.discharge_waits = []
        self.total_times = []
        
    def sim_state(self, simulation, sim_time=None):
        if sim_time is None:
            sim_time = simulation.clock

        status_counts = {}
        for pat in simulation.patients:
            status = pat.status
            status_counts[status] = status_counts.get(status, 0) + 1

        row = {
            'SIM_ID': simulation.sim_id,
            'Simulation clock': round(sim_time, 2),

            'Total patients in ER': simulation.patient_count,
            '# of patients fully treated': simulation.patients_fully_treated,
            '# of patients admitted': simulation.num_admit,
            '# of patients discharged': simulation.num_discharge,
            '# of patients needing labs': simulation.num_labs,

            'Triage Queue Length': len(simulation.queues.triage_queue),
            'Bed Queue Length': len(simulation.queues.bed_queue),
            'Eval Queue Length': len(simulation.queues.eval_queue),
            'Labs Queue Length': len(simulation.queues.lab_queue),
            'Followup Queue Length': len(simulation.queues.followup_queue),
            'Discharge Queue Length': len(simulation.queues.discharge_queue),

            'Triage Nurses Available': simulation.resources.triage_nurses_available,
            'Nurses Available': simulation.resources.nurses_available,
            'Providers Available': simulation.resources.providers_available,
            'Techs Available': simulation.resources.lab_techs_available,
            'Beds Available': simulation.resources.beds_available,

            'WAITING_TRIAGE': status_counts.get('WAITING_TRIAGE', 0),
            'IN_TRIAGE': status_counts.get('IN_TRIAGE', 0),
            'WAITING_BED': status_counts.get('WAITING_BED', 0),
            'TRANSFERRING_TO_BED': status_counts.get('TRANSFERRING_TO_BED', 0),
            'WAITING_EVAL': status_counts.get('WAITING_EVAL', 0),
            'PROVIDER_EVAL': status_counts.get('PROVIDER_EVAL', 0),
            'WAITING_LABS': status_counts.get('WAITING_LABS', 0),
            'GOING_TO_LABS': status_counts.get('GOING_TO_LABS', 0),
            'IN_LABS': status_counts.get('IN_LABS', 0),
            'WAITING_FOLLOWUP': status_counts.get('WAITING_FOLLOWUP', 0),
            'FOLLOWUP': status_counts.get('FOLLOWUP', 0),
            'WAITING_DISCHARGE': status_counts.get('WAITING_DISCHARGE', 0),
            'DISCHARGED': status_counts.get('DISCHARGED', 0),
            'ADMITTED': status_counts.get('ADMITTED', 0),
        }

        simulation.sim_states.append(row)

    def fill_sim_state_stats(self, simulation):
        if not simulation.sim_states:
            return

        fieldnames = list(simulation.sim_states[0].keys())

        try:
            with open(simulation.sim_state_stats, 'w', newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(simulation.sim_states)
        except FileNotFoundError:
            print('Error: No good writing time series.')

    def fill_log(self,simulation):
        try:
            with open(simulation.event_log,"w", newline="") as file:
                writer = csv.writer(file)

                writer.writerow(['Time', 'Patient_ID','ESI', 'Event', 'Resource_ID', 'Patient Status'])

                for event in simulation.events_log:
                    writer.writerow([event[0],event[1],event[2],event[3],event[4],event[5]])
        except FileNotFoundError:
            print("Error: No good writing event log.")            

    #Method to the patient stats file
    def fill_pat_stats(self,simulation):
        try:
            with open(simulation.pat_stats,"w",newline="") as file:
                writer = csv.writer(file)

                writer.writerow(['Patient_ID','Complaint Category','Chief Complaint','Severity','ESI', 'Needed Labs',
                                 'Triage Wait','Bed Wait', 'Eval Wait', 'Labs Wait',
                                  'Followup Wait', 'Discharge Wait', 'Total Time in ER'])
                for pat in simulation.patients:
                    writer.writerow([pat.patient_id,pat.comp_cat,pat.chief_comp,pat.severity,pat.esi,pat.needs_labs
                                     ,pat.triage_wait_time,pat.bed_wait_time,pat.eval_wait_time,pat.labs_wait_time
                                     ,pat.followup_wait_time,pat.discharge_wait_time,pat.total_time])
               
        except FileNotFoundError:
            print("Error: No good writing patient stats.")           

    #Method to fill the simulation stats file
    def fill_summ_stats(self, simulation):
        def avg_available(key):
            return np.mean([row[key] for row in simulation.sim_states])
        sim_summ = {'SIM_ID':simulation.sim_id,
                    
                    'Parameters':{
                        '# of triage nurses': simulation.num_tn,
                        '# of Providers': simulation.num_p,
                        '# of Nurses': simulation.num_n,
                        '# of Techs': simulation.num_t,
                        '# of Beds': simulation.num_b,

                        'Sim time': simulation.max_time,
                        'Patient arrival rate': simulation.mean_num_patients,
                        'Random seed': simulation.rand_seed 
                    },
                    'Results': {
                        'Total # of patients': simulation.patient_count,
                        '# of patients fully treated': simulation.patients_fully_treated,
                        '# of patients admitted': simulation.num_admit,
                        '# of patients discharged': simulation.num_discharge,
                        '% of patients needed labs': round((simulation.num_labs / simulation.patient_count)*100, 2),

                        'Completion rate': round((simulation.patients_fully_treated / simulation.patient_count)*100, 2),
                        'Throughput': round((simulation.patients_fully_treated / simulation.final_time)*60, 2),
                        'Total events processed': len(simulation.events_log),

                        'Triage nurse utilization %': round((1 - avg_available('Triage Nurses Available') / simulation.num_tn)*100, 2),
                        'Nurse utilization %': round((1 - avg_available('Nurses Available') / simulation.num_n)*100, 2),
                        'Provider utilization %': round((1 - avg_available('Providers Available') / simulation.num_p)*100, 2),
                        'Tech utilization %': round((1 - avg_available('Techs Available') / simulation.num_t)*100, 2),
                        'Bed utilization %': round((1 - avg_available('Beds Available') / simulation.num_b)*100, 2),

                        'Avg total time in ER': float(np.mean(self.total_times)),
                        'Median total time in ER': float(np.median(self.total_times)),
                        'Final simulation time': simulation.final_time
                    }
                }
        sim_summ.update(self.comp_wait_stats(simulation))
        sim_summ.update(self.comp_queue_stats(simulation))
        try:
            with open(simulation.summ_stats,'w') as file:
                json.dump(sim_summ,file,indent=4)
        except FileExistsError:
            print('no good so sorry')    
    
    def comp_queue_stats(self, simulation):
        queues = {
            'Triage': simulation.triage_queue_len,
            'Bed': simulation.bed_queue_len,
            'Eval': simulation.eval_queue_len,
            'Labs': simulation.labs_queue_len,
            'Followup': simulation.followup_queue_len,
            'Discharge': simulation.discharge_queue_len
        }
        

        queue_stats = {}

        for name, data in queues.items():
            if data:
                queue_stats[name] = {"Avg": float(np.mean(data)),
                                    "Min": int(np.min(data)),
                                    "Max": int(np.max(data))}
            else:
                queue_stats[name] = {"Avg": None,
                                    "Min": None,
                                    "Max": None}
        
        return {'Queue Length Stats':queue_stats}
    
    def comp_wait_stats(self, simulation):
        wait_times = {
            'Triage': self.triage_waits,
            'Bed': self.bed_waits,
            'Eval': self.eval_waits,
            'Labs': self.labs_waits,
            'Followup': self.followup_waits,
            'Discharge': self.discharge_waits
        }

        queue_stats = {}

        for name, data in wait_times.items():
            clean_waits = [i for i in data if i is not None]
            if data:
                queue_stats[name] = {"Avg": float(np.mean(clean_waits)),
                                    "Min": int(np.min(clean_waits)),
                                    "Max": int(np.max(clean_waits))}
            else:
                queue_stats[name] = {"Avg": None,
                                    "Min": None,
                                    "Max": None}
        
        return {'Queue Wait Time Stats':queue_stats}

        

