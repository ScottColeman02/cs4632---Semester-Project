# cs4632---Semester-Project

Project Description: I plan to implement a DES that represents an Emergency Room. From my simulation I hope to gain insight into how to improve emergency room efficiency. 

Scott Coleman
Team: Red Hot Data Analysts

# Project Status:

The core functionalities of the simuation have been added. Simulations can be run and produce event log output. Features to come include Poisson Distirbution for arrivals ,statistics collection and output file creation, and triage policies. Given that my proposal lacked detailed explanation of specifities of classes I have implented several changes. These are mainly architectural and are explained in the Architecture Overview section.

# Installation Instructions:

To run the simulation users need at least Python 3.10 installed.The only way I have tested running the simulation is through VS Code. At this current stage in the development process I recommend that users do the same. Open the folder containing the program files in VS code.

# Usage: 

To run the simulation program navigate to the Main.py file and run it. The main menu presents the options available. To select one enter the corresponding number and press enter. Before running the simulation it is important that you first choose option 1 and enter the simulation parameters. Once parameters have been assigned the simulation is ready to run. Upon entering option 2 you will be prompted to enter a file path for you event log file. At the end of the file path make sure to enter a valid file name followed by '.txt'. 

# Architecture Overview:

Main.py is something I decided to add to handle the implementation of the simulation. Users are prompted to enter parameters and run the simulation through a simple console menu. 

The Simulation.py file is the main engine of the simulation. It contains the main while loop and handles the retrieval and execution of events. Differing from the UML diagram, the Simulation class does not contain a dictionary for the patients as of now and next_patient_id was handed over to the Patient class. 

The QueueManager.py file contains creation of the queues for each station. The main change here was the implementation of a discharge queue. 

ResourceManager.py handles the seizing and release of resources. Counts are also maintained for each resources type as well as custom stacks that store the actual resource objects. I decided to add a triage nurse object in order to help distinguish between the different job types that nurses perform. 

EventList.py handles the creation of the event list and defines its methods. No changes were made.

TriagePolicy.py is still in the works.

StatsCollector.py is still in the works. Currently I have added a new feature not present in the UML digram which is the event log. 

These files are direct implementations of the composition showed on the UML diagram that they have with the Simulation.py file. 

Patient.py contains the attributes and methods for patient objects. I altered the design of this class quite a bit mainly to imporve clarity. I introduced attributes chief complaint, severity and bed_num as ways to help with triage and esi assignment as well as tracking bed availability.

DataStructures.py contains the classes Queue, PriorityQueue, FIFOQueue, and Stack. The queue related classes contain the methods for their respective queue types. I chose to implement Stack as way to store the resource objects that are created during the simulation.

Resource.py contains the different resource classes besed on their type, all inheriting from Resource. This differs from the UML diagram and again was done to clearly distinguish between the different resource objects.

Event.py contains the Event class and the child classes that correspond to the events that occur during the simulation. I chose to go for this structure to allow me to add custom attributes and needs for each of the events. 
