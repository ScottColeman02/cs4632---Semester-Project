class Simulation:
    clock = 0.0
    event_list = None
    resources = None
    queues = None
    triage_policy = None
    stats = None
    patients = {}
    next_patient_id = 0

    def __init__(self, clock, event_list, resources, queues, triage_policy, stats, patients):
        self.clock = clock
        self.event_list = event_list
        self.resources = resources
        self.queues = queues
        self.triage_policy = triage_policy
        self.stats = stats
        self.patients = patients
    
    #TODO: create run method to begin running a simulation
    #run() -> void

    #TODO: create schedule method to add an event 
    #schedule(Event) -> void

    #TODO: create method to get the current simulation time
    #curr_time() -> float
    pass

    
    