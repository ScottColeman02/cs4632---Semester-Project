class ResourceManager:
    def __init__(self):
        self.nurses_available = 0
        self.beds_available = 0
        self.providers_available = 0
        self.lab_techs_available = 0


    def seize(self, resource, patient):
        if(resource == 0):
            print(resource+" not available")
        resource = resource - 1

    
    def release(self,resource):
        resource = resource + 1