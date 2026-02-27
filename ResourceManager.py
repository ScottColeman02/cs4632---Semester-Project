from DataStructures import Stack
class ResourceManager:
    provider_stack = Stack()
    nurse_stack = Stack()
    tech_stack = Stack()
    bed_stack = Stack()

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
                provider = self.provider_stack.pop()
                provider.available = False
                return provider
            case "nurse":
                if(self.nurses_available == 0):
                    print(resource+" not available") 

                nurse = self.nurse_stack.pop()
                nurse.available = False
                return nurse 
            case "tech":
                if(self.lab_techs_available == 0):
                    print(resource+" not available")

                tech = self.tech_stack.pop()
                tech.available = False
                return tech   
            case "bed":
                if(self.beds_available == 0):
                    print(resource+" not available")      

                bed = self.bed_stack.pop()
                bed.available = False
                return bed  
        

    
    def release(self, name, resource):
        match name:
            case "provider":
                self.providers_available += 1 
                self.provider_stack.push(resource)  
            case "nurse":
                self.nurses_available += 1  
                self.nurse_stack.push(resource)      
            case "tech":
                self.lab_techs_available += 1
                self.tech_stack.push(resource)      
            case "bed":
                self.beds_available += 1
                self.bed_stack.push(resource)
                
        resource.available = True