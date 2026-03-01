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
            num_triage_nurse = int(input("Number of triage nurses: "))
            num_providers = int(input("Number of providers: "))
            num_nurses = int(input("Number of nurses: "))
            num_techs = int(input("Number of lab techs: "))
            num_beds = int(input("Number of beds: "))
            max_time = int(input("Simulation time: "))

            sim.resources.triage_nurses_available = num_triage_nurse
            sim.resources.providers_available = num_providers
            sim.resources.nurses_available = num_nurses
            sim.resources.lab_techs_available = num_techs
            sim.resources.beds_available = num_beds
            sim.max_time = max_time

            for i in range(num_triage_nurse):
                triage_nurse = TriageNurse()
                sim.resources.triage_nurse_stack.push(triage_nurse)
            for i in range(num_providers):
                provider = Provider()
                sim.resources.provider_stack.push(provider)
            for i in range(num_nurses):
                nurse = Nurse()
                sim.resources.nurse_stack.push(nurse)
            for i in range(num_techs):
                tech = LabTech()
                sim.resources.tech_stack.push(tech)
            for i in range(num_beds):
                bed = Bed()
                sim.resources.bed_stack.push(bed)

            sim.max_time = max_time

            print()
            
        case "2":
            sim.run()

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




