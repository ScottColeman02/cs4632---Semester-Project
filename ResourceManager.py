from DataStructures import Stack

class ResourceManager:

    def __init__(self):
        self.nurses_available = 0
        self.beds_available = 0
        self.providers_available = 0
        self.lab_techs_available = 0


    def seize(self, resource):
        match resource:
            case "provider":
                if(self.providers_available == 0):
                    print(resource+" not available")

                self.providers_available -= 1    
            case "nurse":
                if(self.nurses_available == 0):
                    print(resource+" not available") 

                self.nurses_available -= 1        
            case "tech":
                if(self.lab_techs_available == 0):
                    print(resource+" not available")

                self.lab_techs_available -= 1    
            case "bed":
                if(self.beds_available == 0):
                    print(resource+" not available")      

                self.beds_available -= 1  
        

    
    def release(self,resource):
        match resource:
            case "provider":
                self.providers_available += 1    
            case "nurse":
                self.nurses_available += 1        
            case "tech":
                self.lab_techs_available += 1    
            case "bed":
                self.beds_available += 1  