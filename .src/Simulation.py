from EventList import EventList
from ResourceManager import ResourceManager
from QueueManager import QueueManager
from TriagePolicy import TriagePolicy
from Event import Arrive
from StatsCollector import StatsCollector
import numpy as np

class Simulation:
    def __init__(self,name,tn,n,p,t,b,mt,mp,seed,ssi):
        self.sim_id = name
        self.clock = 0.0
        self.max_time = mt
        self.mean_num_patients = mp
        self.sim_state_interv = ssi

        self.num_tn = tn
        self.num_n = n
        self.num_p = p
        self.num_t = t
        self.num_b = b


        self.event_list = EventList()
        self.resources = ResourceManager()
        self.queues = QueueManager()
        self.triage_policy = TriagePolicy()
        self.stats = StatsCollector()
        
        self.patients = []
        self.events_log = []
        self.sim_states = []
        
        self.rand_seed = seed
        if self.rand_seed == -1:
            self.rand = np.random.default_rng()
        else:
            self.rand = np.random.default_rng(self.rand_seed)

        #Core statistics attributes
        self.patient_count = 0 
        self.patients_fully_treated = 0
        self.final_time = 0.0
        self.num_admit = 0
        self.num_discharge = 0
        self.num_labs = 0

        #Lists to store queue lengths throughout the simulation
        self.triage_queue_len = []
        self.bed_queue_len = []
        self.eval_queue_len = []
        self.labs_queue_len = []
        self.followup_queue_len = []
        self.discharge_queue_len = []

        


        #Simulation stat files
        self.event_log = 'sim-'+str(self.sim_id)+'_event_log.csv'
       
        self.pat_stats = 'sim-'+str(self.sim_id)+'_pat_stats.csv'

        self.summ_stats = 'sim-'+str(self.sim_id)+'_summ_stats.json'

        self.sim_state_stats = 'sim-'+str(self.sim_id)+'_states.csv'

    def run(self):
       # file_path= input("Please enter a file path for the simulation results: ")
       # self.stats.event_log = open(file_path, "w")

        self.stats.sim_state(self,self.clock)
        self.next_state_time = self.sim_state_interv

        self.event_list.push(self.clock,Arrive(self))
        while not self.event_list.is_empty() and self.clock < self.max_time:
            time,id, event = self.event_list.pop()

            if int(time) > self.max_time:
                break
            
            while self.next_state_time <= time and self.next_state_time <= self.max_time:
                self.stats.sim_state(self, self.next_state_time)
                self.next_state_time += self.sim_state_interv


            self.clock = round(time,2)
            event.execute()

        self.stats.fill_log(self) 
        self.final_time = self.clock

        self.stats.sim_state(self,self.clock)

        self.stats.fill_summ_stats(self)
        self.stats.fill_pat_stats(self)
        self.stats.fill_sim_state_stats(self)

    def schedule(self, event, time):
        self.event_list.push(time,event)


    def next_patient_arrival(self):
        next_time = self.rand.exponential(1/(self.mean_num_patients/60))

        return next_time

    
    

    
    
