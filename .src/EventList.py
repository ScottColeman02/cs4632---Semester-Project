import heapq
class EventList:
    def __init__(self):
        self.events = []
        self.id = 0


    def push(self, time, event):
        self.id += 1
        heapq.heappush(self.events, (time,self.id,event))
        
    def pop(self):
        return heapq.heappop(self.events)  

    def is_empty(self):
        if len(self.events) == 0:
            return True
        else:
            return False  

    
