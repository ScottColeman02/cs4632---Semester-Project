class StatsCollector:
    def __init__(self):
        self.event_log = open("/Users/scott/Library/CloudStorage/OneDrive-KennesawStateUniversity/Spring 2026/Modeling and Simulation/Semester Project/Test_Outputs/EVENT_LOG.txt","w")

    #TODO: create method to record statistics
    #record()

    #TODO: create method to get the final time for a patient
    #finalize_time(p_id, time) -> float

    #TODO: create method to investigate simulation statistics
    #get_report() -> statistics

    def fill_log(self, events):
        try:
            with open("self.event_log","w"):
                for event in events:
                    self.event_log.write(event)
                    self.event_log.write("\n")

            self.event_log.close()
        except FileNotFoundError:
            print("no good")            


    pass