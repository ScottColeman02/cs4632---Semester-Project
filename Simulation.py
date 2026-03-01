from EventList import EventList
from ResourceManager import ResourceManager
from QueueManager import QueueManager
from TriagePolicy import TriagePolicy
from StatsCollector import StatsCollector
from Event import Event,Arrive,events_log


class Simulation:
    def __init__(self):
        self.clock = 0.0
        self.event_list = EventList()
        self.resources = ResourceManager()
        self.queues = QueueManager()
        self.triage_policy = TriagePolicy()
        self.stats = StatsCollector()
        self.max_time = 0.0
    

    def run(self):
        self.event_list.push(self.clock,Arrive(self))
        while not self.event_list.is_empty() and self.clock < self.max_time:
            time,id, event = self.event_list.pop()

            if int(time) > self.max_time:
                break

            self.clock = time
            print("\nTime is "+str(self.clock))

            event.execute()

        self.stats.fill_log(events_log) 

    def schedule(self, event, time):
        self.event_list.push(time,event)

    
    

    
    