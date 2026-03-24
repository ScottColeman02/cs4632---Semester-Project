from EventList import EventList
from ResourceManager import ResourceManager
from QueueManager import QueueManager
from TriagePolicy import TriagePolicy
from StatsCollector import StatsCollector
from Event import Arrive,events_log
import numpy as np
import random


class Simulation:
    def __init__(self):
        self.sim_id = random.sample(range(0,9999),1)
        self.clock = 0.0
        self.event_list = EventList()
        self.resources = ResourceManager()
        self.queues = QueueManager()
        self.triage_policy = TriagePolicy()
        self.stats = StatsCollector()
        self.max_time = 0.0
        self.mean_num_patients = None
        self.rand = np.random.default_rng()

        #Core statistics attributes
        self.patient_count = 0 
        self.patients_fully_treated = 0
        self.final_time = 0.0
        self.num_admit = 0
        self.num_discharge = 0
        self.num_labs = 0

        #Lists to store queue lengths throughout the simulation
        triage_queue_len = []
        bed_queue_len = []
        eval_queue_len = []
        labs_queue_len = []
        followup_queue_len = []
        discharge_queue_len = []


        #Simulation stat files
        self.sim_stats = "SIM-"+str(self.sim_id)+'_stats.txt'

    def run(self):
       # file_path= input("Please enter a file path for the simulation results: ")
       # self.stats.event_log = open(file_path, "w")

        self.event_list.push(self.clock,Arrive(self))
        while not self.event_list.is_empty() and self.clock < self.max_time:
            time,id, event = self.event_list.pop()

            if int(time) > self.max_time:
                break

            self.clock = time

            event.execute()

        self.stats.fill_log(events_log) 
        self.final_time = self.clock
        self.stats.fill_sim_stats(self)

    def schedule(self, event, time):
        self.event_list.push(time,event)


    def next_patient_arrival(self):
        next_time = self.rand.exponential(1/(self.mean_num_patients/60))

        return next_time

    
    

    
    
