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
            print("no good")            


    pass