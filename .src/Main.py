from Simulation import Simulation
from Patient import Patient
from Event import *
from Resource import *
import sys

sim = Simulation()

while True:
    print("==========ER Simulation==========")
    print("1. Enter simulation parameters")
    print("2. Run simulation")
    print("3. Exit")
    choice = input("Please make a selection: ")
    print()

    match choice:
        case "1":
            sim_name = input('Please enter a name for the simulation: ')
            sim_name = Simulation()

            num_triage_nurse = int(input("Number of triage nurses: "))
            num_providers = int(input("Number of providers: "))
            num_nurses = int(input("Number of nurses: "))
            num_techs = int(input("Number of lab techs: "))
            num_beds = int(input("Number of beds: "))
            max_time = int(input("Simulation time: "))
            mean_num_patients = float(input("Average # of patients: "))

            sim_name.resources.triage_nurses_available = num_triage_nurse
            sim_name.resources.providers_available = num_providers
            sim_name.resources.nurses_available = num_nurses
            sim_name.resources.lab_techs_available = num_techs
            sim_name.resources.beds_available = num_beds
            sim_name.max_time = max_time
            sim_name.mean_num_patients = mean_num_patients

            for i in range(num_triage_nurse):
                triage_nurse = TriageNurse()
                sim_name.resources.triage_nurse_stack.push(triage_nurse)
            for i in range(num_providers):
                provider = Provider()
                sim_name.resources.provider_stack.push(provider)
            for i in range(num_nurses):
                nurse = Nurse()
                sim_name.resources.nurse_stack.push(nurse)
            for i in range(num_techs):
                tech = LabTech()
                sim_name.resources.tech_stack.push(tech)
            for i in range(num_beds):
                bed = Bed()
                sim_name.resources.bed_stack.push(bed)


            print()
            
        case "2":
            sim_name.run()
        case "3":
            sys.exit()

        case _:
            print("Invalid input, try again.")




arrive_test = Arrive(sim)
arrive_test.execute()
arrive_test.execute()

triage_test = Start_Triage(sim)
triage_test.execute()

print(str(sim.queues.triage_queue))




