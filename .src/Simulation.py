from EventList import EventList
from ResourceManager import ResourceManager
from QueueManager import QueueManager
from TriagePolicy import TriagePolicy
from StatsCollector import StatsCollector
from Event import Arrive,events_log
import numpy as np


class Simulation:
    def __init__(self):
        self.clock = 0.0
        self.event_list = EventList()
        self.resources = ResourceManager()
        self.queues = QueueManager()
        self.triage_policy = TriagePolicy()
        self.stats = StatsCollector()
        self.max_time = 0.0
        self.mean_num_patients = None
        self.rand = np.random.default_rng()
        self.patient_count = 0    

    def run(self):
       # file_path= input("Please enter a file path for the simulation results: ")
       # self.stats.event_log = open(file_path, "w")

        self.event_list.push(self.clock,Arrive(self))
        while not self.event_list.is_empty() and self.clock < self.max_time:
            time,id, event = self.event_list.pop()

            if int(time) > self.max_time:
                break

            self.clock = time
            print("\nTime is "+str(round(self.clock,2)))

            event.execute()

        self.stats.fill_log(events_log) 
        print(str(self.patient_count))

    def schedule(self, event, time):
        self.event_list.push(time,event)


    def next_patient_arrival(self):
        next_time = self.rand.exponential(1/(self.mean_num_patients/60))

        return next_time

    
    

    
    
