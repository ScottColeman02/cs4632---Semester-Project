class StatsCollector:
    def __init__(self):
        self.event_log = open("EVENT_LOG","w")
        self.events = []

    #TODO: create method to record statistics
    #record()

    #TODO: create method to get the final time for a patient
    #finalize_time(p_id, time) -> float

    #TODO: create method to investigate simulation statistics
    #get_report() -> statistics

    def fill_log(self, events):
        try:
            with open(self.event_log,"w"):
                for event in events:
                    self.event_log.write(event)

        except FileNotFoundError:
            print("no good")            


    pass