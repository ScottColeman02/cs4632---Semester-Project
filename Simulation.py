from EventList import EventList
from ResourceManager import ResourceManager
from QueueManager import QueueManager
from TriagePolicy import TriagePolicy
from StatsCollector import StatsCollector
class Simulation:
    def __init__(self):
        self.clock = 0.0
        self.event_list = EventList()
        self.resources = ResourceManager()
        self.queues = QueueManager()
        self.triage_policy = TriagePolicy()
        self.stats = StatsCollector()
        self.patients = {}
    
    #TODO: create run method to begin running a simulation
    #run() -> void

    def run(self):
        while self.event_list:
            event = self.event_list.pop()
            
            self.clock += 1

            


    #TODO: create schedule method to add an event 
    #schedule(Event) -> void

    def curr_time(self):
        return self.clock
    

    
    