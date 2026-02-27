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
            num_providers, sim.resources.providers_available = input("Number of providers: ")
            num_nurses, sim.resources.nurses_available = input("Number of nurses: ")
            num_techs, sim.resources.lab_techs_available = input("Number of lab techs: ")
            num_beds, sim.resources.beds_available = input("Number of beds: ")

            for i in range(num_providers+1):
                provider = Provider()
                sim.resources.provider_stack.push(provider)
            for i in range(num_nurses+1):
                nurse = Nurse()
                sim.resources.nurse_stack.push(nurse)
            for i in range(num_techs+1):
                tech = LabTech()
                sim.resources.tech_stack.push(tech)
            for i in range(num_beds+1):
                bed = Bed()
                sim.resources.bed_stack.push(bed)
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




